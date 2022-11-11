import unittest
import stocktrack from stocktrack

class TestTests(unittest.TestCase):
    def test1():
        runner = CliRunner()
        runner.invoke(stocktrack)
        self.assertEqual(result.exit_code == 0)

if __name__ == "__main__":
    unittest.main()
