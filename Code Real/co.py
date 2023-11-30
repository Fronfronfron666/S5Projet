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

flag = True

if __name__ == '__main__':
    try:
        while True:
            if flag:
                mv.turn_wheels(100)
                flag = False
            else:
                mv.turn_wheels(0)

            time.sleep(0.041)

    except KeyboardInterrupt:
        stop()