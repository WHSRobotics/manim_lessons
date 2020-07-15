#!/usr/bin/env python

from manimlib.imports import *
import math
import numpy as np

# To watch one of these scenes, run the following:
# python -m manim example_scenes.py SquareToCircle -pl
#
# Use the flat -l for a faster rendering at a lower
# quality.
# Use -s to skip to the end and just save the final frame
# Use the -p to have the animation (or image, if -s was
# used) pop up once done.
# Use -n <number> to skip ahead to the n'th animation of a scene.
# Use -r <number> to specify a resolution (for example, -r 1080
# for a 1920x1080 video)


class OpeningManimExample(Scene):
    def construct(self):
        title = TextMobject("This is some \\LaTeX")
        basel = TexMobject(
            "\\sum_{n=1}^\\infty "
            "\\frac{1}{n^2} = \\frac{\\pi^2}{6}"
        )
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeInFrom(basel, UP),
        )
        self.wait()

        transform_title = TextMobject("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*map(FadeOutAndShiftDown, basel)),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = TextMobject("This is a grid")
        grid_title.scale(1.5)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeInFromDown(grid_title),
            ShowCreation(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = TextMobject(
            "That was a non-linear function \\\\"
            "applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.apply_function,
            lambda p: p + np.array([
                np.sin(p[1]),
                np.sin(p[0]),
                0,
            ]),
            run_time=3,
        )
        self.wait()
        self.play(
            Transform(grid_title, grid_transform_title)
        )
        self.wait()


class Drive(MovingCameraScene):

    def construct(self):
        odomRadius = .45
        odomHeight= 0.15
        odomWidth = 0.02
        angle = math.radians(20)
        tankRadius = 8
        strafeRadius = -6

        startRobot = Square(side_length=1.2)
        tankRobot = Square(side_length=1.2, color=BLUE)
        strafeRobot = Square(side_length=1.2, color=GREEN)
        movementRobot = Square(side_length=1.2, color=RED)

        odom = [ [Rectangle(height=odomHeight, width=odomWidth) for i in range(3)] for j in range(3) ]
        robotCenters = []
        for x in range(3):
            for y in range(3):
                if y == 0:
                    odom[x][y].move_to(np.array([-odomRadius,0,0]))
                elif y == 1:
                    odom[x][y].move_to(np.array([odomRadius,0,0]))
                else:
                    odom[x][y].move_to(np.array([0,-odomRadius,0]))
                    odom[x][y].rotate_in_place(PI/2)

        for z in range(4):
            robotCenters.append(Dot(np.array([0,0,0])))

        startRobot.add(odom[0][0], odom[0][1], odom[0][2], robotCenters[0])
        tankRobot.add(odom[1][0], odom[1][1], robotCenters[1])
        strafeRobot.add(odom[1][2], robotCenters[2])
        movementRobot.add(odom[2][0], odom[2][1], odom[2][2], robotCenters[3])

        straightTankRobot = tankRobot.copy()
        straightStrafeRobot = strafeRobot.copy()

        def createFunction(function, color=WHITE):
            return ParametricFunction(t_max=angle, function=function, color=color)

        straightTankFunction = createFunction(lambda t : np.array([0, tankRadius*t, 0]), BLUE)
        straightStrafeFunction = createFunction(lambda t : np.array([-strafeRadius*t, 0, 0]), GREEN)

        tankFunction = createFunction(lambda t : np.array([-tankRadius*(1-math.cos(t)), tankRadius*math.sin(t), 0]), BLUE)
        leftOdomFunction = createFunction(lambda t : np.array([-(tankRadius-odomRadius)*(1-math.cos(t))-odomRadius, (tankRadius-odomRadius)*math.sin(t), 0]), BLUE)
        rightOdomFunction = createFunction(lambda t : np.array([-(tankRadius+odomRadius)*(1-math.cos(t))+odomRadius, (tankRadius+odomRadius)*math.sin(t), 0]), BLUE)
        strafeFunction = createFunction(lambda t : np.array([-strafeRadius*math.sin(t), -strafeRadius*(1-math.cos(t)), 0]), GREEN)
        backOdomFunction = createFunction(lambda t : np.array([-(strafeRadius-odomRadius)*math.sin(t), -(strafeRadius-odomRadius)*(1-math.cos(t))-odomRadius, 0]), GREEN)
        movementFunction = createFunction(lambda t : np.array([-strafeRadius * math.sin(t) - tankRadius * (1-math.cos(t)), tankRadius * math.sin(t) - strafeRadius * (1-math.cos(t)), 0]), RED)
        
        tankR1 = Line(tankFunction.get_point_from_function(0), np.array([-tankRadius,0,0]), color=BLUE)
        tankR2 = Line(tankFunction.get_point_from_function(angle), np.array([-tankRadius,0,0]), color=BLUE)
        strafeR1 = Line(np.array([0,0,0]), np.array([0,-strafeRadius,0]), color=GREEN)
        strafeR2 = Line(strafeFunction.get_point_from_function(angle), np.array([0,-strafeRadius,0]), color=GREEN)

        tankEquation = TexMobject("fwd","=","{left","+","right","\\over","2}")
        tankEquation[0].set_color(BLUE)
        tankEquation[2].set_color(BLUE)
        tankEquation[4].set_color(BLUE)
        tankEquation.scale(0.7)

        tankOdomLabel = VGroup(DecimalNumber(0), DecimalNumber(0))
        tankOdomLabel.arrange(RIGHT)
        tankOdomLabel.next_to(startRobot, LEFT*3 + UP*10)

        tempFunction = straightTankFunction.copy()
        self.play(ShowCreation(startRobot))
        # self.play(ShowCreation(tempFunction), MoveAlongPathWhileRotating(straightTankRobot, straightTankFunction, angle, rotate=False))
        # self.play(Uncreate(tempFunction), MoveAlongPathWhileRotating(straightTankRobot, straightTankFunction, angle, reverse=True, rotate=False))
        # self.remove(straightTankRobot)

        # tempFunction = straightStrafeFunction.copy()
        # self.play(ShowCreation(tempFunction), MoveAlongPathWhileRotating(straightStrafeRobot, straightStrafeFunction, angle, rotate=False))
        # self.play(Uncreate(tempFunction), MoveAlongPathWhileRotating(straightStrafeRobot, straightStrafeFunction, angle, reverse=True, rotate=False))
        # self.remove(straightStrafeRobot)

        # self.play(Rotate(startRobot, angle))
        # self.play(Rotate(startRobot, -angle))

        # tempRobot = tankRobot.copy()
        # tempRobot2 = strafeRobot.copy()
        # tempFunction = tankFunction.copy()
        # tempFunction2 = strafeFunction.copy()
        # self.play(ShowCreation(tempFunction), MoveAlongPathWhileRotating(tempRobot, tempFunction, angle), 
        #     ShowCreation(straightTankFunction), MoveAlongPathWhileRotating(straightTankRobot, straightTankFunction, angle, rotate=False))
        # self.play(FadeOut(straightTankFunction), FadeOut(straightTankRobot))
        # self.wait(.5)

        # self.play(ShowCreation(tempFunction2), MoveAlongPathWhileRotating(tempRobot2, tempFunction2, angle), 
        #     ShowCreation(straightStrafeFunction), MoveAlongPathWhileRotating(straightStrafeRobot, straightStrafeFunction, angle, rotate=False))
        # self.play(FadeOut(straightStrafeFunction), FadeOut(straightStrafeRobot))
        # self.wait(.5)

        # movementRobot.move_to(movementFunction.get_point_from_function(angle)).rotate(angle)

        # tempFunction3 = movementFunction.copy()
        # self.play(ReplacementTransform(tempFunction, tempFunction3), ReplacementTransform(tempFunction2, tempFunction3),
        #     ReplacementTransform(tempRobot, movementRobot), ReplacementTransform(tempRobot2, movementRobot))
        # self.wait()

        # self.play(Uncreate(tempFunction3), MoveAlongPathWhileRotating(movementRobot, tempFunction3, angle, reverse=True))
        # self.play(FadeOut(movementRobot))
        # self.wait(2)

        self.play(ApplyMethod(odom[0][0].scale, 1.5), ApplyMethod(odom[0][1].scale, 1.5), run_time=0.5)
        self.play(ApplyMethod(odom[0][0].scale, 1/1.5), ApplyMethod(odom[0][1].scale, 1/1.5), run_time=0.5)
        self.wait()
        self.play(ShowCreation(tankFunction), MoveAlongPathWhileRotating(tankRobot, tankFunction, angle),
            ShowCreation(leftOdomFunction), ShowCreation(rightOdomFunction), run_time=2)
        self.play(self.camera_frame.move_to, leftOdomFunction.get_point_from_function(angle/2) + np.array([-3,1,0]))#, FadeOut(backOdomFunction), FadeOut(movementRobot), FadeOut(movementFunction), FadeOut(strafeRobot))
        tankEquation.next_to(self.camera_frame.get_corner(UP+LEFT), DOWN*6+RIGHT*8)
        self.play(TransformFromCopy(tankFunction, tankEquation[0]), FadeIn(tankEquation[1], run_time=2))
        # self.wait()
        self.play(TransformFromCopy(leftOdomFunction, tankEquation[2]), TransformFromCopy(rightOdomFunction, tankEquation[4]),
            FadeIn(tankEquation[3], run_time=2), FadeIn(tankEquation[5], run_time=2), FadeIn(tankEquation[6], run_time=2))
        self.wait()

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class WarpSquare(Scene):
    def construct(self):
        square = Square()
        self.play(ApplyPointwiseFunction(
            lambda point: complex_to_R3(np.exp(R3_to_complex(point))),
            square
        ))
        self.wait()


class WriteStuff(Scene):
    def construct(self):
        example_text = TextMobject(
            "This is a some text",
            tex_to_color_map={"text": YELLOW}
        )
        example_tex = TexMobject(
            "\\sum_{k=1}^\\infty {1 \\over k^2} = {\\pi^2 \\over 6}",
        )
        group = VGroup(example_text, example_tex)
        group.arrange(DOWN)
        group.set_width(FRAME_WIDTH - 2 * LARGE_BUFF)

        self.play(Write(example_text))
        self.play(Write(example_tex))
        self.wait()


class UpdatersExample(Scene):
    def construct(self):
        decimal = DecimalNumber(
            0,
            show_ellipsis=True,
            num_decimal_places=3,
            include_sign=True,
        )
        square = Square().to_edge(UP)

        decimal.add_updater(lambda d: d.next_to(square, RIGHT))
        decimal.add_updater(lambda d: d.set_value(square.get_center()[1]))
        self.add(square, decimal)
        self.play(
            square.to_edge, DOWN,
            rate_func=there_and_back,
            run_time=5,
        )
        self.wait()

# See old_projects folder for many, many more
