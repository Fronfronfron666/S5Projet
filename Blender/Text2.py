import bpy
import math
from mathutils import Euler
import numpy as np
from mathutils import Vector

collided = False
collision_frame = 0

def metersToCube(value):
    return value * 10/3

acceleration = metersToCube(0.01)
current_speed = 0
max_speed = metersToCube(0.1)

wheel_angle = 0


def stop(vehicule):
    global current_speed, max_speed, acceleration
    #print(current_speed)
    
    if current_speed < 0.002 and current_speed > -0.002:
        current_speed = 0
        
    elif current_speed > 0:
        current_speed -= acceleration
        
    elif current_speed < 0:
        current_speed += acceleration
        
    
        
    current_rotation_x = vehicule.rotation_euler.x
    
    vehicule.location.y -= math.cos(current_rotation_x) * current_speed
    vehicule.location.x -= math.sin(current_rotation_x) * current_speed

def moveForward(vehicule):
    global current_speed, max_speed, acceleration, wheel_angle
    
    if current_speed < max_speed:
        current_speed += acceleration
    else:
        current_speed = max_speed
    
    if(wheel_angle == 0):
        newAngle = 0
    else:
        turning_rad = 13.9/math.sin(wheel_angle) + 6.5/2
        C = 2 * np.pi * turning_rad
        newAngle = (current_speed/C)*2*np.pi
    
    #print(math.radians(newAngle))
    
    vehicule.rotation_euler.x += newAngle
    
    current_rotation_x = vehicule.rotation_euler.x
    
    vehicule.location.y -= math.cos(current_rotation_x) * current_speed
    vehicule.location.x -= math.sin(current_rotation_x) * current_speed

def moveBackward(vehicule):
    global current_speed, max_speed, acceleration, wheel_angle
    
    if current_speed > -max_speed:
        current_speed -= acceleration
    else:
        current_speed = -max_speed
        
    if(wheel_angle == 0):
        newAngle = 0
    else:
        turning_rad = 13.9/math.sin(wheel_angle) + 6.5/2
        C = 2 * np.pi * turning_rad
        newAngle = (current_speed/C)*2*np.pi
    
    vehicule.rotation_euler.x += newAngle
        
    current_rotation_x = vehicule.rotation_euler.x
    
    vehicule.location.y -= math.cos(current_rotation_x) * current_speed
    vehicule.location.x -= math.sin(current_rotation_x) * current_speed


def turn(angle):
    global wheel_angle
    wheel_angle = math.radians(angle)
    
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
            
def capteurUltrason():
    
    current_frame = bpy.context.scene.frame_current
    depsgraph1 = bpy.context.evaluated_depsgraph_get()
    capteur = bpy.data.objects['CapteurUltrason']
    direction_rayon = (0, -1, 0)
    longueur_rayon = 80
    
    capteur_matrix = capteur.matrix_world
    capteur_location = capteur_matrix.translation - Vector((0,capteur.dimensions.y,0))

   
    result, location, normal, index, object, matrix = bpy.context.scene.ray_cast(depsgraph1, capteur_location, direction_rayon, distance=longueur_rayon)

    distanceObstacle = (capteur_location.y-location.y)
    if result:
        
        return distanceObstacle
    
    else:
        return -1 
    
def getStopDistance():
    global current_speed, acceleration
    
    t = current_speed / acceleration
    
    x = current_speed*t + (1/2) * acceleration * t**2
    
    if capteurUltrason() != -1:
        if capteurUltrason() - 0.3 < x:
            return True
        else:
            return False
    
def obstacleInteraction(current_frame, vehicule):
    global collision_frame
    #print("in ob_int")
    if current_frame < collision_frame + 70:
        turn(-10)
        moveBackward(vehicule)
        
    elif current_frame < collision_frame + 85:
        stop(vehicule)
        
    elif current_frame < collision_frame + 140:
        turn(30)
        moveForward(vehicule) 
        
    elif current_frame < collision_frame + 300:
        turn(-20)
        moveForward(vehicule)
    
    elif current_frame < collision_frame + 325:
        turn(0)
        moveForward(vehicule)
        #Suiveur de ligne implementation
    
def main(scene):
    global current_speed, collided, collision_frame
    vehicule = bpy.context.scene.objects.get("Vehicule")
    
    #print(capteurUltrason())
    
    current_frame = scene.frame_current
    #print(wheel_angle)
    #moveForward(vehicule)
    print(math.sin(40))
    if collided == True:
        obstacleInteraction(current_frame, vehicule)
    
    elif getStopDistance() == True:
        stop(vehicule)
        if current_speed == 0:
            collided = True
            collision_frame = current_frame
    
    elif current_frame < 1000:
        moveForward(vehicule)
        
    else:
        stop(vehicule)

start(1)
bpy.app.handlers.frame_change_pre.append(main)

bpy.ops.screen.animation_play()


        