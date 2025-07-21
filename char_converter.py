import os
import argparse
import chardet

# Mapping of CP1252 bytes to UTF-8 replacements
CP1252_MAP = {
    b'\x80': '€',
    b'\x82': '‚',
    b'\x83': 'ƒ',
    b'\x84': '„',
    b'\x85': '…',
    b'\x86': '†',
    b'\x87': '‡',
    b'\x88': 'ˆ',
    b'\x89': '‰',
    b'\x8A': 'Š',
    b'\x8B': '‹',
    b'\x8C': 'Œ',
    b'\x91': '\'',
    b'\x92': '\'',
    b'\x93': '"',
    b'\x94': '"',
    b'\x95': '•',
    b'\x96': '–',
    b'\x97': '—',
    b'\x98': '˜',
    b'\x99': '™',
    b'\x9A': 'š',
    b'\x9B': '›',
    b'\x9C': 'œ',
    b'\x9F': 'Ÿ',
}


def count_cp1252_in_file(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()
    counts = {k: content.count(k) for k in CP1252_MAP}
    return counts


def replace_cp1252_in_file(filepath, suffix=None):
    with open(filepath, 'rb') as f:
        content = f.read()
    total_replacements = 0
    for k, v in CP1252_MAP.items():
        count = content.count(k)
        if count > 0:
            content = content.replace(k, v.encode('utf-8'))
            total_replacements += count
    if total_replacements > 0:
        if suffix:
            base, ext = os.path.splitext(filepath)
            new_filepath = f"{base}{suffix}{ext}"
            with open(new_filepath, 'wb') as f:
                f.write(content)
            print(
                f"Converted: {filepath} -> {new_filepath} ({total_replacements} replacements)")
        else:
            with open(filepath, 'wb') as f:
                f.write(content)
            print(f"Converted: {filepath} ({total_replacements} replacements)")
    return total_replacements


def is_utf8_or_ascii_encoded(filepath):
    with open(filepath, 'rb') as f:
        raw = f.read(4096)
    result = chardet.detect(raw)
    encoding = result['encoding']
    confidence = result['confidence']
    return (encoding in ('utf-8', 'ascii')) and confidence == 1.0


def is_binary_file(filepath):
    with open(filepath, 'rb') as f:
        raw = f.read(4096)
    # Only check for null bytes, which are rare in text files
    return b'\x00' in raw


def find_cp1252_lines(filepath):
    results = {k: [] for k in CP1252_MAP}
    with open(filepath, 'rb') as f:
        for lineno, line in enumerate(f, start=1):
            for k in CP1252_MAP:
                if k in line:
                    results[k].append(lineno)
    # Remove keys with no matches
    return {k: v for k, v in results.items() if v}


def process_file(filepath, write=False, debug=False, suffix=None):
    if debug:
        print(f"Scanning: {filepath}")
    if is_binary_file(filepath):
        if debug:
            print(f"Skipping (binary file): {filepath}")
        return
    if is_utf8_or_ascii_encoded(filepath):
        if debug:
            print(
                f"Skipping (already UTF-8 or ASCII with high confidence): {filepath}")
        return
    line_hits = find_cp1252_lines(filepath)
    total = sum(len(v) for v in line_hits.values())
    if total > 0:
        if write:
            replace_cp1252_in_file(filepath, suffix)
        else:
            found = ", ".join(
                [f"{k}: {len(v)} (lines: {v})" for k, v in line_hits.items()])
            print(f"Found ({found}) in: {filepath}")


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
        description="Find files with common CP1252 characters and optionally convert to UTF-8."
    )
    parser.add_argument(
        "path",
        help="Directory or file to scan and convert"
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Replace CP1252 characters with UTF-8 equivalents"
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
