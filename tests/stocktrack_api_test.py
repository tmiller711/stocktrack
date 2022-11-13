import unittest
from click.testing import CliRunner
from cli.stocktrack import main

class StockTrackTests(unittest.TestCase):
    pass
    # def test_register(self):
    #     runner = CliRunner()
    #     result = runner.invoke(main, ['register'], input="supertest@gmail.com\nsupertest123\nsupertest123")
    #     assert "Account successfully registered" in result.output
    #     self.assertEqual(result.exit_code, 0)

    # def test_login(self):
    #     runner = CliRunner()
    #     result = runner.invoke(main, ['login'], input="supertest@gmail.com\nsupertest123")
    #     assert "Successfully Logged In" in result.output
    #     self.assertEqual(result.exit_code, 0)

    # def test_logout(self):
    #     runner = CliRunner()
    #     result = runner.invoke(main, ['logout'])
    #     assert "Successfully logged out" in result.output
    #     self.assertEqual(result.exit_code, 0)

    # def test_get_data(self):
    #     pass
if __name__ == "__main__":
    unittest.main()
