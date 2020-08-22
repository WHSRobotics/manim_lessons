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

class StrafeOdometry(MovingCameraScene):

    def construct(self):
        odom_radius = .45
        odom_height = 0.15
        odom_width = 0.02
        rotate_angle = math.radians(20)
        dx_radius = 8
        dy_radius = -6

        start_robot = Square(side_length=1.2)
        dx_robot = Square(side_length=1.2, color=BLUE)
        dy_robot = Square(side_length=1.2, color=GREEN)
        movement_robot = Square(side_length=1.2, color=RED_E)

        odom = [[Rectangle(height=odom_height, width=odom_width) for i in range(3)] for j in range(3)]
        robot_centers = [Dot(np.array([0, 0, 0])) for i in range(4)]
        for x in range(3):
            for y in range(3):
                if y == 0:
                    odom[x][y].move_to(np.array([-odom_radius, 0, 0]))
                elif y == 1:
                    odom[x][y].move_to(np.array([odom_radius, 0, 0]))
                else:
                    odom[x][y].move_to(np.array([0, -odom_radius, 0]))
                    odom[x][y].rotate_in_place(PI / 2)

        start_robot.add(odom[0][0], odom[0][1], odom[0][2], robot_centers[0])
        dx_robot.add(odom[1][0], odom[1][1], robot_centers[1])
        dy_robot.add(odom[1][2], robot_centers[2])
        movement_robot.add(odom[2][0], odom[2][1], odom[2][2], robot_centers[3])

        straight_dx_robot = dx_robot.copy()
        straight_dy_robot = dy_robot.copy()

        def create_path(function, color=WHITE):
            return ParametricFunction(t_max=rotate_angle, function=function, color=color)

        straight_dx_path = create_path(lambda t: np.array([0, dx_radius * t, 0]), BLUE)
        straight_dy_path = create_path(lambda t: np.array([-dy_radius * t, 0, 0]), GREEN)
        back_odom_rotate_path = Arc(radius=odom_radius, start_angle=1.5 * PI, angle=rotate_angle).set_color(PURPLE)

        dx_path = create_path(
            lambda t: np.array([-dx_radius * (1 - math.cos(t)), dx_radius * math.sin(t), 0]), BLUE)
        left_odom_path = create_path(
            lambda t: np.array([-(dx_radius - odom_radius) * (1 - math.cos(t)) - odom_radius,
                                (dx_radius - odom_radius) * math.sin(t), 0]), PURPLE)
        right_odom_path = create_path(
            lambda t: np.array([-(dx_radius + odom_radius) * (1 - math.cos(t)) + odom_radius,
                                (dx_radius + odom_radius) * math.sin(t), 0]), PURPLE)

        dy_path = create_path(
            lambda t: np.array([-dy_radius * math.sin(t), -dy_radius * (1 - math.cos(t)), 0]), GREEN)
        back_odom_path = create_path(lambda t: np.array([-(dy_radius - odom_radius) * math.sin(t),
                                                         -(dy_radius - odom_radius) * (
                                                                 1 - math.cos(t)) - odom_radius, 0]), PURPLE)

        movement_path = create_path(
            lambda t: np.array([-dy_radius * math.sin(t) - dx_radius * (1 - math.cos(t)),
                                dx_radius * math.sin(t) - dy_radius * (1 - math.cos(t)), 0]), RED_E)

        robot_axes = VGroup(Arrow(ORIGIN, UP), Arrow(ORIGIN, LEFT), TexMobject("+x").scale(0.5),
                            TexMobject("+y").scale(0.5))
        robot_axes[1].move_to(robot_axes[0].get_start()).shift(LEFT * .25)
        robot_axes[2].next_to(robot_axes[0], RIGHT * .2).shift(DOWN * .05)
        robot_axes[3].next_to(robot_axes[1], DOWN * .2).shift(RIGHT * .05)

        dx_label = TexMobject("dx").scale(0.8).set_color(BLUE)
        dy_label = TexMobject("dy").scale(0.8).set_color(GREEN)

        r_x1 = Line(dx_path.get_point_from_function(0), np.array([-dx_radius, 0, 0]), color=TEAL)
        r_x2 = Line(dx_path.get_point_from_function(rotate_angle), np.array([-dx_radius, 0, 0]), color=TEAL)
        r_y1 = Line(dy_path.get_point_from_function(0), np.array([0, -dy_radius, 0]), color=GOLD)
        r_y2 = Line(dy_path.get_point_from_function(rotate_angle), np.array([0, -dy_radius, 0]), color=GOLD)

        r_x_label = TexMobject("r_x", color=TEAL).scale(0.8).next_to(r_x1, direction=DOWN)
        r_y_label = TexMobject("r_y", color=GOLD).scale(0.8).next_to(r_y2).shift(LEFT)

        dx_angle_marker = VGroup(Arc(radius=1.5, arc_center=np.array([-dx_radius, 0, 0]), angle=rotate_angle),
                                 TexMobject("d\\theta").scale(0.8)).set_color(RED_E)
        dx_angle_marker[1].move_to(dx_angle_marker[0]).shift(UP * .06 + RIGHT * .35)
        dy_angle_marker = VGroup(
            Arc(radius=1.5, arc_center=np.array([0, -dy_radius, 0]), start_angle=1.5 * PI, angle=rotate_angle),
            TexMobject("d\\theta").scale(0.8)).set_color(RED_E)
        dy_angle_marker[1].move_to(dy_angle_marker[0]).shift(RIGHT * .06 + DOWN * .35)

        dx_equation = TexMobject("dx", "=", "{", "leftt", "+", "right", "\\over", "2}", "=").scale(0.8)
        dx_equation[0].set_color(BLUE)
        dx_equation[3].set_color(BLACK)
        dx_equation[5].set_color(PURPLE)
        dx_left_text = TexMobject("left").set_color(PURPLE).scale(0.8)
        dx_odom_label = VGroup(DecimalNumber(0).set_color(PURPLE).scale(0.8),
                               DecimalNumber(0).set_color(PURPLE).scale(0.8))
        dx_equation_label = DecimalNumber(0).set_color(BLUE).scale(0.8)

        arc_length_equation = TexMobject("s", "=", "r", "\\theta").scale(0.8)
        modified_arc_length_equation = TexMobject("r", "=", "s", "/", "\\theta").scale(0.8)

        left_arc_length_equation = TexMobject("left", "=", "(", "r_x", "-", "0.5\\ast", "track width", ")",
                                              "d\\theta").scale(0.8)
        right_arc_length_equation = TexMobject("right", "=", "(", "r_x", "+", "0.5\\ast", "track width", ")",
                                               "d\\theta").scale(0.8)
        left_arc_length_equation[0].set_color(PURPLE)
        left_arc_length_equation[3].set_color(TEAL)
        left_arc_length_equation[6].set_color(GRAY)
        left_arc_length_equation[8].set_color(RED_E)
        right_arc_length_equation[0].set_color(PURPLE)
        right_arc_length_equation[3].set_color(TEAL)
        right_arc_length_equation[6].set_color(GRAY)
        right_arc_length_equation[8].set_color(RED_E)

        unsimplified_dtheta_equation = TexMobject("right", "-", "left", "=", "track width", "\\ast", "d\\theta").scale(
            0.8)
        unsimplified_dtheta_equation[0].set_color(PURPLE)
        unsimplified_dtheta_equation[2].set_color(PURPLE)
        unsimplified_dtheta_equation[4].set_color(GRAY)
        unsimplified_dtheta_equation[6].set_color(RED_E)

        dtheta_equation = TexMobject("d\\theta", "=", "{right", "-", "left", "\\over", "track width}", "=").scale(0.8)
        dtheta_equation[0].set_color(RED_E)
        dtheta_equation[2].set_color(PURPLE)
        dtheta_equation[4].set_color(PURPLE)
        dtheta_equation[6].set_color(GRAY)
        dtheta_equation_label = VGroup(DecimalNumber(rotate_angle).scale(0.8), TexMobject("rad").scale(0.8)).set_color(
            RED_E)
        dtheta_equation_label.arrange()

        dy_equation = TexMobject("dy", "=", "back", "-", "r_{back}", "d\\theta").scale(0.8)
        dy_equation[0].set_color(GREEN)
        dy_equation[2].set_color(PURPLE)
        dy_equation[4].set_color(GRAY)
        dy_equation[5].set_color(RED_E)

        back_odom_equation = TexMobject("back", "=", "dy", "+", "r_{back}", "d\\theta").scale(0.8)
        back_odom_equation[0].set_color(PURPLE)
        back_odom_equation[2].set_color(GREEN)
        back_odom_equation[4].set_color(GRAY)
        back_odom_equation[5].set_color(RED_E)
        back_odom_equation_label = DecimalNumber(0).scale(0.8)

        r_x_equation = TexMobject("r_x", "=", "dx", "/", "d\\theta").scale(0.8)
        r_y_equation = TexMobject("r_y", "=", "back", "/", "d\\theta", "-", "r_{back}").scale(0.8)
        alternate_r_y_equation = TexMobject("r_y", "=", "dy", "/", "d\\theta").scale(0.8)
        unsimplified_r_y_equation = TexMobject("r_y", "=", "(", "back", "-", "r_{back}", "d\\theta", ")", "/",
                                               "d\\theta").scale(0.8)
        r_x_equation[0].set_color(TEAL)
        r_x_equation[2].set_color(BLUE)
        r_x_equation[4].set_color(RED_E)
        r_y_equation[0].set_color(GOLD)
        r_y_equation[2].set_color(PURPLE)
        r_y_equation[4].set_color(RED_E)
        r_y_equation[6].set_color(GRAY)
        alternate_r_y_equation[0].set_color(GOLD)
        alternate_r_y_equation[2].set_color(GREEN)
        alternate_r_y_equation[4].set_color(RED_E)
        unsimplified_r_y_equation[0].set_color(GOLD)
        unsimplified_r_y_equation[3].set_color(PURPLE)
        unsimplified_r_y_equation[5].set_color(GRAY)
        unsimplified_r_y_equation[6].set_color(RED_E)
        unsimplified_r_y_equation[9].set_color(RED_E)

        dx_components = VGroup(
            Line(ORIGIN, r_x2.get_start() + r_x2.get_unit_vector() * dx_radius * (1 - math.cos(rotate_angle))),
            Line(r_x2.get_start() + r_x2.get_unit_vector() * dx_radius * (1 - math.cos(rotate_angle)),
                 r_x2.get_start())).set_color(RED_E)
        dx_components.rotate_about_origin(-rotate_angle)
        dx_components[0].add(
            ArrowTip(start_angle=PI / 2).scale(.5).move_to(dx_components[0].get_end(), aligned_edge=UP).set_color(
                RED_E))
        dx_components[1].add(
            ArrowTip(start_angle=0).scale(.5).move_to(dx_components[1], aligned_edge=RIGHT).set_color(RED_E))

        dy_components = VGroup(
            Line(r_y2.get_start() + r_y2.get_unit_vector() * -dy_radius * (1 - math.cos(rotate_angle)),
                 r_y2.get_start()), Line(ORIGIN, r_y2.get_start() + r_y2.get_unit_vector() * -dy_radius * (
                    1 - math.cos(rotate_angle)))).set_color(RED_E)
        dy_components.rotate_about_origin(-rotate_angle)
        dy_components[0].add(
            ArrowTip(start_angle=1.5 * PI).scale(.5).move_to(dy_components[0], aligned_edge=DOWN).set_color(RED_E))
        dy_components[1].add(
            ArrowTip(start_angle=0).scale(.5).move_to(dy_components[1].get_end(), aligned_edge=RIGHT).set_color(RED_E))

        dx_x_equation = TexMobject("dx_x", "=", "r_x", "sin(", "d\\theta", ")").scale(0.8)
        dx_y_unsimplified_equation = TexMobject("dx_y", "=", "r_x", "-", "r_x", "cos(", "d\\theta", ")").scale(0.8)
        dx_y_equation = TexMobject("dx_y", "=", "-", "r_x", "(1-cos(", "d\\theta", "))").scale(0.8)
        dx_x_equation[0].set_color(RED_E)
        dx_equation[2].set_color(TEAL)
        dx_x_equation[4].set_color(RED_E)
        dx_y_unsimplified_equation[0].set_color(RED_E)
        dx_y_unsimplified_equation[2].set_color(TEAL)
        dx_y_unsimplified_equation[4].set_color(TEAL)
        dx_y_unsimplified_equation[6].set_color(RED_E)
        dx_y_equation[0].set_color(RED_E)
        dx_y_equation[3].set_color(TEAL)
        dx_y_equation[5].set_color(RED_E)

        dy_x_unsimplified_equation = TexMobject("dy_x", "=", "r_y", "-", "r_y", "cos(", "d\\theta", ")").scale(0.8)
        dy_x_equation = TexMobject("dy_x", "=", "r_y", "(1-cos(", "d\\theta", "))").scale(0.8)
        dy_y_equation = TexMobject("dy_y", "=", "r_y", "sin(", "d\\theta", ")").scale(0.8)
        dy_x_unsimplified_equation[0].set_color(RED_E)
        dy_x_unsimplified_equation[2].set_color(GOLD)
        dy_x_unsimplified_equation[4].set_color(GOLD)
        dy_x_unsimplified_equation[6].set_color(RED_E)
        dy_x_equation[0].set_color(RED_E)
        dy_x_equation[2].set_color(GOLD)
        dy_x_equation[4].set_color(RED_E)
        dy_y_equation[0].set_color(RED_E)
        dy_y_equation[2].set_color(GOLD)
        dy_y_equation[4].set_color(RED_E)

        """
        Start animation code
        """
        self.camera_frame.shift(UP)
        self.play(ShowCreation(start_robot))

        # Need temp objects since there_and_back ShowCreations, Uncreates, and Transforms seem to delete them
        temp_straight_dx_path = straight_dx_path.copy()

        # Draw & undraw straight dx/dy + rotate movements individually
        self.play(MoveAlongPathWhileRotating(straight_dx_robot, temp_straight_dx_path, rotate_angle, rotate=False),
                  ShowCreation(temp_straight_dx_path), rate_func=there_and_back, run_time=2)
        self.remove(straight_dx_robot)
        self.wait(.5)

        temp_straight_dy_path = straight_dy_path.copy()
        self.play(MoveAlongPathWhileRotating(straight_dy_robot, temp_straight_dy_path, rotate_angle, rotate=False),
                  ShowCreation(temp_straight_dy_path), rate_func=there_and_back, run_time=2)
        self.remove(straight_dy_robot)
        self.wait(.5)

        self.play(Rotate(start_robot, rotate_angle), rate_func=there_and_back, run_time=2)
        self.wait(.5)

        temp_dx_robot = dx_robot.copy()
        temp_dy_robot = dy_robot.copy()
        temp_dy_path = dy_path.copy()
        temp_dx_path = dx_path.copy()

        # Draw straight & arc dx/dy paths side by side, then fade straight paths
        self.play(MoveAlongPathWhileRotating(temp_dx_robot, temp_dx_path, rotate_angle),
                  MoveAlongPathWhileRotating(straight_dx_robot, straight_dx_path, rotate_angle, rotate=False),
                  ShowCreation(temp_dx_path), ShowCreation(straight_dx_path))
        self.play(FadeOut(straight_dx_path), FadeOut(straight_dx_robot))
        self.wait(.5)

        self.play(MoveAlongPathWhileRotating(temp_dy_robot, temp_dy_path, rotate_angle),
                  MoveAlongPathWhileRotating(straight_dy_robot, straight_dy_path, rotate_angle,
                                             rotate=False),
                  ShowCreation(temp_dy_path), ShowCreation(straight_dy_path))
        self.play(FadeOut(straight_dy_path), FadeOut(straight_dy_robot))
        self.wait(.5)

        temp_movement_path = movement_path.copy()
        movement_robot.move_to(movement_path.get_point_from_function(rotate_angle)).rotate(rotate_angle)

        # Transform arc paths into overall movement path, then undraw movement path
        self.play(ReplacementTransform(temp_dx_robot, movement_robot),
                  ReplacementTransform(temp_dy_robot, movement_robot),
                  ReplacementTransform(temp_dx_path, temp_movement_path),
                  ReplacementTransform(temp_dy_path, temp_movement_path))
        self.wait()

        self.play(MoveAlongPathWhileRotating(movement_robot, temp_movement_path, rotate_angle, reverse=True),
                  Uncreate(temp_movement_path))
        self.play(FadeOut(movement_robot))
        self.wait()

        # Emphasize L/R odom wheels, then draw dx path with odom paths
        self.play(ApplyMethod(odom[0][0].scale, 2), ApplyMethod(odom[0][1].scale, 2), rate_func=there_and_back,
                  run_time=1.5)
        self.wait()

        temp_left_odom_path = left_odom_path.copy()
        temp_right_odom_path = right_odom_path.copy()
        temp_dx_path = dx_path.copy()
        self.play(MoveAlongPathWhileRotating(dx_robot, dx_path, rotate_angle),
                  ShowCreation(temp_left_odom_path), ShowCreation(temp_right_odom_path),
                  ShowCreation(temp_dx_path), run_time=2.5)

        # Move camera so diagram is in bottom right
        self.play(self.camera_frame.move_to,
                  left_odom_path.get_point_from_function(rotate_angle / 2) + np.array([-3, 1, 0]))

        dx_equation.next_to(self.camera_frame.get_corner(UL), DOWN * 4 + RIGHT * 6)
        dx_left_text.move_to(dx_equation[3].get_center())
        temp_dx_left_text = dx_left_text.copy()
        temp_dx_right_text = dx_equation[5].copy()

        # Write out dx equation
        self.play(TransformFromCopy(temp_dx_path, VGroup(dx_equation[0], dx_equation[1])))
        self.play(TransformFromCopy(temp_left_odom_path, temp_dx_left_text),
                  TransformFromCopy(temp_right_odom_path, temp_dx_right_text),
                  FadeIn(dx_equation[4], run_time=2), FadeIn(dx_equation[6], run_time=2),
                  FadeIn(dx_equation[7], run_time=2))
        self.wait(.5)

        dx_odom_label[0].move_to(dx_equation[3].get_center())
        dx_odom_label[1].move_to(dx_equation[5].get_center())
        dx_equation_label.next_to(dx_equation[8], RIGHT * .5)

        # Add in actual values to the dx equation
        self.play(ReplacementTransform(temp_dx_left_text, dx_odom_label[0]),
                  ReplacementTransform(temp_dx_right_text, dx_odom_label[1]), FadeIn(dx_equation[8]),
                  FadeIn(dx_equation_label))
        self.wait(.5)

        # Undraw, then re-draw dx + L/R odom paths, updating the dx equation in real time
        self.play(MoveAlongPathWhileRotating(dx_robot, temp_dx_path, rotate_angle, reverse=True,
                                             decimals_and_scales={dx_odom_label[0]: dx_radius - odom_radius,
                                                                  dx_odom_label[1]: dx_radius + odom_radius,
                                                                  dx_equation_label: dx_radius}),
                  Uncreate(temp_left_odom_path), Uncreate(temp_right_odom_path), Uncreate(temp_dx_path),
                  run_time=2.5)
        self.wait(.75)

        temp_left_odom_path = left_odom_path.copy()
        temp_right_odom_path = right_odom_path.copy()
        temp_dx_path = dx_path.copy()
        self.play(MoveAlongPathWhileRotating(dx_robot, dx_path, rotate_angle,
                                             decimals_and_scales={dx_odom_label[0]: dx_radius - odom_radius,
                                                                  dx_odom_label[1]: dx_radius + odom_radius,
                                                                  dx_equation_label: dx_radius}),
                  ShowCreation(temp_left_odom_path), ShowCreation(temp_right_odom_path),
                  ShowCreation(temp_dx_path), run_time=2.5)
        self.wait()
        self.play(ReplacementTransform(dx_odom_label[0], dx_left_text),
                  ReplacementTransform(dx_odom_label[1], dx_equation[5]),
                  FadeOut(dx_equation[8]), FadeOut(dx_equation_label))
        self.wait()

        # Draw dx arc radii and angle marker
        self.play(ShowCreation(r_x1), ShowCreation(r_x2))
        self.play(Write(r_x_label))
        self.play(ShowCreation(dx_angle_marker))
        self.wait()

        track_width_brace = Brace(VGroup(odom[1][0], odom[1][1]), direction=UP).set_color(GRAY).shift(
            DOWN * .18).rotate(
            rotate_angle, about_point=dx_robot.get_center())
        arc_length_equation.next_to(dx_equation, direction=DOWN, aligned_edge=LEFT)
        arc_length_equation_position_marker = Line(arc_length_equation[0].get_left(),
                                                   arc_length_equation[0].get_right()).next_to(arc_length_equation[0],
                                                                                               direction=DOWN * .35)
        right_arc_length_equation.next_to(arc_length_equation, direction=DOWN, aligned_edge=LEFT)
        left_arc_length_equation.next_to(arc_length_equation, direction=DOWN, aligned_edge=LEFT)
        unsimplified_dtheta_equation.next_to(dx_equation, direction=DOWN, aligned_edge=LEFT)
        dtheta_equation.next_to(dx_equation, direction=DOWN, aligned_edge=LEFT)
        dtheta_equation_label.next_to(dtheta_equation)

        # Write out general arc length equation and walk through the specific equation for the L/R odom wheels
        self.play(Write(arc_length_equation))
        self.wait()
        self.play(ShowCreation(arc_length_equation_position_marker),
                  ReplacementTransform(temp_right_odom_path,
                                       VGroup(right_arc_length_equation[0], right_arc_length_equation[1])))
        self.wait(.5)
        self.play(
            ApplyMethod(arc_length_equation_position_marker.next_to, arc_length_equation[2], {"direction": DOWN * .35}),
            TransformFromCopy(r_x_label, right_arc_length_equation[3]))
        self.wait(.5)
        self.play(ShowCreation(track_width_brace))
        self.play(FadeIn(right_arc_length_equation[4], run_time=1.5),
                  FadeIn(right_arc_length_equation[5], run_time=1.5),
                  TransformFromCopy(track_width_brace, right_arc_length_equation[6]))
        self.wait(.5)
        self.play(FadeIn(right_arc_length_equation[2]), FadeIn(right_arc_length_equation[7]))
        self.play(
            ApplyMethod(arc_length_equation_position_marker.next_to, arc_length_equation[3], {"direction": DOWN * .35}),
            TransformFromCopy(dx_angle_marker[1], right_arc_length_equation[8]))
        self.wait()

        self.play(FadeOut(arc_length_equation), FadeOut(arc_length_equation_position_marker),
                  ApplyMethod(right_arc_length_equation.move_to, arc_length_equation, {"aligned_edge": LEFT}))
        self.wait(.5)

        self.play(ReplacementTransform(temp_left_odom_path, left_arc_length_equation))
        self.wait()

        # Combine the two arc length equations to get the heading equation, then simplify it
        self.play(ReplacementTransform(right_arc_length_equation, unsimplified_dtheta_equation),
                  ReplacementTransform(left_arc_length_equation, unsimplified_dtheta_equation))
        self.wait()
        self.play(ReplacementTransform(unsimplified_dtheta_equation, VGroup(*dtheta_equation[:-1])),
                  FadeOut(track_width_brace))
        self.wait()

        # Fade in heading equation label
        self.play(FadeIn(dtheta_equation[7]), FadeIn(dtheta_equation_label))
        self.wait(.5)

        temp_dx_robot = dx_robot.copy()
        self.add(temp_dx_robot)
        self.remove(dx_robot)
        r_x1.save_state()
        r_x2.save_state()
        dx_angle_marker.save_state()
        self.wait(.5)

        # Transform dx robot to become straight to show how heading approaches 0, then go back
        # ANIMATION 60
        self.play(Transform(temp_dx_robot, straight_dx_robot),
                  Transform(temp_dx_path, straight_dx_path),
                  UpdateFromAlphaFunc(r_x1, lambda mob, alpha: mob.restore().put_start_and_end_on(
                      ORIGIN, LEFT * 100) if alpha > 0.999 else mob.restore().put_start_and_end_on(
                      ORIGIN, LEFT * dx_radius / (1 - alpha + 0.00001))),
                  UpdateFromAlphaFunc(r_x2, lambda mob, alpha: mob.restore().put_start_and_end_on(
                      UP * dx_radius * rotate_angle,
                      UP * dx_radius * rotate_angle + LEFT * 100) if alpha > 0.999 else mob.restore().rotate(
                      -rotate_angle * alpha, about_point=mob.get_start()).put_start_and_end_on(np.array(
                      [-dx_radius / (1 - alpha + 0.00001) * (1 - math.cos(rotate_angle * (1 - alpha + 0.00001))),
                       dx_radius / (1 - alpha + 0.00001) * math.sin(rotate_angle * (1 - alpha + 0.00001)), 0]),
                      LEFT * dx_radius / (1 - alpha + 0.00001))),
                  Transform(r_x_label, TexMobject("\\infty").move_to(r_x_label)),
                  UpdateFromAlphaFunc(dx_angle_marker, lambda mob, alpha: mob.restore().shift(
                      LEFT * (dx_radius / (1 - alpha + 0.00001) - dx_radius)).scale(1 - alpha, about_point=np.array(
                      [mob[0].get_center()[0], 0, 0]))),
                  UpdateFromAlphaFunc(dtheta_equation_label[0],
                                      lambda mob, alpha: mob.set_value(rotate_angle * (1 - alpha))),
                  rate_func=there_and_back, run_time=6)

        self.play(FadeOut(dtheta_equation[7]), FadeOut(dtheta_equation_label))
        self.wait()

        dx_robot_axes = robot_axes.copy()
        dx_robot_axes.next_to(self.camera_frame.get_corner(UR), DL * 4).set_color(WHITE)
        rotate_group = VGroup(start_robot, temp_dx_robot, temp_dx_path, r_x1, r_x2, dx_angle_marker[0])
        dx_components_labels = VGroup(TexMobject("dx_x").next_to(dx_components[0], LEFT).shift(RIGHT * 0.2),
                                      TexMobject("dx_y").next_to(dx_components[1], UP).shift(RIGHT * 0.2)).scale(
            0.8).set_color(dx_components.get_color())
        dx_components_r_angle_marker = VGroup(
            Line(dx_components[0].get_end() + LEFT * 0.25, dx_components[0].get_end() + DL * 0.25),
            Line(dx_components[0].get_end() + DL * 0.25, dx_components[0].get_end() + DOWN * 0.25))

        # Rotate diagram into final-robot-frame, then label dx and its x/y components
        self.play(Rotate(rotate_group, angle=-rotate_angle, about_point=ORIGIN),
                  Transform(dx_angle_marker[1],
                            dx_angle_marker[1].copy().rotate_about_origin(-rotate_angle).rotate(rotate_angle)),
                  Transform(r_x_label, r_x_label.copy().rotate_about_origin(-rotate_angle).rotate(rotate_angle)))

        dx_label.next_to(temp_dx_path).shift(LEFT * 0.1)
        self.play(ShowCreation(dx_label))
        self.play(ReplacementTransform(temp_dx_robot, dx_robot_axes))
        self.wait(.5)
        self.play(ShowCreation(dx_components[0]), ShowCreation(dx_components_labels[0]))
        self.wait(.2)
        self.play(ShowCreation(dx_components[1]), ShowCreation(dx_components_labels[1]))
        self.wait(.5)
        self.play(ShowCreation(dx_components_r_angle_marker))
        self.wait()

        temp_arc_length_equation = arc_length_equation.copy().move_to(dx_equation, aligned_edge=LEFT)
        modified_arc_length_equation.move_to(temp_arc_length_equation, aligned_edge=LEFT)
        r_x_equation.move_to(temp_arc_length_equation, aligned_edge=LEFT)
        dx_x_equation.next_to(r_x_equation, direction=DOWN, aligned_edge=LEFT)
        dx_y_unsimplified_equation.next_to(dx_x_equation, direction=DOWN, aligned_edge=LEFT)
        dx_y_equation.next_to(dx_x_equation, direction=DOWN, aligned_edge=LEFT)
        dx_dtheta_equations = VGroup(*dx_equation[:3], *dx_equation[4:-1], dx_left_text,
                                     dtheta_equation[:-1]).save_state()

        # Shift down dx and dtheta equations
        self.play(UpdateFromAlphaFunc(dx_dtheta_equations,
                                      lambda mob, alpha: mob.restore().shift(DOWN * 4 * alpha).scale(
                                          1 - 0.2 / 0.8 * alpha, about_point=dtheta_equation.get_corner(DL))))
        self.wait()

        # Write out arc length equation and transform into r_x equation
        self.play(Write(temp_arc_length_equation))
        self.wait()
        self.play(Transform(temp_arc_length_equation, modified_arc_length_equation.copy()))
        self.wait()
        self.play(ReplacementTransform(temp_arc_length_equation, r_x_equation))
        self.wait()

        # Write out dx_x equation
        self.play(TransformFromCopy(dx_components_labels[0], VGroup(dx_x_equation[0], dx_x_equation[1])))
        self.wait(.5)
        self.play(TransformFromCopy(r_x_label, dx_x_equation[2]), FadeIn(dx_x_equation[3], run_time=2),
                  TransformFromCopy(dx_angle_marker[1], dx_x_equation[4]), FadeIn(dx_x_equation[5], run_time=2))
        self.wait()

        # Write out dx_y equation, emphasising the necessary lines (using doubled-up temp. lines) for it to make sense
        self.play(
            TransformFromCopy(dx_components_labels[1],
                              VGroup(dx_y_unsimplified_equation[0], dx_y_unsimplified_equation[1])))
        self.wait(.5)

        temp_dx_r2 = Line(r_x2.get_end(), r_x2.get_start()).set_color(TEAL).shift(UP * 0.02)
        temp_dx_r2_2 = temp_dx_r2.copy().shift(DOWN * 0.04)
        self.play(ShowCreation(temp_dx_r2), ShowCreation(temp_dx_r2_2))
        self.wait(.5)
        self.play(ReplacementTransform(temp_dx_r2, dx_y_unsimplified_equation[2]),
                  ReplacementTransform(temp_dx_r2_2, dx_y_unsimplified_equation[2]))
        self.wait(.5)

        temp_line1 = Line(r_x2.get_end(), dx_components[0].get_end()).set_color(WHITE).shift(UP * 0.02)
        temp_line2 = temp_line1.copy().shift(DOWN * 0.04)
        self.play(FadeIn(dx_y_unsimplified_equation[3]))
        self.play(ShowCreation(temp_line1), ShowCreation(temp_line2))
        self.wait(.5)
        self.play(ReplacementTransform(temp_line1, VGroup(*dx_y_unsimplified_equation[4:])),
                  ReplacementTransform(temp_line2, VGroup(*dx_y_unsimplified_equation[4:])))
        self.wait()

        dx_y_equation_end = dx_y_equation[3:].save_state()
        dx_y_equation_end.shift(LEFT * (dx_y_equation_end.get_left() - dx_y_unsimplified_equation[2].get_left()))

        # Factor out r_x from the dx_y equation to simplify
        self.play(ReplacementTransform(dx_y_unsimplified_equation[:2], dx_y_equation[:2]),
                  ReplacementTransform(dx_y_unsimplified_equation[2:], dx_y_equation_end))
        self.wait()

        temp_line1 = Line(dx_components[1].get_start(), dx_components[1].get_end() + LEFT * 0.1).set_color(
            dx_components[1].get_color()).shift(UP * 0.02)
        temp_line2 = temp_line1.copy().shift(DOWN * 0.04)
        temp_arrow = ArrowTip(start_angle=0).scale(0.65).set_color(dx_components[1].get_color()).move_to(
            dx_components[1].get_end(), aligned_edge=RIGHT)
        temp_line1.add(temp_arrow)
        temp_line2.add(temp_arrow.copy())

        temp_line_3 = Line(dx_robot_axes[1].get_start(), dx_robot_axes[1].get_end() + RIGHT * 0.1).set_color(
            dx_robot_axes[1].get_color()).shift(UP * 0.02)
        temp_line_4 = temp_line_3.copy().shift(DOWN * 0.04)
        temp_arrow_tip_2 = ArrowTip(start_angle=PI).scale(0.65).set_color(dx_robot_axes[1].get_color()).move_to(
            dx_robot_axes[1].get_end(), aligned_edge=LEFT)
        temp_line_3.add(temp_arrow_tip_2)
        temp_line_4.add(temp_arrow_tip_2.copy())

        y_arrow_height_diff = dx_robot_axes[1].get_end()[1] - dx_components[1].get_end()[1]

        # Emphasize the opposite directions of the dx_y and robot x vectors, then transform the arrows into a negative
        # sign for the dx_y equation
        self.play(ShowCreation(temp_line1), ShowCreation(temp_line2))
        self.wait(.2)
        self.play(temp_line1.shift, UP * y_arrow_height_diff / 2, temp_line2.shift, UP * y_arrow_height_diff / 2)
        self.wait(.5)
        self.play(ShowCreation(temp_line_3), ShowCreation(temp_line_4))
        self.wait(.2)
        self.play(temp_line_3.shift, DOWN * y_arrow_height_diff / 2, temp_line_4.shift, DOWN * y_arrow_height_diff / 2)
        self.wait()
        self.play(ReplacementTransform(VGroup(temp_line1, temp_line2, temp_line_3, temp_line_4), dx_y_equation[2]),
                  ApplyMethod(dx_y_equation_end.restore))
        self.wait()

        dx_diagram = VGroup(r_x1, r_x2, r_x_label, dx_angle_marker, dx_components, dx_components_labels,
                            dx_components_r_angle_marker, dx_label)

        # Fade out the dx diagram and transform the robot axes back into the dx_robot
        # ANIMATION 102
        self.play(FadeOut(dx_diagram), ReplacementTransform(dx_robot_axes, dx_robot.rotate(-rotate_angle).move_to(
            temp_dx_path.get_end())))
        self.wait()
        self.play(VGroup(start_robot, dx_robot, temp_dx_path).rotate, rotate_angle, {"about_point": ORIGIN})
        self.wait()

        dx_components_equations = VGroup(r_x_equation, dx_x_equation, dx_y_equation)

        # Move the camera frame back to centered and shift the two equation groups out of frame
        self.play(self.camera_frame.move_to, UP, dx_components_equations.shift, UP * 3 + LEFT * 6,
                  dx_dtheta_equations.shift, LEFT * 5)
        self.wait()

        # Move dx robot back to start and fade out
        self.play(MoveAlongPathWhileRotating(dx_robot, temp_dx_path, rotate_angle, reverse=True),
                  Uncreate(temp_dx_path))
        self.play(FadeOut(dx_robot))
        self.wait()

        # Emphasize back odom wheel, then draw dy path with odom path
        self.play(odom[0][2].scale, 2, rate_func=there_and_back, run_time=1.5)
        self.wait()

        temp_back_odom_path = back_odom_path.copy()
        temp_dy_robot = dy_robot.copy()
        temp_dy_path = dy_path.copy()
        self.play(MoveAlongPathWhileRotating(temp_dy_robot, temp_dy_path, rotate_angle),
                  ShowCreation(temp_back_odom_path), ShowCreation(temp_dy_path), run_time=2.5)
        self.wait()

        dy_equation.next_to(self.camera_frame.get_corner(UL), DOWN * 4 + RIGHT * 6)
        question_mark = TexMobject("?").scale(0.8).next_to(dy_equation[3]).shift(UL * 0.05)
        back_odom_equation.next_to(dy_equation, direction=DOWN, aligned_edge=LEFT)
        back_odom_equation_label.next_to(back_odom_equation[1]).shift(UL * 0.05)
        self.play(TransformFromCopy(temp_dy_path, dy_equation[:2]))
        self.wait()
        self.play(TransformFromCopy(temp_back_odom_path, dy_equation[2]))
        self.wait()
        self.play(Write(dy_equation[3]), Write(question_mark))
        self.play(MoveAlongPathWhileRotating(temp_dy_robot, temp_dy_path, rotate_angle, reverse=True),
                  Uncreate(temp_back_odom_path), Uncreate(temp_dy_path))
        self.wait()

        self.play(TransformFromCopy(dy_equation[2], back_odom_equation[:2]),
                  FadeIn(back_odom_equation_label, run_time=2))
        temp_straight_dy_path = straight_dy_path.copy()
        self.play(MoveAlongPathWhileRotating(temp_dy_robot, temp_straight_dy_path, rotate_angle, rotate=False,
                                             decimals_and_scales={back_odom_equation_label: dy_radius}),
                  ShowCreation(temp_straight_dy_path), rate_func=there_and_back, run_time=6)
        self.wait(.5)

        self.play(UpdateFromAlphaFunc(back_odom_equation_label,
                                      lambda mob, alpha: mob.set_value(-odom_radius * rotate_angle * alpha)),
                  Rotate(temp_dy_robot, rotate_angle), ShowCreation(back_odom_rotate_path), run_time=2)
        self.wait(.5)
        # self.play(FadeOut(back_odom_equation[:2]), FadeOut(back_odom_equation_label))
        self.play(FadeOut(back_odom_equation[:2]), FadeOut(question_mark),
                  Transform(back_odom_equation_label, TexMobject("rotate").scale(0.8).move_to(
                      question_mark, aligned_edge=LEFT).shift(DOWN * 0.03)))
        self.wait()

        temp_robot_center = robot_centers[0].copy()
        r_back_brace = Brace(Line(robot_centers[0].get_center(), odom[0][2].get_center()), direction=LEFT).set_color(
            GRAY).stretch(0.8, 0)
        self.add(temp_robot_center)
        self.play(FadeOut(start_robot), FadeOut(temp_dy_robot))
        self.wait()
        self.play(ShowCreation(r_back_brace))
        self.wait()
        self.play(FadeOut(back_odom_equation_label), ReplacementTransform(r_back_brace, dy_equation[4]),
                  FadeIn(dy_equation[5], run_time=2))
        self.wait()

        temp_dy_path = dy_path.copy()
        temp_dy_robot.rotate(-rotate_angle)

        self.play(FadeOut(back_odom_rotate_path), FadeIn(start_robot))
        self.remove(temp_robot_center)
        self.wait()
        self.play(MoveAlongPathWhileRotating(temp_dy_robot, temp_dy_path, rotate_angle), ShowCreation(temp_dy_path))

        # Move camera so diagram is in bottom right
        self.play(self.camera_frame.shift, UP * 1.5 + LEFT * 0.5,
                  dy_equation.shift, UP * 1.5 + LEFT * 0.5)
        self.wait()

        self.play(ShowCreation(r_y1), ShowCreation(r_y2))
        self.wait()

        self.play(Write(r_y_label))
        self.play(ShowCreation(dy_angle_marker))

        dy_robot_axes = robot_axes.copy()
        dy_robot_axes.next_to(self.camera_frame.get_corner(UR), DL * 4).set_color(WHITE)
        rotate_group = VGroup(start_robot, temp_dy_robot, temp_dy_path, r_y1, r_y2,
                              dy_angle_marker[0])
        dy_components_labels = VGroup(
            TexMobject("dy_x").next_to(dy_components[0], RIGHT).shift(DOWN * 0.1 + LEFT * 0.05),
            TexMobject("dy_y").next_to(dy_components[1], UP).shift(DOWN * 0.22 + LEFT * 0.1)).scale(0.8).set_color(
            dy_components.get_color())
        dy_components_r_angle_marker = VGroup(
            Line(dy_components[1].get_end() + LEFT * 0.25, dy_components[1].get_end() + UL * 0.25),
            Line(dy_components[1].get_end() + UL * 0.25, dy_components[1].get_end() + UP * 0.25))

        # Rotate diagram into final-robot-frame, then label dy and its x/y components
        self.play(Rotate(rotate_group, angle=-rotate_angle, about_point=ORIGIN),
                  Transform(dy_angle_marker[1],
                            dy_angle_marker[1].copy().rotate_about_origin(-rotate_angle).rotate(rotate_angle)),
                  Transform(r_y_label, r_y_label.copy().rotate_about_origin(-rotate_angle).rotate(rotate_angle)))

        dy_label.next_to(temp_dy_path, direction=DOWN).shift(UP * 0.2 + LEFT * 0.1)
        self.play(ShowCreation(dy_label))
        self.play(ReplacementTransform(temp_dy_robot, dy_robot_axes))
        self.wait(.5)
        self.play(ShowCreation(dy_components[0]), ShowCreation(dy_components_labels[0]))
        self.wait(.2)
        self.play(ShowCreation(dy_components[1]), ShowCreation(dy_components_labels[1]))
        self.wait(.5)
        self.play(ShowCreation(dy_components_r_angle_marker))
        self.wait()

        r_y_equation.move_to(dy_equation, aligned_edge=LEFT)
        alternate_r_y_equation.move_to(r_y_equation, aligned_edge=LEFT)
        unsimplified_r_y_equation.move_to(r_y_equation, aligned_edge=LEFT)
        long_r_y11 = Line(r_y1.get_start(), odom[0][2].get_center()).set_color(GRAY).shift(LEFT * 0.02)
        long_r_y12 = long_r_y11.copy().shift(RIGHT * 0.04)
        long_r_y21 = Line(r_y2.get_start(), r_y2.get_start() + DOWN * odom_radius).set_color(GRAY).rotate_about_origin(
            rotate_angle).shift(LEFT * 0.04)
        long_r_y22 = long_r_y21.copy().shift(RIGHT * 0.04).rotate_about_origin(-rotate_angle)
        long_r_y21.rotate_about_origin(-rotate_angle)
        dy_x_unsimplified_equation.next_to(r_y_equation, direction=DOWN, aligned_edge=LEFT)
        dy_x_equation.move_to(dy_x_unsimplified_equation, aligned_edge=LEFT)
        dy_y_equation.next_to(dy_x_unsimplified_equation, direction=DOWN, aligned_edge=LEFT)
        underline = Line(r_y_equation[5].get_left(),
                         np.array([r_y_equation[6].get_right()[0], r_y_equation[5].get_left()[1], 0])).shift(
            DOWN * 0.28).set_color(GRAY)

        self.play(ApplyMethod(dy_equation.next_to, r_y_equation, {"direction": DOWN, "aligned_edge": LEFT}),
                  Write(alternate_r_y_equation))
        self.wait()
        self.play(ReplacementTransform(alternate_r_y_equation[:2], unsimplified_r_y_equation[:2]),
                  ReplacementTransform(alternate_r_y_equation[2:],
                                       VGroup(unsimplified_r_y_equation[2], *unsimplified_r_y_equation[7:])),
                  FadeOut(dy_equation[:2]), ReplacementTransform(dy_equation[2:], unsimplified_r_y_equation[3:7]))
        self.wait()
        self.play(ReplacementTransform(unsimplified_r_y_equation[:2], r_y_equation[:2]),
                  ReplacementTransform(unsimplified_r_y_equation[2:], r_y_equation[2:]))
        self.wait()
        self.play(ShowCreation(underline), ShowCreation(long_r_y11), ShowCreation(long_r_y12),
                  ShowCreation(long_r_y21), ShowCreation(long_r_y22))
        self.wait()
        self.play(Uncreate(underline), Uncreate(long_r_y11), Uncreate(long_r_y12),
                  Uncreate(long_r_y21), Uncreate(long_r_y22))
        self.wait()

        # Write out dy_x equation, emphasising the necessary lines (using doubled-up temp. lines) for it to make sense
        self.play(
            TransformFromCopy(dy_components_labels[0],
                              VGroup(dy_x_unsimplified_equation[0], dy_x_unsimplified_equation[1])))
        self.wait(.5)

        temp_dy_r2 = Line(r_y2.get_end(), r_y2.get_start()).set_color(GOLD).shift(LEFT * 0.02)
        temp_dy_r2_2 = temp_dy_r2.copy().shift(RIGHT * 0.04)
        self.play(ShowCreation(temp_dy_r2), ShowCreation(temp_dy_r2_2))
        self.wait(.5)
        self.play(ReplacementTransform(temp_dy_r2, dy_x_unsimplified_equation[2]),
                  ReplacementTransform(temp_dy_r2_2, dy_x_unsimplified_equation[2]))
        self.wait(.5)

        temp_line1 = Line(r_y2.get_end(), dy_components[1].get_end()).set_color(WHITE).shift(LEFT * 0.02)
        temp_line2 = temp_line1.copy().shift(RIGHT * 0.04)
        self.play(FadeIn(dy_x_unsimplified_equation[3]))
        self.play(ShowCreation(temp_line1), ShowCreation(temp_line2))
        self.wait(.5)
        self.play(ReplacementTransform(temp_line1, VGroup(*dy_x_unsimplified_equation[4:])),
                  ReplacementTransform(temp_line2, VGroup(*dy_x_unsimplified_equation[4:])))
        self.wait()

        # Factor out r_y from the dy_x equation to simplify
        self.play(ReplacementTransform(dy_x_unsimplified_equation[:2], dy_x_equation[:2]),
                  ReplacementTransform(dy_x_unsimplified_equation[2:], dy_x_equation[2:]))
        self.wait()

        # Write out dy_y equation
        self.play(TransformFromCopy(dy_components_labels[0], VGroup(dy_y_equation[0], dy_y_equation[1])))
        self.wait(.5)
        self.play(TransformFromCopy(r_y_label, dy_y_equation[2]), FadeIn(dy_y_equation[3], run_time=2),
                  TransformFromCopy(dy_angle_marker[1], dy_y_equation[4]), FadeIn(dy_y_equation[5], run_time=2))
        self.wait()

        dy_components_equations = VGroup(r_y_equation, dy_x_equation, dy_y_equation)
        temp_dx_path = dx_path.copy().rotate_about_origin(-rotate_angle)
        self.play(AnimationGroup(ShowCreation(temp_dx_path),
                                 AnimationGroup(ShowCreation(r_x1), ShowCreation(r_x2), lag_ratio=0),
                                 ShowCreation(r_x_label), ShowCreation(dx_angle_marker),
                                 AnimationGroup(ShowCreation(dx_components[0]), ShowCreation(dx_components_labels[0]),
                                                lag_ratio=0),
                                 AnimationGroup(ShowCreation(dx_components[1]), ShowCreation(dx_components_labels[1]),
                                                lag_ratio=0), lag_ratio=1),
                  Uncreate(dy_components_r_angle_marker),
                  Uncreate(dy_label),
                  Transform(dx_dtheta_equations, dx_dtheta_equations.copy().scale_about_point(
                      0.8 / 0.6, dx_dtheta_equations.copy().get_corner(DL)).shift(RIGHT * (
                          dy_components_equations.copy().get_edge_center(LEFT)[0] + 1.5 -
                          DEFAULT_MOBJECT_TO_MOBJECT_BUFFER - dx_components_equations.copy().get_width() -
                          dx_dtheta_equations.copy().get_edge_center(LEFT)[0]))),
                  self.camera_frame.shift, LEFT * 2.5,
                  dy_components_equations.shift, RIGHT * 2,
                  dx_components_equations.next_to, dy_components_equations.copy().shift(RIGHT * 1.5),
                  {"direction": LEFT},
                  run_time=3)
        self.wait()

        top_to_bottom_equation_distance = r_x_equation.get_edge_center(UP) - dtheta_equation[:-1].get_edge_center(UP)
        movement_path.rotate_about_origin(-rotate_angle)
        movement_robot.move_to(movement_path.get_point_from_function(rotate_angle)).rotate_about_origin(
            -rotate_angle).rotate(rotate_angle)
        self.play(dtheta_equation[:-1].shift, UP * top_to_bottom_equation_distance,
                  r_x_equation.shift, DOWN * top_to_bottom_equation_distance,
                  r_y_equation.next_to, r_x_equation.copy().shift(DOWN * top_to_bottom_equation_distance),
                  {"direction": DOWN, "aligned_edge": LEFT},
                  VGroup(dx_x_equation, dx_y_equation, dy_x_equation, dy_y_equation).shift,
                  DOWN * (dtheta_equation[:-1].copy().get_height() - r_x_equation.copy().get_height()))
        self.wait()
        self.play(FadeOut(VGroup(r_x1, r_x2, r_y1, r_y2, dx_angle_marker, dy_angle_marker, r_x_label, r_y_label)))
        self.play(FadeIn(movement_robot), ReplacementTransform(VGroup(temp_dx_path, temp_dy_path), movement_path))
        self.wait()

        dx_x_length = dx_components[0].get_height()
        dx_y_length = dx_components[1].get_width()
        dy_x_length = dy_components[0].get_height()
        dy_y_length = dy_components[1].get_width()

        self.play(FadeOut(VGroup(dx_components_labels, dy_components_labels)))
        self.play(dy_components[1].put_start_and_end_on, dx_components[1].get_end(), dx_components[1].get_end() + dy_y_length*RIGHT,
                  dy_components[0].shift, dx_x_length*UP, dx_y_length*RIGHT)
        self.wait()
        # Ivan's bad code
        # self.play(dy_components[0].put_start_and_end_on, dx_components[0].get_end(),
        #           dx_components[0].get_end() + DOWN * dy_x_length)
        # self.play(dx_components[1].shift, DOWN * dy_x_length,
        #           dy_components[1].put_start_and_end_on,
        #           dx_components[0].get_end() + DOWN * dy_x_length + RIGHT * dx_y_length,
        #           dx_components[0].get_end() + DOWN * dy_x_length + RIGHT * (dx_y_length + dy_y_length))
        # self.wait()
