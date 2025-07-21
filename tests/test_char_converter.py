import os
import tempfile
import unittest
from char_converter import (
    count_cp1252_in_file,
    replace_cp1252_in_file,
    process_file,
    find_cp1252_lines,
    is_binary_file,
    is_utf8_or_ascii_encoded
)
from unittest.mock import patch
import io


class TestCharConverter(unittest.TestCase):
    def test_count_cp1252_in_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write((b"Hello\x92World\x93\x94!"))
            tmp_path = tmp.name

        counts = count_cp1252_in_file(tmp_path)
        self.assertEqual(counts[b'\x92'], 1)
        self.assertEqual(counts[b'\x93'], 1)
        self.assertEqual(counts[b'\x94'], 1)
        os.remove(tmp_path)

    def test_find_cp1252_lines(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write((b"Hello\x92World\nFoo\x93Bar\nBaz\x94Qux\n"))
            tmp_path = tmp.name

        lines = find_cp1252_lines(tmp_path)
        self.assertIn(1, lines[b'\x92'])
        self.assertIn(2, lines[b'\x93'])
        self.assertIn(3, lines[b'\x94'])
        os.remove(tmp_path)

    def test_replace_cp1252_in_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write((b"Hello\x92World\x93\x94!"))
            tmp_path = tmp.name

        count = replace_cp1252_in_file(tmp_path)
        self.assertEqual(count, 3)
        with open(tmp_path, 'rb') as f:
            content = f.read()
        self.assertNotIn(b'\x92', content)
        self.assertNotIn(b'\x93', content)
        self.assertNotIn(b'\x94', content)
        self.assertIn('\''.encode('utf-8'), content)
        self.assertIn('"'.encode('utf-8'), content)
        self.assertIn('"'.encode('utf-8'), content)
        os.remove(tmp_path)

    def test_replace_cp1252_in_file_with_suffix(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            tmp.write((b"Hello\x92World"))
            tmp_path = tmp.name
            base, ext = os.path.splitext(tmp_path)
            new_path = f"{base}_utf8{ext}"

        count = replace_cp1252_in_file(tmp_path, suffix="_utf8")
        self.assertEqual(count, 1)
        with open(new_path, 'rb') as f:
            content = f.read()
        self.assertNotIn(b'\x92', content)
        self.assertIn('\''.encode('utf-8'), content)
        os.remove(tmp_path)
        os.remove(new_path)

    def test_process_file_dry_run_prints_lines(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write((b"Hello\x92World\nFoo\x93Bar\nBaz\x94Qux\n"))
            tmp_path = tmp.name

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            process_file(tmp_path, write=False)
            output = fake_out.getvalue()
        self.assertIn(
            "Found (b'\\x92': 1 (lines: [1]), b'\\x93': 1 (lines: [2]), b'\\x94': 1 (lines: [3]))", output)
        os.remove(tmp_path)

    def test_process_file_debug_prints(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write((b"Hello\x92World"))
            tmp_path = tmp.name

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            process_file(tmp_path, write=False, debug=True)
            output = fake_out.getvalue()
        self.assertIn(f"Scanning: {tmp_path}", output)
        os.remove(tmp_path)

    def test_is_utf8_or_ascii_encoded(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(("Hello World").encode('utf-8'))
            tmp_path = tmp.name
        self.assertTrue(is_utf8_or_ascii_encoded(tmp_path))
        os.remove(tmp_path)

    def test_is_binary_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"\x00\x01\x02\x03")
            tmp_path = tmp.name
        self.assertTrue(is_binary_file(tmp_path))
        os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
