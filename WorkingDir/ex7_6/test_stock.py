# test_stock.py

import stock

import unittest


class TestStock(unittest.TestCase):

    # Test for success

    def test_create(self):
        """
        Test that you can create a Stock using keyword arguments such as Stock(name='GOOG',shares=100,price=490.1).
        """
        s = stock.Stock('GOOG', 100, 490.1)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_create_keyword(self):
        """
        Same as test_create() with keywords in parameters
        """
        s = stock.Stock(name='GOOG', shares=100, price=490.1)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_cost(self):
        """
        Test that the cost property returns a correct value
        """
        s = stock.Stock('GOOG', 100, 490.1)
        self.assertEqual(s.cost, s.shares * s.price)

    def test_sell(self):
        """
        Test that the sell() method correctly updates the shares
        """
        starting_shares = 100
        seller = 10

        s = stock.Stock('GOOG', starting_shares, 490.1)
        
        s.sell(seller)

        self.assertEqual(s.shares, starting_shares - seller)

    def test_from_row(self):
        """
        Test that the from_row() class method creates a new instance from good data.
        """
        t = stock.Stock.from_row(['PIPPO', 431, 34.22])
        self.assertEqual(t.name, 'PIPPO')
        self.assertEqual(t.shares, 431)
        self.assertEqual(t.price, 34.22)

    def test_repr(self):
        """
        Test that the __repr__() method creates a proper representation string.
        """
        s = stock.Stock('GOOG', 100, 490.1)
        self.assertEqual(repr(s), "Stock('GOOG',100,490.1)")

    def test_eq(self):
        """
        Test the comparison operator method __eq__()
        """
        s1 = stock.Stock('GOOG', 100, 490.1)
        s2 = stock.Stock('GOOG', 100, 490.1)

        self.assertTrue(s1 == s2)

    # Test for error management

    def test_bad_shares_string(self):
        """
        Test that setting shares to a string raises a TypeError
        """
        with self.assertRaises(TypeError):
            s = stock.Stock('GOOG', '50', 490.1)

    def test_bad_shares_negative(self):
        """
        Test that setting shares to a negative number raises a ValueError
        """
        with self.assertRaises(ValueError):
            s = stock.Stock('GOOG', -10, 490.1)

    def test_bad_price_string(self):
        """
        Test that setting price to a string raises a TypeError
        """
        with self.assertRaises(TypeError):
            s = stock.Stock('GOOG', 50, '490.1')

    def test_bad_price_negative(self):
        """
        Test that setting price to a negative number raises a ValueError
        """
        with self.assertRaises(ValueError):
            s = stock.Stock('GOOG', 10, -490.1)

    def test_bad_attribute(self):
        """
        Test that setting a non-existent attribute share raises an AttributeError
        """
        s = stock.Stock('GOOG', 10, 490.1)
        with self.assertRaises(AttributeError):
            s.share = 54


if __name__ == '__main__':
    unittest.main()