# CCRAWLER

A simple, fast command-line tool that recursively searches directories for files matching a pattern with wildcard support.

## Features

- Recursive directory scanning
- Wildcard pattern matching (e.g., `*.txt`, `test*`)
- Saves results to a file with full paths
- Safe regex handling - prevents injection attacks
- Interactive prompts for easy use

## Installation

### From source:
```bash
git clone https://github.com/puzzled-cat/ccrawler.git
cd ccrawler/ccrawler
```

## Usage

Simply run the command and follow the prompts:
```bash
python ccrawler.py
```

You'll be asked to:
1. Enter a directory to scan
2. Enter a search pattern

### Example
```
$ python ccrawler.py
Enter directory to scan: ~/Documents
Enter search query: *.pdf

[1] Found: report.pdf
[2] Found: invoice.pdf
[3] Found: notes.pdf

Found: 3
Results saved to: <DIR>/output.txt
```

### Search Patterns

- **Exact match**: `report.pdf` - finds files with names containing "report.pdf"
- **Wildcards**: `*.txt` - finds all .txt files
- **Partial match**: `test*` - finds files starting with "test"
- **Case insensitive**: Searches ignore case automatically

## Output

Results are saved to `output.txt` in the current directory with the format:
```
0 | /full/path/to/file1.txt
1 | /full/path/to/file2.txt
```

## Requirements

- Python 3.7+
- No external dependencies

## Development

### Running tests
```bash
python -m unittest ccrawler/tests/test.py
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
