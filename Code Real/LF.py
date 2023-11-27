from SunFounder_Line_Follower import Line_Follower
import time

lf = Line_Follower.Line_Follower()
th = 100

def LF():
    sensors = lf.read_analog()
    for i in range(len(sensors)):
        if sensors[i] > th:
           sensors[i] = 1
        else:
            sensors[i] = 0

    return sensors