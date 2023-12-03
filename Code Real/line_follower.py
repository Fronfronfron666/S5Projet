from SunFounder_Line_Follower import Line_Follower
import mouvement as mv

line_follower = Line_Follower.Line_Follower()
threshold = 100
previous_sensor_result = [False, False, False, False, False]
previous_sensor_state = [False, False, False, False, False]
current_wheel_angle = 0
lost_counter = 0
is_lost = False
is_stopped = False
is_spinning = False

def change_previous_sensor_result(line_sensor_results, previous_sensor_result, previous_sensor_state):
    data = line_sensor_results
    previous_result = previous_sensor_result
    previous_state = previous_sensor_state

    if previous_sensor_result != line_sensor_results:
        previous_state = previous_result
        previous_result = data

    return previous_result, previous_state

def find_line():
    turn_limit = 0
    if previous_sensor_state == [True, False, False, False, False] or previous_sensor_state == [True, True, False, False, False]:
        turn_limit = 55
    elif previous_sensor_state == [False, False, False, False, True] or previous_sensor_state == [False, False, False, True, True]:
        turn_limit = -55
    return turn_limit


def get_new_turn_value_under_limit(limit):
    change_value = 1
    if current_wheel_angle < limit - change_value:
        return current_wheel_angle + change_value
    elif current_wheel_angle > limit + change_value:
        return current_wheel_angle - change_value
    return limit


def get_turn_value(line_sensor_results):
    global is_spinning, previous_sensor_result, previous_sensor_state, stop_vehicle, current_wheel_angle, lost_counter, is_lost, is_stopped
    turn_limit = 0
    previous_sensor_result, previous_sensor_state = change_previous_sensor_result(line_sensor_results, previous_sensor_result, previous_sensor_state)

    print("line_sensor_result       :", line_sensor_results)
    print("previous_sensor_result   :", previous_sensor_result)
    print("previous_sensor_state    :", previous_sensor_state)
    is_spinning = False
    if line_sensor_results == [False, False, False, False, False]:

        if previous_sensor_state == [True, False, False, False, False] or previous_sensor_state == [True, True, False, False, False]:
            if lost_counter < 550:
                turn_limit = -55
                is_spinning = True
            else:
                is_lost = True
                turn_limit = find_line()

        elif previous_sensor_state == [False, False, False, False, True] or previous_sensor_state == [False, False, False, True, True]:
            if lost_counter < 550:
                turn_limit = 55
                is_spinning = True
            else:
                is_lost = True
                turn_limit = find_line()
        else:  # perdu
            turn_limit = 0
        lost_counter += 1

    else:
        lost_counter = 0
        is_lost = False
        if line_sensor_results == [True, True, True, True, True] and previous_sensor_state != [False, False, False, False, False]:  # stop vehicle
            turn_limit = 0
            mv.stop()
            is_stopped = True

        elif line_sensor_results == [True, False, False, False, False]:
            if previous_sensor_state == [False, True, False, False, False] or previous_sensor_state == [True, True, False, False, False] or previous_sensor_state == [False, False, False, False, False]:
                turn_limit = -40
            else:
                turn_limit = 20

        elif line_sensor_results == [False, False, False, False, True]:
            if previous_sensor_state == [False, False, False, True, False] or previous_sensor_state == [False, False, False, True, True] or previous_sensor_state == [False, False, False, False, False]:
                turn_limit = 40
            else:
                turn_limit = -20

        elif line_sensor_results == [False, True, False, False, False]:
            if previous_sensor_state == [True, False, False, False, False]:
                turn_limit = 5
            else:
                turn_limit = -10

        elif line_sensor_results == [False, False, False, True, False]:
            if previous_sensor_state == [False, False, False, False, True] or previous_sensor_state == [False, False, False, True, True]:
                turn_limit = -5
            else:
                turn_limit = 10

        elif line_sensor_results == [False, False, True, False, False]:
            turn_limit = 0

        elif line_sensor_results == [False, True, True, False, False]:
            if previous_sensor_state == [False, True, False, False, False]:
                turn_limit = -10
            else:
                turn_limit = 10

        elif line_sensor_results == [False, False, True, True, False]:
            if previous_sensor_state == [False, False, False, True, False]:
                turn_limit = 10
            else:
                turn_limit = -10

        elif line_sensor_results == [True, True, False, False, False]:
            if previous_sensor_state == [True, False, False, False, False]:
                turn_limit = -5
            else:
                turn_limit = -12

        elif line_sensor_results == [False, False, False, True, True]:
            if previous_sensor_state == [False, False, False, False, True]:
                turn_limit = 5
            else:
                turn_limit = 12
        else:
            print("Comprends pas")

    new_angle = get_new_turn_value_under_limit(turn_limit)
    current_wheel_angle = new_angle
    return new_angle


def get_line_follower_result():
    line_sensor_result = line_follower.read_analog()
    for i in range(len(line_sensor_result)):
        if line_sensor_result[i] > threshold:
            line_sensor_result[i] = False
        else:
            line_sensor_result[i] = True
    return line_sensor_result
