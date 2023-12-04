#!/usr/bin/env python
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
            mv.turn_wheels(0)
            bw.forward()
            mv.accelerate()
            mv.set_current_speed()
            mv.check_max_and_min_speed()
            time.sleep(0.041)

    except KeyboardInterrupt:
        stop()