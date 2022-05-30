# yield test
import random


def get_even(list_of_nums):
    for i in list_of_nums:
        if i % 2 == 0:
            yield i


list_of_nums = [1, 2, 3, 4, 5, 6, 7,  8, 9, 10, 15, 42, 55, 100]


def run_me():
    print("")
    print("Yield operator tests")
    print("Filter data: " + str(list_of_nums))

    print("Even numbers only: ", end=" ")
    for i in get_even(list_of_nums):
        print(i, end=" ")


def calc_cubes():
    print("")
    count = 1
    max_count = random.randint(4, 8)
    start_number = random.randint(1, 11)
    print(f"Numbers to the power of 3 from {start_number}")
    for num in next_cube(start_number):
        if count > max_count:
            break
        print(num)
        count += 1


def next_cube(start_number):
    acc = start_number
    while True:
        yield acc ** 3
        acc += 1
