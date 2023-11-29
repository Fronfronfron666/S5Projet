#!/usr/bin/env python
from picar import front_wheels
from picar import back_wheels
import time
import picar
import mouvement as mv
import ulrason as us
import line_follower

picar.setup()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels (db=' config')
timeFrame = 0.041

def stop():
    bw.stop()
    fw.turn_straight()


if __name__ == '__main__':
    flag = False
    timeSinceDetect = 0
    try:
        while True:
            print(us.get_ultrasonic_avoidance())
            if not flag:
                mv.turn_wheels(line_follower.get_turn_value(line_follower.get_line_follower_result()))
                mv.accelerate()
                mv.move()

            if us.get_ultrasonic_avoidance() == 1:
                flag = True
                stop()

            if flag:
                if timeSinceDetect <= 2:
                    mv.move_back()
                elif timeSinceDetect <= 3:
                    mv.move_back()
                    mv.turn_wheels(-55)
                elif timeSinceDetect <= 6:
                    mv.move()
                    mv.turn_wheels(0)
                elif timeSinceDetect <= 10:
                    mv.move()
                    mv.turn_wheels(-55)




            time.sleep(timeFrame)

            if flag:
                timeSinceDetect += timeFrame
    except KeyboardInterrupt:
        stop()