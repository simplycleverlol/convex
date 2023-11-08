from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Void()

    # Нульугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        assert isinstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь нульугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)

    # Мощность пересечеия пустоты с чем угодно - пустота
    def test_isp(self):
        assert self.f.isp() == 0


class TestPoint:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0))

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь одноугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)

    # Нет отрезка
    def test_isp0(self):
        assert self.f.isp() == 0

    # Точка на отрезке
    def test_isp1(self):
        self.f.setcutsegment(R2Point(-1, -1), R2Point(1, 1))
        assert self.f.isp() == 1

    # Точка на конце отрезка
    def test_isp2(self):
        self.f.setcutsegment(R2Point(0, 0), R2Point(1, 1))
        assert self.f.isp() == 1

    # Точка не на отрезке
    def test_isp3(self):
        self.f.setcutsegment(R2Point(-1, 1), R2Point(1, 1))
        assert self.f.isp() == 0

    # Точка не на отрезке, но на его прямой
    def test_isp4(self):
        self.f.setcutsegment(R2Point(5, 0), R2Point(1, 0))
        assert self.f.isp() == 0


class TestSegment:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0))

    # Двуугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        assert isinstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        assert self.f.perimeter() == approx(2.0)

    # Площадь двуугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки двуугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    # При добавлении точки двуугольник может превратиться в другой двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)

    # Тесты на мощность множества пересечения
    # Без отрезка
    def test_isp1(self):
        assert self.f.isp() == 0

    # Соприкасаются концами и не параллельны
    def test_isp2(self):
        self.f.cs = Segment(R2Point(1, 0), R2Point(0, 1))
        assert self.f.isp() == 1

    # Соприкасаются концами и параллельны
    def test_isp3(self):
        self.f.cs = Segment(R2Point(1, 0), R2Point(2, 0))
        assert self.f.isp() == 1
        self.f.cs = Segment(R2Point(0, 0), R2Point(-2, 0))
        assert self.f.isp() == 1

    # накладываются справа, слева, посередине
    def test_isp4(self):
        self.f.cs = Segment(R2Point(0.5, 0), R2Point(2, 0))
        assert self.f.isp() == float('inf')
        self.f.cs = Segment(R2Point(-1, 0), R2Point(0.2, 0))
        assert self.f.isp() == float('inf')
        self.f.cs = Segment(R2Point(0.5, 0), R2Point(0.2, 0))
        assert self.f.isp() == float('inf')

    # пересекаются посередине
    def test_isp5(self):
        self.f.cs = Segment(R2Point(1, 1), R2Point(0, -1))
        assert self.f.isp() == 1
        self.f.cs = Segment(R2Point(0, 1), R2Point(1, -1))
        assert self.f.isp() == 1

    # параллельны
    def test_isp6(self):
        self.f.cs = Segment(R2Point(0.5, 1), R2Point(2, 1))
        assert self.f.isp() == 0
        self.f.cs = Segment(R2Point(-1, 1), R2Point(0.2, 1))
        assert self.f.isp() == 0
        self.f.cs = Segment(R2Point(0.5, 1), R2Point(0.2, 1))
        assert self.f.isp() == 0

    # не параллельны и не пересекаются
    def test_isp3(self):
        self.f.cs = Segment(R2Point(1, 1), R2Point(2, 0))
        assert self.f.isp() == 0
        self.f.cs = Segment(R2Point(0, 1), R2Point(-2, 0))
        assert self.f.isp() == 0
        self.f.cs = Segment(R2Point(1, 1), R2Point(0, 2))
        assert self.f.isp() == 0
        self.f.cs = Segment(R2Point(1, 1), R2Point(-1, 0))
        assert self.f.isp() == 0
        self.f.cs = Segment(R2Point(0, -2), R2Point(1, -1))
        assert self.f.isp() == 0

    # совпадают
    def test_isp4(self):
        self.f.cs = self.f
        assert self.f.isp() == float('inf')


class TestPolygon:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Polygon(
            R2Point(
                0.0, 0.0), R2Point(
                1.0, 0.0), R2Point(
                0.0, 1.0))

    # Многоугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Polygon (многоугольник)
    def test_polygon(self):
        assert isinstance(self.f, Polygon)

    # Изменение количества вершин многоугольника
    # изначально их три
    def test_vertexes1(self):
        assert self.f.points.size() == 3
    # добавление точки внутрь многоугольника не меняет их количества

    def test_vertexes2(self):
        assert self.f.add(R2Point(0.1, 0.1)).points.size() == 3
    # добавление другой точки может изменить их количество

    def test_vertexes3(self):
        assert self.f.add(R2Point(1.0, 1.0)).points.size() == 4
    # изменения выпуклой оболочки могут и уменьшать их количество

    def test_vertexes4(self):
        assert self.f.add(
            R2Point(
                0.4,
                1.0)).add(
            R2Point(
                1.0,
                0.4)).add(
                    R2Point(
                        0.8,
                        0.9)).add(
                            R2Point(
                                0.9,
                                0.8)).points.size() == 7
        assert self.f.add(R2Point(2.0, 2.0)).points.size() == 4

    # Изменение периметра многоугольника
    # изначально он равен сумме длин сторон
    def test_perimeter1(self):
        assert self.f.perimeter() == approx(2.0 + sqrt(2.0))

    # добавление точки может его изменить
    def test_perimeter2(self):
        assert self.f.add(R2Point(1.0, 1.0)).perimeter() == approx(4.0)

    # Изменение площади многоугольника
    # изначально она равна (неориентированной) площади треугольника
    def test_аrea1(self):
        assert self.f.area() == approx(0.5)

    # добавление точки может увеличить площадь
    def test_area2(self):
        assert self.f.add(R2Point(1.0, 1.0)).area() == approx(1.0)

    # мощность пересечения
    def test_isp0(self):
        assert self.f.isp() == 0

    def test_isp1(self):
        self.f = Void(Segment(R2Point(1, 1), R2Point(4, 4)))
        assert self.f.isp() == 0
        self.f = self.f.add(R2Point(0, 0))
        assert self.f.isp() == 0
        self.f = self.f.add(R2Point(4, 0))
        assert self.f.isp() == 0
        self.f = self.f.add(R2Point(4, 4))
        assert self.f.isp() == float('inf')
        self.f = self.f.add(R2Point(0, 4))
        assert self.f.isp() == 1
        self.f = self.f.add(R2Point(4, 8))
        assert self.f.isp() == 1
        self.f = self.f.add(R2Point(-1, -1))
        assert self.f.isp() == 1
        self.f = self.f.add(R2Point(5, 5))
        assert self.f.isp() == 0

    def test_isp2(self):
        self.f = Void(Segment(R2Point(1, 1), R2Point(3, 1)))
        assert self.f.isp() == 0
        self.f = self.f.add(R2Point(1, 0))
        assert self.f.isp() == 0
        self.f = self.f.add(R2Point(3, 0))
        assert self.f.isp() == 0
        self.f = self.f.add(R2Point(2, 4))
        assert self.f.isp() == 2
        self.f = self.f.add(R2Point(1, 4))
        assert self.f.isp() == 2
        self.f = self.f.add(R2Point(3, 4))
        assert self.f.isp() == 2
        self.f = self.f.add(R2Point(0, 0))
        assert self.f.isp() == 1
        self.f = self.f.add(R2Point(5, 0))
        assert self.f.isp() == 0
