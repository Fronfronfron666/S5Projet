#!/usr/bin/env python
from picar import front_wheels
from picar import back_wheels
import time
import picar
import mouvement as mv
import ulrason as us
import line_follower
import multiprocessing

picar.setup()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db=' config')

flag = False
detection_time = time.perf_counter()
counter = 0


def stop():
    bw.stop()
    fw.turn_straight()


def dodge():
    global detection_time, flag
    time_since_detect = time.perf_counter() - detection_time
    print("time since detection:    ",time_since_detect)
    if time_since_detect <= 0.25:
        mv.stop()
    elif time_since_detect <= 1.4:
        mv.move_back()
        mv.turn_wheels(-55)
    elif time_since_detect <= 3.6:
        mv.move_frontward()
        mv.turn_wheels(0)
    elif time_since_detect <= 4.3:
        mv.move_frontward()
        mv.turn_wheels(-50)
    elif time_since_detect <= 5.2:
        mv.move_frontward()
        mv.turn_wheels(-50)
    elif time_since_detect > 5.2:
        line_follower.previous_sensor_state = [False, False, False, False, False]
        line_follower.previous_sensor_result = [False, False, False, False, False]
        flag = False
        timeSinceDetect = 0.0
        timeSinceDetect += timeSinceDetect - time.perf_counter()


def process_picar(number, q):
    global detection_time, flag
    last_range_value = 50
    try:
        while True:
            if not flag:
                mv.turn_wheels(line_follower.get_turn_value(line_follower.get_line_follower_result()))
                mv.accelerate()
                mv.move_with_spin()

                if q.empty() is False:
                    last_range_value = q.get()
                print("last range value", last_range_value)

                if last_range_value <= 3:
                    stop()
                    flag = True
            else:
                print("Dodging")
                dodge()
    except KeyboardInterrupt:
        stop()

def process_sensor_distance(number, q):
    try:
        while True:
            range_value = us.get_ultrasonic_avoidance()
            #print("got range:   ", range_value)
            q.put(range_value)
    except KeyboardInterrupt:
        stop()


if __name__ == '__main__':
    q = multiprocessing.Manager().Queue()
    number = 0

    p_picar = multiprocessing.Process(target=process_picar, args=(number, q))
    p_distance = multiprocessing.Process(target=process_sensor_distance, args=(number, q))
    p_picar.start()
    p_distance.start()
    p_picar.join()
    p_distance.join()
