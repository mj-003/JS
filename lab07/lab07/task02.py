# a) Funkcja zwraca True, jeśli każdy element iterable
# spełnia predykat pred, w przeciwnym przypadku False.
def forall(pred, iterable) -> bool:
    return all(map(pred, iterable))


print(forall(lambda x: x > 0, [1, 2, 3]))


# b) Funkcja zwraca True, jeśli co najmniej jeden element
# iterable spełnia predykat pred, w przeciwnym przypadku False.
def exists(pred, iterable) -> bool:
    return any(map(pred, iterable))


print(exists(lambda x: x > 0, [-1, -2, -3]))


# c) Funkcja zwraca True, jeśli co najmniej n elementów iterable
# spełnia predykat pred, w przeciwnym przypadku False.
def atleast(n, pred, iterable) -> bool:
    return len(list(filter(pred, iterable))) >= n


print(atleast(2, lambda x: x > 0, [1, 2, 3]))


# funkcja zwraca True, jeśli co najwyżej n elementów iterable
# spełnia predykat pred, w przeciwnym przypadku False
def atmost(n, pred, iterable):
    return len(list(filter(pred, iterable))) <= n


print(atmost(2, lambda x: x > 0, [1, 2, 3]))