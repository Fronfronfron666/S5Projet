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


#if line_follower.MAX_SPEED == 80:
#    delai1 = 1
#    delai2 = delai1 + 1.2
#    delai3 = delai2 + 1
#
#    delai4 = delai3 + 1.8
#    delai5 = delai4 + 1.1
#    delai6 = delai5 + 0
#    delai7 = delai6 + 1.7

#elif line_follower.MAX_SPEED == 60:
#    delai1 = 1
#    delai2 = delai1 + 1.2
#    delai3 = delai2 + 1

#    delai4 = delai3 + 1.8
#    delai5 = delai4 + 1.1
#    delai6 = delai5 + 0
#    delai7 = delai6 + 1.7


delai1 = 2.4
delai2 = delai1 + 2

def dodge():
    global detection_time, flag

    line_follower.previous_sensor_state = [False, False, False, False, False]
    line_follower.previous_sensor_result = [False, False, False, False, False]

    time_since_detect = time.perf_counter() - detection_time
    print("time since detection:    ",time_since_detect)

    if time_since_detect <= delai1:
        mv.stop()
    elif time_since_detect <= delai2:
        mv.turn_wheels(0)
        mv.move_back()
    else:
        mv.stop()


#    elif time_since_detect <= delai7 and not line_follower.get_line_follower_result()[2]:
#        mv.move_frontward()
#        mv.turn_wheels(-45)
#        print("7")
#
#    elif not line_follower.get_line_follower_result()[0]:
#        print("8")
#        mv.move_frontward()
#        mv.turn_wheels(35)
#    else:
#        flag = False

truth_table = [0,0,0,0,0]

def manage_truth_table(value):
    global truth_table
    truth_table[4] = truth_table[3]
    truth_table[3] = truth_table[2]
    truth_table[4] = truth_table[1]
    truth_table[1] = truth_table[0]
    truth_table[1] = value


def process_picar(number, q):
    global detection_time, flag, truth_table
    last_range_value = 50
    try:
        while True:
            if q.empty() is False:
                value = q.get()
                manage_truth_table(value)
                print("truth_table  :", truth_table)
                #if value is not 0:
                    #last_range_value = value
            #print("last range value", last_range_value)

            if not flag:
                mv.turn_wheels(line_follower.get_turn_value(line_follower.get_line_follower_result()))
                mv.move_with_spin()

                if last_range_value == 1:
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
            range_value = us.less_than(3)
            manage_truth_table(range_value)
            print("new value    : ",range_value)
            print("truth_table  : ", truth_table)

            q.put(range_value)
    except KeyboardInterrupt:
        stop()


if __name__ == '__main__':
    q = multiprocessing.Manager().Queue()
    number = 0

    #p_picar = multiprocessing.Process(target=process_picar, args=(number, q))
    p_distance = multiprocessing.Process(target=process_sensor_distance, args=(number, q))
    #p_picar.start()
    p_distance.start()
    #p_picar.join()
    p_distance.join()
