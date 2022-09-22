from .functions import *

class Property:
    def __init__(self, function, conditions=None, use_tuple=False):
        self.function = function
        self.recipe = self.function.__doc__.split("\n")[2].strip()
        self.p, self.l, self.c = map(int, self.function.__doc__.split("\n")[1].split(","))
        self.conditions = conditions if conditions else []
        self.type = "tuple" if use_tuple else "frozenset"
        self.unknown = set()
        self.known = set()

    def txt(self):
        return "\n".join(map(lambda x: self.recipe.format(*x), self.unknown)), "\n".join(map(lambda x: self.recipe.format(*x), self.known))
    
    def tex(self, objects):
        def tree(objs):
            x = set(objs)
            while True:
                n = len(x)
                to_be_added = set()
                for obj in x:
                    for parent in obj.parents:
                        to_be_added.add(parent)
                x.update(to_be_added)
                if n == len(x):
                    break
            return x
        def relabeling(objs):
            point_labels = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z".split(",")
            line_labels = "u,v,w,x,y,z,s,t".split(",")
            circle_labels = "\\alpha,\\beta,\\gamma,\\delta,\\omega,\\kappa,\\lambda".split(",")
            p, l, c = 0, 0, 0
            for obj in objs:
                if obj.type == "P":
                    obj.change_label(point_labels[p])
                    p += 1
                elif obj.type == "L":
                    obj.change_label(line_labels[l])
                    l += 1
                elif obj.type == "C":
                    obj.change_label(circle_labels[c])
                    c += 1
        with open("templates/example.property") as file:
            s = file.read()
        objs = tree(objects)
        objs = sorted(objs, key=lambda x: 1000 * x.depth + x.id)
        relabeling(objs)
        s = s.replace("ASY_CONTENT", "\n".join(map(lambda x: x.asy(), objs)))
        s = s.replace("DESCRIPTION", self.recipe.format(*objects))
        s = s.replace("OTHERS", "\\\\\n".join(map(lambda x: x.txt(), objs)))
        return s

    @staticmethod
    def default():
        return (
            Property(is_collinear, [different_points]),
            Property(is_concyclic, [different_points, not_three_collinear, not_isosceles_trapezoid_or_parallelogram, not_deltoid]),
            Property(is_concurrent, [different_lines, not_two_parallel]),
            Property(is_parallel, [different_lines]),
            Property(is_perpendicular, [different_lines]),
            Property(is_tangent, [different_circles]),
            Property(is_pl, use_tuple=True),
            Property(is_pc, use_tuple=True),
            Property(is_lc, use_tuple=True)
        )
