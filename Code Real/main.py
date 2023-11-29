#!/usr/bin/env python
from picar import front_wheels
from picar import back_wheels
import time
import picar
import mouvement as mv
import ulrason
import line_follower

picar.setup()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels (db=' config')
#def start_bouge():
 #   print('Demarrage')
  #  fw.turn_straight() # Correspond a 90
   # bw.forward()
   # bw.speed = 70
   # time.sleep(5)
   # fw.turn(0)
   # bw.backward()
   # bw.speed = 20
   # time.sleep(5)
   # fw.turn(180)

#    bw.forward()
#    time.sleep(5)
#    fw.turn(90)  # tout droit
#    bw.forward()
#    bw.speed = 70
#    time.sleep(5)
#    bw.stop()

def stop():
    bw.stop()
    fw.turn_straight()

if __name__ == '__main__':
    try:
        while True:
            mv.turn_wheels(line_follower.get_turn_value(line_follower.get_line_follower_result()))
            #mv.turn_wheels(50)
            mv.accelerate()
            mv.move()
            time.sleep(0.041)

    except KeyboardInterrupt:
        stop()