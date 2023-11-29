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
    timeSinceDetect = 0.0
    try:
        while True:
            print(timeSinceDetect)
            if not flag:
                mv.turn_wheels(line_follower.get_turn_value(line_follower.get_line_follower_result()))
                mv.accelerate()
                mv.move()
                print(us.get_ultrasonic_avoidance())

            if us.get_ultrasonic_avoidance() <= 4 and not flag:
                flag = True
                stop()

            if flag:
                if timeSinceDetect <= .25:
                    print("AAA")
                    mv.move_back()
                elif timeSinceDetect <= .5:
                    print("BBB")
                    mv.move_back()
                    mv.turn_wheels(-55)
                elif timeSinceDetect <= 1.5:
                    print("CCC")
                    mv.move_frontward()
                    mv.turn_wheels(0)
                elif timeSinceDetect <= 2:
                    print("DDD")
                    mv.move_frontward()
                    mv.turn_wheels(-50)
                else:
                    flag = False




            time.sleep(timeFrame)

            if flag:
                timeSinceDetect += timeFrame
    except KeyboardInterrupt:
        stop()