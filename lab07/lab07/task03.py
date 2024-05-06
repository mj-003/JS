import string
import random


class PasswordGenerator:
    def __init__(self, length, count, charset=string.ascii_letters + string.digits):
        self.length = length
        self.count = count
        self.charset = charset

    def __iter__(self):  # Method to make the class iterable
        return self

    def __next__(self):     # Method to create next random password
        if self.count == 0:
            raise StopIteration()
        self.count -= 1
        return ''.join(random.choice(self.charset) for _ in range(self.length))


if __name__ == "__main__":
    password_generator = PasswordGenerator(10, 5)
    print(next(password_generator))
    for password in password_generator:
        print(password)

