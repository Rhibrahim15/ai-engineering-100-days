
import unittest

from baseline import analyze_numbers


class TestAnalyzeNumbers(unittest.TestCase):
    def test_multiple_numbers(self):
        result = analyze_numbers([2, 4, 6])

        self.assertEqual(result["count"], 3)
        self.assertEqual(result["sum"], 12)
        self.assertEqual(result["average"], 4.0)

    def test_single_number(self):
        result = analyze_numbers([5])

        self.assertEqual(result["count"], 1)
        self.assertEqual(result["sum"], 5)
        self.assertEqual(result["average"], 5.0)

    def test_empty_list(self):
        result = analyze_numbers([])

        self.assertEqual(result["count"], 0)
        self.assertEqual(result["sum"], 0)
        self.assertIsNone(result["average"])

    def test_negative_numbers(self):
        result = analyze_numbers([-2, 2])

        self.assertEqual(result["count"], 2)
        self.assertEqual(result["sum"], 0)
        self.assertEqual(result["average"], 0.0)


if __name__ == "__main__":
    unittest.main()
