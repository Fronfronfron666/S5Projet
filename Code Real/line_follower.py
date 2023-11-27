from SunFounder_Line_Follower import Line_Follower
import time

line_follower = Line_Follower.Line_Follower()
threshold = 100

def change_previous_sensor_result(line_sensor_results, previous_sensor_result, previous_sensor_state):
    data = line_sensor_results
    previous_result = previous_sensor_result
    previous_state = previous_sensor_state

    if previous_sensor_result != data:
        previous_state = previous_result
        previous_result = data
    return previous_result, previous_state

def get_turn_value(line_sensor_results, previous_sensor_result, previous_sensor_state):
    turn_value = 0
    previous_sensor_result, previous_sensor_state = change_previous_sensor_result(line_sensor_results, previous_sensor_result, previous_sensor_state)
    match line_sensor_results:
        case [False, False, False, False, False]:
            if previous_sensor_state == [True, False, False, False, False] or previous_sensor_state == [True, True, False, False, False]:
                turn_value = -45
            elif previous_sensor_state == [False, False, False, False, True] or previous_sensor_state == [False, False, False, True, True]:
                turn_value = 45
            else:  # perdu
                turn_value = 0

        case [True, True, True, True, True]:  # stop vehicle
            turn_value = 0
            stop(vehicle)
            stop_vehicle = True

        case [True, False, False, False, False]:
            if previous_sensor_state == [False, True, False, False, False] or previous_sensor_state == [True, True, False, False, False] or previous_sensor_state == [False, False, False, False, False]:
                turn_value = -30
            else:
                turn_value = 20

        case [False, False, False, False, True]:
            if previous_sensor_state == [False, False, False, True, False] or previous_sensor_state == [False, False, False, True, True] or previous_sensor_state == [False, False, False, False, False]:
                turn_value = 30
            else:
                turn_value = -20

        case [False, True, False, False, False]:
            if previous_sensor_state == [True, False, False, False, False]:
                turn_value = 5
            else:
                turn_value = -10

        case [False, False, False, True, False]:
            if previous_sensor_state == [False, False, False, False, True] or previous_sensor_state == [False, False, False, True, True]:
                turn_value = -5
            else:
                turn_value = 10

        case [False, False, True, False, False]:
            turn_value = 0

        case [False, True, True, False, False]:
            if previous_sensor_state == [False, True, False, False, False]:
                turn_value = -10
            else:
                turn_value = 10

        case [False, False, True, True, False]:
            if previous_sensor_state == [False, False, False, True, False]:
                turn_value = 10
            else:
                turn_value = -10

        case [True, True, False, False, False]:
            if previous_sensor_state == [True, False, False, False, False]:
                turn_value = -5
            else:
                turn_value = -12

        case [False, False, False, True, True]:
            if previous_sensor_state == [False, False, False, False, True]:
                turn_value = 5
            else:
                turn_value = 12
        case _:
            print("Comprends pas")
    return turn_value

def get_line_follower_result():
    line_sensor_result = line_follower.read_analog()
    for i in range(len(sensors)):
        if line_sensor_result[i] > threshold:
           line_sensor_result[i] = False
        else:
            line_sensor_result[i] = True
    return line_sensor_result