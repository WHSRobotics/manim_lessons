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

class Drive(MovingCameraScene):

    def construct(self):
        odomRadius = .45
        odomHeight = 0.15
        odomWidth = 0.02
        rotateAngle = math.radians(20)
        tankRadius = 8
        strafeRadius = -6

        startRobot = Square(side_length=1.2)
        tankRobot = Square(side_length=1.2, color=BLUE)
        strafeRobot = Square(side_length=1.2, color=GREEN)
        movementRobot = Square(side_length=1.2, color=RED)

        odom = [[Rectangle(height=odomHeight, width=odomWidth) for i in range(3)] for j in range(3)]
        robotCenters = []
        for x in range(3):
            for y in range(3):
                if y == 0:
                    odom[x][y].move_to(np.array([-odomRadius, 0, 0]))
                elif y == 1:
                    odom[x][y].move_to(np.array([odomRadius, 0, 0]))
                else:
                    odom[x][y].move_to(np.array([0, -odomRadius, 0]))
                    odom[x][y].rotate_in_place(PI / 2)

        for z in range(4):
            robotCenters.append(Dot(np.array([0, 0, 0])))

        startRobot.add(odom[0][0], odom[0][1], odom[0][2], robotCenters[0])
        tankRobot.add(odom[1][0], odom[1][1], robotCenters[1])
        strafeRobot.add(odom[1][2], robotCenters[2])
        movementRobot.add(odom[2][0], odom[2][1], odom[2][2], robotCenters[3])

        straightTankRobot = tankRobot.copy()
        straightStrafeRobot = strafeRobot.copy()

        def createFunction(function, color=WHITE):
            return ParametricFunction(t_max=rotateAngle, function=function, color=color)

        straightTankFunction = createFunction(lambda t: np.array([0, tankRadius * t, 0]), BLUE)
        straightLeftOdomFunction = createFunction(lambda t: np.array([-odomRadius, tankRadius * t, 0]), PURPLE)
        straightRightOdomFunction = createFunction(lambda t: np.array([odomRadius, tankRadius * t, 0]), PURPLE)
        straightStrafeFunction = createFunction(lambda t: np.array([-strafeRadius * t, 0, 0]), GREEN)

        tankFunction = createFunction(
            lambda t: np.array([-tankRadius * (1 - math.cos(t)), tankRadius * math.sin(t), 0]), BLUE)
        leftOdomFunction = createFunction(
            lambda t: np.array([-(tankRadius - odomRadius) * (1 - math.cos(t)) - odomRadius,
                                (tankRadius - odomRadius) * math.sin(t), 0]), PURPLE)
        rightOdomFunction = createFunction(
            lambda t: np.array([-(tankRadius + odomRadius) * (1 - math.cos(t)) + odomRadius,
                                (tankRadius + odomRadius) * math.sin(t), 0]), PURPLE)

        strafeFunction = createFunction(
            lambda t: np.array([-strafeRadius * math.sin(t), -strafeRadius * (1 - math.cos(t)), 0]), GREEN)
        backOdomFunction = createFunction(lambda t: np.array([-(strafeRadius - odomRadius) * math.sin(t),
                                                              -(strafeRadius - odomRadius) * (
                                                                      1 - math.cos(t)) - odomRadius, 0]), GREEN)

        movementFunction = createFunction(
            lambda t: np.array([-strafeRadius * math.sin(t) - tankRadius * (1 - math.cos(t)),
                                tankRadius * math.sin(t) - strafeRadius * (1 - math.cos(t)), 0]), RED)

        robotAxes = VGroup(Arrow(ORIGIN, UP), Arrow(ORIGIN, LEFT), TexMobject("+x").scale(0.5),
                           TexMobject("+y").scale(0.5))
        robotAxes[1].move_to(robotAxes[0].get_start()).shift(LEFT * .25)
        robotAxes[2].next_to(robotAxes[0], RIGHT * .2).shift(DOWN * .05)
        robotAxes[3].next_to(robotAxes[1], DOWN * .2).shift(RIGHT * .05)

        dxLabel = TexMobject("dx").scale(0.8).set_color(BLUE)
        tankR1 = Line(tankFunction.get_point_from_function(0), np.array([-tankRadius, 0, 0]), color=BLUE)
        tankR2 = Line(tankFunction.get_point_from_function(rotateAngle), np.array([-tankRadius, 0, 0]), color=BLUE)
        rxLabel = TexMobject("r_x").scale(0.8).next_to(tankR1, direction=DOWN)
        tankAngleMarker = VGroup(Arc(radius=1.5, arc_center=np.array([-tankRadius, 0, 0]), angle=rotateAngle),
                                 TexMobject("d\\theta").scale(0.8)).set_color(PINK)
        tankAngleMarker[1].move_to(tankAngleMarker[0].get_center()).shift(UP * .06 + RIGHT * .3)
        strafeR1 = Line(np.array([0, 0, 0]), np.array([0, -strafeRadius, 0]), color=GREEN)
        strafeR2 = Line(strafeFunction.get_point_from_function(rotateAngle), np.array([0, -strafeRadius, 0]),
                        color=GREEN)

        dxEquation = TexMobject("dx", "=", "{", "leftt", "+", "right", "\\over", "2}", "=").scale(0.8)
        dxEquation[0].set_color(BLUE)
        dxEquation[3].set_color(BLACK)
        dxEquation[5].set_color(PURPLE)
        dxLeftText = TexMobject("left").set_color(PURPLE).scale(0.8)
        dxOdomLabel = VGroup(DecimalNumber(0).set_color(PURPLE).scale(0.8),
                             DecimalNumber(0).set_color(PURPLE).scale(0.8))
        dxEquationLabel = DecimalNumber(0).set_color(BLUE).scale(0.8)
        dxComponents = VGroup(Line(ORIGIN, tankFunction.get_point_from_function(
            rotateAngle) + tankR2.get_unit_vector() * tankRadius * (1 - math.cos(rotateAngle))), Line(
            tankFunction.get_point_from_function(rotateAngle) + tankR2.get_unit_vector() * tankRadius * (
                    1 - math.cos(rotateAngle)), tankFunction.get_point_from_function(rotateAngle))).set_color(RED_E)
        dxComponents.rotate_about_origin(-rotateAngle)
        dxComponents[0].add(
            ArrowTip(start_angle=PI / 2).scale(.5).move_to(dxComponents[0].get_end(), aligned_edge=UP).set_color(RED_E))
        dxComponents[1].add(
            ArrowTip(start_angle=0).scale(.5).move_to(dxComponents[1], aligned_edge=RIGHT).set_color(RED_E))

        dx_xEquation = TexMobject("dx_x", "=", "r_x", "sin(", "d\\theta", ")").scale(0.8)
        dx_xEquation[0].set_color(RED_E)
        dx_xEquation[4].set_color(PINK)

        dx_yUnsimplifiedEquation = TexMobject("dx_y", "=", "r_x", "-", "r_x", "cos(", "d\\theta", ")").scale(0.8)
        dx_yUnsimplifiedEquation[0].set_color(RED_E)
        dx_yUnsimplifiedEquation[6].set_color(PINK)

        dx_yEquation = TexMobject("dx_y", "=", "-", "r_x", "(1-cos(", "d\\theta", "))").scale(0.8)
        dx_yEquation[0].set_color(RED_E)
        dx_yEquation[5].set_color(PINK)

        arcLengthEquation = TexMobject("s", "=", "r", "\\theta").scale(0.8)
        leftArcLengthEquation = TexMobject("left", "=", "(", "r_x", "-", "0.5\\ast", "track width", ")",
                                           "d\\theta").scale(0.8)
        leftArcLengthEquation[0].set_color(PURPLE)
        leftArcLengthEquation[6].set_color(GRAY)
        leftArcLengthEquation[8].set_color(PINK)
        rightArcLengthEquation = TexMobject("right", "=", "(", "r_x", "+", "0.5\\ast", "track width", ")",
                                            "d\\theta").scale(0.8)
        rightArcLengthEquation[0].set_color(PURPLE)
        rightArcLengthEquation[6].set_color(GRAY)
        rightArcLengthEquation[8].set_color(PINK)
        unsimplifiedHeadingEquation = TexMobject("right", "-", "left", "=", "track width", "\\ast", "d\\theta").scale(
            0.8)

        unsimplifiedHeadingEquation[0].set_color(PURPLE)
        unsimplifiedHeadingEquation[2].set_color(PURPLE)
        unsimplifiedHeadingEquation[4].set_color(GRAY)
        unsimplifiedHeadingEquation[6].set_color(PINK)

        headingEquation = TexMobject("d\\theta", "=", "{right", "-", "left", "\\over", "track width}", "=").scale(0.8)
        headingEquation[0].set_color(PINK)
        headingEquation[2].set_color(PURPLE)
        headingEquation[4].set_color(PURPLE)
        headingEquation[6].set_color(GRAY)
        headingEquationLabel = VGroup(DecimalNumber(rotateAngle).scale(0.8), TexMobject("rad").scale(0.8)).set_color(
            PINK)
        headingEquationLabel.arrange()

        # Start animation code
        self.camera_frame.shift(UP)
        self.play(ShowCreation(startRobot))

        # Draw & undraw straight tank/strafe + rotate movements individually
        #     Need temp objects since there_and_back ShowCreations, Uncreates, and Transforms seem to delete them
        tempStraightTankFunction = straightTankFunction.copy()
        self.play(ShowCreation(tempStraightTankFunction),
                  MoveAlongPathWhileRotating(straightTankRobot, tempStraightTankFunction, rotateAngle, rotate=False),
                  rate_func=there_and_back, run_time=2)
        self.remove(straightTankRobot)
        self.wait(.5)

        tempStraightStrafeFunction = straightStrafeFunction.copy()
        self.play(ShowCreation(tempStraightStrafeFunction),
                  MoveAlongPathWhileRotating(straightStrafeRobot, tempStraightStrafeFunction, rotateAngle,
                                             rotate=False),
                  rate_func=there_and_back, run_time=2)
        self.remove(straightStrafeRobot)
        self.wait(.5)

        self.play(Rotate(startRobot, rotateAngle), rate_func=there_and_back, run_time=2)
        self.wait(.5)

        # Draw straight & arc tank/strafe paths side by side, then fade straight paths
        tempTankRobot = tankRobot.copy()
        tempStrafeRobot = strafeRobot.copy()
        tempTankFunction = tankFunction.copy()
        tempStrafeFunction = strafeFunction.copy()
        self.play(MoveAlongPathWhileRotating(tempTankRobot, tempTankFunction, rotateAngle),
                  MoveAlongPathWhileRotating(straightTankRobot, straightTankFunction, rotateAngle, rotate=False),
                  ShowCreation(tempTankFunction), ShowCreation(straightTankFunction))
        self.play(FadeOut(straightTankFunction), FadeOut(straightTankRobot))
        self.wait(.5)

        self.play(MoveAlongPathWhileRotating(tempStrafeRobot, tempStrafeFunction, rotateAngle),
                  MoveAlongPathWhileRotating(straightStrafeRobot, straightStrafeFunction, rotateAngle, rotate=False),
                  ShowCreation(tempStrafeFunction), ShowCreation(straightStrafeFunction))
        self.play(FadeOut(straightStrafeFunction), FadeOut(straightStrafeRobot))
        self.wait(.5)

        # Transform arc paths into overall movement path, then undraw movement path
        tempMovementFunction = movementFunction.copy()
        movementRobot.move_to(movementFunction.get_point_from_function(rotateAngle)).rotate(rotateAngle)
        self.play(ReplacementTransform(tempTankRobot, movementRobot),
                  ReplacementTransform(tempStrafeRobot, movementRobot),
                  ReplacementTransform(tempTankFunction, tempMovementFunction),
                  ReplacementTransform(tempStrafeFunction, tempMovementFunction))
        self.wait()

        self.play(MoveAlongPathWhileRotating(movementRobot, tempMovementFunction, rotateAngle, reverse=True),
                  Uncreate(tempMovementFunction))
        self.play(FadeOut(movementRobot))
        self.wait(2)

        # Emphasize L/R odom wheels, then draw tank path with odom paths
        self.play(ApplyMethod(odom[0][0].scale, 2), ApplyMethod(odom[0][1].scale, 2), rate_func=there_and_back,
                  run_time=1.5)
        self.wait()
        tempLeftOdomFunction = leftOdomFunction.copy()
        tempRightOdomFunction = rightOdomFunction.copy()
        tempTankFunction = tankFunction.copy()
        self.play(MoveAlongPathWhileRotating(tankRobot, tankFunction, rotateAngle),
                  ShowCreation(tempLeftOdomFunction), ShowCreation(tempRightOdomFunction),
                  ShowCreation(tempTankFunction), run_time=2.5)

        # Move camera so diagram is in bottom right, then write out forward equation
        self.play(self.camera_frame.move_to,
                  leftOdomFunction.get_point_from_function(rotateAngle / 2) + np.array([-3, 1, 0]))

        dxEquation.next_to(self.camera_frame.get_corner(UP + LEFT), DOWN * 4 + RIGHT * 6)
        dxLeftText.move_to(dxEquation[3].get_center())
        tempTankLeftText = dxLeftText.copy()
        tempTankRightText = dxEquation[5].copy()
        self.play(TransformFromCopy(tempTankFunction, VGroup(dxEquation[0], dxEquation[1])))
        self.play(TransformFromCopy(tempLeftOdomFunction, tempTankLeftText),
                  TransformFromCopy(tempRightOdomFunction, tempTankRightText),
                  FadeIn(dxEquation[4], run_time=2), FadeIn(dxEquation[6], run_time=2),
                  FadeIn(dxEquation[7], run_time=2))
        self.wait(.5)

        # Add in actual values to the tank equation
        dxOdomLabel[0].move_to(dxEquation[3].get_center())
        dxOdomLabel[1].move_to(dxEquation[4].get_center())
        dxEquationLabel.next_to(dxEquation[8], RIGHT * .5)
        self.play(ReplacementTransform(tempTankLeftText, dxOdomLabel[0]),
                  ReplacementTransform(tempTankRightText, dxOdomLabel[1]), FadeIn(dxEquation[8]),
                  FadeIn(dxEquationLabel))
        self.wait(.5)

        # Undraw, then re-draw tank + L/R odom paths, updating the tank equation in real time
        self.play(MoveAlongPathWhileRotating(tankRobot, tempTankFunction, rotateAngle, reverse=True,
                                             decimals_and_scales={dxOdomLabel[0]: tankRadius - odomRadius,
                                                                  dxOdomLabel[1]: tankRadius + odomRadius,
                                                                  dxEquationLabel: tankRadius}),
                  Uncreate(tempLeftOdomFunction), Uncreate(tempRightOdomFunction), Uncreate(tempTankFunction),
                  run_time=2.5)
        self.wait(.75)

        tempLeftOdomFunction = leftOdomFunction.copy()
        tempRightOdomFunction = rightOdomFunction.copy()
        tempTankFunction = tankFunction.copy()
        self.play(MoveAlongPathWhileRotating(tankRobot, tankFunction, rotateAngle,
                                             decimals_and_scales={dxOdomLabel[0]: tankRadius - odomRadius,
                                                                  dxOdomLabel[1]: tankRadius + odomRadius,
                                                                  dxEquationLabel: tankRadius}),
                  ShowCreation(tempLeftOdomFunction), ShowCreation(tempRightOdomFunction),
                  ShowCreation(tempTankFunction), run_time=2.5)
        self.wait()
        self.play(ReplacementTransform(dxOdomLabel[0], dxLeftText),
                  ReplacementTransform(dxOdomLabel[1], dxEquation[5]),
                  FadeOut(dxEquation[8]), FadeOut(dxEquationLabel))
        self.wait()

        # Draw tank arc radii and angle marker
        self.play(ShowCreation(tankR1), ShowCreation(tankR2))
        self.play(Write(rxLabel))
        self.play(ShowCreation(tankAngleMarker))
        self.wait()

        trackWidthBrace = Brace(VGroup(odom[1][0], odom[1][1]), direction=UP).set_color(GRAY).shift(DOWN * .18).rotate(
            rotateAngle, about_point=tankRobot.get_center())
        arcLengthEquation.next_to(dxEquation, direction=DOWN, aligned_edge=LEFT)
        arcLengthEquationPositionMarker = Line(arcLengthEquation[0].get_left(),
                                               arcLengthEquation[0].get_right()).next_to(arcLengthEquation[0],
                                                                                         direction=DOWN * .35)
        rightArcLengthEquation.next_to(arcLengthEquation, direction=DOWN, aligned_edge=LEFT)
        leftArcLengthEquation.next_to(arcLengthEquation, direction=DOWN, aligned_edge=LEFT)
        unsimplifiedHeadingEquation.next_to(dxEquation, direction=DOWN, aligned_edge=LEFT)
        headingEquation.next_to(dxEquation, direction=DOWN, aligned_edge=LEFT)
        headingEquationLabel.next_to(headingEquation)

        # Write out general arc length equation and walk through the specific equation for the L/R odom wheels
        self.play(Write(arcLengthEquation))
        self.wait()
        self.play(ShowCreation(arcLengthEquationPositionMarker),
                  ReplacementTransform(tempRightOdomFunction,
                                       VGroup(rightArcLengthEquation[0], rightArcLengthEquation[1])))
        self.wait(.5)
        self.play(ApplyMethod(arcLengthEquationPositionMarker.next_to, arcLengthEquation[2], {"direction": DOWN * .35}),
                  TransformFromCopy(rxLabel, rightArcLengthEquation[3]))
        self.wait(.5)
        self.play(ShowCreation(trackWidthBrace))
        self.play(FadeIn(rightArcLengthEquation[4], run_time=1.5), FadeIn(rightArcLengthEquation[5], run_time=1.5),
                  TransformFromCopy(trackWidthBrace, rightArcLengthEquation[6]))
        self.wait(.5)
        self.play(FadeIn(rightArcLengthEquation[2]), FadeIn(rightArcLengthEquation[7]))
        self.play(ApplyMethod(arcLengthEquationPositionMarker.next_to, arcLengthEquation[3], {"direction": DOWN * .35}),
                  TransformFromCopy(tankAngleMarker[1], rightArcLengthEquation[8]))
        self.wait()

        self.play(FadeOut(arcLengthEquation), FadeOut(arcLengthEquationPositionMarker),
                  ApplyMethod(rightArcLengthEquation.move_to, arcLengthEquation, {"aligned_edge": LEFT}))
        self.wait(.5)

        self.play(ReplacementTransform(tempLeftOdomFunction, leftArcLengthEquation))
        self.wait()

        # Combine the two arc length equations to get the heading equation, then simplify it
        self.play(ReplacementTransform(rightArcLengthEquation, unsimplifiedHeadingEquation),
                  ReplacementTransform(leftArcLengthEquation, unsimplifiedHeadingEquation))
        self.wait()
        self.play(ReplacementTransform(unsimplifiedHeadingEquation, VGroup(*headingEquation[:-1])),
                  FadeOut(trackWidthBrace))
        self.wait()

        # Fade in heading equation label
        self.play(FadeIn(headingEquation[7]), FadeIn(headingEquationLabel))
        self.wait(.5)

        tempTankRobot = tankRobot.copy()
        self.add(tempTankRobot)
        self.remove(tankRobot)
        tankR1.save_state()
        tankR2.save_state()
        tankAngleMarker[0].save_state()
        tankAngleMarker[1].save_state()

        # Transform tank robot to become straight to show how heading approaches 0, then go back
        self.play(Transform(tempTankRobot, straightTankRobot),
                  Transform(tempTankFunction, straightTankFunction),
                  UpdateFromAlphaFunc(tankR1, lambda mob, alpha: mob.restore().put_start_and_end_on(ORIGIN,
                                                                                                    LEFT * 100) if alpha > 0.999 else mob.restore().put_start_and_end_on(
                      ORIGIN, LEFT * tankRadius / (1 - alpha + 0.00001))),
                  UpdateFromAlphaFunc(tankR2, lambda mob, alpha: mob.restore().put_start_and_end_on(
                      UP * tankRadius * rotateAngle,
                      UP * tankRadius * rotateAngle + LEFT * 100) if alpha > 0.999 else mob.restore().rotate(
                      -rotateAngle * alpha, about_point=mob.get_start()).put_start_and_end_on(np.array(
                      [-tankRadius / (1 - alpha + 0.00001) * (1 - math.cos(rotateAngle * (1 - alpha + 0.00001))),
                       tankRadius / (1 - alpha + 0.00001) * math.sin(rotateAngle * (1 - alpha + 0.00001)), 0]),
                      LEFT * tankRadius / (
                              1 - alpha + 0.00001))),
                  Transform(rxLabel, TexMobject("\\infty").move_to(rxLabel)),
                  UpdateFromAlphaFunc(tankAngleMarker[0], lambda mob, alpha: mob.restore().shift(
                      LEFT * (tankRadius / (1 - alpha + 0.00001) - tankRadius)).scale(1 - alpha,
                                                                                      about_point=LEFT * tankRadius / (
                                                                                              1 - alpha + 0.00001))),
                  UpdateFromAlphaFunc(tankAngleMarker[1], lambda mob, alpha: mob.restore().shift(
                      LEFT * (tankRadius / (1 - alpha + 0.00001) - tankRadius))),
                  UpdateFromAlphaFunc(headingEquationLabel[0],
                                      lambda mob, alpha: mob.set_value(rotateAngle * (1 - alpha))),
                  rate_func=there_and_back, run_time=6)
        self.wait(.5)

        self.play(FadeOut(headingEquation[7]), FadeOut(headingEquationLabel))
        self.wait()

        robotAxes.next_to(self.camera_frame.get_corner(UR), DL * 4).set_color(BLUE)
        rotateGroup = VGroup(startRobot, tempTankRobot, tempTankFunction, tankR1, tankR2, tankAngleMarker[0])
        dxComponentsLabels = VGroup(TexMobject("dx_x").next_to(dxComponents[0], LEFT).shift(RIGHT * 0.2),
                                    TexMobject("dx_y").next_to(dxComponents[1], UP).shift(RIGHT * 0.2)).scale(
            0.8).set_color(dxComponents.get_color())
        dxComponentsRAngleMarker = VGroup(
            Line(dxComponents[0].get_end() + LEFT * 0.25, dxComponents[0].get_end() + LEFT * 0.25 + DOWN * 0.25),
            Line(dxComponents[0].get_end() + LEFT * 0.25 + DOWN * 0.25, dxComponents[0].get_end() + DOWN * 0.25))

        # Rotate diagram into final-robot-frame, then label dx and its x/y components
        self.play(Rotate(rotateGroup, angle=-rotateAngle, about_point=ORIGIN),
                  Transform(tankAngleMarker[1],
                            tankAngleMarker[1].copy().rotate_about_origin(-rotateAngle).rotate(rotateAngle)),
                  Transform(rxLabel, rxLabel.copy().rotate_about_origin(-rotateAngle).rotate(rotateAngle)))
        dxLabel.next_to(tempTankFunction).shift(LEFT * 0.1)
        self.play(ShowCreation(dxLabel))
        self.play(ReplacementTransform(tempTankRobot, robotAxes))
        self.wait(.5)
        self.play(ShowCreation(dxComponents[0]), ShowCreation(dxComponentsLabels[0]))
        self.wait(.2)
        self.play(ShowCreation(dxComponents[1]), ShowCreation(dxComponentsLabels[1]))
        self.wait(.5)
        self.play(ShowCreation(dxComponentsRAngleMarker))
        self.wait()

        dx_xEquation.move_to(dxEquation)
        dx_yUnsimplifiedEquation.next_to(dx_xEquation, direction=DOWN, aligned_edge=LEFT)
        dx_yEquation.next_to(dx_xEquation, direction=DOWN, aligned_edge=LEFT)
        firstEquationGroup = VGroup(*dxEquation[:3], *dxEquation[4:-1], dxLeftText, headingEquation[:-1]).save_state()

        # Shift down dx and dtheta equations
        self.play(UpdateFromAlphaFunc(firstEquationGroup,
                                      lambda mob, alpha: mob.restore().shift(DOWN * 4 * alpha).scale(
                                          1 - 0.2 / 0.8 * alpha, about_point=headingEquation.get_corner(DL))))
        self.wait()

        # Write out dx_x equation
        self.play(TransformFromCopy(dxComponentsLabels[0], VGroup(dx_xEquation[0], dx_xEquation[1])))
        self.wait(.5)
        self.play(TransformFromCopy(rxLabel, dx_xEquation[2]), FadeIn(dx_xEquation[3], run_time=2),
                  TransformFromCopy(tankAngleMarker[1], dx_xEquation[4]), FadeIn(dx_xEquation[5], run_time=2))
        self.wait()

        # Write out dx_y equation, emphasising the necessary lines (using doubled-up temp. lines) for it to make sense
        self.play(
            TransformFromCopy(dxComponentsLabels[1], VGroup(dx_yUnsimplifiedEquation[0], dx_yUnsimplifiedEquation[1])))
        self.wait(.5)
        tempTankR2 = Line(tankR2.get_end(), tankR2.get_start()).set_color(BLUE).shift(UP * 0.02)
        temp2TankR2 = tempTankR2.copy().shift(DOWN * 0.04)
        self.play(ShowCreation(tempTankR2), ShowCreation(temp2TankR2))
        self.wait(.5)
        self.play(ReplacementTransform(tempTankR2, dx_yUnsimplifiedEquation[2]),
                  ReplacementTransform(temp2TankR2, dx_yUnsimplifiedEquation[2]))
        self.wait(.5)

        tempLine = Line(tankR2.get_end(), dxComponents[0].get_end()).set_color(BLUE).shift(UP * 0.02)
        tempLine2 = tempLine.copy().shift(DOWN * 0.04)
        self.play(FadeIn(dx_yUnsimplifiedEquation[3]), ShowCreation(tempLine), ShowCreation(tempLine2))
        self.play(ReplacementTransform(tempLine, VGroup(*dx_yUnsimplifiedEquation[4:])),
                  ReplacementTransform(tempLine2, VGroup(*dx_yUnsimplifiedEquation[4:])))
        self.wait()

        # Factor out r_x from the dx_y equation to simplify
        self.play(ReplacementTransform(dx_yUnsimplifiedEquation, VGroup(*dx_yEquation[:2], *dx_yEquation[3:])))
        self.wait()

        tempLine = Line(dxComponents[1].get_start(), dxComponents[1].get_end() + LEFT * 0.1).set_color(
            dxComponents[1].get_color()).shift(UP * 0.02)
        tempLine2 = tempLine.copy().shift(DOWN * 0.04)
        tempArrow = ArrowTip(start_angle=0).scale(0.65).set_color(dxComponents[1].get_color()).move_to(
            dxComponents[1].get_end(), aligned_edge=RIGHT)
        tempLine.add(tempArrow)
        tempLine2.add(tempArrow.copy())

        tempLine3 = Line(robotAxes[1].get_start(), robotAxes[1].get_end() + RIGHT * 0.1).set_color(
            robotAxes[1].get_color()).shift(UP * 0.02)
        tempLine4 = tempLine3.copy().shift(DOWN * 0.04)
        tempArrowTip2 = ArrowTip(start_angle=PI).scale(0.65).set_color(robotAxes[1].get_color()).move_to(
            robotAxes[1].get_end(), aligned_edge=LEFT)
        tempLine3.add(tempArrowTip2)
        tempLine4.add(tempArrowTip2.copy())

        yArrowHeightDiff = robotAxes[1].get_end()[1] - dxComponents[1].get_end()[1]

        # Emphasize the opposite directions of the dx_y and robot x vectors, then transform the arrows into a negative
        # sign for the dx_y equation
        self.play(ShowCreation(tempLine), ShowCreation(tempLine2))
        self.wait(.2)
        self.play(tempLine.shift, UP * yArrowHeightDiff / 2, tempLine2.shift, UP * yArrowHeightDiff / 2)
        self.wait(.5)
        self.play(ShowCreation(tempLine3), ShowCreation(tempLine4))
        self.wait(.2)
        self.play(tempLine3.shift, DOWN * yArrowHeightDiff / 2, tempLine4.shift, DOWN * yArrowHeightDiff / 2)
        self.wait()
        self.play(ReplacementTransform(VGroup(tempLine, tempLine2, tempLine3, tempLine4), dx_yEquation[2]))
        self.wait()
