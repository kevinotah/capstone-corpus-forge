def calculate_average(numbers):
    total = 0
    for n in numbers:
        total = total + n
    result = total / len(numbers)
    return result

def find_max(numbers):
    max_val = numbers[0]
    for n in numbers:
        if n > max_val:
            max_val = n
    return max_val

scores = [85, 92, 78, 95, 88, 73, 90]

avg = calculate_average(scores)
mx = find_max(scores)

print("Scores:", scores)
print("Average:", avg)
print("Max score:", mx)
