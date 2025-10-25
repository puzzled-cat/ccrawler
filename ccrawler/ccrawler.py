import os
from pathlib import Path
import re

def get_valid_path(prompt):
    while True:
        p = Path(input(prompt).strip()).expanduser().resolve()
        if p.exists():
            return p
        print("Path does not exist, try again.")
        
def build_safe_search_regex(user_query: str) -> re.Pattern:
    q = user_query.strip()[:256]
    q = re.escape(q)
    q = q.replace(r"\*", ".*")
    return re.compile(q, re.IGNORECASE)

open("output.txt", "w").close()
FOUND = 0
PATH = get_valid_path("Enter directory to scan: ")
SEARCH_QUERY = input("Enter search query: ").strip()
rx = build_safe_search_regex(SEARCH_QUERY)

with open("output.txt", "a") as fh:
    for root, dirs, files in os.walk(PATH):
        for filename in files:
            if rx.search(filename):
                FOUND += 1
                fh.write(f"{FOUND} | {Path(root) / filename}\n")
                print(f"[{FOUND}] Found: {filename}")

print(f"\nFound: {FOUND}")
print(f"Results saved to: {Path('output.txt').resolve()}")
