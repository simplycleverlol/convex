#Задача: выяснить, пересекается отрезок с полосой, -1 < y < 1, или нет
#Функция должна возвращать логическое значение
from r2point import R2Point as R2

def r2less(a: R2, b: R2): # True if a < b
    Ba, Bb = a.x+a.y, b.x+b.y # y = -x + B
    if Ba == Bb: # => на одной прямой
        return a.y < b.y
    return Ba < Bb

def intersec(a: R2, b: R2):
    if -1 < a.y < 1 or -1 < b.y < 1:
        return True
    return a.y <= -1.0 and b.y >= 1.0 or b.y <= -1 and a.y >= 1
    
class seg:
    #Для успешного хранения отрезков в множестве, им нужно иметь хэш
    #Хэш удобно считать как хэш соответствующего кортежа, но как привести
    #отрезки с одинаковыми точками в разном порядке к одному виду?
    #Определю отношение точек - точка меньше другой, если она 
    # лежит строго ниже прямой y = -x + b, содержащей другую точку,
    # или на одной прямой с ней, но ниже по y-координате
    def __init__(self, a, b) -> None:
        self.a, self.b = (a, b) if r2less(a, b) else (b, a)
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        if self is other:
            return True
        return self.a == other.a and self.b == other.b
    
    #def __hash__(self) -> int:
    #    return (self.a.x, self.a.y, self.b.x, self.b.y).__hash__()
    
    def intersec(self):
        return intersec(self.a, self.b)
    
if __name__ == '__main__':
    a, b = R2(-1.1, 1), R2(7.7, -1.1)
    print(seg(a, b) == seg(b, a))
    print(seg(a, b) in {seg(b, a), None})
