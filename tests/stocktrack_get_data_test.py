import unittest
from click.testing import CliRunner
from tools.stocktrack import main

class TestTests(unittest.TestCase):
    def test1(self):
        runner = CliRunner()
        result = runner.invoke(main)
        self.assertEqual(result.exit_code, 0)

if __name__ == "__main__":
    unittest.main()
