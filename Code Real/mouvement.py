#!/usr/bin/env python
from picar import front_wheels
from picar import back_wheels
import time
import picar


picar.setup()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels (db='config')

ajustement_angle_roues = 7
currentspeed = 0
maxspeed = 30

def turn_wheels(degree):
    angle = 90 + degree + ajustement_angle_roues
    if angle > 180:
        angle = 180
    fw.turn(angle)

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

def accelerate():
    global currentspeed

    currentspeed += 1
    check_max_and_min_speed()

def decelerate():
    global currentspeed

    currentspeed -= 1
    check_max_and_min_speed()

def move():
    bw.forward()
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