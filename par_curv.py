from manimlib import *


def regular_vertices(n, *, radius=1, start_angle=None):
    if start_angle is None:
        if n % 2 == 0:
            start_angle = 0
        else:
            start_angle = TAU / 4

    start_vector = rotate_vector(RIGHT * radius, start_angle)
    vertices = compass_directions(n, start_vector)

    return vertices, start_angle


class Star(Polygon):
    """ Develop by friedkeenan"""

    def __init__(self, n=6, *, density=2, outer_radius=1, inner_radius=None, start_angle=None, **kwargs):
        if density <= 0 or density >= n / 2:
            raise ValueError(f"Incompatible density {density}")

        inner_angle = TAU / (2 * n)

        if inner_radius is None:
            # Calculate the inner radius for n and density.
            # See https://math.stackexchange.com/a/2136292

            outer_angle = TAU * density / n

            inverse_x = 1 - np.tan(inner_angle) * \
                ((np.cos(outer_angle) - 1) / np.sin(outer_angle))

            inner_radius = outer_radius / (np.cos(inner_angle) * inverse_x)

        outer_vertices, self.start_angle = regular_vertices(
            n, radius=outer_radius, start_angle=start_angle)
        inner_vertices, _ = regular_vertices(
            n, radius=inner_radius, start_angle=self.start_angle + inner_angle)

        vertices = []
        for pair in zip(outer_vertices, inner_vertices):
            vertices.extend(pair)

        super().__init__(*vertices, **kwargs)


class MmodNTrackerSTAR(Scene):
    CONFIG = {
        "number_of_lines": 300,
        "gradient_colors": [RED, YELLOW, BLUE],
        "end_value": int(4 * 60 / 3),
        "total_time": 4 * 60,
    }

    def construct(self):
        circle = Star()
        circle.rotate(PI/2).set_height(FRAME_HEIGHT*0.9)

        mod_tracker = ValueTracker(1)
        lines = self.get_m_mod_n_objects(circle, mod_tracker.get_value())
        self.add(circle, lines)
        self.wait(2)
        lines.add_updater(
            lambda mob: mob.become(
                self.get_m_mod_n_objects(circle, mod_tracker.get_value())
            )
        )
        self.add(circle, lines)
        self.play(
            mod_tracker.set_value, self.end_value,
            rate_func=linear,
            run_time=self.total_time
        )
        lines.clear_updaters()
        self.wait(16)

    def get_m_mod_n_objects(self, circle, x, y=None):
        if y == None:
            y = self.number_of_lines
        lines = VGroup()
        for i in range(y):
            start_point = circle.point_from_proportion((i % y)/y)
            end_point = circle.point_from_proportion(((i*x) % y)/y)
            line = Line(start_point, end_point).set_stroke(width=1)
            lines.add(line)
        lines.set_color_by_gradient(*self.gradient_colors)
        return lines
