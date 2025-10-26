import os
from pathlib import Path
import re

def get_valid_path(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input == "":
            current_path = Path.cwd()
            print(f"Using: [{current_path}]")
            return current_path
        p = Path(user_input).expanduser().resolve()
        if p.exists():
            return p
        print("Path does not exist, try again.")

def build_safe_search_regex(user_query: str) -> re.Pattern:
    q = user_query.strip()[:256]
    q = re.escape(q)
    q = q.replace(r"\*", ".*")
    return re.compile(q, re.IGNORECASE)

def main():
    open("output.txt", "w").close()
    FOUND = 0
    PATH = get_valid_path("Enter directory to scan: ")
    SEARCH_QUERY = input("Enter search query: ").strip()
    rx = build_safe_search_regex(SEARCH_QUERY)
    
    with open("output.txt", "a") as fh:
        for root, files in os.walk(PATH):
            for filename in files:
                if rx.search(filename):
                    FOUND += 1
                    fh.write(f"{FOUND} | {Path(root) / filename}\n")
                    print(f"[{FOUND}] Found: {filename}")
    
    print(f"\nFound: {FOUND}")
    print(f"Results saved to: {Path('output.txt').resolve()}")

if __name__ == "__main__":
    main()