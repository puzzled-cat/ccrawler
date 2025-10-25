import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
import re as _re

def get_valid_path(prompt):
    while True:
        p = Path(input(prompt).strip()).expanduser().resolve()
        if p.exists():
            return p
        print("Path does not exist, try again.")

def build_safe_search_regex(user_query: str) -> _re.Pattern:
    q = user_query.strip()[:256]
    q = _re.escape(q)
    q = q.replace(r"\*", ".*")
    return _re.compile(q, _re.IGNORECASE)


class TestGetValidPath(unittest.TestCase):
    
    def test_valid_path_first_try(self):
        """Test that a valid path is returned immediately"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('builtins.input', return_value=tmpdir):
                result = get_valid_path("Enter path: ")
                self.assertEqual(result, Path(tmpdir).resolve())
    
    def test_invalid_then_valid_path(self):
        """Test that it keeps asking until a valid path is given"""
        with tempfile.TemporaryDirectory() as tmpdir:
            inputs = ['/fake/nonexistent/path', tmpdir]
            with patch('builtins.input', side_effect=inputs):
                with patch('builtins.print') as mock_print:
                    result = get_valid_path("Enter path: ")
                    self.assertEqual(result, Path(tmpdir).resolve())
                    mock_print.assert_called_with("Path does not exist, try again.")
    
    def test_expands_tilde(self):
        """Test that ~ gets expanded to home directory"""
        with patch('builtins.input', return_value='~'):
            result = get_valid_path("Enter path: ")
            self.assertEqual(result, Path.home().resolve())
    
    def test_strips_whitespace(self):
        """Test that leading/trailing whitespace is handled"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('builtins.input', return_value=f"  {tmpdir}  "):
                result = get_valid_path("Enter path: ")
                self.assertEqual(result, Path(tmpdir).resolve())


class TestBuildSafeSearchRegex(unittest.TestCase):
    
    def test_basic_literal_search(self):
        """Test basic text search without special characters.
        build_safe_search_regex('test.txt') should match 'test.txt' anywhere in the string.
        """
        pattern = build_safe_search_regex("test.txt")
        self.assertTrue(pattern.search("test.txt"))
        self.assertTrue(pattern.search("mytest.txt"))
        self.assertFalse(pattern.search("other.txt"))
    
    def test_case_insensitive(self):
        """Test that search is case insensitive"""
        pattern = build_safe_search_regex("TEST")
        self.assertTrue(pattern.search("test"))
        self.assertTrue(pattern.search("Test"))
        self.assertTrue(pattern.search("TEST"))
    
    def test_wildcard_asterisk(self):
        """Test that * acts as a wildcard"""
        pattern = build_safe_search_regex("test*.txt")
        self.assertTrue(pattern.search("test123.txt"))
        self.assertTrue(pattern.search("test.txt"))
        self.assertTrue(pattern.search("testfile.txt"))
        self.assertFalse(pattern.search("other.txt"))
    
    def test_escapes_regex_special_chars(self):
        """Test that regex special characters are escaped literally"""
        pattern = build_safe_search_regex("file(1).txt")
        self.assertTrue(pattern.search("file(1).txt"))
        self.assertFalse(pattern.search("file1.txt"))
        
        pattern = build_safe_search_regex("test[abc].txt")
        self.assertTrue(pattern.search("test[abc].txt"))
        self.assertFalse(pattern.search("testa.txt"))
    
    def test_truncates_long_queries(self):
        """Test that queries longer than 256 chars are truncated before escaping"""
        long_query = "a" * 300
        pattern = build_safe_search_regex(long_query)
        
        self.assertTrue(pattern.search("a" * 256))

        self.assertTrue(pattern.search("a" * 257 + "b"))
    
    def test_strips_whitespace(self):
        """Test that leading/trailing whitespace is removed before building regex"""
        pattern = build_safe_search_regex("  test.txt  ")
        # Should match exact filename
        self.assertTrue(pattern.search("test.txt"))
        # And also match where it's a substring, since we are using re.search
        self.assertTrue(pattern.search("mytest.txt"))
    
    def test_empty_query(self):
        """Test handling of empty query"""
        pattern = build_safe_search_regex("")
        self.assertTrue(pattern.search("anything.txt"))
        self.assertTrue(pattern.search(""))
    
    def test_multiple_wildcards(self):
        """Test multiple wildcards in one query"""
        pattern = build_safe_search_regex("*.py*")
        self.assertTrue(pattern.search("test.py"))
        self.assertTrue(pattern.search("file.python"))
        self.assertTrue(pattern.search("anything.pyc"))


if __name__ == '__main__':
    unittest.main()
