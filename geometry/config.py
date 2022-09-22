from itertools import combinations, permutations
from random import sample, choice, random
from datetime import datetime
from os import mkdir
from math import pi
# from .objects import Point, Line, Circle, P, L, C <-- the goal
from .objects import *
from .construction import Construction

class Config:
    def __init__(self, initial):
        self.points = [p for p in initial if isinstance(p, Point)]
        self.lines = [l for l in initial if isinstance(l, Line)]
        self.circles = [c for c in initial if isinstance(c, Circle)]
        self.collinears = set()
        self.concyclics = set()
        self.equals = set()
        self.concurrents = set()
        self.parallels = set()
        self.perpendiculars = set()
        self.tangents = set()
        self.pls = set()
        self.pcs = set()
        self.lcs = set()
    
    @property
    def objects(self):
        objects = self.points + self.lines + self.circles
        return sorted(objects, key=lambda x: x.depth * 1000 + x.id)
    
    @staticmethod
    def triangle():
        a = 1.83 + (2 * random() - 1) * 0.09
        b = pi + 0.44 + (2 * random() - 1) * 0.09
        c = 3 * pi - b
        return Config([Point(P.dir(a)), Point(P.dir(b)), Point(P.dir(c))])
    
    def run(self, obj_limit):
        while len(self.objects) < obj_limit:
            print(len(self.objects))
            self.apply_random_construction()
        print("adding trivial properties")
        self.add_trivial_properties()
        print("saving")
        self.save()
    
    def apply_random_construction(self):
        construction = choice(Construction.default())
        if not self.select_can(construction.p, construction.l, construction.c):
            return
        objects = self.select_one(construction.p, construction.l, construction.c)
        for condition in construction.conditions:
            if not condition(*objects):
                return
        self.construct(Config.apply(construction.functions, objects))
    
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

    @staticmethod
    def apply(functions, objects):
        objs = []
        for f in functions:
            o = f(*objects)
            if isinstance(o, tuple):
                for i, oo in enumerate(o):
                    obj = None
                    recipe = f.__doc__.split("\n")[i + 1].strip()
                    if isinstance(oo, P):
                        obj = Point(oo, recipe, objects)
                    elif isinstance(oo, L):
                        obj = Line(oo, recipe, objects)
                    elif isinstance(oo, C):
                        obj = Circle(oo, recipe, objects)
                    objs.append(obj)
            else:
                obj = None
                recipe = f.__doc__.split("\n")[1].strip()
                if isinstance(o, P):
                    obj = Point(o, recipe, objects)
                elif isinstance(o, L):
                    obj = Line(o, recipe, objects)
                elif isinstance(o, C):
                    obj = Circle(o, recipe, objects)
                objs.append(obj)
        for obj in objects:
            if isinstance(obj, Circle):
                objs.append(Point(obj.o, "center of {0}", (obj,)))
        return objs + list(objects)
    
    def construct(self, objects):
        config = Config(objects)
        # swap points if same
        pr = []
        for cp in config.points:
            for sp in self.points:
                if cp @ sp:
                    pr.append((cp, sp))
                    break
        for cp, sp in pr:
            config.points.remove(cp)
            config.points.append(sp)
        # swap lines if same
        lr = []
        for cl in config.lines:
            for sl in self.lines:
                if cl @ sl:
                    lr.append((cl, sl))
                    break
        for cl, sl in lr:
            config.lines.remove(cl)
            config.lines.append(sl)
        # swap circles if same
        cr = []
        for cc in config.circles:
            for sc in self.circles:
                if cc @ sc:
                    cr.append((cc, sc))
                    break
        for cc, sc in cr:
            config.circles.remove(cc)
            config.circles.append(sc)
        self.points.extend([p for p in config.points if p not in self.points])
        self.lines.extend([l for l in config.lines if l not in self.lines])
        self.circles.extend([c for c in config.circles if c not in self.circles])
        self.collinears.update(config.search_collinears())
        self.concyclics.update(config.search_concyclics())
        self.equals.update(config.search_equals())
        self.concurrents.update(config.search_concurrents())
        self.parallels.update(config.search_parallels())
        self.perpendiculars.update(config.search_perpendiculars())
        self.tangents.update(config.search_tangents())
        self.pls.update(config.search_pls())
        self.pcs.update(config.search_pcs())
        self.lcs.update(config.search_lcs())

    def search_collinears(self):
        new_collinears = set()
        for points in combinations(self.points, 3):
            if is_different_points(points) and is_collinear(*points):
                if frozenset(points) not in self.collinears:
                    new_collinears.add(frozenset(points))
        return new_collinears
    
    def search_concyclics(self):
        new_concyclics = set()
        for points in combinations(self.points, 4):
            if is_different_points(points) and not_three_collinear(points) and not is_isosceles_trapezoid_or_parallelogram(*points) and not is_deltoid(*points) and is_concyclic(*points):
                if frozenset(points) not in self.concyclics:
                    new_concyclics.add(frozenset(points))
        return new_concyclics
    
    def search_equals(self):
        return set()
    
    def search_concurrents(self):
        new_concurrents = set()
        for lines in combinations(self.lines, 3):
            if is_different_lines(lines) and not_two_parallel(lines) and is_concurrent(*lines):
                if frozenset(lines) not in self.concurrents:
                    new_concurrents.add(frozenset(lines))
        return new_concurrents
    
    def search_parallels(self):
        new_parallels = set()
        for lines in combinations(self.lines, 2):
            if is_different_lines(lines) and is_parallel(*lines):
                if frozenset(lines) not in self.parallels:
                    new_parallels.add(frozenset(lines))
        return new_parallels
    
    def search_perpendiculars(self):
        new_perpendiculars = set()
        for lines in combinations(self.lines, 2):
            if is_perpendicular(*lines):
                if frozenset(lines) not in self.perpendiculars:
                    new_perpendiculars.add(frozenset(lines))
        return new_perpendiculars
    
    def search_tangents(self):
        new_tangents = set()
        for circles in combinations(self.circles, 2):
            if is_different_circles(circles) and is_tangent(*circles):
                if frozenset(circles) not in self.tangents:
                    new_tangents.add(frozenset(circles))
        return new_tangents
    
    def search_pls(self):
        new_pls = set()
        for point in self.points:
            for line in self.lines:
                if is_pl(point, line):
                    if (point, line) not in self.pls:
                        new_pls.add((point, line))
        return new_pls
    
    def search_pcs(self):
        new_pcs = set()
        for point in self.points:
            for circle in self.circles:
                if is_pc(point, circle):
                    if (point, circle) not in self.pcs:
                        new_pcs.add((point, circle))
        return new_pcs
    
    def search_lcs(self):
        new_lcs = set()
        for line in self.lines:
            for circle in self.circles:
                if is_lc(line, circle):
                    if (line, circle) not in self.lcs:
                        new_lcs.add((line, circle))
        return new_lcs
    
    def search_properties(self):
        print("searcing properties")
        properties = []
        print("collinears")
        for pro in self.search_collinears():
            properties.append([collinear_str, pro])
        print("concyclics") # takes time
        for pro in self.search_concyclics():
            properties.append([concyclic_str, pro])
        print("equals")
        for pro in self.search_equals():
            properties.append([equal_str, pro])
        print("concurrents")
        for pro in self.search_concurrents():
            properties.append([concurrent_str, pro])
        print("parallels")
        for pro in self.search_parallels():
            properties.append([parallel_str, pro])
        print("perpendiculars")
        for pro in self.search_perpendiculars():
            properties.append([perpendicular_str, pro])
        print("pls")
        for pro in self.search_pls():
            properties.append([pl_str, pro])
        print("pcs")
        for pro in self.search_pcs():
            properties.append([pc_str, pro])
        print("lcs")
        for pro in self.search_lcs():
            properties.append([lc_str, pro])
        return properties
    
    def known_properties(self):
        properties = []
        for pro in self.collinears:
            properties.append([collinear_str, pro])
        for pro in self.concyclics:
            properties.append([concyclic_str, pro])
        for pro in self.equals:
            properties.append([equal_str, pro])
        for pro in self.concurrents:
            properties.append([concurrent_str, pro])
        for pro in self.parallels:
            properties.append([parallel_str, pro])
        for pro in self.perpendiculars:
            properties.append([perpendicular_str, pro])
        for pro in self.pls:
            properties.append([pl_str, pro])
        for pro in self.pcs:
            properties.append([pc_str, pro])
        for pro in self.lcs:
            properties.append([lc_str, pro])
        return properties
    
    def add_trivial_properties(self):
        print("trivial 1")
        # points on a line are collinear
        for u in self.lines:
            points = [a for a in self.points if (a, u) in self.pls]
            for i in combinations(points, 3):
                self.collinears.add(frozenset(i))
        print("trivial 2")
        # lines through a point are concurrent
        for a in self.points:
            lines = [u for u in self.lines if (a, u) in self.pls]
            for i in combinations(lines, 3):
                self.concurrents.add(frozenset(i))
        print("trivial 3")
        # points on a circle are concyclic
        for s in self.circles:
            points = [a for a in self.points if (a, s) in self.pcs]
            for i in combinations(points, 4):
                self.concyclics.add(frozenset(i))
        print("trivial 4")
        # lines, parallel and perpendicular
        for u, v, w in permutations(self.lines, 3):
            if frozenset((u, v)) in self.parallels and frozenset((u, w)) in self.parallels:
                self.parallels.add(frozenset((v, w)))
            if frozenset((u, v)) in self.parallels and frozenset((u, w)) in self.perpendiculars:
                self.perpendiculars.add(frozenset((v, w)))
            if frozenset((u, v)) in self.perpendiculars and frozenset((u, w)) in self.perpendiculars:
                self.parallels.add(frozenset((v, w)))
        print("trivial 5")
        # a, b, c collinear and a, b, d collinear then a, b, c, d collinear
        for a, b in combinations(self.points, 2):
            collinears = [col for col in self.collinears if a in col and b in col]
            if len(collinears) > 1:
                all_points = [p for col in collinears for p in col]
                for i in combinations(all_points, 3):
                    self.collinears.add(frozenset(i))
        """
        print("trivial 6") # takes time
        # abc = adc = 90 the a, b, c, d concyclic
        for a, b, c, d in permutations(self.points, 4):
            ab = [u for u in self.lines if (a, u) in self.pls and (b, u) in self.pls]
            bc = [u for u in self.lines if (b, u) in self.pls and (c, u) in self.pls]
            cd = [u for u in self.lines if (c, u) in self.pls and (d, u) in self.pls]
            da = [u for u in self.lines if (d, u) in self.pls and (a, u) in self.pls]
            if ab and bc and cd and da:
                if frozenset((ab[0], bc[0])) in self.perpendiculars and frozenset((cd[0], da[0])) in self.perpendiculars:
                    self.concyclics.add(frozenset((a, b, c, d)))
        """
    
    def nice_labels(self):
        point_labels = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z".split(",")
        line_labels = "u,v,w,x,y,z,s,t".split(",")
        circle_labels = "\\alpha,\\beta,\\gamma,\\delta,\\omega,\\kappa,\\lambda".split(",")
        dct = {}
        for i, point in enumerate(sorted(self.points, key=lambda x: x.id)):
            j = i % len(point_labels)
            n = i // len(point_labels)
            n = str(n) if n else ""
            dct[str(point)] = f"${point_labels[j]}{n}$"
        for i, line in enumerate(sorted(self.lines, key=lambda x: x.id)):
            j = i % len(line_labels)
            n = i // len(line_labels)
            n = str(n) if n else ""
            dct[str(line)] = f"${line_labels[j]}{n}$"
        for i, circle in enumerate(sorted(self.circles, key=lambda x: x.id)):
            j = i % len(circle_labels)
            n = i // len(circle_labels)
            n = str(n) if n else ""
            dct[str(circle)] = f"${circle_labels[j]}{n}$"
        return dct
    
    @staticmethod
    def replace_using_dict(dct, string):
        s = string
        for a, b in dct.items():
            s = s.replace(a, b)
        return s

    def save(self):
        x = datetime.now()
        name = f"{x.year}-{'-'.join(map(lambda e: str(e).zfill(2), [x.month, x.day, x.hour, x.minute, x.second]))}"
        folder = f"outputs/{name}"
        mkdir(folder)
        with open(f"{folder}/test.txt", "w+") as file:
            file.write(self.txt())
        with open(f"{folder}/test.tex", "w+") as file:
            file.write(self.tex())
        with open(f"{folder}/test.asy", "w+") as file:
            file.write(self.asy())
        with open("templates/latexmkrc", "r+") as file:
            latexmkrc = file.read()
        with open(f"{folder}/latexmkrc", "w+") as file:
            file.write(latexmkrc)
        with open("templates/compile.bat", "r+") as file:
            bat = file.read()
        with open(f"{folder}/compile.bat", "w+") as file:
            file.write(bat)

    def tex(self):
        properties = self.search_properties()
        with open("templates/example.property", "r+") as file:
            property_content = file.read()
        
        def tex_property(property):
            description, objects = property
            max_depth = max(objects, key=lambda obj: obj.depth).depth
            min_depth = min(objects, key=lambda obj: obj.depth).depth
            depth_difference = max_depth - min_depth
            config = Config.tree(objects)
            dct = config.nice_labels()
            asy = Config.replace_using_dict(dct, config.asy(raw=True))
            label = f"{Config.replace_using_dict(dct, description.format(*objects))}, max-depth = {max_depth}, depth-diff = {depth_difference}"
            others = "\\\\\n".join([Config.replace_using_dict(dct, obj.txt()) for obj in config.objects])
            return property_content.replace("ASY_CONTENT", asy).replace("DESCRIPTION", label).replace("OTHERS", others)
        
        def property_sorter(property):
            max_depth = max(property[1], key=lambda obj: obj.depth).depth
            min_depth = min(property[1], key=lambda obj: obj.depth).depth
            depth_diff = max_depth - min_depth
            return max_depth * 1000 + depth_diff
        
        with open("templates/example.tex", "r+") as file:
            content = file.read()
        return content.replace("CONTENT", "".join([tex_property(property) for property in sorted(properties, key=property_sorter)]))
        
    def asy(self, raw=False):
        asy = ""
        if not raw:
            with open(f"templates/example.asy", "r+") as file:
                asy = file.read()
        for p in self.points:
            asy += p.asy() if not raw else p.asy2()
        for l in self.lines:
            pls = [p for p in self.points if is_pl(p, l)]
            width = max(self.points, key=lambda p: p.x).x - min(self.points, key=lambda p: p.x).x if self.points else 0
            asy += l.asy(pls, width)
        for c in self.circles:
            asy += c.asy()
        return asy
    
    def txt(self):
        s = "Configuration\n"
        for p in self.points:
            s += p.txt()
        for l in self.lines:
            s += l.txt()
        for c in self.circles:
            s += c.txt()
        return s
    
    @staticmethod
    def tree(objects):
        objs = set(objects)
        while True:
            n = len(objs)
            to_be_added = set()
            for obj in objs:
                for parent in obj.parents:
                    to_be_added.add(parent)
            objs.update(to_be_added)
            if n == len(objs):
                break
        return Config(objs)
    