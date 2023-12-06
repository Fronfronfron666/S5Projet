#!/usr/bin/env python
import numpy as np
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


if line_follower.can_spin:
    delai1 = 2.2
    delai2 = delai1 + 1.9
    delai3 = delai2 + 0.6
    delai4 = delai3 + 2.4
    delai5 = delai4 + 0.5
    delai6 = delai5 + 1
    delai7 = delai6 + 0.1
    delai8 = delai7 + 0.6
else:
    delai1 = 2.2
    delai2 = delai1 + 1.8#2.2
    delai3 = delai2 + 0.6
    delai4 = delai3 + 3
    delai5 = delai4 + 0.5
    delai6 = delai5 + 1.3
    delai7 = delai6 + 0.1
    delai8 = delai7 + 0.8


def dodge():
    global detection_time, flag

    line_follower.previous_sensor_state = [False, False, False, False, False]
    line_follower.previous_sensor_result = [False, False, False, False, False]

    time_since_detect = time.perf_counter() - detection_time

    if time_since_detect <= delai1:
        mv.stop()
    elif time_since_detect <= delai2:
        mv.turn_wheels(0)
        mv.move_back()
    elif  time_since_detect <= delai3:
        mv.stop()
        mv.turn_wheels(0)
    elif time_since_detect <= delai4:
        mv.turn_wheels(-35)
        mv.move_frontward()
    elif time_since_detect <= delai5:
        mv.turn_wheels(0)
        mv.move_frontward()
    elif time_since_detect <= delai6:
        mv.turn_wheels(45)
        mv.move_frontward()
    elif time_since_detect <= delai7:
        mv.turn_wheels(0)
        mv.move_frontward()
    elif time_since_detect <= delai8:
        mv.turn_wheels(45)
        mv.move_frontward()
    elif not line_follower.get_line_follower_result()[2]:
        mv.move_frontward()
        mv.turn_wheels(35)
    else:
        line_follower.last_range_value = 40
        flag = False

def process_picar(number, q):
    global detection_time, flag
    try:
        while True:
            if q.empty() is False:
                line_follower.last_range_value = q.get()

            if not flag:
                mv.turn_wheels(line_follower.get_turn_value(line_follower.get_line_follower_result()))
                mv.move_with_spin()

                if line_follower.can_spin:
                    if line_follower.last_range_value <= 18 and line_follower.currentspeed >= 35:
                        mv.stop()
                        detection_time = time.perf_counter()
                        mv.stop()
                        flag = True
                    elif line_follower.last_range_value <= 13:
                        mv.stop()
                        detection_time = time.perf_counter()
                        mv.stop()
                        flag = True
                else:
                    if line_follower.last_range_value <= 17 and line_follower.currentspeed >= 60:
                        mv.stop()
                        detection_time = time.perf_counter()
                        mv.stop()
                        flag = True
                    elif line_follower.last_range_value <= 12:
                        mv.stop()
                        detection_time = time.perf_counter()
                        mv.stop()
                        flag = True
            else:
                dodge()

    except KeyboardInterrupt:
        stop()

def process_sensor_distance(number, q):
    try:
        while True:
            range_value = us.get_ultrasonic_avoidance()
            print(range_value)
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
