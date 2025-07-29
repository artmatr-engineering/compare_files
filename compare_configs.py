#!/usr/bin/env python3

import argparse


def compare_ini_files(file1_path, file2_path):
    """Compare two INI files and report differences"""

    with open(file1_path, "r", encoding="utf-8", errors="ignore") as f1:
        lines1 = f1.readlines()

    with open(file2_path, "r", encoding="utf-8", errors="ignore") as f2:
        lines2 = f2.readlines()

    differences = []

    # Compare line by line
    max_lines = max(len(lines1), len(lines2))

    for i in range(max_lines):
        line1 = lines1[i].strip() if i < len(lines1) else ""
        line2 = lines2[i].strip() if i < len(lines2) else ""

        if line1 != line2:
            differences.append({"line_number": i + 1, "file1_content": line1, "file2_content": line2})

    return differences


def main():
    parser = argparse.ArgumentParser(description="Compare two INI files and report differences")
    parser.add_argument("file1", help="Path to the first INI file")
    parser.add_argument("file2", help="Path to the second INI file")

    args = parser.parse_args()

    file1 = args.file1
    file2 = args.file2

    print(f"Comparing {file1} vs {file2}")
    print("=" * 60)

    differences = compare_ini_files(file1, file2)

    if not differences:
        print("No differences found between the files.")
        return

    print(f"Found {len(differences)} differences:\n")

    for diff in differences:
        print(f"Line {diff['line_number']}:")
        print(f"  {file1}: {diff['file1_content']}")
        print(f"  {file2}: {diff['file2_content']}")
        print()


if __name__ == "__main__":
    main()
