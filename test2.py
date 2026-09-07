from pathlib import Path


# Frontend root directory
FRONTEND_DIR = Path("web")

# Output file
OUTPUT_FILE = Path("frontend_code.txt")

# Code files we want to extract
CODE_EXTENSIONS = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".css",
    ".scss",
    ".sass",
    ".html",
    ".json",
    ".txt",
    ".md",
    ".yml",
    ".yaml",
}


def extract_frontend_code():
    if not FRONTEND_DIR.exists():
        print(f"Frontend directory not found: {FRONTEND_DIR}")
        return

    files = []

    # Recursively find files
    for path in FRONTEND_DIR.rglob("*"):
        if not path.is_file():
            continue

        # Skip dependencies and generated/cache directories
        if any(
            part in {
                "node_modules",
                ".git",
                ".vite",
                "dist",
                "build",
                "__pycache__",
            }
            for part in path.parts
        ):
            continue

        # Skip compiled files
        if path.suffix.lower() in {
            ".pyc",
            ".map",
        }:
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
        output.write("SFMS FRONTEND SOURCE CODE\n")
        output.write("=" * 100 + "\n\n")

        output.write(
            f"Frontend directory: {FRONTEND_DIR.resolve()}\n"
        )

        output.write(
            f"Total files: {len(files)}\n\n"
        )

        for index, file_path in enumerate(files, start=1):

            relative_path = file_path.relative_to(
                FRONTEND_DIR
            )

            output.write("\n")
            output.write("=" * 100 + "\n")
            output.write(
                f"FILE {index}: frontend/{relative_path}"
            )
            output.write("\n")
            output.write("=" * 100 + "\n\n")

            try:
                content = file_path.read_text(
                    encoding="utf-8"
                )

                if content.strip():
                    output.write(content)
                else:
                    output.write("[EMPTY FILE]")

            except UnicodeDecodeError:
                output.write(
                    "[Could not decode this file as UTF-8]"
                )

            except Exception as error:
                output.write(
                    f"[Error reading file: {error}]"
                )

            output.write("\n\n")

    print("Frontend extraction completed.")
    print(f"Files extracted: {len(files)}")
    print(f"Output: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    extract_frontend_code()