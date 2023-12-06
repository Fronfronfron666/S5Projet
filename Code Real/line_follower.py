from SunFounder_Line_Follower import Line_Follower
import mouvement as mv
import settings

line_follower = Line_Follower.Line_Follower()
threshold = 100
previous_sensor_result = [False, False, False, False, False]
previous_sensor_state = [False, False, False, False, False]
lost_counter = 0
currentspeed = 0
is_lost = False
is_getting_lost = False
is_stopped = False
is_spinning = False

can_spin = settings.can_spin
never_lost = settings.never_lost

if can_spin:
    MAX_SPEED = 100
else:
    MAX_SPEED = 80
last_range_value = 100


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
    if previous_sensor_state == [True, False, False, False, False] or previous_sensor_state == [True, True, False,
                                                                                                False, False]:
        turn_limit = 55
    elif previous_sensor_state == [False, False, False, False, True] or previous_sensor_state == [False, False, False,
                                                                                                  True, True]:
        turn_limit = -55
    return turn_limit


def get_turn_value(line_sensor_results):
    global is_getting_lost, is_spinning, previous_sensor_result, previous_sensor_state, stop_vehicle, current_wheel_angle, lost_counter, is_lost, is_stopped
    print(line_sensor_results)
    if can_spin:
        if currentspeed <= 30:
            lost_counter_threshhold = 180
        else:
            lost_counter_threshhold = 350
    else:
        if currentspeed <= 30:
            lost_counter_threshhold = 260
        else:
            lost_counter_threshhold = 120

    turn_limit = 0
    previous_sensor_result, previous_sensor_state = change_previous_sensor_result(line_sensor_results,
                                                                                  previous_sensor_result,
                                                                                  previous_sensor_state)

    is_spinning = False

    if not is_stopped:
        if line_sensor_results == [False, False, False, False, False]:

            if previous_sensor_state == [True, False, False, False, False] or previous_sensor_state == [True, True,
                                                                                                        False, False,
                                                                                                        False]:
                if lost_counter < lost_counter_threshhold:
                    turn_limit = -55
                    is_getting_lost = True
                    if can_spin:
                        is_spinning = True
                else:
                    if not never_lost:
                        is_lost = True
                        is_getting_lost = False
                    if mv.is_moving_frontward:
                        turn_limit = -55
                    else:
                        turn_limit = find_line()

            elif previous_sensor_state == [False, False, False, False, True] or previous_sensor_state == [False, False,
                                                                                                          False, True,
                                                                                                          True]:
                if lost_counter < lost_counter_threshhold:
                    turn_limit = 55
                    if can_spin:
                        is_spinning = True
                else:
                    if not never_lost:
                        is_lost = True
                    if mv.is_moving_frontward:
                        turn_limit = 55
                    else:
                        turn_limit = find_line()
            else:  # perdu
                turn_limit = 0
            lost_counter += 1

        else:
            lost_counter = 0
            is_lost = False
            if line_sensor_results == [True, True, True, True, True] and previous_sensor_state != [False, False, False,
                                                                                                       False,
                                                                                                       False]:  # stop vehicle
                turn_limit = 0
                is_stopped = True

            elif line_sensor_results == [True, False, False, False, False]:
                if previous_sensor_state == [False, True, False, False, False] or previous_sensor_state == [True, True,
                                                                                                                False,
                                                                                                                False,
                                                                                                                False] or previous_sensor_state == [
                                                                                                                False, False, False, False, False]:
                    turn_limit = -40
                else:
                    turn_limit = 20

            elif line_sensor_results == [False, False, False, False, True]:
                if previous_sensor_state == [False, False, False, True, False] or previous_sensor_state == [False,
                                                                                                                False,
                                                                                                                False, True,
                                                                                                                True] or previous_sensor_state == [
                                                                                                                False, False, False, False, False]:
                    turn_limit = 40
                else:
                    turn_limit = -20

            elif line_sensor_results == [False, True, False, False, False]:
                if previous_sensor_state == [True, False, False, False, False]:
                    turn_limit = 5
                else:
                    turn_limit = -10

            elif line_sensor_results == [False, False, False, True, False]:
                if previous_sensor_state == [False, False, False, False, True] or previous_sensor_state == [False,
                                                                                                                False,
                                                                                                                False, True,
                                                                                                                True]:
                    turn_limit = -5
                else:
                    turn_limit = 10

            elif line_sensor_results == [False, False, True, False, False]:
                turn_limit = 0

            elif line_sensor_results == [False, True, True, False, False]:
                if previous_sensor_state == [False, True, False, False, False]:
                    turn_limit = -10
                else:
                    turn_limit = 6

            elif line_sensor_results == [False, False, True, True, False]:
                if previous_sensor_state == [False, False, False, True, False]:
                    turn_limit = 10
                else:
                    turn_limit = -6

            elif line_sensor_results == [True, True, False, False, False]:
                if previous_sensor_state == [True, False, False, False, False]:
                    turn_limit = -30
                else:
                    turn_limit = -8

            elif line_sensor_results == [False, False, False, True, True]:
                if previous_sensor_state == [False, False, False, False, True]:
                    turn_limit = 30
                else:
                    turn_limit = 8
    else:
        turn_limit = 0
    return turn_limit


def get_line_follower_result():
    line_sensor_result = line_follower.read_analog()
    for i in range(len(line_sensor_result)):
        if line_sensor_result[i] > threshold:
            line_sensor_result[i] = False
        else:
            line_sensor_result[i] = True
    return line_sensor_result
