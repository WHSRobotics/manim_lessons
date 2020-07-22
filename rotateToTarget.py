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

class RotateToTarget(MovingCameraScene):
    def construct(self):
        angle_to_target = PI/3

        text = TextMobject("Rotate To Target")
        robot = Square(side_length=1.5)
        current_headding = Line()
        text.move_to(robot.get_center() + np.array([0, 1, 0]))
        self.add(text)
        self.play(GrowFromCenter(robot))

        def rotate_to_target(obj):
            current_angle = obj.get_
            angle_to_target = current

        rotate_robot = Rotate(robot, angle=angle_to_target)
        self.play(rotate_robot)
        self.wait(2)
