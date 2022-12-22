import unittest
from click.testing import CliRunner
from cli.stocktrack import main
import pathlib
import requests
import json

def get_path():
    return pathlib.Path(__file__).parent.resolve()

def check_token():
    try:
        with open(f"{get_path()}/credentials.txt", 'r') as file:
            data = json.loads(file.read())
            r = requests.get('http://127.0.0.1:8000/account/getaccount', headers={'Authorization': f"Bearer {data['access']}"})
            if r.ok:
                return True
            else:
                return False
    except:
        return False

def get_test_dir():
    try:
        with open(f"{get_path()}/test_dir.txt", "r") as f:
            return f.read().strip()
    except:
        return None

def get_results_dir():
    try:
        with open(f"{get_path()}/results_dir.txt", "r") as f:
            return f.read().strip()
    except:
        return None


class StockTrackTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.path = get_path()

    def test_dirs(self):
        result = self.runner.invoke(main, ['setdir'], input=f"{self.path}\n{self.path}")
        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        result = self.runner.invoke(main, ['create', 'test123'])
        print(result.output, 'alsjfoiasfpsd-fj9sdfj9')
        self.assertEqual(result.exit_code, 0)

    # figure out how to exit graph
    def test_run_no_out(self):
        result = self.runner.invoke(main, ['run'], input='test/n10')
        self.runner.invoke(main, input='10')
        self.assertEqual(result.exit_code, 0)

    def test_run_out(self):
        result = self.runner.invoke(main, ['run', '-o test'], input='test\n10')
        self.assertEqual(result.exit_code, 0)

    def test_delete_notexist(self):
        result = self.runner.invoke(main, ['delete'], input='not_exist')
        assert "Error deleting not_exist" in result.output
        self.assertEqual(result.exit_code, 0)

    def test_delete_exist(self):
        result = self.runner.invoke(main, ['delete'], input='test123')
        assert "test123 Successfully Deleted" in result.output
        self.assertEqual(result.exit_code, 0)

if __name__ == "__main__":
    unittest.main()
