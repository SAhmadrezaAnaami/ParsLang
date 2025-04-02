
import sys
import os
from components.BUILTIN_FUNCTIONS import run

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: parslang <filename.pars>")
        sys.exit(1)

    filename = sys.argv[1]

    if not filename.lower().endswith(".pars"):
        print(f"Error: Invalid file extension. Expected '.pars', but got '{os.path.splitext(filename)[1]}'")
        print(f"Provided filename: {filename}")
        sys.exit(1)

    if not os.path.exists(filename):
        print(f"Error: File not found: '{filename}'")
        sys.exit(1)

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            script_content = f.read()
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

    if not script_content.strip():
        print(f"Warning: File '{filename}' is empty or contains only whitespace.")
        sys.exit(0)


    result, error = run(filename, script_content)

    if error:
        print(error.as_string())
        sys.exit(1)

    sys.exit(0)
