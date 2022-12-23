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

class SetDirectoriesTest(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.path = get_path()

    def test_dirs(self):
        result = self.runner.invoke(main, ['setdir'], input=f"{self.path}\n{self.path}")
        self.assertEqual(result.exit_code, 0)

class CreateTestTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.path = get_path()
        self.runner.invoke(main, ['setdir'], input=f"{self.path}\n{self.path}")
        self.test_name = "test123"

    def test_create(self):
        # test creating a new test
        result = self.runner.invoke(main, ['create', self.test_name, '-ne'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.isfile(f"{self.path}/{self.test_name}.txt"))

    def test_create_exists(self):
        result = self.runner.invoke(main, ['create', self.test_name])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.isfile(f"{self.path}/{self.test_name}.txt"))

        result = self.runner.invoke(main, ['create', self.test_name])
        self.assertIn(f"Test '{self.test_name}' already exists", result.output)

class RunTestTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.path = get_path()
        self.runner.invoke(main, ['setdir'], input=f"{self.path}\n{self.path}")
        self.test_name = "test123"
        self.runner.invoke(main, ['create', self.test_name])
        self.output_name = 'result'

        lines = ['use rsi\n', 'buy {\n', 'divergence bull rsi 15\n', '}\n', 'sell {\n', 'crossing rsi > 70\n', '}']
        with open('test123.txt', 'w') as test_file:
            test_file.writelines(lines)

    def tearDown(self):
        test_dir = get_path()
        if os.path.isfile(f"{test_dir}/{self.test_name}.txt"):
            os.remove(f"{test_dir}/{self.test_name}.txt")
        if os.path.isfile(f"{test_dir}/{self.output_name}.txt"):
            os.remove(f"{test_dir}/{self.output_name}.txt")

    # def test_run_no_out(self):
    #     result = self.runner.invoke(main, ['run'], input='test123\nspy\n10')
    #     self.runner.invoke(main, input='10')
    #     print(result.output)
    #     self.assertEqual(result.exit_code, 0)
        
    # def test_run_out(self):
    #     result = self.runner.invoke(main, ['run', f'-o {self.output_name}'], input='test123\nspy\n10')
    #     print(result.output)
    #     self.assertEqual(result.exit_code, 0)

class DeleteTestTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_delete_notexist(self):
        result = self.runner.invoke(main, ['delete'], input='not_exist')
        assert "Error deleting not_exist" in result.output
        self.assertEqual(result.exit_code, 0)

    def test_delete_exist(self):
        result = self.runner.invoke(main, ['delete'], input='test123')
        assert "test123 Successfully Deleted" in result.output
        self.assertEqual(result.exit_code, 0)

# class LoginTests(unittest.TestCase):
#     def setUp(self):
#         self.runner = CliRunner()
#         self.email = 'testuser@gmail.com'
#         self.password = 'testpassword'
#         self.runner.invoke(main, ['logout'])

#     def test_login_success(self):
#         result = self.runner.invoke(main, ['login'], input=f"{self.email}\n{self.password}")
#         self.assertEqual(result.exit_code, 0)
#         self.assertIn("Successfully Logged In", result.output)

#     def test_login_bad_password(self):
#         result = self.runner.invoke(main, ['login'], input=f"{self.email}\nbadpassword")
#         self.assertIn("Error logging in", result.output)

if __name__ == "__main__":
    unittest.main()
