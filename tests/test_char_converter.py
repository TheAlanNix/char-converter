import os
import tempfile
import unittest
from char_converter import (
    count_0x92_in_file,
    replace_0x92_in_file,
    process_file
)
from unittest.mock import patch
import io


class TestCharConverter(unittest.TestCase):
    def test_count_0x92_in_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"Hello\x92World\x92!")
            tmp_path = tmp.name

        count = count_0x92_in_file(tmp_path)
        self.assertEqual(count, 2)
        os.remove(tmp_path)

    def test_replace_0x92_in_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"Hello\x92World")
            tmp_path = tmp.name

        count = replace_0x92_in_file(tmp_path)
        self.assertEqual(count, 1)
        with open(tmp_path, 'rb') as f:
            content = f.read()
        self.assertNotIn(b'\x92', content)
        self.assertIn('’'.encode('utf-8'), content)
        os.remove(tmp_path)

    def test_process_file_dry_run_prints(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"Hello\x92World\x92!")
            tmp_path = tmp.name

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            process_file(tmp_path, write=False)
            output = fake_out.getvalue()
        self.assertIn("Found 2 occurrence(s) in:", output)
        os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
