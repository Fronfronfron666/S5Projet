#!/usr/bin/env python
import keyboard
from picar import front_wheels
from picar import back_wheels
import time
import picar
import mouvement as mv
import ulrason
import line_follower

picar.setup()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels (db=' config')

def stop():
    bw.stop()
    fw.turn_straight()

if __name__ == '__main__':
    try:
        while True:
            if keyboard.is_pressed("w") and keyboard.is_pressed("s"):
                mv.stop()
            elif keyboard.is_pressed("w"):
                mv.accelerate()
                bw.forward()
            elif keyboard.is_pressed("s"):
                mv.accelerate()
                bw.backward()
            else:
                mv.stop()

            if keyboard.is_pressed("a") and keyboard.is_pressed("d"):
                mv.turn_wheels(0)
            elif keyboard.is_pressed("a"):
                mv.turn_wheels(-45)
            elif keyboard.is_pressed("d"):
                mv.turn_wheels(45)
            else:
                mv.turn_wheels(0)


    except KeyboardInterrupt:
        stop()