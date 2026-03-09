import os
import argparse


def print_directory_structure(root_dir, show_files=False, exclude_dirs=None, prefix=""):
    if exclude_dirs is None:
        exclude_dirs = []

    entries = os.listdir(root_dir)
    entries = sorted(entries)
    pointers = ["├── "] * (len(entries) - 1) + ["└── "]

    for pointer, entry in zip(pointers, entries):
        path = os.path.join(root_dir, entry)

        # Skip excluded directories
        if any(exclude in path for exclude in exclude_dirs):
            continue

        if os.path.isdir(path):
            print(prefix + pointer + entry + "/")
            new_prefix = prefix + ("│   " if pointer == "├── " else "    ")
            print_directory_structure(path, show_files, exclude_dirs, new_prefix)
        elif show_files:
            print(prefix + pointer + entry)


def main():
    parser = argparse.ArgumentParser(
        description="Print directory structure recursively."
    )
    parser.add_argument("root_dir", help="Root directory to start from")
    parser.add_argument(
        "--show-files",
        action="store_true",
        help="Show files in the directory structure",
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        default=[],
        help="Directories to exclude (partial path or name)",
    )

    args = parser.parse_args()

    print(args.root_dir + "/")
    print_directory_structure(args.root_dir, args.show_files, args.exclude)


if __name__ == "__main__":
    main()
