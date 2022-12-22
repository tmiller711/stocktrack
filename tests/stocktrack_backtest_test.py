import unittest
from click.testing import CliRunner
from cli.stocktrack import main
import pathlib
import requests
import json
import os

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
        self.test_name = 'test123'
        self.output_name = 'test'
    
    def tearDown(self):
        # Clean up any files or directories created during the tests
        test_dir = get_test_dir()
        if os.path.isfile(f"{self.path}/{self.test_name}.txt"):
            os.remove(f"{self.path}/{self.test_name}.txt")
        if os.path.isfile(f"{self.path}/{self.output_name}.txt"):
            os.remove(f"{self.path}/{self.output_name}.txt")

    def test_dirs(self):
        result = self.runner.invoke(main, ['setdir'], input=f"{self.path}\n{self.path}")
        self.assertEqual(result.exit_code, 0)

    def test_create(self):
        # test creating a new test
        result = self.runner.invoke(main, ['create', self.test_name])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.isfile(f"{self.path}/{self.test_name}.txt"))

        # Test creating a test with a name that already exists
        result = self.runner.invoke(main, ['create', self.test_name])
        self.assertIn(f"Test '{self.test_name}' already exists", result.output)



    # figure out how to exit graph
    # def test_run_no_out(self):
    #     result = self.runner.invoke(main, ['run'], input='test/n10')
    #     self.runner.invoke(main, input='10')
    #     self.assertEqual(result.exit_code, 0)

    # def test_run_out(self):
    #     result = self.runner.invoke(main, ['run', '-o test'], input='test\n10')
    #     self.assertEqual(result.exit_code, 0)

    # def test_delete_notexist(self):
    #     result = self.runner.invoke(main, ['delete'], input='not_exist')
    #     assert "Error deleting not_exist" in result.output
    #     self.assertEqual(result.exit_code, 0)

    # def test_delete_exist(self):
    #     result = self.runner.invoke(main, ['delete'], input='test123')
    #     assert "test123 Successfully Deleted" in result.output
    #     self.assertEqual(result.exit_code, 0)

if __name__ == "__main__":
    unittest.main()
