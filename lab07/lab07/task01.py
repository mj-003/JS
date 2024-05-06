# a) Write a function that takes a list of strings and returns an acronym.
def acronym(input_list: list[str]) -> str:
    return "".join(map(lambda s: s[0].upper() if len(s) > 0 else "", input_list))


print(acronym(["hello", "world"]))


# b) Write a function that takes a list of numbers and returns the median.
def median(numbers: list[int | float]) -> int | float:
    sorted_numbers = sorted(numbers)
    return (
        sorted_numbers[len(numbers) // 2]
        if len(numbers) % 2 == 1
        else (sorted_numbers[len(numbers) // 2 - 1] + sorted_numbers[len(numbers) // 2])
             / 2
    )


print(median([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))


# c) Write a function that takes float x and float epsilon and returns
#    the square root of x with precision epsilon.
def newton_sqrt(x: float, epsilon: float) -> float:
    def inner_newton_sqrt(x_, y, epsilon_):
        match (y >= 0, abs(y * y - x_) < epsilon_):
            case (True, True):
                return y
            case (True, False):
                return inner_newton_sqrt(x_, (y + x_ / y) / 2, epsilon_)
            case (False, _):
                return None

    return inner_newton_sqrt(x, x, epsilon)


print(newton_sqrt(3, 0.1))


# d) Write a function that takes a string and returns a dictionary
def make_alpha_dict(string: str) -> dict[str, list[str]]:
    return {
        char: [word for word in string.split() if char in word]
        for char in filter(lambda x: x.isalpha(), string)
    }


print(make_alpha_dict("ona i on"))


# e) Write a function that takes a list of lists and returns a flat list.
def flatten(input_list):
    return [
        elem
        for item in input_list
        for elem in flatten(item)] \
        if (type(input_list) is list or type(input_list) is tuple) else [input_list]


print(flatten([1, [2, 3], [[4, 5], 6], [1, 2, 3, 4, 5, 6]]))
