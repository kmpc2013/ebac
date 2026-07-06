array = [1, 2, 3, 4, 4, 5, 6, 6, 7, 8, 9]
array_count = {}

for number in array:
    if number in array_count:
        array_count[number] += 1
    else:
        array_count[number] = 1


array_duplicated = [
    number for number, count in array_count.items() if count > 1
]

print(array_duplicated)