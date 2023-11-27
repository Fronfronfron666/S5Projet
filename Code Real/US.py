from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance

UA = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)

def US():
        return UA.get_distance()