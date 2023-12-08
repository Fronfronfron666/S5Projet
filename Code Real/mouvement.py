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
#lf.currentspeed = 0
wheel_angle = 0
is_moving_frontward = True

"""
Entrée: L'angle voulue
Sortie: L'angle que les roues devrait etre
Fonction: Assure que les roues ne change pas d'angle brusquement
"""
def get_new_turn_value_under_limit(target_angle):
    if lf.currentspeed <= 25:
        change_value = 8
    else:
        change_value = 1.5

    if wheel_angle - 90 - ajustement_angle_roues <= target_angle - change_value:
        return wheel_angle - 90 - ajustement_angle_roues + change_value
    elif wheel_angle - 90 - ajustement_angle_roues >= target_angle + change_value:
        return wheel_angle - 90 - ajustement_angle_roues - change_value
    return target_angle

"""
Entrée: Vitesse vise
Sortie: N/A
Fonction: Ralentie le robot jusqu'a l'arret
"""
def slow_down_to(target):
    if target <= lf.currentspeed:
        stop()
    else:
        lf.currentspeed = 10

"""
Entrée: Angle
Sortie: N/A
Fonction: Change l'angle des roues en prennent compte de l'angle d'ajustement (prend des angle de -90 a 90)
"""
def turn_wheels(degree):
    global wheel_angle
    wheel_angle = 90 + get_new_turn_value_under_limit(degree) + ajustement_angle_roues
    #print("int wheel_angle: ", get_new_turn_value_under_limit(degree))
    if wheel_angle > 180:
        wheel_angle = 180
    fw.turn(int(wheel_angle))

"""
Entrée: N/A
Sortie: N/A
Fonction: Met les roues droites en fonction de l'angle d'ajustement
"""
def turnStraight():
    turn_wheels(0+ ajustement_angle_roues)

"""
Entrée: N/A
Sortie: N/A
Fonction: Test la calibration des roues avants
"""
def checkCallibration():
    turnStraight()
    bw.speed = 50
    time.sleep(5)
    bw.stop()

"""
Entrée: N/A
Sortie: N/A
Fonction: Fait tournée seulement la roue droite pour tourner plus etroitement
"""
def spin_left():
    bw.left_wheel.stop()
    bw.right_wheel.backward()
    set_current_speed()

"""
Entrée: N/A
Sortie: N/A
Fonction: Fait tournée seulement la roue gauche pour tourner plus etroitement
"""
def spin_right():
    bw.left_wheel.backward()
    bw.right_wheel.stop()
    set_current_speed()

"""
Entrée: N/A
Sortie: N/A
Fonction: assure que le robot reste dans les bornes de vitesse maximum definie
"""
def check_max_and_min_speed():
    if lf.currentspeed > lf.MAX_SPEED:
        lf.currentspeed = lf.MAX_SPEED
    elif lf.currentspeed <= 0:
        lf.currentspeed = 0


"""
Entrée: N/A
Sortie: N/A
Fonction: Gestion de l'acceleration
"""
def accelerate():
    if lf.currentspeed == 0:
        lf.currentspeed = 20
    elif lf.currentspeed <= 40:
        lf.currentspeed += 0.15
    else:
        lf.currentspeed +=0.3
    check_max_and_min_speed()


"""
Entrée: N/A
Sortie: N/A
Fonction: Verifie si le robot avance, recule ou ne bouge pas
"""
def move():
    global is_moving_frontward
    #print("is_lost:  ",lf.is_lost)
    if not lf.is_stopped:
        if lf.is_lost:
            #print("move back")
            move_back()
        else:

            if lf.currentspeed != 0 and is_moving_frontward == False:
                stop()
                if lf.currentspeed == 0:
                    is_moving_frontward = True
            else:
                is_moving_frontward = True
                bw.backward()
                accelerate()
                set_current_speed()
    else:
        stop()

"""
Entrée: N/A
Sortie: N/A
Fonction: Permet au robot de tourner avec une seule roue selon le sens de la vitesse et de l'angle des roues
"""
def move_with_spin():
    global is_moving_frontward

    if not lf.is_stopped:
        if lf.is_lost:
            move_back()
        else:
            if lf.currentspeed != 0 and is_moving_frontward == False:
                stop_boucle()
                if lf.currentspeed == 0:
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
        final_stop()


"""
Entrée: N/A
Sortie: N/A
Fonction: Deplacement pour la track 4
"""
def move_back_track_4():
    if not lf.is_stopped:
        is_moving_frontward = False
        bw.forward()
        set_current_speed()

"""
Entrée: N/A
Sortie: N/A
Fonction: Arrete le robot en decelerant
"""
def stop():
    #print("current speed: ", lf.currentspeed)
    if lf.currentspeed <= 10:
        lf.currentspeed = 0
    elif lf.currentspeed <= 30:
        lf.currentspeed -= 0.3
    else:
        lf.currentspeed -= 0.3
    check_max_and_min_speed()
    set_current_speed()

"""
Entrée: N/A
Sortie: N/A
Fonction: Arrete le robot en decelerant
"""
def final_stop():
    if lf.currentspeed <= 25:
        lf.currentspeed = 0
    elif lf.currentspeed <= 40:
        lf.currentspeed -= 0.7
    else:
        lf.currentspeed -= 1
    check_max_and_min_speed()
    set_current_speed()

"""
Entrée: N/A
Sortie: N/A
Fonction: Arrete completement le robot
"""
def stop_boucle():

    while lf.currentspeed != 0:
        #print("current speed: ", lf.currentspeed)
        lf.currentspeed -= 0.5
        check_max_and_min_speed()
        set_current_speed()
    # if lf.currentspeed == 0:
    # bw.stop()

"""
Entrée: N/A
Sortie: N/A
Fonction: Fait reculer le robot
"""
def move_back():
    global is_moving_frontward
    #print("is moving_frontward  :", is_moving_frontward)
    if is_moving_frontward:
        #print("ici")
        stop()
        if lf.currentspeed == 0:
            is_moving_frontward = False
    else:
        #print("no")
        bw.forward()
        accelerate()
        set_current_speed()
        check_max_and_min_speed()

"""
Entrée: N/A
Sortie: N/A
Fonction: fait avancer le robot
"""
def move_frontward():
    global is_moving_frontward
    if not is_moving_frontward:
        stop()
        if lf.currentspeed == 0:
            is_moving_frontward = True
    else:
        bw.backward()
        accelerate()
        set_current_speed()
        check_max_and_min_speed()

"""
Entrée: N/A
Sortie: N/A
Fonction: Change la vitesse du robot
"""
def set_current_speed():
    new_speed = int(lf.currentspeed * get_turning_factor_on_speed_value())
    bw.speed = new_speed


"""
Entrée: N/A
Sortie: N/A
Fonction: fait avancer le robot
"""
def move_frontward():
    global is_moving_frontward
    if not is_moving_frontward:
        stop()
        if lf.currentspeed == 0:
            is_moving_frontward = True
    else:
        bw.backward()
        accelerate()
        set_current_speed()

"""
Entrée: N/A
Sortie: N/A
Fonction: Ralentie le robot selon l'angle des roues
"""
def get_turning_factor_on_speed_value():
    return 1 - (np.abs((wheel_angle - 90 - ajustement_angle_roues)/55)/2.75)