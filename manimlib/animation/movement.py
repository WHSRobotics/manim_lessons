from manimlib.animation.animation import Animation
from manimlib.utils.rate_functions import linear


class Homotopy(Animation):
    CONFIG = {
        "run_time": 3,
        "apply_function_kwargs": {},
    }

    def __init__(self, homotopy, mobject, **kwargs):
        """
        Homotopy is a function from
        (x, y, z, t) to (x', y', z')
        """
        self.homotopy = homotopy
        super().__init__(mobject, **kwargs)

    def function_at_time_t(self, t):
        return lambda p: self.homotopy(*p, t)

    def interpolate_submobject(self, submob, start, alpha):
        submob.points = start.points
        submob.apply_function(
            self.function_at_time_t(alpha),
            **self.apply_function_kwargs
        )


class SmoothedVectorizedHomotopy(Homotopy):
    def interpolate_submobject(self, submob, start, alpha):
        Homotopy.interpolate_submobject(self, submob, start, alpha)
        submob.make_smooth()


class ComplexHomotopy(Homotopy):
    def __init__(self, complex_homotopy, mobject, **kwargs):
        """
        Complex Hootopy a function Cx[0, 1] to C
        """
        def homotopy(x, y, z, t):
            c = complex_homotopy(complex(x, y), t)
            return (c.real, c.imag, z)
        Homotopy.__init__(self, homotopy, mobject, **kwargs)


class PhaseFlow(Animation):
    CONFIG = {
        "virtual_time": 1,
        "rate_func": linear,
        "suspend_mobject_updating": False,
    }

    def __init__(self, function, mobject, **kwargs):
        self.function = function
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        if hasattr(self, "last_alpha"):
            dt = self.virtual_time * (alpha - self.last_alpha)
            self.mobject.apply_function(
                lambda p: p + dt * self.function(p)
            )
        self.last_alpha = alpha


class MoveAlongPath(Animation):
    CONFIG = {
        "suspend_mobject_updating": False,
    }

    def __init__(self, mobject, path, **kwargs):
        self.path = path
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        point = self.path.point_from_proportion(alpha)
        self.mobject.move_to(point)

class MoveAlongPathWhileRotating(Animation):
    CONFIG = {
        "suspend_mobject_updating": False,
    }

    def __init__(self, mobject, function, angle=0, reverse=False, rotate=True, decimal=None, decimal2=None, scale=0, scale2=None, **kwargs):
        self.mobject = mobject
        self.function = function
        self.angle = angle
        self.reverse = reverse
        self.rotate = rotate
        self.decimal = decimal
        self.scale = scale
        self.decimal2 = decimal2
        if scale2 == None:
            self.scale2 = scale
        else:
            self.scale2 = scale2
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        self.mobject.become(self.starting_mobject)
        if self.reverse:
            arc_angle = self.angle*(1-alpha)
            rotate_angle = -self.angle*alpha
            point = self.function.get_point_from_function(arc_angle)
        else:
            arc_angle = self.angle*alpha
            rotate_angle = arc_angle
            point = self.function.get_point_from_function(arc_angle)
        
        self.mobject.move_to(point)
        if self.rotate:
            self.mobject.rotate(rotate_angle)

        if self.decimal != None:
            self.decimal.set_value(self.scale*arc_angle)
        if self.decimal2 != None:
            self.decimal2.set_value(self.scale2*arc_angle)