# Char Converter

Finds and converts files containing common Windows CP1252 “smart” characters to their UTF-8 equivalents.

## Supported Characters

- Euro (€), single/double quotes (‘ ’ “ ”), en/em dash (– —), ellipsis (…), bullet (•), trademark (™), and more.

## Setup

It is recommended to use a Python virtual environment.

```sh
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
```

Install requirements:

```sh
pip install -r requirements.txt
```

## Features

- Skips binary files and files already encoded as UTF-8 or ASCII (with high confidence).
- Reports the hex code, count, and line numbers for each found character.

## Usage

### Dry Run (default)

Prints files and counts of CP1252 characters found, with line numbers, without making changes:

```sh
python char_converter.py /path/to/your/folder
python char_converter.py /path/to/your/file.txt
```

### Replace Mode

Replaces all supported CP1252 characters with their UTF-8 equivalents:

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

To print each file being scanned and skipped:

```sh
python char_converter.py /path/to/your/folder --debug
python char_converter.py /path/to/your/file.txt --debug
```
