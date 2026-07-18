import tempfile
import unittest
from pathlib import Path

from health import main, scan


class HealthTests(unittest.TestCase):
    def test_score_and_suggestions(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "README.md").touch()
            result = scan(directory)
            self.assertEqual(result["score"], 14)
            self.assertIn("level", result)
            self.assertTrue(result["suggestions"])

    def test_minimum_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(main([directory, "--minimum", "50", "--json"]), 1)


if __name__ == "__main__":
    unittest.main()
