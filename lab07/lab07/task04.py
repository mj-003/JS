import sys


def make_generator(f):  # Function to create generator
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1

    return generator


def factorial(n):  # Function to calculate factorial number
    if n == 0:
        return 1
    return n * factorial(n - 1)


def fibonacci(n):  # Function to calculate fibonacci number
    if n == 1 or n == 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def print_sequence(generator, elements):  # Function to print sequence
    for i, number in enumerate(generator()):
        if i == elements:
            break
        sys.stdout.write(f"{number} ")


if __name__ == "__main__":
    num_elem = 5

    print("Factorial numbers:")
    factorial_generator = make_generator(factorial)
    print_sequence(factorial_generator, num_elem)
    print()

    print("Fibonacci numbers:")
    fibonacci_generator = make_generator(fibonacci)
    print_sequence(fibonacci_generator, num_elem)
    print()

    print("Geometric sequence:")
    geometric_sequence_generator = make_generator(lambda n: 2 ** n)
    print_sequence(geometric_sequence_generator, num_elem)
    print()

    print("Power sequence:")
    power_sequence_generator = make_generator(lambda n: n ** 2)
    print_sequence(power_sequence_generator, num_elem)
    print()

    print("Harmonic sequence:")
    harmonic_sequence_generator = make_generator(lambda n: 1 / n)
    print_sequence(harmonic_sequence_generator, num_elem)
