import unittest
from click.testing import CliRunner
from cli.stocktrack import main

class StockTrackTests(unittest.TestCase):
    def test_create(self):
        runner = CliRunner()
        result = runner.invoke(main, ['create', 'test'])
        self.assertEqual(result.exit_code, 0)

    def test_edit_not_exist(self):
        runner = CliRunner()
        result = runner.invoke(main, ['edit'], input='tester_test')
        assert "Test 'tester_test' does not exist" in result.output
        self.assertEqual(result.exit_code, 0)

    # figure out how to exit graph
    # def test_run_no_out(self):
    #     runner = CliRunner()
    #     result = runner.invoke(main, ['run'], input='test', )
    #     runner.invoke(main, input='10')
    #     self.assertEqual(result.exit_code, 0)

    # def test_run_out(self):
    #     runner = CliRunner()
    #     result = runner.invoke(main, ['run', '-o test'], input='test\n10')
    #     self.assertEqual(result.exit_code, 0)

    def test_delete_notexist(self):
        runner = CliRunner()
        result = runner.invoke(main, ['delete'], input='not_exist')
        assert "Error deleting not_exist" in result.output
        self.assertEqual(result.exit_code, 0)

    # def test_delete_exist(self):
    #     runner = CliRunner()
    #     result = runner.invoke(main, ['delete'], input='test')
    #     assert "test Successfully Deleted" in result.output
    #     self.assertEqual(result.exit_code, 0)

if __name__ == "__main__":
    unittest.main()
