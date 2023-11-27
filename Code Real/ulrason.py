from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance

ultrasonic_avoidance = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)

def get_ultrasonic_avoidance():
        return ultrasonic_avoidance.get_distance()
