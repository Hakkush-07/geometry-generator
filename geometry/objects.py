from decimal import Decimal

epsilon = Decimal(10) ** Decimal(-7)
figure_border = 20

class P:
    def __init__(self, x, y):
        assert abs(x) < figure_border and abs(y) < figure_border
        self.x, self.y = Decimal(x), Decimal(y)

class L:
    def __init__(self, a, b, c):
        assert abs(a) > epsilon or abs(b) > epsilon
        self.a, self.b, self.c = Decimal(a), Decimal(b), Decimal(c)

class C:
    def __init__(self, o, r):
        assert r > epsilon
        self.o, self.r = o, Decimal(r)

class Obj:
    def __init__(self, _id, _type, recipe, parents):
        self.id = _id
        self.type = _type
        self.recipe = recipe if recipe is not None else "initial"
        self.parents = parents if parents is not None else []
        self.depth = max(self.parents, key=lambda obj: obj.depth).depth + 1 if self.parents else 0
        self.label = f"{self.type}({self.id})"
    
    def __repr__(self):
        return self.label
    
    def change_label(self, label):
        self.label = f"${label}$"
    
    def txt(self):
        return f"{self} is {self.recipe.format(*self.parents)}"
    
    def asy(self):
        if self.type == "P":
            pass
        
class Point(Obj, P):
    count = 0
    def __init__(self, x, y, recipe=None, parents=None):
        P.__init__(self, x, y)
        Obj.__init__(self, Point.count, "P", recipe, parents)
        Point.count += 1
    
    def asy(self):
        x = 0 if abs(self.x) < epsilon else self.x
        y = 0 if abs(self.y) < epsilon else self.y
        return f'dot("{self.label}", ({x}, {y}), dir(90));'

class Line(Obj, L):
    count = 0
    def __init__(self, a, b, c, recipe=None, parents=None):
        L.__init__(self, a, b, c)
        Obj.__init__(self, Line.count, "L", recipe, parents)
        Line.count += 1
    
    def asy(self):
        return ""

class Circle(Obj, C):
    count = 0
    def __init__(self, o, r, recipe=None, parents=None):
        C.__init__(self, o, r)
        Obj.__init__(self, Circle.count, "C", recipe, parents)
        Circle.count += 1
    
    def asy(self):
        x = 0 if abs(self.o.x) < epsilon else self.o.x
        y = 0 if abs(self.o.y) < epsilon else self.o.y
        return f"draw(circle(({x}, {y}), {self.r}));"
