# Char Converter

Finds and converts files containing the Windows CP1252 `0x92` character to UTF-8 apostrophe (`’`).

## Usage

### Dry Run (default)

Prints files and counts of `0x92` characters found, without making changes:

```sh
python char_converter.py /path/to/your/folder
python char_converter.py /path/to/your/file.txt
```

### Replace Mode

Replaces all `0x92` characters with UTF-8 apostrophe (`’`):

```sh
python char_converter.py /path/to/your/folder --write
python char_converter.py /path/to/your/file.txt --write
```

### Optional Suffix

To save converted files with a suffix (e.g. `_utf8`):

```sh
python char_converter.py /path/to/your/folder --write --suffix _utf8
python char_converter.py /path/to/your/file.txt --write --suffix _utf8
```

### Debug Logging

To print each file being scanned:

```sh
python char_converter.py /path/to/your/folder --debug
python char_converter.py /path/to/your/file.txt --debug
```
