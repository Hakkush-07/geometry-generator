from .functions import *

class Construction:
    def __init__(self, functions, conditions):
        self.functions = functions
        self.conditions = conditions
        self.p, self.l, self.c = map(int, self.functions[0].__doc__.split("\n")[1].split(","))
        assert all([tuple(map(int, f.__doc__.split("\n")[1].split(","))) == (self.p, self.l, self.c) for f in self.functions])

    @staticmethod
    def default():
        return (
            Construction(
                [
                    midpoint, 
                    line, 
                    perpendicular_bisector, 
                    circle_diameter,
                    reflections_pp,
                    perpendicular_throughs,
                    circle_centereds
                ],
                [
                    different_points
                ]
            ),
            Construction(
                [
                    reflection_pl,
                    foot,
                    perpendicular_line,
                    parallel_line
                ],
                [
                    not_pl
                ]
            ),
            Construction(
                [
                    perpendicular_line
                ],
                [
                    is_pl
                ]
            ),
            Construction(
                [
                    tangent_points,
                    tangent_lines,
                    polar
                ],
                [
                    out_pc
                ]
            ),
            Construction(
                [
                    intersection_ll,
                    angle_bisectors,
                    reflections_ll
                ],
                [
                    different_lines,
                    not_two_parallel
                ]
            ),
            Construction(
                [
                    intersections_lc,
                    pole
                ],
                [
                    intersecting_lc,
                    not_through_center
                ]
            ),
            Construction(
                [
                    intersections_cc,
                    radical_axis,
                    tangent_points_external,
                    tangent_lines_external,
                    tangent_intersection_external
                ],
                [
                    nice_circles,
                    cc_1
                ]
            ),
            Construction(
                [
                    radical_axis,
                    tangent_points_external,
                    tangent_points_internal,
                    tangent_lines_external,
                    tangent_lines_internal,
                    tangent_intersection_external,
                    tangent_intersection_internal
                ],
                [
                    nice_circles,
                    cc_2
                ]
            ),
            Construction(
                [
                    intersection_cc,
                    radical_axis,
                    tangent_points_external,
                    tangent_lines_external,
                    tangent_intersection_external
                ],
                [
                    nice_circles,
                    cc_3
                ]
            ),
            Construction(
                [
                    intersection_cc,
                    radical_axis
                ],
                [
                    nice_circles,
                    cc_4
                ]
            ),
            Construction(
                [
                    sides,
                    internal_angle_bisectors,
                    external_angle_bisectors,
                    altitudes,
                    medians,
                    feet,
                    midpoints,
                    tangents,
                    circumcircle,
                    circumcenter,
                    incircle,
                    incenter,
                    excircles,
                    excenters,
                    orthocenter,
                    centroid
                ],
                [
                    different_points,
                    not_three_collinear
                ]
            ),
            Construction(
                [
                    intersection_ppl,
                    tangent_points_ppl,
                    tangent_circles_ppl
                ],
                [
                    nice_ppl
                ]
            ),
            Construction(
                [
                    intersections_ppc
                ],
                [
                    nice_ppc
                ]
            ),
            Construction(
                [
                    radical_center
                ],
                [
                    different_circles,
                    not_centers_collinear
                ]
            ),
            Construction(
                [
                    intersection_pppp,
                    intersections_pppp
                ],
                [
                    different_points,
                    not_three_collinear
                ]
            ),
            Construction(
                [
                    intersections_pppl
                ],
                [
                    nice_pppl
                ]
            ),
            Construction(
                [
                    intersections_pppc
                ],
                [
                    nice_pppc
                ]
            ),
            Construction(
                [
                    intersection_ppppp,
                    intersections_ppppp
                ],
                [
                    different_points,
                    not_three_collinear,
                    nice_ppppp
                ]
            )
        )
