import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
from ccrawler.__main__ import parse_args, main, get_valid_path, build_safe_search_regex

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

class TestParseArgs(unittest.TestCase):
    
    def test_no_arguments_interactive_mode(self):
        """Test that no arguments returns None for directory and query"""
        with patch('sys.argv', ['ccrawler']):
            args = parse_args()
            self.assertIsNone(args.directory)
            self.assertIsNone(args.query)
            self.assertEqual(args.output, 'output.txt')
            self.assertFalse(args.quiet)
    
    def test_both_positional_arguments(self):
        """Test providing both directory and query"""
        with patch('sys.argv', ['ccrawler', '/tmp', '*.txt']):
            args = parse_args()
            self.assertEqual(args.directory, '/tmp')
            self.assertEqual(args.query, '*.txt')
            self.assertEqual(args.output, 'output.txt')
    
    def test_custom_output_file(self):
        """Test -o/--output option"""
        with patch('sys.argv', ['ccrawler', '/tmp', '*.txt', '-o', 'results.txt']):
            args = parse_args()
            self.assertEqual(args.output, 'results.txt')
        
        with patch('sys.argv', ['ccrawler', '/tmp', '*.txt', '--output', 'custom.txt']):
            args = parse_args()
            self.assertEqual(args.output, 'custom.txt')
    
    def test_quiet_flag(self):
        """Test -q/--quiet flag"""
        with patch('sys.argv', ['ccrawler', '/tmp', '*.txt', '-q']):
            args = parse_args()
            self.assertTrue(args.quiet)
        
        with patch('sys.argv', ['ccrawler', '/tmp', '*.txt', '--quiet']):
            args = parse_args()
            self.assertTrue(args.quiet)
    
    def test_only_directory_provided(self):
        """Test providing only directory argument"""
        with patch('sys.argv', ['ccrawler', '/tmp']):
            args = parse_args()
            self.assertEqual(args.directory, '/tmp')
            self.assertIsNone(args.query)
    
    def test_all_options_combined(self):
        """Test all options together"""
        with patch('sys.argv', ['ccrawler', '~/Documents', '*.pdf', '-o', 'found.txt', '-q']):
            args = parse_args()
            self.assertEqual(args.directory, '~/Documents')
            self.assertEqual(args.query, '*.pdf')
            self.assertEqual(args.output, 'found.txt')
            self.assertTrue(args.quiet)


class TestMainFunction(unittest.TestCase):
    
    def test_main_with_cli_args_valid_directory(self):
        """Test main function with command-line arguments and valid directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("content")
            
            with patch('sys.argv', ['ccrawler', tmpdir, '*.txt', '-o', 'test_output.txt', '-q']):
                main()
                
                # Check output file was created
                output = Path('test_output.txt')
                self.assertTrue(output.exists())
                content = output.read_text()
                self.assertIn('test.txt', content)
                output.unlink()  # Clean up
    
    def test_main_with_invalid_directory(self):
        """Test main function with non-existent directory"""
        with patch('sys.argv', ['ccrawler', '/fake/nonexistent/path', '*.txt']):
            with patch('builtins.print') as mock_print:
                main()
                mock_print.assert_called_with("Error: Directory '/fake/nonexistent/path' does not exist")
    
    def test_main_interactive_mode(self):
        """Test main function in interactive mode"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "sample.py"
            test_file.write_text("print('hello')")
            
            inputs = [tmpdir, '*.py']
            with patch('sys.argv', ['ccrawler']):
                with patch('builtins.input', side_effect=inputs):
                    with patch('builtins.print'):
                        main()
                        
                        output = Path('output.txt')
                        self.assertTrue(output.exists())
                        content = output.read_text()
                        self.assertIn('sample.py', content)
                        output.unlink()  # Clean up


if __name__ == '__main__':
    unittest.main()
