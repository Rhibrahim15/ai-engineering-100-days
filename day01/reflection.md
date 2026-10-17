# Day 01 Reflection
# Day 01 Reflection

**1. Why do we check whether the count is greater than zero?**

When the list is empty, its count is zero. Dividing by zero raises a `ZeroDivisionError`, so the function returns `None` for the average when there are no numbers.

**2. What is the difference between the implementation and the tests?**

`baseline.py` contains the `analyze_numbers()` function that calculates the count, sum, and average. `test_baseline.py` contains automated tests that check whether the function returns the expected results for different inputs.

**3. Why do we test edge cases?**

Edge cases help reveal bugs that ordinary inputs might not expose. Testing empty lists, single numbers, negative numbers, and decimals helps us check whether the function behaves correctly under different conditions.