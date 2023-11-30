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

counter = 0

if __name__ == '__main__':
    try:
        while True:
            counter += 1
            print(counter)
            if counter <= 49:
                #turn_value = line_follower.get_turn_value(line_follower.get_line_follower_result())
                mv.turn_wheels(0)
                mv.accelerate()
                mv.move_back_track_4()
                time.sleep(0.041)
            else:
                stop()

    except KeyboardInterrupt:
        stop()