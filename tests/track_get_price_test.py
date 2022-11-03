from click.testing import CliRunner
import unittest
from main import main

class StockTrackGetPriceTests(unittest.TestCase):

    def test_get_price_tsla_lower(self):
        runner = CliRunner()
        result = runner.invoke(main, ['get', 'price', 'tsla'])
        self.assertEqual(result.exit_code, 0)

    def test_get_price_tsla_upper(self):
        runner = CliRunner()
        result = runner.invoke(main, ['get', 'price', 'TSLA'])
        self.assertEqual(result.exit_code, 0)
        
    def test_get_price_tsla_unknown(self):
        company = 'unknown'
        runner = CliRunner()
        result = runner.invoke(main, ['get', 'price', company])
        self.assertNotEqual(result.exit_code, 0)
        self.assertEqual(result.output, f'Company {company} not found')

if __name__ == '__main__':
    unittest.main()
