from deq import Deq
from r2point import R2Point
from intersections import *

# Задача: Вычисляется мощность множества пересечения
# границы выпуклой оболочки с полосой -1 < y < 1

# Возможные ответы: 0, inf, 1
# так как полоса задана строгим неравенством, при наличии в оболочке
# больше двух точек, невозможна ситуация,
# в которой только одна, или конечное ненулевое множество точек границы 
# принадлежат полосе. Если хотя бы одна точка границы содержится в полосе,
# то содержится и часть соответствующих ей отрезков 

# Особенности решения:
# так как решение должно быть индуктивным, а значение мощности бывает
# только 0 или бесконечность, причем если пересечение стало не пустым,
# то пустым оно уже не станет
# Непустое пересечение имеют ребра, концы которых находятся внутри
# полосы или по разные стороны от неё
  



class Figure:
    """ Абстрактная фигура """
    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)

    def isp(self):
        return 0


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p: R2Point):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)

    def isp(self):
        return int(-1.0 < self.p.y < 1.0)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def includes(self, p: R2Point):
        if R2Point.is_triangle(self.p, self.q, p):
            return False
        return p.is_inside(self.p, self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            self = Polygon(self.p, self.q, r)
        elif self.q.is_inside(self.p, r):
            self.q = r
        elif self.p.is_inside(r, self.q):
            self.p = r
        return self

    def isp(self):
        return float('inf') if intersec(self.p, self.q) else 0


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self._isp = intersec(a, b) or intersec(b, c) or intersec(c, a)


    def __ispadd(self, a: R2Point, b: R2Point):
        if  not self._isp:
            self._isp = intersec(a, b)

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def isp(self):
        return float('inf') if self._isp else 0
    # добавление новой точки

    def add(self, t):

        # поиск освещённого ребра
        for _ in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):
            l, f = self.points.last(), self.points.first()
            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= f.dist(l)
            self._area += abs(R2Point.area(t, f, l))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                # удаляем полуинтервал
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            # Добавляем два ребра
            
            self.__ispadd(self.points.first(), t)
            self.__ispadd(t, self.points.last())
            self.points.push_first(t)

        return self


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
