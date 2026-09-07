from pathlib import Path


# Backend root directory
BACKEND_DIR = Path("backend")

# Output file
OUTPUT_FILE = Path("backend_code.txt")

# Code files we want to extract
CODE_EXTENSIONS = {
    ".py",
    ".txt",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
}


def extract_backend_code():
    if not BACKEND_DIR.exists():
        print(f"Backend directory not found: {BACKEND_DIR}")
        return

    files = []

    # Recursively find files
    for path in BACKEND_DIR.rglob("*"):
        if not path.is_file():
            continue

        # Skip Python cache files
        if "__pycache__" in path.parts:
            continue

        # Skip compiled Python files
        if path.suffix == ".pyc":
            continue

        if path.suffix.lower() in CODE_EXTENSIONS:
            files.append(path)

    # Sort files so the output is organized
    files.sort()

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as output:

        output.write("=" * 100 + "\n")
        output.write("SFMS BACKEND SOURCE CODE\n")
        output.write("=" * 100 + "\n\n")

        output.write(
            f"Total files: {len(files)}\n\n"
        )

        for index, file_path in enumerate(files, start=1):

            relative_path = file_path.relative_to(BACKEND_DIR)

            output.write("\n")
            output.write("=" * 100 + "\n")
            output.write(
                f"FILE {index}: backend/{relative_path}"
            )
            output.write("\n")
            output.write("=" * 100 + "\n\n")

            try:
                content = file_path.read_text(
                    encoding="utf-8"
                )

                output.write(content)

            except UnicodeDecodeError:
                output.write(
                    "[Could not decode this file as UTF-8]"
                )

            except Exception as error:
                output.write(
                    f"[Error reading file: {error}]"
                )

            output.write("\n\n")

    print("Backend extraction completed.")
    print(f"Files extracted: {len(files)}")
    print(f"Output: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    extract_backend_code()