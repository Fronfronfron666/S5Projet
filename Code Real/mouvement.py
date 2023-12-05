#!/usr/bin/env python
import numpy as np
from picar import front_wheels
from picar import back_wheels
import time
import picar
import line_follower as lf


picar.setup()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels (db='config')

ajustement_angle_roues = 10
currentspeed = 0
wheel_angle = 0
is_moving_frontward = True

def get_new_turn_value_under_limit(limit):
    if currentspeed <= 10:
        change_value = 5
    else:
        change_value = 1

    if wheel_angle - 90 - ajustement_angle_roues <= limit - change_value:
        return wheel_angle - 90 - ajustement_angle_roues + change_value
    elif wheel_angle - 90 - ajustement_angle_roues >= limit + change_value:
        return wheel_angle - 90 - ajustement_angle_roues - change_value
    return limit

def turn_wheels(degree):
    global wheel_angle
    wheel_angle = 90 + int(get_new_turn_value_under_limit(degree)) + ajustement_angle_roues
    print("int wheel_angle: ", get_new_turn_value_under_limit(degree))
    if wheel_angle > 180:
        wheel_angle = 180
    fw.turn(wheel_angle)

def turnStraight():
    turn_wheels(0)

def checkCallibration():
    turnStraight()
    bw.speed = 50
    time.sleep(5)
    bw.stop()

def spin_left():
    bw.left_wheel.stop()
    bw.right_wheel.backward()
    set_current_speed()

def spin_right():
    bw.left_wheel.backward()
    bw.right_wheel.stop()
    set_current_speed()

def check_max_and_min_speed():
    global currentspeed
    if currentspeed > lf.MAX_SPEED:
        currentspeed = lf.MAX_SPEED
    elif currentspeed <= 0:
        currentspeed = 0


def accelerate():
    global currentspeed
    if currentspeed == 0:
        currentspeed = 5
    elif currentspeed <= 30:
        currentspeed += 0.15
    else:
        currentspeed +=0.5
    check_max_and_min_speed()


def move():
    global is_moving_frontward, currentspeed
    #print("is_lost:  ",lf.is_lost)
    if not lf.is_stopped:
        if lf.is_lost:
            print("move back")
            move_back()
        else:

            if currentspeed != 0 and is_moving_frontward == False:
                stop()
                if currentspeed == 0:
                    is_moving_frontward = True
            else:
                is_moving_frontward = True
                bw.backward()
                accelerate()
                set_current_speed()
    else:
        stop()

def move_with_spin():

    global is_moving_frontward, currentspeed
    print("is_lost:  ",lf.is_lost)
    print("is_moving Frontward:     ", is_moving_frontward)
    if not lf.is_stopped:
        if lf.is_lost:
            print("move back")
            move_back()
        else:
            if currentspeed != 0 and is_moving_frontward == False:
                stop_boucle()
                if currentspeed == 0:
                    is_moving_frontward = True
            else:
                is_moving_frontward = True
                if lf.is_spinning:
                    if lf.get_turn_value(lf.get_line_follower_result()) < 0:
                        spin_left()
                    else:
                        spin_right()
                else:
                    accelerate()
                    bw.backward()
                    set_current_speed()
    else:
        stop()


def move_back_track_4():
    if not lf.is_stopped:
        is_moving_frontward = False
        bw.forward()
        set_current_speed()


def stop():
    global currentspeed
    print("current speed: ", currentspeed)
    if currentspeed <= 10:
        currentspeed = 0
    elif currentspeed <= 30:
        currentspeed -= 0.3
    else:
        currentspeed -= 0.5
    check_max_and_min_speed()
    set_current_speed()


def stop_boucle():
    global currentspeed

    while currentspeed != 0:
        print("current speed: ", currentspeed)
        currentspeed -= 0.5
        check_max_and_min_speed()
        set_current_speed()
    # if currentspeed == 0:
    # bw.stop()

def move_back():
    global currentspeed, is_moving_frontward
    #print("is moving_frontward  :", is_moving_frontward)
    if is_moving_frontward:
        print("ici")
        stop()
        if currentspeed == 0:
            is_moving_frontward = False
    else:
        print("no")
        bw.forward()
        accelerate()
        set_current_speed()
        check_max_and_min_speed()


def move_frontward():
    global is_moving_frontward, currentspeed
    if not is_moving_frontward:
        stop()
        if currentspeed == 0:
            is_moving_frontward = True
    else:
        bw.backward()
        accelerate()
        set_current_speed()
        check_max_and_min_speed()


def set_current_speed():
    new_speed = int(currentspeed * get_turning_factor_on_speed_value())
    bw.speed = new_speed


def move_frontward():
    global is_moving_frontward, currentspeed
    if not is_moving_frontward:
        stop()
        if currentspeed == 0:
            is_moving_frontward = True
    else:
        bw.backward()
        accelerate()
        set_current_speed()


def get_turning_factor_on_speed_value():
    return 1 - (np.abs((wheel_angle - 90 - ajustement_angle_roues)/55)/4)