from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance

ultrasonic_avoidance = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)

"""
Entrée: N/A
Sortie: Distance detecte par le capteur ultrasonique
Fonction: Donne la distance detecte par le capteur ultrasonique
"""
def get_ultrasonic_avoidance():
        return ultrasonic_avoidance.get_distance()

