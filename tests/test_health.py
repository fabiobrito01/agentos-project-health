import tempfile, unittest
from pathlib import Path
from health import scan
class TestHealth(unittest.TestCase):
 def test_score(self):
  with tempfile.TemporaryDirectory() as d:
   Path(d,"README.md").touch(); self.assertEqual(scan(d)["score"],20)
if __name__=="__main__": unittest.main()
