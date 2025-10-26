# CCRAWLER
A simple, fast command-line tool that recursively searches directories for files matching a pattern with wildcard support.

## Features
- Recursive directory scanning
- Wildcard pattern matching (e.g., `*.txt`, `test*`)
- Saves results to a file with full paths
- Safe regex handling - prevents injection attacks
- Interactive prompts for easy use

## Installation

### Using pipx (Recommended)
```bash
git clone https://github.com/puzzled-cat/ccrawler.git
cd ccrawler
pipx install -e .
```

### Using pip with virtual environment
```bash
git clone https://github.com/puzzled-cat/ccrawler.git
cd ccrawler
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

## Usage Examples

### Interactive Mode
Simply run without arguments and follow the prompts:
```bash
ccrawler
# Enter directory to scan (press Enter for current): ~/Documents
# Enter search query: *.pdf
```

### Quick Search
Search for all Python files in your home directory:
```bash
ccrawler ~ "*.py"
```

### Search Current Directory
Find all markdown files in the current directory:
```bash
ccrawler . "*.md"
```

Or just use current directory by default:
```bash
ccrawler "*.txt"
```

### Custom Output File
Save results to a specific file:
```bash
ccrawler ~/Projects "test*" -o test-files.txt
```

### Quiet Mode
Suppress progress output (only show final summary):
```bash
ccrawler ~/Downloads "*.zip" -q
```

### Combined Options
Search with custom output and quiet mode:
```bash
ccrawler ~/Documents "report*" -o reports.txt -q
```

### Pattern Examples
```bash
# All text files
ccrawler ~/Documents "*.txt"

# Files starting with "test"
ccrawler ~/Projects "test*"

# Files containing "2024"
ccrawler ~/Photos "*2024*"

# Specific file name (case-insensitive)
ccrawler ~/Downloads "invoice.pdf"

# Python test files
ccrawler ~/code "test_*.py"
```

### Real-World Examples
```bash
# Find all config files in your home directory
ccrawler ~ "*.conf" -o config-files.txt

# Locate all JavaScript files in a project
ccrawler ~/my-project "*.js"

# Find log files from today
ccrawler /var/log "*$(date +%Y%m%d)*" -q

# Search for all images
ccrawler ~/Pictures "*.jpg" -o photos.txt
```

### Search Patterns
- **Exact match**: `report.pdf` - finds files with names containing "report.pdf"
- **Wildcards**: `*.txt` - finds all .txt files
- **Partial match**: `test*` - finds files starting with "test"
- **Case insensitive**: Searches ignore case automatically

## Output
By default, results are saved to `output.txt` in the directory where you run the command, with the format:
```
1 | /full/path/to/file1.txt
2 | /full/path/to/file2.txt
```

## Requirements
- Python 3.8+
- No external dependencies

## Development

### Running tests
```bash
python -m unittest ccrawler.tests.test # from root
```

### Uninstalling
```bash
pipx uninstall ccrawler
# or
pip uninstall ccrawler
```

## Roadmap

### Enhanced Features
- [ ] Add command-line arguments (skip interactive prompts)
- [ ] Custom output file name/location option
- [ ] Exclude patterns (ignore certain files/directories)
- [ ] File size and date filtering
- [ ] Search file contents, not just names

### User Experience
- [ ] Progress bar for large directories
- [ ] Colorized terminal output
- [ ] JSON/CSV output format options
- [ ] Configuration file support (~/.ccrawlerrc)
- [ ] Verbose/quiet modes

### Production Ready
- [ ] Comprehensive test suite
- [ ] Performance benchmarks
- [ ] Documentation website
- [ ] PyPI package distribution
- [ ] Windows/macOS/Linux binaries

## License
MIT License - see LICENSE file for details

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.