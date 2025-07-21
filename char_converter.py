import os
import argparse


def count_0x92_in_file(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()
    count = content.count(b'\x92')
    return count


def replace_0x92_in_file(filepath, suffix=None):
    with open(filepath, 'rb') as f:
        content = f.read()
    count = content.count(b'\x92')
    if count > 0:
        new_content = content.replace(b'\x92', '’'.encode('utf-8'))
        if suffix:
            base, ext = os.path.splitext(filepath)
            new_filepath = f"{base}{suffix}{ext}"
            with open(new_filepath, 'wb') as f:
                f.write(new_content)
            print(
                f"Converted: {filepath} -> {new_filepath} ({count} replacements)")
        else:
            with open(filepath, 'wb') as f:
                f.write(new_content)
            print(f"Converted: {filepath} ({count} replacements)")
    return count


def process_file(filepath, write=False, debug=False, suffix=None):
    if debug:
        print(f"Scanning: {filepath}")
    count = count_0x92_in_file(filepath)
    if count > 0:
        if write:
            replace_0x92_in_file(filepath, suffix)
        else:
            print(f"Found {count} occurrence(s) in: {filepath}")


def find_and_convert(path, write=False, debug=False, suffix=None):
    if os.path.isfile(path):
        process_file(path, write, debug, suffix)
    else:
        for dirpath, _, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                process_file(filepath, write, debug, suffix)


def main():
    parser = argparse.ArgumentParser(
        description="Find files with 0x92 character and optionally convert to UTF-8 apostrophe."
    )
    parser.add_argument(
        "path",
        help="Directory or file to scan and convert"
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Replace 0x92 character with UTF-8 apostrophe"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging (prints each file being scanned)"
    )
    parser.add_argument(
        "--suffix",
        type=str,
        default=None,
        help="Optional suffix for converted files (e.g. _utf8)"
    )
    args = parser.parse_args()
    find_and_convert(args.path, args.write, args.debug, args.suffix)


if __name__ == "__main__":
    main()
