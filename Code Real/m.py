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
bw = back_wheels.Back_Wheels (db=' config')

def stop():
    bw.stop()
    fw.turn_straight()

counter = 0



def process_picar(q):
    last_range_value = 0
    while True:
        mv.turn_wheels(line_follower.get_turn_value(line_follower.get_line_follower_result()))
        #mv.turn_wheels(50)
        mv.accelerate()
        #mv.move()
        mv.move_with_spin()
        time.sleep(0.041)
        if q.empty() is not False:
            last_range_value = q.get()
        print("last range value", last_range_value)


def process_sensor_distance(q):
    while True:
        range_value = us.get_ultrasonic_avoidance()
        print("got range:   ", range_value)
        q.put(range_value)


if __name__ == '__main__':
    q = multiprocessing.Queue()
    try:
        p_picar = multiprocessing.Process(target=process_picar, args=(q))
        p_distance = multiprocessing.Process(target=process_sensor_distance, args=(q))
        p_picar.start()
        p_distance.start()
        p_picar.join()
        p_distance.join()
    except KeyboardInterrupt:
        stop()