#!/usr/bin/env python
from picar import front_wheels
from picar import back_wheels
import time
import picar
import mouvement as mv
import ulrason
import line_follower

def stop():
    bw.stop()
    fw.turn_straight()

if __name__ == '__main__':
    try:
        while True:
            mv.turn_wheels(0)
            #mv.turn_wheels(50)
            mv.accelerate()
            mv.move_back()
            time.sleep(0.041)

    except KeyboardInterrupt:
        stop()