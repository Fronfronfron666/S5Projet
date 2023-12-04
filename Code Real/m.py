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


#pour MAX_SPEED = 80
delai1 = 1
delai2 = delai1 + 1.2
delai3 = delai2 + 1

delai4 = delai3 + 1.8
delai5 = delai4 + 1.1
delai6 = delai5 + 0
delai7 = delai6 + 1.7

def dodge():
    global detection_time, flag

    line_follower.previous_sensor_state = [False, False, False, False, False]
    line_follower.previous_sensor_result = [False, False, False, False, False]

    time_since_detect = time.perf_counter() - detection_time
    print("time since detection:    ",time_since_detect)
    if time_since_detect <= delai1:
        mv.move_back()
        print("1")

    elif time_since_detect <= delai2:
        mv.move_back()
        mv.turn_wheels(-55)
        print("2")

    elif time_since_detect <= delai3:
        mv.stop()
        print("3")

    elif time_since_detect <= delai4:
        mv.move_frontward()
        mv.turn_wheels(0)
        print("4")
    elif time_since_detect <= delai5:
        mv.move_frontward()
        mv.turn_wheels(-55)
        print("5")

    elif time_since_detect <= delai6:
        mv.move_frontward()
        mv.turn_wheels(0)
        print("6")

    elif time_since_detect <= delai7 and not line_follower.get_line_follower_result()[2]:
        mv.move_frontward()
        mv.turn_wheels(-45)
        print("7")

    elif not line_follower.get_line_follower_result()[4]:
        print("8")
        mv.move_frontward()
        mv.turn_wheels(35)
    else:
        flag = False


def process_picar(number, q):
    global detection_time, flag
    last_range_value = 50
    try:
        while True:
            if q.empty() is False:
                value = q.get()
                if value is not 0:
                    last_range_value = value
            print("last range value", last_range_value)

            if not flag:
                mv.turn_wheels(line_follower.get_turn_value(line_follower.get_line_follower_result()))
                mv.move_with_spin()

                if last_range_value <= 4:
                    last_range_value = 50
                    detection_time = time.perf_counter()
                    mv.stop()
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
