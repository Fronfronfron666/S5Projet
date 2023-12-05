#!/usr/bin/env python
from picar import front_wheels
from picar import back_wheels
import time
import picar
import mouvement as mv
import line_follower

picar.setup()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels (db=' config')

def stop():
    bw.stop()
    fw.turn_straight()

counter = 0


if __name__ == '__main__':

    try:
        while True:
            mv.turn_wheels(-45)
            time.sleep(2)
            mv.turn_wheels(45)
            time.sleep(2)
    except KeyboardInterrupt:
        stop()