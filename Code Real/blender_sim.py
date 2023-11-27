import bpy
import math
from mathutils import Euler
import numpy as np
from mathutils import Vector

collided = False
collision_frame = 0


def metersToCube(value):
    return value * 10 / 3


defaultBallPos = [0, 0, 0]
acceleration = metersToCube(0.05)
current_speed = 0
max_speed = metersToCube(0.1)
vehicule_a = ""
Forward_acceleration = False
wheel_angle = 0
case4 = False
stop_vehicle = False


def stop(vehicule):
    global current_speed, max_speed, acceleration, vehicule_a
    # print(current_speed)
    if np.abs(current_speed) - acceleration < 0:
        setBillePos("no_acceleration")
        current_speed = 0

    elif current_speed < 0.001 and current_speed > -0.001:
        current_speed = 0

    elif current_speed > 0:
        setBillePos("accelerating_minus")
        current_speed -= acceleration

    elif current_speed < 0:
        setBillePos("accelerating_plus")
        current_speed += acceleration

    current_rotation_x = vehicule.rotation_euler.x

    vehicule.location.y -= math.cos(current_rotation_x) * current_speed
    vehicule.location.x -= math.sin(current_rotation_x) * current_speed


def moveForward(vehicule):
    global current_speed, max_speed, acceleration, wheel_angle, vehicule_a, Forward_acceleration

    if current_speed < max_speed and current_speed >= 0 and Forward_acceleration == False:
        setBillePos("accelerating_plus")
        current_speed += acceleration
    elif Forward_acceleration == True:
        print("rien")
    else:
        setBillePos("no_acceleration")
        current_speed = max_speed

    if (wheel_angle == 0):
        newAngle = 0
    else:
        turning_rad = 13.9 / math.sin(wheel_angle) + 6.5 / 2
        C = 2 * np.pi * turning_rad
        newAngle = (current_speed / C) * 2 * np.pi

    vehicule.rotation_euler.x += newAngle

    current_rotation_x = vehicule.rotation_euler.x

    vehicule.location.y -= math.cos(current_rotation_x) * current_speed
    vehicule.location.x -= math.sin(current_rotation_x) * current_speed


def moveBackward(vehicule):
    global current_speed, max_speed, acceleration, wheel_angle, vehicule_a

    if current_speed > -max_speed:
        setBillePos("accelerating_minus")
        current_speed -= acceleration
    else:
        setBillePos("no_acceleration")
        current_speed = -max_speed

    if (wheel_angle == 0):
        newAngle = 0
    else:
        turning_rad = 13.9 / math.sin(wheel_angle) + 6.5 / 2
        C = 2 * np.pi * turning_rad
        newAngle = (current_speed / C) * 2 * np.pi

    vehicule.rotation_euler.x += newAngle

    current_rotation_x = vehicule.rotation_euler.x

    vehicule.location.y -= math.cos(current_rotation_x) * current_speed
    vehicule.location.x -= math.sin(current_rotation_x) * current_speed


def turn(angle):
    global wheel_angle
    wheel_angle = math.radians(angle)
    print(angle, "     ", wheel_angle)


def start(position):
    global case4
    vehicule = bpy.context.scene.objects.get("Vehicule")
    sphere = bpy.context.scene.objects.get("Sphere")

    sphere.location.y = -8.11

    vehicule.location.y = 0
    vehicule.rotation_euler.x = 0
    vehicule.rotation_euler.x = 0

    match position:
        case 1:
            vehicule.location.x = 0
            case4 = False
        case 2:
            vehicule.location.x = -90
            case4 = False
        case 3:
            vehicule.location.x = -150
            case4 = False
        case 4:
            vehicule.location.x = -210
            vehicule.location.y = -7.5
            case4 = True


def capteurUltrason():
    current_frame = bpy.context.scene.frame_current
    depsgraph1 = bpy.context.evaluated_depsgraph_get()
    capteur = bpy.data.objects['CapteurUltrason']
    direction_rayon = (0, -1, 0)
    longueur_rayon = 80

    capteur_matrix = capteur.matrix_world
    capteur_location = capteur_matrix.translation - Vector((0, capteur.dimensions.y, 0))

    result, location, normal, index, object, matrix = bpy.context.scene.ray_cast(depsgraph1, capteur_location,
                                                                                 direction_rayon,
                                                                                 distance=longueur_rayon)

    distanceObstacle = (capteur_location.y - location.y)
    if result:

        return distanceObstacle

    else:
        return -1


def getStopDistance():
    global current_speed, acceleration

    t = current_speed / acceleration

    x = current_speed * t + (1 / 2) * acceleration * t ** 2

    if capteurUltrason() != -1:
        if capteurUltrason() - 0.3 < x:
            return True
        else:
            return False


def obstacleInteraction(current_frame, vehicule):
    global collision_frame, collided
    # print("in ob_int")
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

    else:  # current_frame < collision_frame + 325:
        collided = False
        collision_frame = 0
        # Suiveur de ligne implementation


def setBillePos(acceleration):
    global current_speed, defaultBallPos, max_speed, vehicule_a
    ball = bpy.context.scene.objects.get("Sphere")

    match acceleration:
        case "no_acceleration":
            # print(defaultBallPos)
            ball.location = [0.0000, -8.1100, 7.2714]

        case "accelerating_minus":
            newLocation = getBall(True)
            ball.location.y = newLocation[1]
            ball.location.x = newLocation[0]
            ball.location.z = newLocation[2]

        case "accelerating_plus":
            newLocation = getBall(False)
            ball.location.y = newLocation[1]
            ball.location.x = newLocation[0]
            ball.location.z = newLocation[2]


def getBall(minus):
    global current_speed, defaultBallPos
    y = (1 / 2 * current_speed ** 2) / 9.81
    x = np.sqrt(140 ** 2 - (140 - np.abs(y)) ** 2)

    newBallPos = [0, 0, 0]

    if minus == True:
        x = -x

    newBallPos[0] = defaultBallPos[0] + 0
    newBallPos[1] = defaultBallPos[1] + x
    newBallPos[2] = defaultBallPos[2] + y

    return newBallPos


######## Cod added from Zach  #############


def get_line_sensor_results():
    depsgraph_line_sensor = bpy.context.evaluated_depsgraph_get()

    line_sensors = [bpy.data.objects['sensor.000'], bpy.data.objects['sensor.001'], bpy.data.objects['sensor.002'],
                    bpy.data.objects['sensor.003'], bpy.data.objects['sensor.004']]

    line_sensor_matrixes = [line_sensors[0].matrix_world, line_sensors[1].matrix_world, line_sensors[2].matrix_world,
                            line_sensors[3].matrix_world, line_sensors[4].matrix_world]

    line_sensor_translations_lower_z = [
        line_sensor_matrixes[0].translation - Vector((0, 0, line_sensors[0].dimensions.z)),
        line_sensor_matrixes[1].translation - Vector((0, 0, line_sensors[1].dimensions.z)),
        line_sensor_matrixes[2].translation - Vector((0, 0, line_sensors[2].dimensions.z)),
        line_sensor_matrixes[3].translation - Vector((0, 0, line_sensors[3].dimensions.z)),
        line_sensor_matrixes[4].translation - Vector((0, 0, line_sensors[4].dimensions.z))]

    direction_rayon_line_sensor = (0, 0, -1)
    longeur_rayon_line_sensor = 4

    results = np.empty(5, dtype=object)
    results_locations = np.empty(5, dtype=object)
    results_normals = np.empty(5, dtype=object)
    results_indexes = np.empty(5, dtype=object)
    results_objects = np.empty(5, dtype=object)
    results_matrixes = np.empty(5, dtype=object)

    for sensor_index in range(5):
        results[sensor_index], results_locations[sensor_index], results_normals[sensor_index], results_indexes[
            sensor_index], results_objects[sensor_index], results_matrixes[sensor_index] = bpy.context.scene.ray_cast(
            depsgraph_line_sensor, line_sensor_translations_lower_z[sensor_index], direction_rayon_line_sensor,
            distance=longeur_rayon_line_sensor)

    print(results)
    # print(results_locations)

    return results


previous_sensor_result = [False, False, False, False, False]
previous_sensor_state = [False, False, False, False, False]


def convert_sensor_result_to_bool(line_sensor_results):
    result = [False, False, False, False, False]
    if line_sensor_results[0]:
        result[0] = True
    if line_sensor_results[1]:
        result[1] = True
    if line_sensor_results[2]:
        result[2] = True
    if line_sensor_results[3]:
        result[3] = True
    if line_sensor_results[4]:
        result[4] = True
    return result


def follow_line(line_sensor_results, vehicle):
    global previous_sensor_state, previous_sensor_result, stop_vehicle

    result = convert_sensor_result_to_bool(line_sensor_results)

    change_previous_sensor_result(result)

    match result:
        case [False, False, False, False, False]:
            if previous_sensor_state == [True, False, False, False, False] or previous_sensor_state == [True, True,
                                                                                                        False, False,
                                                                                                        False]:
                turn(-45)
            elif previous_sensor_state == [False, False, False, False, True] or previous_sensor_state == [False, False,
                                                                                                          False, True,
                                                                                                          True]:
                turn(45)
            # elif previous_sensor_state == [False, False, False, False, False] and
            else:  # perdu
                turn(0)

        case [True, True, True, True, True]:  # stop vehicle
            turn(0)
            stop(vehicle)
            stop_vehicle = True

        case [True, False, False, False, False]:
            if previous_sensor_state == [False, True, False, False, False] or previous_sensor_state == [True, True,
                                                                                                        False, False,
                                                                                                        False] or previous_sensor_state == [
                False, False, False, False, False]:
                turn(-30)
            else:
                turn(20)
        case [False, False, False, False, True]:
            if previous_sensor_state == [False, False, False, True, False] or previous_sensor_state == [False, False,
                                                                                                        False, True,
                                                                                                        True] or previous_sensor_state == [
                False, False, False, False, False]:
                turn(30)
            else:
                turn(-20)

        case [False, True, False, False, False]:
            if previous_sensor_state == [True, False, False, False, False]:
                turn(5)
                # elif previous_sensor_state == [False, False, True, False, False]:
                # turn(-10)
            else:
                turn(-10)
        case [False, False, False, True, False]:
            if previous_sensor_state == [False, False, False, False, True] or previous_sensor_state == [False, False,
                                                                                                        False, True,
                                                                                                        True]:
                turn(-5)
                # elif previous_sensor_state == [False, False, True, False, False]:
                # turn(10)
            else:
                turn(10)
        case [False, False, True, False, False]:
            turn(0)

        case [False, True, True, False, False]:
            if previous_sensor_state == [False, True, False, False, False]:
                turn(-10)
            else:
                turn(10)

        case [False, False, True, True, False]:
            if previous_sensor_state == [False, False, False, True, False]:
                turn(10)
            else:
                turn(-10)

        case [True, True, False, False, False]:
            if previous_sensor_state == [True, False, False, False, False]:
                turn(-5)
            else:
                turn(-12)

        case [False, False, False, True, True]:
            if previous_sensor_state == [False, False, False, False, True]:
                turn(5)
            else:
                turn(12)
        case _:
            print("Comprends pas")
            # turn(0)

    moveForward(vehicle)
    return


def change_previous_sensor_result(data):
    global previous_sensor_result, previous_sensor_state

    if previous_sensor_result != data:
        previous_sensor_state = previous_sensor_result
        previous_sensor_result = data

    return


######## Code  added from Zach fin #############
def track1(vehicule, current_frame):
    global current_speed, collided, collision_frame, Forward_acceleration
    vehicule = bpy.context.scene.objects.get("Vehicule")

    if collided == True:
        obstacleInteraction(current_frame, vehicule)

    elif getStopDistance() == True:
        Forward_acceleration = True
        stop(vehicule)
        if current_speed == 0:
            collided = True
            collision_frame = current_frame
            Forward_acceleration = False
    elif stop_vehicle == False:
        track2(vehicule, current_frame)
    else:
        stop(vehicule)


def track2(vehicule, current_frame):
    line_sensor_results = get_line_sensor_results()
    collision_sensor_result = False
    follow_line(line_sensor_results, vehicule)


def track4(vehicule, current_frame):
    if current_frame < 50:
        stop(vehicule)
    elif current_frame < 150:
        moveForward(vehicule)
    elif current_frame < 170:
        stop(vehicule)
    elif current_frame < 270:
        moveBackward(vehicule)
    else:
        stop(vehicule)
    return


def main(scene):
    global current_speed, case4
    vehicule = bpy.context.scene.objects.get("Vehicule")
    if stop_vehicle == False:
        # print(capteurUltrason())

        current_frame = scene.frame_current

        if case4 == True:
            track4(vehicule, current_frame)
        else:
            track1(vehicule, current_frame)


start(4)
defaultBallPos = [0.0000, -8.1100, 7.2714]
bpy.app.handlers.frame_change_pre.append(main)

bpy.ops.screen.animation_play()


