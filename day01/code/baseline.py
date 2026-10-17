
def analyze_numbers(numbers):
    count = len(numbers)
    total_sum = sum(numbers)
    average = total_sum / count if count > 0 else None

    return {
        "count": count,
        "sum": total_sum,
        "average": average,
    }
