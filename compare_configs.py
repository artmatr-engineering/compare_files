#!/usr/bin/env python3

import argparse
import csv
import os


def strip_comments(line):
    """Remove comments from a line, preserving the content before the comment."""
    comment_pos = line.find(";")
    if comment_pos != -1:
        return line[:comment_pos].rstrip()
    comment_pos = line.find("#")
    if comment_pos != -1:
        return line[:comment_pos].rstrip()
    return line


def compare_ini_files(file1_path, file2_path):
    with open(file1_path, "r", encoding="utf-8", errors="ignore") as f1:
        lines1 = f1.readlines()

    with open(file2_path, "r", encoding="utf-8", errors="ignore") as f2:
        lines2 = f2.readlines()

    differences = []

    max_lines = max(len(lines1), len(lines2))

    for i in range(max_lines):
        line1 = lines1[i].strip() if i < len(lines1) else ""
        line2 = lines2[i].strip() if i < len(lines2) else ""

        # Strip comments for comparison
        line1_no_comments = strip_comments(line1)
        line2_no_comments = strip_comments(line2)

        if line1_no_comments != line2_no_comments:
            differences.append({"line_number": i + 1, "file1_content": line1, "file2_content": line2})

    return differences


def write_differences_to_csv(differences, file1, file2, output_csv):
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Line Number", f"{os.path.basename(file1)}", f"{os.path.basename(file2)}"])
        for diff in differences:
            writer.writerow([diff["line_number"], diff["file1_content"], diff["file2_content"]])


def main():
    parser = argparse.ArgumentParser(description="Compare two INI files and output differences as CSV")
    parser.add_argument("file1", help="Path to the first INI file")
    parser.add_argument("file2", help="Path to the second INI file")
    parser.add_argument("--output", "-o", help="Output CSV file name", default="ini_diff.csv")

    args = parser.parse_args()

    file1 = args.file1
    file2 = args.file2
    output_csv = args.output

    print(f"Comparing {file1} vs {file2}")
    print("=" * 60)

    differences = compare_ini_files(file1, file2)

    if not differences:
        print("No differences found between the files.")
        return

    print(f"Found {len(differences)} differences. Writing to {output_csv} ...")
    write_differences_to_csv(differences, file1, file2, output_csv)
    print(f"CSV written: {output_csv}")


if __name__ == "__main__":
    main()
