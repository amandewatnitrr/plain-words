import io
import json
import unittest
from unittest import mock

import plainwords


class Tests(unittest.TestCase):
    def test_prompt_contains_letter_and_language(self):
        p = plainwords.build_prompt("  Pay by 1 May  ", "Hindi")
        self.assertIn("Pay by 1 May", p)
        self.assertIn("Hindi", p)

    def test_empty_letter_rejected(self):
        with self.assertRaises(ValueError):
            plainwords.explain("   ")

    def test_explain_parses_response(self):
        fake = io.BytesIO(json.dumps({"response": " ok \n"}).encode())
        with mock.patch("urllib.request.urlopen", return_value=fake) as m:
            self.assertEqual(plainwords.explain("hello"), "ok")
            sent = json.loads(m.call_args[0][0].data)
            self.assertFalse(sent["stream"])
            self.assertEqual(sent["model"], plainwords.DEFAULT_MODEL)


if __name__ == "__main__":
    unittest.main()
