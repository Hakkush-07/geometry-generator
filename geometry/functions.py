from .objects import P, L, C, epsilon, Decimal
from math import atan, pi
from itertools import combinations, permutations

def distance_pp(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2).sqrt()

def distance_pl(a, u):
    return abs(u.a * a.x + u.b * a.y - u.c) / (u.a ** 2 + u.b ** 2).sqrt()

def angle(u, v):
    x = u.a * v.a + u.b * v.b
    return abs(Decimal(atan((v.a * u.b - u.a * v.b) / x))) if x else Decimal(pi) / Decimal(2)

def midpoint(a, b):
    """
    2,0,0
    midpoint of {0}{1}
    """
    return P((a.x + b.x) / 2, (a.y + b.y) / 2)

def line(a, b):
    """
    2,0,0
    line {0}{1}
    """
    return L(b.y - a.y, a.x - b.x, a.x * b.y - a.y * b.x)

def perpendicular_bisector(a, b):
    """
    2,0,0
    perpendicular bisector of {0}{1}
    """
    return L(a.x - b.x, a.y - b.y, (a.x ** 2 + a.y ** 2 - b.x ** 2 - b.y ** 2) / 2)

def circle_diameter(a, b):
    """
    2,0,0
    circle with diameter {0}{1}
    """
    return C(midpoint(a, b), distance_pp(a, b) / 2)

def reflection_pp(a, b):
    """
    2,0,0
    reflection of {0} over {1}
    """
    return P(2 * b.x - a.x, 2 * b.y - a.y)

def reflections_pp(a, b):
    """
    2,0,0
    reflection of {0} over {1}
    reflection of {1} over {0}
    """
    return reflection_pp(a, b), reflection_pp(b, a)

def perpendicular_through(a, b):
    """
    2,0,0
    line through {0} perpendicular to {0}{1}
    """
    return L(a.x - b.x, a.y - b.y, a.x ** 2 + a.y ** 2 - a.x * b.x - a.y * b.y)

def perpendicular_throughs(a, b):
    """
    2,0,0
    line through {0} perpendicular to {0}{1}
    line through {1} perpendicular to {1}{0}
    """
    return perpendicular_through(a, b), perpendicular_through(b, a)

def circle_centered(a, b):
    """
    2,0,0
    circle centered {0} through {1}
    """
    return C(a, distance_pp(a, b))

def circle_centereds(a, b):
    """
    2,0,0
    circle centered {0} through {1}
    circle centered {1} through {0}
    """
    return circle_centered(a, b), circle_centered(b, a)

def reflection_pl(a, u):
    """
    1,1,0
    reflection of {0} over {1}
    """
    return reflection_pp(a, foot(a, u))

def foot(a, u):
    """
    1,1,0
    foot of {0} over {1}
    """
    return intersection_ll(u, perpendicular_line(a, u))

def perpendicular_line(a, u):
    """
    1,1,0
    line through {0} perpendicular to {1}
    """
    return L(u.b, -u.a, a.x * u.b - a.y * u.a)

def parallel_line(a, u):
    """
    1,1,0
    line through {0} parallel to {1}
    """
    return L(u.a, u.b, a.x * u.a + a.y * u.b)

def tangent_points(a, s):
    """
    1,0,1
    a tangency point from {0} to {1}
    a tangency point from {0} to {1}
    """
    return intersections_cc(s, circle_diameter(a, s.o))

def tangent_lines(a, s):
    """
    1,0,1
    line through {0} tangent to {1}
    line through {0} tangent to {1}
    """
    tp1, tp2 = tangent_points(a, s)
    tl1 = line(a, tp1) if tp1 else None
    tl2 = line(a, tp2) if tp2 else None
    return tl1, tl2

def polar(a, s):
    """
    1,0,1
    polar line of {0} wrt {1}
    """
    d = (s.r / distance_pp(a, s.o)) ** 2
    p = P(s.o.x + d * (a.x - s.o.x), s.o.y + d * (a.y - s.o.y))
    return perpendicular_through(p, s.o)

def circle_pc(a, s):
    """
    1,0,1
    circle with diameter {0} and center of {1}
    """
    return circle_diameter(a, s.o)

def intersection_ll(u, v):
    """
    0,2,0
    intersection of {0} and {1}
    """
    return P((u.c * v.b - u.b * v.c) / (u.a * v.b - u.b * v.a), (u.c * v.a - u.a * v.c) / (u.b * v.a - u.a * v.b))

def angle_bisector_1(u, v):
    """
    0,2,0
    an angle bisectors of {0} and {1}
    """
    return L(u.a / (u.a ** 2 + u.b ** 2).sqrt() - v.a / (v.a ** 2 + v.b ** 2).sqrt(), u.b / (u.a ** 2 + u.b ** 2).sqrt() - v.b / (v.a ** 2 + v.b ** 2).sqrt(), u.c / (u.a ** 2 + u.b ** 2).sqrt() - v.c / (v.a ** 2 + v.b ** 2).sqrt())

def angle_bisector_2(u, v):
    """
    0,2,0
    an angle bisectors of {0} and {1}
    """
    return L(u.a / (u.a ** 2 + u.b ** 2).sqrt() + v.a / (v.a ** 2 + v.b ** 2).sqrt(), u.b / (u.a ** 2 + u.b ** 2).sqrt() + v.b / (v.a ** 2 + v.b ** 2).sqrt(), u.c / (u.a ** 2 + u.b ** 2).sqrt() + v.c / (v.a ** 2 + v.b ** 2).sqrt())

def angle_bisectors(u, v):
    """
    0,2,0
    an angle bisector of {0} and {1}
    an angle bisector of {0} and {1}
    """
    return angle_bisector_1(u, v), angle_bisector_2(u, v)

def reflection_ll(u, v):
    """
    0,2,0
    reflection of {0} over {1}
    """
    i = intersection_ll(u, v)
    x, y = i.x, i.y
    m = u.a * v.b * v.b - u.a * v.a * v.a - 2 * u.b * v.a * v.b
    n = u.b * v.b * v.b - u.b * v.a * v.a - 2 * u.a * v.a * v.b
    return L(m, -n, x * m - y * n)

def reflections_ll(u, v):
    """
    0,2,0
    reflection of {0} over {1}
    reflection of {1} over {0}
    """
    return reflection_ll(u, v), reflection_ll(v, u)

def intersection_lc_1(u, s):
    """
    0,1,1
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
    0,1,1
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
    0,1,1
    an intersections of {0} and {1}
    an intersections of {0} and {1}
    """
    return intersection_lc_1(u, s), intersection_lc_2(u, s)

def pole(u, s):
    """
    0,1,1
    pole of {0} wrt {1}
    """
    d = (s.r / distance_pl(s.o, u)) ** 2
    a = foot(s.o, u)
    return P(s.o.x + d * (a.x - s.o.x), s.o.y + d * (a.y - s.o.y))

def intersections_cc(s, t):
    """
    0,0,2
    an intersections of {0} and {1}
    an intersections of {0} and {1}
    """
    return intersections_lc(radical_axis(s, t), s)

def intersection_cc(s, t):
    """
    0,0,2
    tangency point of tangent circles {0} and {1}
    """
    return intersection_ll(line(s.o, t.o), radical_axis(s, t))

def radical_axis(s, t):
    """
    0,0,2
    radical axis of {0} and {1}
    """
    return L(2 * (s.o.x - t.o.x), 2 * (s.o.y - t.o.y), t.r ** 2 - s.r ** 2 + s.o.x ** 2 - t.o.x ** 2 + s.o.y ** 2 - t.o.y ** 2)

def tangent_points_external(s, t):
    """
    0,0,2
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
    0,0,2
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
    0,0,2
    intersection of external tangents of {0} and {1}
    """
    return P((s.o.x * t.r - t.o.x * s.r) / (t.r - s.r), (s.o.y * t.r - t.o.y * s.r) / (t.r - s.r))

def tangent_intersection_internal(s, t):
    """
    0,0,2
    intersection of internal tangents of {0} and {1}
    """
    0,0,2
    return P((s.o.x * t.r + t.o.x * s.r) / (t.r + s.r), (s.o.y * t.r + t.o.y * s.r) / (t.r + s.r))

def tangent_lines_external(s, t):
    """
    0,0,2
    an external tangent of {0} and {1}
    an external tangent of {0} and {1}
    """
    return tangent_lines(tangent_intersection_external(s, t), s)

def tangent_lines_internal(s, t):
    """
    0,0,2
    an internal tangent of {0} and {1}
    an internal tangent of {0} and {1}
    """
    return tangent_lines(tangent_intersection_internal(s, t), s)

def sides(a, b, c):
    """
    3,0,0
    line {1}{2}
    line {2}{0}
    line {0}{1}
    """
    return line(b, c), line(c, a), line(a, b)

def internal_angle_bisector(a, b, c):
    """
    3,0,0
    internal angle bisector of {2}{0}{1}
    """
    u, v = line(a, b), line(c, a)
    return L(u.a / (u.a ** 2 + u.b ** 2).sqrt() - v.a / (v.a ** 2 + v.b ** 2).sqrt(), u.b / (u.a ** 2 + u.b ** 2).sqrt() - v.b / (v.a ** 2 + v.b ** 2).sqrt(), u.c / (u.a ** 2 + u.b ** 2).sqrt() - v.c / (v.a ** 2 + v.b ** 2).sqrt())

def internal_angle_bisectors(a, b, c):
    """
    3,0,0
    internal angle bisector of {2}{0}{1}
    internal angle bisector of {0}{1}{2}
    internal angle bisector of {1}{2}{0}
    """
    return internal_angle_bisector(a, b, c), internal_angle_bisector(b, c, a), internal_angle_bisector(c, a, b)

def external_angle_bisector(a, b, c):
    """
    3,0,0
    external angle bisector of {2}{0}{1}
    """
    u, v = line(a, b), line(c, a)
    return L(u.a / (u.a ** 2 + u.b ** 2).sqrt() + v.a / (v.a ** 2 + v.b ** 2).sqrt(), u.b / (u.a ** 2 + u.b ** 2).sqrt() + v.b / (v.a ** 2 + v.b ** 2).sqrt(), u.c / (u.a ** 2 + u.b ** 2).sqrt() + v.c / (v.a ** 2 + v.b ** 2).sqrt())

def external_angle_bisectors(a, b, c):
    """
    3,0,0
    external angle bisector of {2}{0}{1}
    external angle bisector of {0}{1}{2}
    external angle bisector of {1}{2}{0}
    """
    return external_angle_bisector(a, b, c), external_angle_bisector(b, c, a), external_angle_bisector(c, a, b)

def altitude(a, b, c):
    """
    3,0,0
    altitude from {0} to {1}{2}
    """
    return perpendicular_line(a, line(b, c))

def altitudes(a, b, c):
    """
    3,0,0
    altitude from {0} to {1}{2}
    altitude from {1} to {2}{0}
    altitude from {2} to {0}{1}
    """
    return altitude(a, b, c), altitude(b, c, a), altitude(c, a, b)

def median(a, b, c):
    """
    3,0,0
    median-{0} of {0}{1}{2}
    """
    return line(a, midpoint(b, c))

def medians(a, b, c):
    """
    3,0,0
    median-{0} of {0}{1}{2}
    median-{1} of {0}{1}{2}
    median-{2} of {0}{1}{2}
    """
    return median(a, b, c), median(b, c, a), median(c, a, b)

def foot_ppp(a, b, c):
    """
    3,0,0
    foot of {0} on {1}{2}
    """
    return foot(a, line(b, c))

def feet(a, b, c):
    """
    3,0,0
    foot of {0} on {1}{2}
    foot of {1} on {2}{0}
    foot of {2} on {0}{1}
    """
    return foot_ppp(a, b, c), foot_ppp(b, c, a), foot_ppp(c, a, b)

def midpoints(a, b, c):
    """
    3,0,0
    midpoint of {1}{2}
    midpoint of {2}{0}
    midpoint of {0}{1}
    """
    return midpoint(b, c), midpoint(c, a), midpoint(a, b)

def tangent(a, b, c):
    """
    3,0,0
    tangent line from {0} to circumcircle of {0}{1}{2}
    """
    return perpendicular_through(a, circumcenter(a, b, c))

def tangents(a, b, c):
    """
    3,0,0
    tangent line from {0} to circumcircle of {0}{1}{2}
    tangent line from {1} to circumcircle of {0}{1}{2}
    tangent line from {2} to circumcircle of {0}{1}{2}
    """
    return tangent(a, b, c), tangent(b, c, a), tangent(c, a, b)

def circumcenter(a, b, c):
    """
    3,0,0
    circumcenter of {0}{1}{2}
    """
    return intersection_ll(perpendicular_bisector(a, b), perpendicular_bisector(a, c))

def circumradius(a, b, c):
    """
    3,0,0
    circumradius of {0}{1}{2}
    """
    return distance_pp(a, circumcenter(a, b, c))

def circumcircle(a, b, c):
    """
    3,0,0
    circumcircle of {0}{1}{2}
    """
    return C(circumcenter(a, b, c), circumradius(a, b, c))

def incenter(a, b, c):
    """
    3,0,0
    incenter of {0}{1}{2}
    """
    return intersection_ll(internal_angle_bisector(b, c, a), internal_angle_bisector(c, a, b))

def inradius(a, b, c):
    """
    3,0,0
    inradius of {0}{1}{2}
    """
    return distance_pl(incenter(a, b, c), line(b, c))

def incircle(a, b, c):
    """
    3,0,0
    incircle of {0}{1}{2}
    """
    return C(incenter(a, b, c), inradius(a, b, c))

def excenter(a, b, c):
    """
    3,0,0
    excenter-{0} of {0}{1}{2}
    excenter-{1} of {0}{1}{2}
    excenter-{2} of {0}{1}{2}
    """
    return intersection_ll(external_angle_bisector(b, c, a), external_angle_bisector(c, a, b))

def exradius(a, b, c):
    """
    3,0,0
    exradius-{0} of {0}{1}{2}
    """
    return distance_pl(excenter(a, b, c), line(b, c))

def excenters(a, b, c):
    """
    3,0,0
    excenter-{0} of {0}{1}{2}
    excenter-{1} of {0}{1}{2}
    excenter-{2} of {0}{1}{2}
    """
    return excenter(a, b, c), excenter(b, c, a), excenter(c, a, b)

def excircle(a, b, c):
    """
    3,0,0
    excircle-{0} of {0}{1}{2}
    """
    return C(excenter(a, b, c), exradius(a, b, c))

def excircles(a, b, c):
    """
    3,0,0
    excircle-{0} of {0}{1}{2}
    excircle-{1} of {0}{1}{2}
    excircle-{2} of {0}{1}{2}
    """
    return excircle(a, b, c), excircle(b, c, a), excircle(c, a, b)

def orthocenter(a, b, c):
    """
    3,0,0
    orthocenter of {0}{1}{2}
    """
    return intersection_ll(altitude(b, c, a), altitude(c, a, b))

def centroid(a, b, c):
    """
    3,0,0
    centroid of {0}{1}{2}
    """
    return P((a.x + b.x + c.x) / 3, (a.y + b.y + c.y) / 3)

def intersection_ppl(a, b, u):
    """
    2,1,0
    intersection of {0}{1} and {2}
    """
    return intersection_ll(line(a, b), u)

def tangent_points_ppl(a, b, u):
    """
    2,1,0
    a tangency point of circle through {0}, {1} and tangent to {2}
    a tangency point of circle through {0}, {1} and tangent to {2}
    """
    x = intersection_ppl(a, b, u)
    r2 = distance_pp(x, a) * distance_pp(x, b)
    return intersections_lc(u, C(x, r2.sqrt()))

def tangent_circles_ppl(a, b, u):
    """
    2,1,0
    a circle through {0}, {1} and tangent to {2}
    a circle through {0}, {1} and tangent to {2}
    """
    c, d = tangent_points_ppl(a, b, u)
    return circumcircle(a, b, c), circumcircle(a, b, d)

def intersections_ppc(a, b, s):
    """
    2,0,1
    an intersection of {0}{1} and {2}
    an intersection of {0}{1} and {2}
    """
    return intersections_lc(line(a, b), s)

def radical_center(s, t, m):
    """
    0,0,3
    radical center of {0}, {1}, {2}
    """
    return intersection_ll(radical_axis(s, t), radical_axis(s, m))

def intersections_pppp(a, b, c, d):
    """
    4,0,0
    intersection of {0}{1} and {2}{3}
    intersection of {0}{2} and {1}{3}
    intersection of {0}{3} and {1}{2}
    """
    return intersection_ll(line(a, b), line(c, d)), intersection_ll(line(a, c), line(b, d)), intersection_ll(line(a, d), line(b, c))

def intersection_pppp(a, b, c, d):
    """
    4,0,0
    an intersection of circumcircle of {0}{1}{2} and {0}{3}
    an intersection of circumcircle of {0}{1}{2} and {0}{3}
    """
    return intersections_lc(line(a, d), circumcircle(a, b, c))

def intersections_pppl(a, b, c, u):
    """
    3,1,0
    an intersection of circumcircle of {0}{1}{2} and {3}
    an intersection of circumcircle of {0}{1}{2} and {3}
    """
    return intersections_lc(u, circumcircle(a, b, c))

def intersections_pppc(a, b, c, s):
    """
    3,0,1
    an intersection of circumcircle of {0}{1}{2} and {3}
    an intersection of circumcircle of {0}{1}{2} and {3}
    """
    return intersections_cc(s, circumcircle(a, b, c))

def intersections_ppppp(a, b, c, d, e):
    """
    5,0,0
    an intersection of {0}{1} and circumcircle of {2}{3}{4}
    an intersection of {0}{1} and circumcircle of {2}{3}{4}
    """
    return intersections_lc(line(a, b), circumcircle(c, d, e))

def intersection_ppppp(a, b, c, d, e):
    """
    5,0,0
    intersection of circumcircles of {0}{1}{2} and {0}{3}{4}
    """
    return intersections_cc(circumcircle(a, b, c), circumcircle(a, d, e))

def different_points(*points):
    for a, b in combinations(points, 2):
        if abs(a.x - b.x) < epsilon and abs(a.y - b.y) < epsilon:
            return False
    return True

def different_lines(*lines):
    for u, v in combinations(lines, 2):
        if abs(u.a * v.c - u.c * v.a) < epsilon and abs(u.b * v.c - u.c * v.b) < epsilon:
            return False
    return True

def different_circles(*circles):
    for s, t in combinations(circles, 2):
        if not different_points(s.o, t.o) and abs(s.r - t.r) < epsilon:
            return False
    return True

def not_three_collinear(*points):
    return not any([is_collinear(a, b, c) for a, b, c in combinations(points, 3)])

def not_two_parallel(*lines):
    return not any([is_parallel(u, v) for u, v in combinations(lines, 2)])

def not_isosceles_trapezoid_or_parallelogram(a, b, c, d):
    for aa, bb, cc, dd in permutations((a, b, c, d), 4):
        if is_parallel(line(aa, bb), line(cc, dd)) and abs(distance_pp(aa, cc) - distance_pp(bb, dd)) < epsilon:
            return False
    return True

def not_deltoid(a, b, c, d):
    for aa, bb, cc, dd in permutations((a, b, c, d), 4):
        if is_perpendicular(line(aa, cc), line(bb, dd)) and (abs(distance_pp(aa, bb) - distance_pp(aa, dd)) < epsilon or abs(distance_pp(bb, aa) - distance_pp(bb, cc))):
            return False
    return True

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

def is_collinear(a, b, c):
    """
    3,0,0
    {0}, {1}, {2} are collinear
    """
    return distance_pl(a, line(b, c)) < epsilon

def is_concyclic(a, b, c, d):
    """
    4,0,0
    {0}, {1}, {2}, {3} are concyclic
    """
    return abs(angle(line(a, b), line(a, c)) - angle(line(d, b), line(d, c))) < epsilon and abs(angle(line(b, a), line(b, c)) - angle(line(d, a), line(d, c))) < epsilon

def is_concurrent(u, v, w):
    """
    0,3,0
    {0}, {1}, {2} are concurrent
    """
    return abs(u.a * v.c * w.b + u.b * v.a * w.c + u.c * v.b * w.a - u.a * v.b * w.c - u.b * v. c * w.a - u.c * v.a * w.b) < epsilon

def is_parallel(u, v):
    """
    0,2,0
    {0} and {1} are parallel
    """
    return angle(u, v) < epsilon

def is_perpendicular(u, v):
    """
    0,2,0
    {0} and {1} are perpendicular
    """
    return Decimal(pi) / Decimal(2) - angle(u, v) < epsilon

def is_tangent(s, t):
    """
    0,0,2
    {0} and {1} are tangent
    """
    d = distance_pp(s.o, t.o)
    return abs(d - (s.r + t.r)) < epsilon or abs(d - abs(s.r - t.r)) < epsilon

def is_pl(a, u):
    """
    1,1,0
    {0} is on {1}
    """
    return distance_pl(a, u) < epsilon

def is_pc(a, s):
    """
    1,0,1
    {0} is on {1}
    """
    return pcr(a, s) == 0

def is_lc(u, s):
    """
    0,1,1
    {0} is tangent to {1}
    """
    return lcr(u, s) == 0

def not_pl(a, u):
    return not is_pl(a, u)

def out_pc(a, s):
    return pcr(a, s) == 1

def intersecting_lc(u, s):
    return lcr(u, s) == -1

def not_through_center(u, s):
    return not_pl(s.o, u)

def different_radius(*circles):
    for s, t in combinations(circles, 2):
        if abs(s.r - t.r) < epsilon:
            return False
    return True

def different_center(*circles):
    for s, t in combinations(circles, 2):
        if not different_points(s.o, t.o):
            return False
    return True

def nice_circles(s, t):
    return different_center(s, t) and different_radius(s, t)

def cc_1(s, t):
    return ccr(s, t) == 2

def cc_2(s, t):
    return ccr(s, t) == 1

def cc_3(s, t):
    return ccr(s, t) == 0

def cc_4(s, t):
    return ccr(s, t) == -1

def not_centers_collinear(s, t, m):
    return not is_collinear(s.o, t.o, m.o)

def nice_ppl(a, b, u):
    return different_points(a, b) and not is_parallel(line(a, b), u) and not_pl(a, u) and not_pl(b, u)

def nice_ppc(a, b, s):
    return different_points(a, b) and intersecting_lc(line(a, b), s)

def nice_pppl(a, b, c, u):
    return different_points(a, b, c) and not is_collinear(a, b, c) and intersecting_lc(u, circumcircle(a, b, c))

def nice_pppc(a, b, c, s):
    return different_points(a, b, c) and not is_collinear(a, b, c) and ccr(s, circumcircle(a, b, c)) == 2

def nice_ppppp(a, b, c, d, e):
    return lcr(line(a, b), circumcircle(c, d, e)) == -1
