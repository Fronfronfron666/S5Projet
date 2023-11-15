import bpy
import math
from mathutils import Euler
import numpy as np

#collided = False
#collision_frame = 0

def metersToCube(value):
    return value * 10/3

acceleration = metersToCube(0.01)
current_speed = 0
max_speed = metersToCube(0.1)

wheel_angle = 0


def stop(vehicule):
    global current_speed, max_speed, acceleration
    print(current_speed)
    if current_speed > 0:
        current_speed -= acceleration
        
    elif current_speed < 0:
        current_speed += acceleration
        
    else:
        current_speed = 0
        
    current_rotation_x = vehicule.rotation_euler.x
    
    vehicule.location.y -= math.cos(current_rotation_x) * current_speed
    vehicule.location.x -= math.sin(current_rotation_x) * current_speed

def moveForward(vehicule):
    global current_speed, max_speed, acceleration
    
    if current_speed < max_speed:
        current_speed += acceleration
    else:
        current_speed = max_speed
    
    if(wheel_angle == 0):
        newAngle = 0
    else:
        turning_rad = 13.9/math.sin(wheel_angle) + 6.5/2
        C = 2 * np.pi * turning_rad
        newAngle = (current_speed/C)*360
    
    vehicule.rotation_euler.x += math.radians(newAngle)
    
    current_rotation_x = vehicule.rotation_euler.x
    
    vehicule.location.y -= math.cos(current_rotation_x) * current_speed
    vehicule.location.x -= math.sin(current_rotation_x) * current_speed

def moveBackward(vehicule):
    global current_speed, max_speed, acceleration
    
    if current_speed > -max_speed:
        current_speed -= acceleration
    else:
        current_speed = -max_speed
        
    if(wheel_angle == 0):
        newAngle = 0
    else:
        turning_rad = 13.9/math.sin(wheel_angle) + 6.5/2
        C = 2 * np.pi * turning_rad
        newAngle = (current_speed/C)*360
    
    vehicule.rotation_euler.x += math.radians(newAngle)
        
    current_rotation_x = vehicule.rotation_euler.x
    
    vehicule.location.y -= math.cos(current_rotation_x) * current_speed
    vehicule.location.x -= math.sin(current_rotation_x) * current_speed


def turn(vehicule, angle):
    global wheel_angle
    wheel_angle = -angle
    
def start(position):
    
    vehicule = bpy.context.scene.objects.get("Vehicule")
    vehicule.location.y = 0
    vehicule.rotation_euler.x = 0
    vehicule.rotation_euler.x = 0
    
    match position:    
        case 1:
            vehicule.location.x = 0
        case 2:
            vehicule.location.x = -102.5
        case 3:
            vehicule.location.x = -175
        case 4:
            vehicule.location.x = -225
    
def main(scene):
    global current_speed
    vehicule = bpy.context.scene.objects.get("Vehicule")
    
    print(current_speed)
    
    current_frame = scene.frame_current
    
    #moveForward(vehicule)
    if current_frame < 1000:
        moveForward(vehicule)
        turn(vehicule, 30)
    else:
        stop(vehicule)
        #moveBackward(vehicule)
        #moveBackward(vehicule)
        #turn(vehicule, 0)

start(1)
bpy.app.handlers.frame_change_pre.append(main)

bpy.ops.screen.animation_play()
