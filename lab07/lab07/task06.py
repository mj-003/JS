import logging
import inspect
import time
import types


def log(level):
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s: %(message)s')
    logger = logging.getLogger()

    def log_decorator(obj):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            end = time.perf_counter()
            exec_time = end - start
            info = ''

            if inspect.isclass(obj):
                info = (f"Creation time: {start}, Class: {obj.__name__}, " +
                        f"Arguments: {args}")

            elif isinstance(obj, types.FunctionType):
                result = obj(*args, **kwargs)
                info = (f"Call time: {start}, Exec duration: {exec_time} " +
                        f"Function name: {obj.__name__}, arguments: {args}, " +
                        f"result: {result}")

            logger.log(level, info)

        return wrapper
    return log_decorator


@log(logging.DEBUG)
def add_two_numbers(x: int, y: int) -> int:
    return x + y


@log(logging.INFO)
class ExampleName:
    def __init__(self, name: str) -> None:
        self.name = name


if __name__ == "__main__":
    add_two_numbers(5, 2)
    ExampleName('example')
