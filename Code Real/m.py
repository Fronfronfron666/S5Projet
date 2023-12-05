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


delai1 = 2.4
delai2 = delai1 + 2.2
delai3 = delai2 + 0.6
delai4 = delai3 + 2.7
delai5 = delai4 + 0
delai6 = delai5 + 1.3
delai7 = delai6 + 0
delai8 = delai7 + 1

def dodge():
    global detection_time, flag, last_range_value

    line_follower.previous_sensor_state = [False, False, False, False, False]
    line_follower.previous_sensor_result = [False, False, False, False, False]

    time_since_detect = time.perf_counter() - detection_time
    #print("time since detection:    ",time_since_detect)

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
        last_range_value = 40
        flag = False

last_range_value = 40

def process_picar(number, q):
    global detection_time, flag, last_range_value
    try:
        while True:
            if q.empty() is False:
                new_value = q.get()
                print("new value:   ", new_value)
                print("Last value:  ", last_range_value)
                if new_value < 1.25 * last_range_value or new_value > 0.75 * last_range_value:
                    last_range_value = new_value

            if not flag:
                mv.turn_wheels(line_follower.get_turn_value(line_follower.get_line_follower_result()))
                mv.move_with_spin()
                if last_range_value <= 13:
                    mv.stop()
                    detection_time = time.perf_counter()
                    mv.stop()
                    flag = True

                elif last_range_value <= 20:
                    mv.slow_down_to(15)
                elif last_range_value <= 38:
                    mv.slow_down_to(30)

            else:
                dodge()

    except KeyboardInterrupt:
        stop()

def process_sensor_distance(number, q):
    try:
        while True:
            range_value = us.get_ultrasonic_avoidance()
            print("range :  ", range_value)
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
