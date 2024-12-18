import numpy as np
from typing import Tuple

class InterpretacionAngulos:
    def __init__(self):
        """
        Inicializa el estado de la clase.
        """
        self.last_command = ""
        self.servo_ranges = {
            "servo_base": (180, 0),
            "servo_hombro": (180, 0),
            "servo_muneca": (0, 180),
        }

    def interpretar_posicion(self, x: int, y: int):
        """
        Interpreta la posición en función de las coordenadas (x, y).
        """
        print(f"Procesando posición: x={x}, y={y}")
        angles = self.definir_angulos(x, y)
        return angles
        #self.enviar_comandos(angles)

    def definir_angulos(self, x: int, y: int) -> Tuple[int, int, int]:
        """
        Calcula los ángulos para los servomotores en función de las coordenadas (x, y).
        """
        servo_base_angle = int(np.interp(x, [0, 640], self.servo_ranges["servo_base"]))
        servo_hombro_angle = int(np.interp(y, [0, 480], self.servo_ranges["servo_hombro"]))
        servo_muneca_angle = int(np.interp(y, [0, 480], self.servo_ranges["servo_muneca"]))

        #print(f"Ángulos calculados: servo_base={servo_base_angle}, servo_hombro={servo_hombro_angle}, servo_muneca={servo_muneca_angle}")
        return servo_base_angle, servo_hombro_angle, servo_muneca_angle

    '''
    def enviar_comandos(self, angles: Tuple[int, int, int]):
        """
        Envía los comandos a los servomotores.
        """
        # Este método puede ser implementado con serialización para enviar comandos.
        print(f"Enviando comandos a los servomotores: {angles}")
    '''