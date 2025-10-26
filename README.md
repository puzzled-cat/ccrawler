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

## Usage
After installation, simply run the command from anywhere:
```bash
ccrawler
```

You'll be asked to:
1. Enter a directory to scan
2. Enter a search pattern

### Example
```
$ ccrawler
Enter directory to scan: ~/Documents
Enter search query: *.pdf
[1] Found: report.pdf
[2] Found: invoice.pdf
[3] Found: notes.pdf

Found: 3
Results saved to: /current/directory/output.txt
```

### Search Patterns
- **Exact match**: `report.pdf` - finds files with names containing "report.pdf"
- **Wildcards**: `*.txt` - finds all .txt files
- **Partial match**: `test*` - finds files starting with "test"
- **Case insensitive**: Searches ignore case automatically

## Output
Results are saved to `output.txt` in the directory where you run the command, with the format:
```
1 | /full/path/to/file1.txt
2 | /full/path/to/file2.txt
```

## Requirements
- Python 3.8+
- No external dependencies

## Development

### Project Structure
```
ccrawler/
├── ccrawler/
│   ├── __init__.py
│   ├── __main__.py
│   └── tests/
│       └── test.py
├── pyproject.toml
└── README.md
```

### Running tests
```bash
python -m pytest ccrawler/tests/
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