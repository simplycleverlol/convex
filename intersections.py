# Задача: выяснить, пересекается отрезок с полосой, -1 < y < 1, или нет
# Функция должна возвращать логическое значение
from r2point import R2Point as R2


def intersec(a: R2, b: R2):
    if -1 < a.y < 1 or -1 < b.y < 1:
        return True
    return a.y <= -1.0 and b.y >= 1.0 or b.y <= -1 and a.y >= 1
