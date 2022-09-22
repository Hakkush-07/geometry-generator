from decimal import Decimal
from itertools import combinations, permutations
from math import atan, pi, sin, cos

class P:
    def __init__(self, x, y):
        assert abs(x) < figure_border and abs(y) < figure_border
        self.x, self.y = Decimal(x), Decimal(y)
    
    def __matmul__(self, other):
        return abs(self.x - other.x) < epsilon and abs(self.y - other.y) < epsilon
    
    @staticmethod
    def dir(angle):
        return P(cos(angle), sin(angle))

class L:
    def __init__(self, a, b, c):
        assert abs(a) > epsilon or abs(b) > epsilon
        self.a, self.b, self.c = Decimal(a), Decimal(b), Decimal(c)
    
    def __matmul__(self, other):
        return abs(self.a * other.c - self.c * other.a) < epsilon and abs(self.b * other.c - self.c * other.b) < epsilon

class C:
    def __init__(self, o, r):
        assert abs(r) > epsilon
        self.o, self.r = o, Decimal(r)
    
    def __matmul__(self, other):
        return self.o @ other.o and abs(self.r - other.r) < epsilon

class Point(P):
    count = 0
    def __init__(self, point, recipe="an initial point", parents=()):
        super().__init__(point.x, point.y)
        self.id = Point.count
        Point.count += 1
        self.recipe = recipe
        self.parents = parents
        self.depth = max(self.parents, key=lambda obj: obj.depth).depth + 1 if self.parents else 0
    
    def __repr__(self):
        return f"Point({self.id})"
    
    def asy(self):
        x = 0 if abs(self.x) < epsilon else self.x
        y = 0 if abs(self.y) < epsilon else self.y
        return f'dot("$P{self.id}$", ({x}, {y}), dir(90));\n'
    
    def asy2(self):
        x = 0 if abs(self.x) < epsilon else self.x
        y = 0 if abs(self.y) < epsilon else self.y
        return f'dot("{self}", ({x}, {y}), dir(90));\n'
    
    def txt(self):
        return f"{self} is {self.recipe.format(*self.parents)}\n"

class Line(L):
    count = 0
    def __init__(self, line, recipe="an initial line", parents=()):
        super().__init__(line.a, line.b, line.c)
        self.id = Line.count
        Line.count += 1
        self.recipe = recipe
        self.parents = parents
        self.depth = max(self.parents, key=lambda obj: obj.depth).depth + 1 if self.parents else 0
    
    def __repr__(self):
        return f"Line({self.id})"
    
    def asy(self, pls, w):
        k = Decimal(0.1)
        if not pls:
            return "\n"
        if len(pls) == 1:
            x, y = pls[0].x, pls[0].y
            w = max(w, Decimal(2.5))
            d = w * k
            if abs(self.a) < epsilon:
                ax = x - d
                bx = x + d
                ay = by = self.c / self.b
                ax = 0 if abs(ax) < epsilon else ax
                ay = 0 if abs(ay) < epsilon else ay
                bx = 0 if abs(bx) < epsilon else bx
                by = 0 if abs(by) < epsilon else by
                return f"draw(({ax}, {ay}) -- ({bx}, {by}));\n"
            if abs(self.b) < epsilon:
                d = w * k
                ay = y - d
                by = y + d
                ax = bx = self.c / self.a
                ax = 0 if abs(ax) < epsilon else ax
                ay = 0 if abs(ay) < epsilon else ay
                bx = 0 if abs(bx) < epsilon else bx
                by = 0 if abs(by) < epsilon else by
                return f"draw(({ax}, {ay}) -- ({bx}, {by}));\n"
            a = atan(-self.a / self.b)
            dxm = w * k * Decimal(cos(a))
            dym = w * k * Decimal(sin(a))
            ax = x - dxm
            bx = x + dxm
            ay = y - dym
            by = y + dym
            ax = 0 if abs(ax) < epsilon else ax
            ay = 0 if abs(ay) < epsilon else ay
            bx = 0 if abs(bx) < epsilon else bx
            by = 0 if abs(by) < epsilon else by
            return f"draw(({ax}, {ay}) -- ({bx}, {by}));\n"
        if abs(self.a) < epsilon:
            p_min, p_max = min(pls, key=lambda p: p.x), max(pls, key=lambda p: p.x)
            d = p_max.x - p_min.x
            dm = d * k
            ax = p_min.x - dm
            bx = p_max.x + dm
            ay = by = self.c / self.b
            ax = 0 if abs(ax) < epsilon else ax
            ay = 0 if abs(ay) < epsilon else ay
            bx = 0 if abs(bx) < epsilon else bx
            by = 0 if abs(by) < epsilon else by
            return f"draw(({ax}, {ay}) -- ({bx}, {by}));\n"
        if abs(self.b) < epsilon:
            p_min, p_max = min(pls, key=lambda p: p.y), max(pls, key=lambda p: p.y)
            d = p_max.y - p_min.y
            dm = d * k
            ay = p_min.y - dm
            by = p_max.y + dm
            ax = bx = self.c / self.a
            ax = 0 if abs(ax) < epsilon else ax
            ay = 0 if abs(ay) < epsilon else ay
            bx = 0 if abs(bx) < epsilon else bx
            by = 0 if abs(by) < epsilon else by
            return f"draw(({ax}, {ay}) -- ({bx}, {by}));\n"
        p_min, p_max = min(pls, key=lambda p: p.x), max(pls, key=lambda p: p.x)
        dx = p_max.x - p_min.x
        dy = p_max.y - p_min.y
        dxm = dx * k
        dym = dy * k
        ax = p_min.x - dxm
        bx = p_max.x + dxm
        ay = p_min.y - dym
        by = p_max.y + dym
        ax = 0 if abs(ax) < epsilon else ax
        ay = 0 if abs(ay) < epsilon else ay
        bx = 0 if abs(bx) < epsilon else bx
        by = 0 if abs(by) < epsilon else by
        return f"draw(({ax}, {ay}) -- ({bx}, {by}));\n"
    
    def txt(self):
        return f"{self} is {self.recipe.format(*self.parents)}\n"

class Circle(C):
    count = 0
    def __init__(self, circle, recipe="an initial circle", parents=()):
        super().__init__(circle.o, circle.r)
        self.id = Circle.count
        Circle.count += 1
        self.recipe = recipe
        self.parents = parents
        self.depth = max(self.parents, key=lambda obj: obj.depth).depth + 1 if self.parents else 0
    
    def __repr__(self):
        return f"Circle({self.id})"
    
    def asy(self):
        x = 0 if abs(self.o.x) < epsilon else self.o.x
        y = 0 if abs(self.o.y) < epsilon else self.o.y
        return f"draw(circle(({x}, {y}), {self.r}));\n"
    
    def txt(self):
        return f"{self} is {self.recipe.format(*self.parents)}\n"

# constants

epsilon = Decimal(10) ** Decimal(-7)
figure_border = 500

# control

collinear_str = "{0}, {1}, {2} are collinear"
concyclic_str = "{0}, {1}, {2}, {3} are concyclic"
equal_str = "{0}{1} and {2}{3} have same length"
concurrent_str = "{0}, {1}, {2} are concurrent"
parallel_str = "{0} and {1} are parallel"
perpendicular_str = "{0} and {1} are perpendicular"
pl_str = "{0} is on {1}"
pc_str = "{0} is on {1}"
lc_str = "{0} is tangent to {1}"

def is_collinear(a, b, c):
    return distance_pl(a, line(b, c)) < epsilon

def is_concyclic(a, b, c, d):
    return abs(angle(line(a, b), line(a, c)) - angle(line(d, b), line(d, c))) < epsilon and abs(angle(line(b, a), line(b, c)) - angle(line(d, a), line(d, c))) < epsilon

def is_concurrent(u, v, w):
    return abs(u.a * v.c * w.b + u.b * v.a * w.c + u.c * v.b * w.a - u.a * v.b * w.c - u.b * v. c * w.a - u.c * v.a * w.b) < epsilon

def is_parallel(u, v):
    return angle(u, v) < epsilon

def is_perpendicular(u, v):
    return Decimal(pi) / Decimal(2) - angle(u, v) < epsilon

def is_tangent(s, t):
    d = distance_pp(s.o, t.o)
    return abs(d - (s.r + t.r)) < epsilon or abs(d - abs(s.r - t.r)) < epsilon

def is_pl(a, u):
    return distance_pl(a, u) < epsilon

def is_pc(a, s):
    return pcr(a, s) == 0

def is_lc(u, s):
    return lcr(u, s) == 0

def is_different_points(points):
    return not any([a @ b for a, b in combinations(points, 2)])

def not_three_collinear(points):
    return not any([is_collinear(a, b, c) for a, b, c in combinations(points, 3)])

def is_isosceles_trapezoid_or_parallelogram(a, b, c, d):
    for aa, bb, cc, dd in permutations((a, b, c, d), 4):
        if is_parallel(line(aa, bb), line(cc, dd)) and abs(distance_pp(aa, cc) - distance_pp(bb, dd)) < epsilon:
            return True
    return False

def is_deltoid(a, b, c, d):
    for aa, bb, cc, dd in permutations((a, b, c, d), 4):
        if is_perpendicular(line(aa, cc), line(bb, dd)) and (abs(distance_pp(aa, bb) - distance_pp(aa, dd)) < epsilon or abs(distance_pp(bb, aa) - distance_pp(bb, cc))):
            return True
    return False

def is_different_lines(lines):
    return not any([u @ v for u, v in combinations(lines, 2)])

def not_two_parallel(lines):
    return not any([is_parallel(u, v) for u, v in combinations(lines, 2)])

def is_different_circles(circles):
    return not any([s @ t for s, t in combinations(circles, 2)])

def is_bad_circles(s, t):
    return s.o @ t.o or abs(s.r - t.r) < epsilon

def pcr(a, s):
    x = distance_pp(s.o, a) - s.r
    if abs(x) < epsilon:
        return 0
    return -1 if x < 0 else 1

def lcr(u, s):
    x = distance_pl(s.o, u) - s.r
    if abs(x) < epsilon:
        return 0
    return -1 if x < 0 else 1

def ccr(s, t):
    # -2: out inside, -1: on inside, 0: on outside, 1: out outside, 2: in
    reg = lcr(radical_axis(s, t), s)
    ins = distance_pp(s.o, t.o) - abs(s.r - t.r) < epsilon
    if ins:
        if reg == 1:
            return -2
        elif reg == 0:
            return -1
    else:
        if reg == 1:
            return 1
        elif reg == 0:
            return 0
        elif reg == -1:
            return 2

def is_nice_pppl(a, b, c, u):
    return lcr(u, circumcircle(a, b, c)) == -1

def is_nice_pppc(a, b, c, s):
    return ccr(s, circumcircle(a, b, c)) == 2

def is_nice_ppppp(a, b, c, d, e):
    return lcr(line(a, b), circumcircle(c, d, e)) == -1

# calculation

def distance_pp(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2).sqrt()

def distance_pl(a, u):
    return abs(u.a * a.x + u.b * a.y - u.c) / (u.a ** 2 + u.b ** 2).sqrt()

def angle(u, v):
    x = u.a * v.a + u.b * v.b
    return abs(Decimal(atan((v.a * u.b - u.a * v.b) / x))) if x else Decimal(pi) / Decimal(2)

# pp

def midpoint(a, b):
    """
    midpoint of {0}{1}
    """
    return P((a.x + b.x) / 2, (a.y + b.y) / 2)

def line(a, b):
    """
    line {0}{1}
    """
    return L(b.y - a.y, a.x - b.x, a.x * b.y - a.y * b.x)

def perpendicular_bisector(a, b):
    """
    perpendicular bisector of {0}{1}
    """
    return L(a.x - b.x, a.y - b.y, (a.x ** 2 + a.y ** 2 - b.x ** 2 - b.y ** 2) / 2)

def circle_diameter(a, b):
    """
    circle with diameter {0}{1}
    """
    return C(midpoint(a, b), distance_pp(a, b) / 2)

def reflection_pp(a, b):
    """
    reflection of {0} over {1}
    """
    return P(2 * b.x - a.x, 2 * b.y - a.y)

def reflections_pp(a, b):
    """
    reflection of {0} over {1}
    reflection of {1} over {0}
    """
    return reflection_pp(a, b), reflection_pp(b, a)

def perpendicular_through(a, b):
    """
    line through {0} perpendicular to {0}{1}
    """
    return L(a.x - b.x, a.y - b.y, a.x ** 2 + a.y ** 2 - a.x * b.x - a.y * b.y)

def perpendicular_throughs(a, b):
    """
    line through {0} perpendicular to {0}{1}
    line through {1} perpendicular to {1}{0}
    """
    return perpendicular_through(a, b), perpendicular_through(b, a)

def circle_centered(a, b):
    """
    circle centered {0} through {1}
    """
    return C(a, distance_pp(a, b))

def circle_centereds(a, b):
    """
    circle centered {0} through {1}
    circle centered {1} through {0}
    """
    return circle_centered(a, b), circle_centered(b, a)

pp_fl = [
    midpoint,
    line,
    perpendicular_bisector,
    circle_diameter,
    reflections_pp,
    perpendicular_throughs,
    circle_centereds
]

# pl

def reflection_pl(a, u):
    """
    reflection of {0} over {1}
    """
    return reflection_pp(a, foot(a, u))

def foot(a, u):
    """
    foot of {0} over {1}
    """
    return intersection_ll(u, perpendicular_line(a, u))

def perpendicular_line(a, u):
    """
    line through {0} perpendicular to {1}
    """
    return L(u.b, -u.a, a.x * u.b - a.y * u.a)

def parallel_line(a, u):
    """
    line through {0} parallel to {1}
    """
    return L(u.a, u.b, a.x * u.a + a.y * u.b)

pl_1_fl = [
    perpendicular_line
]

pl_2_fl = [
    reflection_pl,
    foot,
    perpendicular_line,
    parallel_line
]

# pc

def tangent_points(a, s):
    """
    a tangency point from {0} to {1}
    a tangency point from {0} to {1}
    """
    return intersections_cc(s, circle_diameter(a, s.o))

def tangent_lines(a, s):
    """
    line through {0} tangent to {1}
    line through {0} tangent to {1}
    """
    tp1, tp2 = tangent_points(a, s)
    tl1 = line(a, tp1) if tp1 else None
    tl2 = line(a, tp2) if tp2 else None
    return tl1, tl2

def polar(a, s):
    """
    polar line of {0} wrt {1}
    """
    d = (s.r / distance_pp(a, s.o)) ** 2
    p = P(s.o.x + d * (a.x - s.o.x), s.o.y + d * (a.y - s.o.y))
    return perpendicular_through(p, s.o)

def circle_pc(a, s):
    """
    circle with diameter {0} and center of {1}
    """
    return circle_diameter(a, s.o)

pc_1_fl = [
    polar
]

pc_2_fl = [
    polar
]

pc_3_fl = [
    tangent_points,
    tangent_lines,
    polar,
    circle_pc
]

# ll

def intersection_ll(u, v):
    """
    intersection of {0} and {1}
    """
    return P((u.c * v.b - u.b * v.c) / (u.a * v.b - u.b * v.a), (u.c * v.a - u.a * v.c) / (u.b * v.a - u.a * v.b))

def angle_bisector_1(u, v):
    """
    an angle bisectors of {0} and {1}
    """
    return L(u.a / (u.a ** 2 + u.b ** 2).sqrt() - v.a / (v.a ** 2 + v.b ** 2).sqrt(), u.b / (u.a ** 2 + u.b ** 2).sqrt() - v.b / (v.a ** 2 + v.b ** 2).sqrt(), u.c / (u.a ** 2 + u.b ** 2).sqrt() - v.c / (v.a ** 2 + v.b ** 2).sqrt())

def angle_bisector_2(u, v):
    """
    an angle bisectors of {0} and {1}
    """
    return L(u.a / (u.a ** 2 + u.b ** 2).sqrt() + v.a / (v.a ** 2 + v.b ** 2).sqrt(), u.b / (u.a ** 2 + u.b ** 2).sqrt() + v.b / (v.a ** 2 + v.b ** 2).sqrt(), u.c / (u.a ** 2 + u.b ** 2).sqrt() + v.c / (v.a ** 2 + v.b ** 2).sqrt())

def angle_bisectors(u, v):
    """
    an angle bisector of {0} and {1}
    an angle bisector of {0} and {1}
    """
    return angle_bisector_1(u, v), angle_bisector_2(u, v)

def reflection_ll(u, v):
    """
    reflection of {0} over {1}
    """
    i = intersection_ll(u, v)
    x, y = i.x, i.y
    m = u.a * v.b * v.b - u.a * v.a * v.a - 2 * u.b * v.a * v.b
    n = u.b * v.b * v.b - u.b * v.a * v.a - 2 * u.a * v.a * v.b
    return L(m, -n, x * m - y * n)

def reflections_ll(u, v):
    """
    reflection of {0} over {1}
    reflection of {1} over {0}
    """
    return reflection_ll(u, v), reflection_ll(v, u)


ll_fl = [
    intersection_ll,
    angle_bisectors,
    reflections_ll
]

# lc

def intersection_lc_1(u, s):
    """
    an intersections of {0} and {1}
    """
    if abs(u.b) < epsilon:
        a = u.a ** 2 + u.b ** 2
        b = 2 * (s.o.x * u.a * u.b - s.o.y * u.a * u.a - u.b * u.c)
        c = (s.o.y ** 2) * (u.a ** 2) + (u.c ** 2) - 2 * s.o.x * u.a * u.c + (s.o.x ** 2) * (u.a ** 2) - (s.r ** 2) * (u.a ** 2)
        d = (b ** 2 - 4 * a * c).sqrt()
        y = (-b + d) / (2 * a)
        x = (u.c - u.b * y) / u.a
        return P(x, y)
    else:
        a = u.a ** 2 + u.b ** 2
        b = 2 * (s.o.y * u.a * u.b - s.o.x * u.b * u.b - u.a * u.c)
        c = (s.o.x ** 2) * (u.b ** 2) + (u.c ** 2) - 2 * s.o.y * u.b * u.c + (s.o.y ** 2) * (u.b ** 2) - (s.r ** 2) * (u.b ** 2)
        d = (b ** 2 - 4 * a * c).sqrt()
        x = (-b + d) / (2 * a)
        y = (u.c - u.a * x) / u.b
        return P(x, y)

def intersection_lc_2(u, s):
    """
    an intersections of {0} and {1}
    """
    if abs(u.b) < epsilon:
        a = u.a ** 2 + u.b ** 2
        b = 2 * (s.o.x * u.a * u.b - s.o.y * u.a * u.a - u.b * u.c)
        c = (s.o.y ** 2) * (u.a ** 2) + (u.c ** 2) - 2 * s.o.x * u.a * u.c + (s.o.x ** 2) * (u.a ** 2) - (s.r ** 2) * (u.a ** 2)
        d = (b ** 2 - 4 * a * c).sqrt()
        y = (-b - d) / (2 * a)
        x = (u.c - u.b * y) / u.a
        return P(x, y)
    else:
        a = u.a ** 2 + u.b ** 2
        b = 2 * (s.o.y * u.a * u.b - s.o.x * u.b * u.b - u.a * u.c)
        c = (s.o.x ** 2) * (u.b ** 2) + (u.c ** 2) - 2 * s.o.y * u.b * u.c + (s.o.y ** 2) * (u.b ** 2) - (s.r ** 2) * (u.b ** 2)
        d = (b ** 2 - 4 * a * c).sqrt()
        x = (-b - d) / (2 * a)
        y = (u.c - u.a * x) / u.b
        return P(x, y)

def intersections_lc(u, s):
    """
    an intersections of {0} and {1}
    an intersections of {0} and {1}
    """
    return intersection_lc_1(u, s), intersection_lc_2(u, s)

def pole(u, s):
    """
    pole of {0} wrt {1}
    """
    d = (s.r / distance_pl(s.o, u)) ** 2
    a = foot(s.o, u)
    return P(s.o.x + d * (a.x - s.o.x), s.o.y + d * (a.y - s.o.y))

lc_1_fl = [
    intersections_lc,
    pole
]

lc_2_fl = [
    pole
]

lc_3_fl = [
    pole
]

# cc

def intersections_cc(s, t):
    """
    an intersections of {0} and {1}
    an intersections of {0} and {1}
    """
    return intersections_lc(radical_axis(s, t), s)

def intersection_cc(s, t):
    """
    tangency point of tangent circles {0} and {1}
    """
    return intersection_ll(line(s.o, t.o), radical_axis(s, t))

def radical_axis(s, t):
    """
    radical axis of {0} and {1}
    """
    return L(2 * (s.o.x - t.o.x), 2 * (s.o.y - t.o.y), t.r ** 2 - s.r ** 2 + s.o.x ** 2 - t.o.x ** 2 + s.o.y ** 2 - t.o.y ** 2)

def tangent_points_external(s, t):
    """
    an external tangent point of {0} and {1}
    an external tangent point of {0} and {1}
    an external tangent point of {0} and {1}
    an external tangent point of {0} and {1}
    """
    p1, p2 = tangent_points(tangent_intersection_external(s, t), s)
    p3, p4 = tangent_points(tangent_intersection_external(s, t), t)
    return p1, p2, p3, p4

def tangent_points_internal(s, t):
    """
    an internal tangent point of {0} and {1}
    an internal tangent point of {0} and {1}
    an internal tangent point of {0} and {1}
    an internal tangent point of {0} and {1}
    """
    p1, p2 = tangent_points(tangent_intersection_internal(s, t), s)
    p3, p4 = tangent_points(tangent_intersection_internal(s, t), t)
    return p1, p2, p3, p4

def tangent_intersection_external(s, t):
    """
    intersection of external tangents of {0} and {1}
    """
    return P((s.o.x * t.r - t.o.x * s.r) / (t.r - s.r), (s.o.y * t.r - t.o.y * s.r) / (t.r - s.r))

def tangent_intersection_internal(s, t):
    """
    intersection of internal tangents of {0} and {1}
    """
    return P((s.o.x * t.r + t.o.x * s.r) / (t.r + s.r), (s.o.y * t.r + t.o.y * s.r) / (t.r + s.r))

def tangent_lines_external(s, t):
    """
    an external tangent of {0} and {1}
    an external tangent of {0} and {1}
    """
    return tangent_lines(tangent_intersection_external(s, t), s)

def tangent_lines_internal(s, t):
    """
    an internal tangent of {0} and {1}
    an internal tangent of {0} and {1}
    """
    return tangent_lines(tangent_intersection_internal(s, t), s)

cc_1_fl = [
    intersection_cc,
    radical_axis
]

cc_2_fl = [
    intersection_cc,
    tangent_points_external,
    tangent_intersection_external,
    tangent_lines_external,
    radical_axis
]

cc_3_fl = [
    tangent_points_external,
    tangent_points_internal,
    tangent_intersection_external,
    tangent_intersection_internal,
    tangent_lines_external,
    tangent_lines_internal,
    radical_axis
]

cc_4_fl = [
    intersections_cc,
    tangent_points_external,
    tangent_intersection_external,
    tangent_lines_external,
    radical_axis
]

# ppp

def sides(a, b, c):
    """
    line {1}{2}
    line {2}{0}
    line {0}{1}
    """
    return line(b, c), line(c, a), line(a, b)

def internal_angle_bisector(a, b, c):
    """
    internal angle bisector of {2}{0}{1}
    """
    u, v = line(a, b), line(c, a)
    return L(u.a / (u.a ** 2 + u.b ** 2).sqrt() - v.a / (v.a ** 2 + v.b ** 2).sqrt(), u.b / (u.a ** 2 + u.b ** 2).sqrt() - v.b / (v.a ** 2 + v.b ** 2).sqrt(), u.c / (u.a ** 2 + u.b ** 2).sqrt() - v.c / (v.a ** 2 + v.b ** 2).sqrt())

def internal_angle_bisectors(a, b, c):
    """
    internal angle bisector of {2}{0}{1}
    internal angle bisector of {0}{1}{2}
    internal angle bisector of {1}{2}{0}
    """
    return internal_angle_bisector(a, b, c), internal_angle_bisector(b, c, a), internal_angle_bisector(c, a, b)

def external_angle_bisector(a, b, c):
    """
    external angle bisector of {2}{0}{1}
    """
    u, v = line(a, b), line(c, a)
    return L(u.a / (u.a ** 2 + u.b ** 2).sqrt() + v.a / (v.a ** 2 + v.b ** 2).sqrt(), u.b / (u.a ** 2 + u.b ** 2).sqrt() + v.b / (v.a ** 2 + v.b ** 2).sqrt(), u.c / (u.a ** 2 + u.b ** 2).sqrt() + v.c / (v.a ** 2 + v.b ** 2).sqrt())

def external_angle_bisectors(a, b, c):
    """
    external angle bisector of {2}{0}{1}
    external angle bisector of {0}{1}{2}
    external angle bisector of {1}{2}{0}
    """
    return external_angle_bisector(a, b, c), external_angle_bisector(b, c, a), external_angle_bisector(c, a, b)

def altitude(a, b, c):
    """
    altitude from {0} to {1}{2}
    """
    return perpendicular_line(a, line(b, c))

def altitudes(a, b, c):
    """
    altitude from {0} to {1}{2}
    altitude from {1} to {2}{0}
    altitude from {2} to {0}{1}
    """
    return altitude(a, b, c), altitude(b, c, a), altitude(c, a, b)

def median(a, b, c):
    """
    median-{0} of {0}{1}{2}
    """
    return line(a, midpoint(b, c))

def medians(a, b, c):
    """
    median-{0} of {0}{1}{2}
    median-{1} of {0}{1}{2}
    median-{2} of {0}{1}{2}
    """
    return median(a, b, c), median(b, c, a), median(c, a, b)

def foot_ppp(a, b, c):
    """
    foot of {0} on {1}{2}
    """
    return foot(a, line(b, c))

def feet(a, b, c):
    """
    foot of {0} on {1}{2}
    foot of {1} on {2}{0}
    foot of {2} on {0}{1}
    """
    return foot_ppp(a, b, c), foot_ppp(b, c, a), foot_ppp(c, a, b)

def midpoints(a, b, c):
    """
    midpoint of {1}{2}
    midpoint of {2}{0}
    midpoint of {0}{1}
    """
    return midpoint(b, c), midpoint(c, a), midpoint(a, b)

def tangent(a, b, c):
    """
    tangent line from {0} to circumcircle of {0}{1}{2}
    """
    return perpendicular_through(a, circumcenter(a, b, c))

def tangents(a, b, c):
    """
    tangent line from {0} to circumcircle of {0}{1}{2}
    tangent line from {1} to circumcircle of {0}{1}{2}
    tangent line from {2} to circumcircle of {0}{1}{2}
    """
    return tangent(a, b, c), tangent(b, c, a), tangent(c, a, b)

def circumcenter(a, b, c):
    """
    circumcenter of {0}{1}{2}
    """
    return intersection_ll(perpendicular_bisector(a, b), perpendicular_bisector(a, c))

def circumradius(a, b, c):
    """
    circumradius of {0}{1}{2}
    """
    return distance_pp(a, circumcenter(a, b, c))

def circumcircle(a, b, c):
    """
    circumcircle of {0}{1}{2}
    """
    return C(circumcenter(a, b, c), circumradius(a, b, c))

def incenter(a, b, c):
    """
    incenter of {0}{1}{2}
    """
    return intersection_ll(internal_angle_bisector(b, c, a), internal_angle_bisector(c, a, b))

def inradius(a, b, c):
    """
    inradius of {0}{1}{2}
    """
    return distance_pl(incenter(a, b, c), line(b, c))

def incircle(a, b, c):
    """
    incircle of {0}{1}{2}
    """
    return C(incenter(a, b, c), inradius(a, b, c))

def excenter(a, b, c):
    """
    excenter-{0} of {0}{1}{2}
    excenter-{1} of {0}{1}{2}
    excenter-{2} of {0}{1}{2}
    """
    return intersection_ll(external_angle_bisector(b, c, a), external_angle_bisector(c, a, b))

def exradius(a, b, c):
    """
    exradius-{0} of {0}{1}{2}
    """
    return distance_pl(excenter(a, b, c), line(b, c))

def excenters(a, b, c):
    """
    excenter-{0} of {0}{1}{2}
    excenter-{1} of {0}{1}{2}
    excenter-{2} of {0}{1}{2}
    """
    return excenter(a, b, c), excenter(b, c, a), excenter(c, a, b)

def excircle(a, b, c):
    """
    excircle-{0} of {0}{1}{2}
    """
    return C(excenter(a, b, c), exradius(a, b, c))

def excircles(a, b, c):
    """
    excircle-{0} of {0}{1}{2}
    excircle-{1} of {0}{1}{2}
    excircle-{2} of {0}{1}{2}
    """
    return excircle(a, b, c), excircle(b, c, a), excircle(c, a, b)

def orthocenter(a, b, c):
    """
    orthocenter of {0}{1}{2}
    """
    return intersection_ll(altitude(b, c, a), altitude(c, a, b))

def centroid(a, b, c):
    """
    centroid of {0}{1}{2}
    """
    return P((a.x + b.x + c.x) / 3, (a.y + b.y + c.y) / 3)

ppp_fl = [
    sides,
    internal_angle_bisectors, 
    external_angle_bisectors, 
    altitudes,
    medians, 
    feet, 
    midpoints,
    tangents, 
    circumcenter, 
    circumcircle, 
    incenter, 
    incircle, 
    excenters,
    excircles,
    orthocenter, 
    centroid
]

# ppl

def intersection_ppl(a, b, u):
    """
    intersection of {0}{1} and {2}
    """
    return intersection_ll(line(a, b), u)

def tangent_points_ppl(a, b, u):
    """
    a tangency point of circle through {0}, {1} and tangent to {2}
    a tangency point of circle through {0}, {1} and tangent to {2}
    """
    x = intersection_ppl(a, b, u)
    r2 = distance_pp(x, a) * distance_pp(x, b)
    return intersections_lc(u, C(x, r2.sqrt()))

def tangent_circles_ppl(a, b, u):
    """
    a circle through {0}, {1} and tangent to {2}
    a circle through {0}, {1} and tangent to {2}
    """
    c, d = tangent_points_ppl(a, b, u)
    return circumcircle(a, b, c), circumcircle(a, b, d)

ppl_fl = [
    intersection_ppl,
    tangent_points_ppl,
    tangent_circles_ppl
]

# ppc

def intersections_ppc(a, b, s):
    """
    an intersection of {0}{1} and {2}
    an intersection of {0}{1} and {2}
    """
    return intersections_lc(line(a, b), s)

ppc_fl = [
    intersections_ppc
]

# ccc

def radical_center(s, t, m):
    """
    radical center of {0}, {1}, {2}
    """
    return intersection_ll(radical_axis(s, t), radical_axis(s, m))

ccc_fl = [
    radical_center
]

# pppp

def intersections_pppp(a, b, c, d):
    """
    intersection of {0}{1} and {2}{3}
    intersection of {0}{2} and {1}{3}
    intersection of {0}{3} and {1}{2}
    """
    return intersection_ll(line(a, b), line(c, d)), intersection_ll(line(a, c), line(b, d)), intersection_ll(line(a, d), line(b, c))

def intersection_pppp(a, b, c, d):
    """
    an intersection of circumcircle of {0}{1}{2} and {0}{3}
    an intersection of circumcircle of {0}{1}{2} and {0}{3}
    """
    return intersections_lc(line(a, d), circumcircle(a, b, c))

pppp_fl = [
    intersections_pppp,
    intersection_pppp
]

# pppl

def intersections_pppl(a, b, c, u):
    """
    an intersection of circumcircle of {0}{1}{2} and {3}
    an intersection of circumcircle of {0}{1}{2} and {3}
    """
    return intersections_lc(u, circumcircle(a, b, c))

pppl_fl = [
    intersections_pppl
]

# pppc

def intersections_pppc(a, b, c, s):
    """
    an intersection of circumcircle of {0}{1}{2} and {3}
    an intersection of circumcircle of {0}{1}{2} and {3}
    """
    return intersections_cc(s, circumcircle(a, b, c))

pppc_fl = [
    intersections_pppc
]

# ppppp

def intersections_ppppp(a, b, c, d, e):
    """
    an intersection of {0}{1} and circumcircle of {2}{3}{4}
    an intersection of {0}{1} and circumcircle of {2}{3}{4}
    """
    return intersections_lc(line(a, b), circumcircle(c, d, e))

def intersection_ppppp(a, b, c, d, e):
    """
    intersection of circumcircles of {0}{1}{2} and {0}{3}{4}
    """
    return intersections_cc(circumcircle(a, b, c), circumcircle(a, d, e))

ppppp_fl = [
    intersections_ppppp,
    intersection_ppppp
]

