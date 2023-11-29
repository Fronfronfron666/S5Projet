#!/usr/bin/env python
from picar import front_wheels
from picar import back_wheels
import time
import picar
import line_follower as lf


picar.setup()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels (db='config')

ajustement_angle_roues = 10
currentspeed = 0
MAX_SPEED = 100
wheel_angle = 0
is_moving_frontward = True

def turn_wheels(degree):
    global wheel_angle
    wheel_angle = 90 + degree + ajustement_angle_roues
    if wheel_angle > 180:
        wheel_angle = 180
    fw.turn(wheel_angle)

def turnStraight():
    turn_wheels(0)

def checkCallibration():
    turnStraight()
    bw.speed = 50
    time.sleep(5)
    bw.stop()


def check_max_and_min_speed():
    global currentspeed, MAX_SPEED
    if currentspeed > MAX_SPEED:
        currentspeed = MAX_SPEED
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
    currentspeed += 5
    check_max_and_min_speed()

def decelerate():
    global currentspeed

    currentspeed -= 1
    check_max_and_min_speed()

def move():
    global is_moving_frontward, currentspeed
    #print("is_lost:  ",lf.is_lost)
    if lf.is_lost:
        print("move back")
        move_back()
    else:

        if currentspeed != 0 and is_moving_frontward == False:
            stop()
            if currentspeed == 0:
                is_moving_frontward = True
        else:
            is_moving_frontward = True
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

def stop():
    global currentspeed
    currentspeed -= 20
    check_max_and_min_speed()
    if currentspeed == 0:
        bw.stop()
    else:
        bw.speed = currentspeed


def move_back():
    global currentspeed, is_moving_frontward
    #print("is moving_frontward  :", is_moving_frontward)
    if is_moving_frontward:
        print("ici")
        stop()
        if currentspeed ==0:
            is_moving_frontward = False
    else:
        print("no")
        currentspeed += 5
        check_max_and_min_speed()
        bw.forward()
        bw.speed = currentspeed


def move_frontward():
    global is_moving_frontward, currentspeed
    #print("is_lost:  ",lf.is_lost)
    if not is_moving_frontward:
        stop()
        if currentspeed == 0:
            is_moving_frontward = True
    else:
        bw.backward()
        accelerate()
        bw.speed = currentspeed