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
        leftOdomFunction = createFunction(lambda t : np.array([-(tankRadius-odomRadius)*(1-math.cos(t))-odomRadius, 
            (tankRadius-odomRadius)*math.sin(t), 0]), BLUE)
        rightOdomFunction = createFunction(lambda t : np.array([-(tankRadius+odomRadius)*(1-math.cos(t))+odomRadius, 
            (tankRadius+odomRadius)*math.sin(t), 0]), BLUE)

        strafeFunction = createFunction(lambda t : np.array([-strafeRadius*math.sin(t), -strafeRadius*(1-math.cos(t)), 0]), GREEN)
        backOdomFunction = createFunction(lambda t : np.array([-(strafeRadius-odomRadius)*math.sin(t), 
            -(strafeRadius-odomRadius)*(1-math.cos(t))-odomRadius, 0]), GREEN)

        movementFunction = createFunction(lambda t : np.array([-strafeRadius * math.sin(t) - tankRadius * (1-math.cos(t)), 
            tankRadius * math.sin(t) - strafeRadius * (1-math.cos(t)), 0]), RED)
        
        tankR1 = Line(tankFunction.get_point_from_function(0), np.array([-tankRadius,0,0]), color=BLUE)
        tankR2 = Line(tankFunction.get_point_from_function(angle), np.array([-tankRadius,0,0]), color=BLUE)
        strafeR1 = Line(np.array([0,0,0]), np.array([0,-strafeRadius,0]), color=GREEN)
        strafeR2 = Line(strafeFunction.get_point_from_function(angle), np.array([0,-strafeRadius,0]), color=GREEN)

        tankEquation = TexMobject("fwd","=","{ left","+","right","\\over","2}","=")
        tankEquation[0].set_color(BLUE)
        tankEquation[2].set_color(BLUE)
        tankEquation[4].set_color(BLUE)
        tankEquation.scale(0.7)

        tankOdomLabel = VGroup(DecimalNumber(0).scale(.7), DecimalNumber(0).scale(.7))
        # tankOdomLabel.arrange(RIGHT)
        tankOdomLabel.next_to(startRobot, LEFT*3 + UP*10)
        tankEquationLabel = DecimalNumber(0).scale(.7)


        # Start animation code
        self.play(ShowCreation(startRobot))

        # Draw & undraw straight tank/strafe + rotate movements individually
            # Need temp objects since there_and_back ShowCreations, Uncreates, and Transforms seem to delete them
        tempStraightTankFunction = straightTankFunction.copy()
        self.play(ShowCreation(tempStraightTankFunction), 
            MoveAlongPathWhileRotating(straightTankRobot, tempStraightTankFunction, angle, rotate=False), 
            rate_func=there_and_back, run_time=2)
        self.remove(straightTankRobot)
        self.wait(.5)

        tempStraightStrafeFunction = straightStrafeFunction.copy()
        self.play(ShowCreation(tempStraightStrafeFunction), 
            MoveAlongPathWhileRotating(straightStrafeRobot, tempStraightStrafeFunction, angle, rotate=False),
            rate_func=there_and_back, run_time=2)
        self.remove(straightStrafeRobot)
        self.wait(.5)

        self.play(Rotate(startRobot, angle), rate_func=there_and_back, run_time=2)
        self.wait(.5)

        # Draw straight & arc tank/strafe paths side by side, then fade straight paths
        tempTankRobot = tankRobot.copy()
        tempStrafeRobot = strafeRobot.copy()
        tempTankFunction = tankFunction.copy()
        tempStrafeFunction = strafeFunction.copy()
        self.play(MoveAlongPathWhileRotating(tempTankRobot, tempTankFunction, angle),
            MoveAlongPathWhileRotating(straightTankRobot, straightTankFunction, angle, rotate=False), 
            ShowCreation(tempTankFunction), ShowCreation(straightTankFunction))
        self.play(FadeOut(straightTankFunction), FadeOut(straightTankRobot))
        self.wait(.5)

        self.play(MoveAlongPathWhileRotating(tempStrafeRobot, tempStrafeFunction, angle),
            MoveAlongPathWhileRotating(straightStrafeRobot, straightStrafeFunction, angle, rotate=False),
            ShowCreation(tempStrafeFunction), ShowCreation(straightStrafeFunction))
        self.play(FadeOut(straightStrafeFunction), FadeOut(straightStrafeRobot))
        self.wait(.5)

        # Transform arc paths into overall movement path, then undraw movement path
        tempMovementFunction = movementFunction.copy()
        movementRobot.move_to(movementFunction.get_point_from_function(angle)).rotate(angle)
        self.play(ReplacementTransform(tempTankRobot, movementRobot), ReplacementTransform(tempStrafeRobot, movementRobot), 
            ReplacementTransform(tempTankFunction, tempMovementFunction), ReplacementTransform(tempStrafeFunction, tempMovementFunction))
        self.wait()

        self.play(MoveAlongPathWhileRotating(movementRobot, tempMovementFunction, angle, reverse=True), 
            Uncreate(tempMovementFunction))
        self.play(FadeOut(movementRobot))
        self.wait(2)

        # Emphasize L/R odom wheels, then draw tank path with odom paths 
        self.play(ApplyMethod(odom[0][0].scale, 2), ApplyMethod(odom[0][1].scale, 2), run_time=0.6)
        self.play(ApplyMethod(odom[0][0].scale, 1/2), ApplyMethod(odom[0][1].scale, 1/2), run_time=0.6)
        self.wait()
        tempLeftOdomFunction = leftOdomFunction.copy()
        tempRightOdomFunction = rightOdomFunction.copy()
        tempTankFunction = tankFunction.copy()
        self.play(MoveAlongPathWhileRotating(tankRobot, tankFunction, angle),
            ShowCreation(tempLeftOdomFunction), ShowCreation(tempRightOdomFunction), ShowCreation(tempTankFunction), run_time=2.5)

        # Move camera so diagram is in bottom right, then write out forward equation
        self.play(self.camera_frame.move_to, leftOdomFunction.get_point_from_function(angle/2) + np.array([-3,1,0]))

        tankEquation.next_to(self.camera_frame.get_corner(UP+LEFT), DOWN*6+RIGHT*8)
        self.play(TransformFromCopy(tempTankFunction, tankEquation[0]), FadeIn(tankEquation[1], run_time=2))
        self.play(TransformFromCopy(tempLeftOdomFunction, tankEquation[2]), TransformFromCopy(tempRightOdomFunction, tankEquation[4]),
            FadeIn(tankEquation[3], run_time=2), FadeIn(tankEquation[5], run_time=2), 
            FadeIn(tankEquation[6], run_time=2), FadeIn(tankEquation[7], run_time=2))
        self.wait()

        # Add in actual values to the tank equation
        tankOdomLabel[0].move_to(tankEquation[2].get_center())
        tankOdomLabel[1].move_to(tankEquation[4].get_center())
        tankEquationLabel.next_to(tankEquation[7], RIGHT*.5)
        self.play(ReplacementTransform(tankEquation[2], tankOdomLabel[0]), 
            ReplacementTransform(tankEquation[4], tankOdomLabel[1]), FadeIn(tankEquationLabel))

        # Undraw, then re-draw tank + L/R odom paths, updating the tank equation in real time
        self.play(MoveAlongPathWhileRotating(tankRobot, tempTankFunction, angle, reverse=True, 
            decimals_and_scales={tankOdomLabel[0]: tankRadius-odomRadius, tankOdomLabel[1]: tankRadius+odomRadius, tankEquationLabel: tankRadius}),
            Uncreate(tempLeftOdomFunction), Uncreate(tempRightOdomFunction), Uncreate(tempTankFunction), run_time=2)
        self.wait(.75)

        tempLeftOdomFunction = leftOdomFunction.copy()
        tempRightOdomFunction = rightOdomFunction.copy()
        tempTankFunction = tankFunction.copy()
        self.play(MoveAlongPathWhileRotating(tankRobot, tankFunction, angle, 
            decimals_and_scales={tankOdomLabel[0]: tankRadius-odomRadius, tankOdomLabel[1]: tankRadius+odomRadius, tankEquationLabel: tankRadius}),
            ShowCreation(tempLeftOdomFunction), ShowCreation(tempRightOdomFunction), ShowCreation(tempTankFunction), run_time=2)
        self.wait()