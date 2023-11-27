#!/usr/bin/env python
from picar import front_wheels
from picar import back_wheels
import time
import picar


picar.setup()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels (db='config')

def turnWheels(degree):
        fw.turn(90 + degree)

def turnStraight():
    fw.turn(97)

def checkCallibration():
    turnStraight()
    bw.speed = 50
    time.sleep(5)
    bw.stop()


def startFW(targetSpeed):
    for i in range(targetSpeed):
        bw.speed = i
        time.sleep(0.01)

    time.sleep(5)
    bw.stop()



def testFW():
    for i in range(180):
        print(i)