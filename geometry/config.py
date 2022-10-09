from random import random, choice, sample
from math import sin, cos, pi
from itertools import combinations, permutations
from datetime import datetime
from os import mkdir
from .objects import P, L, C, Point, Line, Circle
from .construction import Construction
from .property import Property
from .functions import different_points, different_lines, different_circles

class Config:
    def __init__(self, objects):
        self.objects = list(objects)
        self.properties = Property.default()
    
    @property
    def points(self):
        return [obj for obj in self.objects if obj.type == "P"]
    
    @property
    def lines(self):
        return [obj for obj in self.objects if obj.type == "L"]
    
    @property
    def circles(self):
        return [obj for obj in self.objects if obj.type == "C"]
    
    @staticmethod
    def triangle():
        a = 1.83 + (2 * random() - 1) * 0.09
        b = pi + 0.44 + (2 * random() - 1) * 0.09
        c = 3 * pi - b
        p1, p2, p3 = P(cos(a), sin(a)), P(cos(b), sin(b)), P(cos(c), sin(c))
        return Config([Point(p1.x, p1.y), Point(p2.x, p2.y), Point(p3.x, p3.y)])

    def run(self, object_limit):
        while len(self.objects) < object_limit:
            self.apply_random_construction()
        self.add_trivial_properties()
        self.search_unknown_properties()
    
    def apply_random_construction(self):
        construction = choice(Construction.default())
        if not self.select_can(construction.p, construction.l, construction.c):
            return
        objects = self.select_one(construction.p, construction.l, construction.c)
        for condition in construction.conditions:
            if not condition(*objects):
                return
        new_objects = []
        for function in construction.functions:
            objs = function(*objects)
            if isinstance(objs, tuple):
                for i, oo in enumerate(objs):
                    obj = None
                    recipe = function.__doc__.split("\n")[i + 2].strip()
                    if isinstance(oo, P):
                        obj = Point(oo.x, oo.y, recipe, objects)
                    elif isinstance(oo, L):
                        obj = Line(oo.a, oo.b, oo.c, recipe, objects)
                    elif isinstance(oo, C):
                        obj = Circle(oo.o, oo.r, recipe, objects)
                    new_objects.append(obj)
            else:
                obj = None
                recipe = function.__doc__.split("\n")[2].strip()
                ob = objs
                if isinstance(ob, P):
                    obj = Point(ob.x, ob.y, recipe, objects)
                elif isinstance(ob, L):
                    obj = Line(ob.a, ob.b, ob.c, recipe, objects)
                elif isinstance(ob, C):
                    obj = Circle(ob.o, ob.r, recipe, objects)
                new_objects.append(obj)
        config = Config(objects + new_objects)
        remove_points = [(cp, sp) for cp in config.points for sp in self.points if not different_points(cp, sp)]
        remove_lines = [(cl, sl) for cl in config.lines for sl in self.lines if not different_lines(cl, sl)]
        remove_circles = [(cc, sc) for cc in config.circles for sc in self.circles if not different_circles(cc, sc)]
        for cp, sp in remove_points:
            config.objects.remove(cp)
            config.objects.append(sp)
        for cl, sl in remove_lines:
            config.objects.remove(cl)
            config.objects.append(sl)
        for cc, sc in remove_circles:
            config.objects.remove(cc)
            config.objects.append(sc)
        self.objects.extend([obj for obj in config.objects if obj not in self.objects])
        config.search_unknown_properties()
        for i, property in enumerate(self.properties):
            property.known.update(config.properties[i].unknown)
    
    def select_can(self, p, l, c):
        if len(self.points) < p:
            return False
        if len(self.lines) < l:
            return False
        if len(self.circles) < c:
            return False
        return True
    
    def select_one(self, p, l, c):
        selected_points = sample(self.points, p)
        selected_lines = sample(self.lines, l)
        selected_circles = sample(self.circles, c)
        objects = selected_points + selected_lines + selected_circles
        return objects
    
    def select_all(self, p, l, c):
        points = list(combinations(self.points, p)) if p else [()]
        lines = list(combinations(self.lines, l)) if l else [()]
        circles = list(combinations(self.circles, c)) if c else [()]
        objects = []
        for ps in points:
            for ls in lines:
                for cs in circles:
                    objects.append(list(ps) + list(ls) + list(cs))
        return objects

    def add_trivial_properties(self):
        collinears, concyclics, concurrents, parallels, perpendiculars, tangents, pls, pcs, lcs = [property.unknown for property in self.properties]
        # points on a line are collinear
        for u in self.lines:
            points = [a for a in self.points if (a, u) in pls]
            for i in combinations(points, 3):
                self.properties[0].known.add(frozenset(i))
        # lines through a point are concurrent
        for a in self.points:
            lines = [u for u in self.lines if (a, u) in pls]
            for i in combinations(lines, 3):
                self.properties[2].known.add(frozenset(i))
        # points on a circle are concyclic
        for s in self.circles:
            points = [a for a in self.points if (a, s) in pcs]
            for i in combinations(points, 4):
                self.properties[1].known.add(frozenset(i))
        # lines, parallel and perpendicular
        for u, v, w in permutations(self.lines, 3):
            if frozenset((u, v)) in parallels and frozenset((u, w)) in parallels:
                self.properties[3].known.add(frozenset((v, w)))
            if frozenset((u, v)) in parallels and frozenset((u, w)) in perpendiculars:
                self.properties[4].known.add(frozenset((v, w)))
            if frozenset((u, v)) in perpendiculars and frozenset((u, w)) in perpendiculars:
                self.properties[3].known.add(frozenset((v, w)))
        # a, b, c collinear and a, b, d collinear then a, b, c, d collinear
        for a, b in combinations(self.points, 2):
            cols = [col for col in collinears if a in col and b in col]
            if len(cols) > 1:
                all_points = [p for col in cols for p in col]
                for i in combinations(all_points, 3):
                    self.properties[0].known.add(frozenset(i))

    def search_unknown_properties(self):
        for property in self.properties:
            for selection in self.select_all(property.p, property.l, property.c):
                suitable = True
                for condition in property.conditions:
                    if not condition(*selection):
                        suitable = False
                        break
                if suitable and property.function(*selection):
                    obj = None
                    if property.type == "frozenset":
                        obj = frozenset(selection)
                    elif property.type == "tuple":
                        obj = tuple(selection)
                    if obj not in property.known:
                        property.unknown.add(obj)

    def txt(self):
        u, k = [], []
        for unk, knw in [property.txt() for property in self.properties]:
            u.append(unk)
            k.append(knw)
        a = "Config"
        b = "Objects\n" + "\n".join(map(lambda x: x.txt(), self.objects))
        c = "Unknown Properties\n" + "\n".join(u)
        d = "Known Properties\n" + "\n".join(k)
        return "\n\n".join([a, b, c, d]) + "\n"

    def asy(self):
        with open(f"templates/example.asy", "r+") as file:
            s = file.read()
        s += "\n".join(map(lambda x: x.asy(), self.objects))
        return s

    def tex(self):
        def property_sorter(probj):
            max_depth = max(probj[1], key=lambda obj: obj.depth).depth
            min_depth = min(probj[1], key=lambda obj: obj.depth).depth
            depth_diff = max_depth - min_depth
            return max_depth * 1000 + depth_diff
        with open("templates/example.tex") as file:
            s = file.read()
        lst = [(property, objects) for property in self.properties for objects in property.unknown]
        t = "".join([property.tex(objects) for property, objects in sorted(lst, key=property_sorter)])
        return s.replace("CONTENT", t)

    def save(self):
        x = datetime.now()
        name = f"{x.year}-{'-'.join(map(lambda e: str(e).zfill(2), [x.month, x.day, x.hour, x.minute, x.second]))}"
        folder = f"outputs/{name}"
        mkdir(folder)
        print(f"output is ready in {folder}")
        print(sum([len(property.unknown) for property in self.properties]), "unknown properties found")
        with open(f"{folder}/config.txt", "w+") as file:
            file.write(self.txt())
        with open(f"{folder}/test.asy", "w+") as file:
            file.write(self.asy())
        with open(f"{folder}/config.tex", "w+") as file:
            file.write(self.tex())
        with open("templates/latexmkrc", "r+") as file:
            latexmkrc = file.read()
        with open(f"{folder}/latexmkrc", "w+") as file:
            file.write(latexmkrc)

