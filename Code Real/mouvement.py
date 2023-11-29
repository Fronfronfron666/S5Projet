#!/usr/bin/env python
from picar import front_wheels
from picar import back_wheels
import time
import picar
import line_follower as lf


picar.setup()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels (db='config')

ajustement_angle_roues = 7
currentspeed = 0
maxspeed = 500
wheel_angle = 0

def turn_wheels(degree):
    global wheel_angle
    wheel_angle = 90 + degree + ajustement_angle_roues
    if wheel_angle > 180:
        wheel_angle = 180
    fw.turn(wheel_angle)

def turnStraight():
    fw.turn(97)

def checkCallibration():
    turnStraight()
    bw.speed = 50
    time.sleep(5)
    bw.stop()


def check_max_and_min_speed():
    global currentspeed, maxspeed
    if currentspeed > maxspeed:
        currentspeed = maxspeed
    elif currentspeed < 0:
        currentspeed = 0

def is_turning():
    turning = False
    if lf.current_wheel_angle != 0:
        turning = True
    return turning

def avancer_test():
    acceleration = 5


def get_accceleration():
    acceleration = 5
    wheel_angle = lf.current_wheel_angle
    if wheel_angle != 0:
        if wheel_angle <= -10 or wheel_angle >= 10:
            if wheel_angle <= -20 or wheel_angle >= 20:
                acceleration = 2
            else:
                acceleration = 3
        else:
            acceleration = 4
    return acceleration

def accelerate():
    global currentspeed
    currentspeed += 1
    check_max_and_min_speed()

def decelerate():
    global currentspeed

    currentspeed -= 1
    check_max_and_min_speed()

def move():
    bw.backward()
    bw.speed = currentspeed

def startForward(targetSpeed):
    for i in range(targetSpeed):
        bw.speed = i
        time.sleep(0.01)

    time.sleep(5)
    bw.stop()


def testFW():
    for i in range(180):
        print(i)