from itertools import combinations
from random import sample, choice, random
from datetime import datetime
import os
from .objects import *

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
        function_list = [
            self.pp,
            self.pl,
            self.pc,
            self.ll,
            self.lc,
            self.cc,
            self.ppp,
            self.ppl,
            self.ppc,
            self.pppp,
            self.pppl,
            self.pppc,
            self.ppppp
        ]
        obj_count = len(self.objects)
        while obj_count < obj_limit:
            f = choice(function_list)
            print(f"object count = {obj_count}, applying {f.__name__}")
            f()
            obj_count = len(self.objects)
        print("adding trivial properties")
        self.add_trivial_properties()
        print("saving")
        self.save()
    
    def pp(self):
        if len(self.points) < 2:
            return
        a, b = sample(self.points, 2)
        if a @ b:
            return
        self.construct(Config.apply(pp_fl, (a, b)))
    
    def pl(self):
        if len(self.points) < 1 or len(self.lines) < 1:
            return
        a, u = choice(self.points), choice(self.lines)
        if is_pl(a, u):
            self.construct(Config.apply(pl_1_fl, (a, u)))
        else:
            self.construct(Config.apply(pl_2_fl, (a, u)))
    
    def pc(self):
        if len(self.points) < 1 or len(self.circles) < 1:
            return
        a, s = choice(self.points), choice(self.circles)
        if a @ s.o:
            return
        r = pcr(a, s)
        if r == -1:
            self.construct(Config.apply(pc_1_fl, (a, s)))
        elif r == 0:
            self.construct(Config.apply(pc_2_fl, (a, s)))
        elif r == 1:
            self.construct(Config.apply(pc_3_fl, (a, s)))
    
    def ll(self):
        if len(self.lines) < 2:
            return
        u, v = sample(self.lines, 2)
        if is_parallel(u, v):
            return
        self.construct(Config.apply(ll_fl, (u, v)))
    
    def lc(self):
        if len(self.lines) < 1 or len(self.circles) < 1:
            return
        u, s = choice(self.lines), choice(self.circles)
        if is_pl(s.o, u):
            return
        r = lcr(u, s)
        if r == -1:
            self.construct(Config.apply(lc_1_fl, (u, s)))
        elif r == 0:
            self.construct(Config.apply(lc_2_fl, (u, s)))
        elif r == 1:
            self.construct(Config.apply(lc_3_fl, (u, s)))
    
    def cc(self):
        if len(self.circles) < 2:
            return
        s, t = sample(self.circles, 2)
        if is_bad_circles(s, t):
            return
        r = ccr(s, t)
        if r == -2:
            return
        elif r == -1:
            self.construct(Config.apply(cc_1_fl, (s, t)))
        elif r == 0:
            self.construct(Config.apply(cc_2_fl, (s, t)))
        elif r == 1:
            self.construct(Config.apply(cc_3_fl, (s, t)))
        elif r == 2:
            self.construct(Config.apply(cc_4_fl, (s, t)))
    
    def ppp(self):
        if len(self.points) < 3:
            return
        a, b, c = sample(self.points, 3)
        if not is_different_points((a, b, c)):
            return
        if is_collinear(a, b, c):
            return
        self.construct(Config.apply(ppp_fl, (a, b, c)))
    
    def ppl(self):
        if len(self.points) < 2 or len(self.lines) < 1:
            return
        a, b = sample(self.points, 2)
        u = choice(self.lines)
        if a @ b:
            return
        if is_parallel(line(a, b), u):
            return
        if is_pl(a, u) or is_pl(b, u):
            return
        self.construct(Config.apply(ppl_fl, (a, b, u)))
    
    def ppc(self):
        if len(self.points) < 2 or len(self.circles) < 1:
            return
        a, b = sample(self.points, 2)
        s = choice(self.circles)
        if a @ b:
            return
        if lcr(line(a, b), s) != -1:
            return
        self.construct(Config.apply(ppc_fl, (a, b, s)))

    def ccc(self):
        if len(self.circles) < 3:
            return
        s, t, m = sample(self.circles, 3)
        if is_bad_circles(s, t) or is_bad_circles(s, m) or is_bad_circles(t, m):
            return
        if is_collinear(s.o, t.o, m.o):
            return
        self.construct(Config.apply(ccc_fl, (s, t, m)))

    def pppp(self):
        if len(self.points) < 4:
            return
        a, b, c, d = sample(self.points, 4)
        if not is_different_points((a, b, c, d)):
            return
        if not not_three_collinear((a, b, c, d)):
            return
        self.construct(Config.apply(pppp_fl, (a, b, c, d)))
    
    def pppl(self):
        if len(self.points) < 3 or len(self.lines) < 1:
            return
        a, b, c = sample(self.points, 3)
        u = choice(self.lines)
        if not is_different_points((a, b, c)):
            return
        if is_collinear(a, b, c):
            return
        if not is_nice_pppl(a, b, c, u):
            return
        self.construct(Config.apply(pppl_fl, (a, b, c, u)))
    
    def pppc(self):
        if len(self.points) < 3 or len(self.circles) < 1:
            return
        a, b, c = sample(self.points, 3)
        s = choice(self.circles)
        if not is_different_points((a, b, c)):
            return
        if is_collinear(a, b, c):
            return
        if not is_nice_pppc(a, b, c, s):
            return
        self.construct(Config.apply(pppc_fl, (a, b, c, s)))

    def ppppp(self):
        if len(self.points) < 5:
            return
        a, b, c, d, e = sample(self.points, 5)
        if not is_different_points((a, b, c, d, e)):
            return
        if not not_three_collinear((a, b, c, d, e)):
            return
        if not is_nice_ppppp(a, b, c, d, e):
            return
        self.construct(Config.apply(ppppp_fl, (a, b, c, d, e)))

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
        folder = f"outputs/tests/{name}"
        if not os.path.exists(folder):
            os.mkdir(folder)
        with open(f"{folder}/test.txt", "w+") as file:
            file.write(self.txt())
        with open(f"{folder}/test.tex", "w+") as file:
            file.write(self.tex(self.search_properties()))
        with open(f"{folder}/test.asy", "w+") as file:
            file.write(self.asy())
        with open("outputs/templates/latexmkrc", "r+") as file:
            latexmkrc = file.read()
        with open(f"{folder}/latexmkrc", "w+") as file:
            file.write(latexmkrc)
        os.chdir(os.getcwd() + "\\" + folder.replace('/', '\\'))
        os.system('"C:\\Program Files\\Asymptote\\asy" -o test2 test.asy')
        os.system(f"latexmk -aux-directory=auxs -pdf") # this takes time

    def tex(self, properties):
        with open("outputs/templates/example.property", "r+") as file:
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
        
        with open("outputs/templates/example.tex", "r+") as file:
            content = file.read()
        return content.replace("CONTENT", "".join([tex_property(property) for property in sorted(properties, key=property_sorter)]))
        
    def asy(self, raw=False):
        asy = ""
        if not raw:
            with open(f"outputs/templates/example.asy", "r+") as file:
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
    