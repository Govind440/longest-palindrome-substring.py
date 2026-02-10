import unittest
from io import StringIO
import sys


# Import the factorial function
def factorial(n):
    fact = 1
    for i in range(1, n + 1):
        fact *= i
        print(fact)
    return fact


class TestFactorial(unittest.TestCase):
    """Test cases for the factorial function"""

    def setUp(self):
        """Capture print output for each test"""
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        """Reset stdout after each test"""
        sys.stdout = sys.__stdout__

    def test_factorial_of_5(self):
        """Test factorial of 5 (should be 120)"""
        result = factorial(5)
        self.assertEqual(result, 120)

    def test_factorial_of_0(self):
        """Test factorial of 0 (should be 1)"""
        result = factorial(0)
        self.assertEqual(result, 1)

    def test_factorial_of_1(self):
        """Test factorial of 1 (should be 1)"""
        result = factorial(1)
        self.assertEqual(result, 1)

    def test_factorial_of_3(self):
        """Test factorial of 3 (should be 6)"""
        result = factorial(3)
        self.assertEqual(result, 6)

    def test_factorial_of_10(self):
        """Test factorial of 10 (should be 3628800)"""
        result = factorial(10)
        self.assertEqual(result, 3628800)

    def test_factorial_print_output(self):
        """Test that factorial prints intermediate results"""
        factorial(3)
        output = self.held_output.getvalue()
        # Should print: 1, 2, 6 (each on new line)
        self.assertIn("1", output)
        self.assertIn("2", output)
        self.assertIn("6", output)

    def test_factorial_of_negative_returns_1(self):
        """Test factorial of negative number (should return 1)"""
        result = factorial(-5)
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
