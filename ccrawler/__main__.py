import os
from pathlib import Path
import re
import argparse

# Basic color codes
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'  # Resets color back to default

def parse_args():
    parser = argparse.ArgumentParser(
        description="Recursively search directories for files matching a pattern."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=None,
        help="Directory to scan (default: current directory or interactive prompt)"
    )
    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        help="Search pattern with wildcard support (e.g., *.txt)"
    )
    parser.add_argument(
            "-o", "--output",
            default="output.txt",
            help="Output file name (default: output.txt)"
        )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress output"
    )        
    return parser.parse_args()
        
def get_valid_path(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input == "":
            current_path = Path.cwd()          
            return current_path
        p = Path(user_input).expanduser().resolve()
        if p.exists():
            return p
        print(f"{RED}[ERROR]{RESET} Path does not exist, try again.")
        
def build_safe_search_regex(user_query: str) -> re.Pattern:
    q = user_query.strip()[:256]
    q = re.escape(q)
    q = q.replace(r"\*", ".*")
    return re.compile(q, re.IGNORECASE)

def main():
    args = parse_args()
    
    # Handle directory argument
    if args.directory is None:
        PATH = get_valid_path("Enter directory to scan (press Enter for current): ")
    else:
        PATH = Path(args.directory).expanduser().resolve()
        if not PATH.exists():
            print(f"{RED}[ERROR]{RESET} Directory '{args.directory}' does not exist.")
            return
    
    # Handle query argument
    if args.query is None:
        SEARCH_QUERY = input("Enter search query: ").strip()
    else:
        SEARCH_QUERY = args.query
    
    # Use the output argument
    output_file = args.output
    open(output_file, "w").close()
    
    FOUND = 0
    rx = build_safe_search_regex(SEARCH_QUERY)
    
    if not args.quiet:
        print(f"\n{BLUE}[INFO]{RESET} Searching in: {PATH}")
        print(f"{BLUE}[INFO]{RESET} Pattern: '{SEARCH_QUERY}'")
        print(f"{BLUE}[INFO]{RESET} Writing results to: {output_file}\n")
    
    with open(output_file, "a") as fh:
        for root, dirs, files in os.walk(PATH):
            for filename in files:
                if rx.search(filename):
                    FOUND += 1
                    fh.write(f"{FOUND} | {Path(root) / filename}\n")
                    if not args.quiet:
                        print(f"{BLUE}[{FOUND}] {RESET}{GREEN}Found:{RESET} {filename}")    
    
    print(f"\n{GREEN}[SUCCESS]{RESET} Found {FOUND} matching files.")
    print(f"{BLUE}[INFO]{RESET} Results saved to: {Path(output_file).resolve()}")


if __name__ == "__main__":
    main()