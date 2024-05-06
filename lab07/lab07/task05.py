from functools import cache

from task04 import fibonacci, make_generator
from task04 import print_sequence


def make_generator_mem(f):
    @cache
    def memoized_f(n):
        return f(n)

    return make_generator(memoized_f)


if __name__ == "__main__":
    elements = 35
    fibonacci_generator_mem = make_generator_mem(fibonacci)

    print("Memoized generator:")
    print_sequence(fibonacci_generator_mem, elements)
    print("\nMemoized generator 2nd run:")
    print_sequence(fibonacci_generator_mem, elements)