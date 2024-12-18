import cv2
import requests
from angle_interpretation.main import InterpretacionAngulos

class DeteccionObjetos:
    def __init__(self, rows=5, cols=7, camera_width=640, camera_height=480):
        """
        Inicializa los parámetros de la clase.
        """
        self.rows = rows
        self.cols = cols
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.cell_width = self.camera_width // self.cols
        self.cell_height = self.camera_height // self.rows

        # Configuración de la cámara
        self.cap = cv2.VideoCapture(1)
        self.cap.set(3, self.camera_width)
        self.cap.set(4, self.camera_height)

        # Instancia de InterpretacionAngulos
        self.angulos = InterpretacionAngulos()
        self.angulo_AUX = [0, 0, 0]  # Almacena valores auxiliares solo para la garra
        self.angulo_garra = 0

    def create_grid(self, image):
        """
        Superpone un grid sobre la imagen dada.
        """
        for r in range(1, self.rows):
            cv2.line(image, (0, r * self.cell_height), 
                     (self.camera_width, r * self.cell_height), 
                     (255, 255, 255), 1)
        for c in range(1, self.cols):
            cv2.line(image, (c * self.cell_width, 0), 
                     (c * self.cell_width, self.camera_height), 
                     (255, 255, 255), 1)
            
        # Dibujar botones en la esquina inferior izquierda
        cv2.rectangle(image, (10, 400), (150, 440), (50, 50, 255), -1)  # Botón "Abrir Garra"
        cv2.rectangle(image, (10, 450), (150, 490), (50, 255, 50), -1)  # Botón "Cerrar Garra"
        cv2.putText(image, "Abrir Garra", (20, 430), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, (255, 255, 255), 2)
        cv2.putText(image, "Cerrar Garra", (20, 480), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, (255, 255, 255), 2)

    def mouse_callback(self, event, x, y, flags, param):
        """
        Detecta el clic del mouse y envía las coordenadas a la clase InterpretacionAngulos.
        También realiza una solicitud HTTP al servidor local.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"Coordenadas del clic: (x: {x}, y: {y})")

            if 10 <= x <= 150 and 400 <= y <= 440:
                # Botón "Abrir Garra" presionado
                self.angulo_garra = 180
                command = f"{self.angulo_AUX[0]}-{self.angulo_AUX[1]}-{self.angulo_AUX[2]}-{self.angulo_garra}"
                print("Botón 'Abrir Garra' presionado.")
            elif 10 <= x <= 150 and 450 <= y <= 490:
                # Botón "Cerrar Garra" presionado
                self.angulo_garra = 30
                command = f"{self.angulo_AUX[0]}-{self.angulo_AUX[1]}-{self.angulo_AUX[2]}-{self.angulo_garra}"
                print("Botón 'Cerrar Garra' presionado.")
            else:
                # Calcular ángulos para movimiento normal
                angulos = self.angulos.interpretar_posicion(x, y)
                self.angulo_AUX = angulos[:]  # Guardar copia en angulo_AUX
                command = f"{angulos[0]}-{angulos[1]}-{angulos[2]}-{self.angulo_garra}"
                print("Movimiento detectado.")

            print(f"Comando generado: {command}")

            # Enviar ángulos al servidor local
            try:
                response = requests.get(f"http://localhost:3000/{command}")
                response.raise_for_status()  # Lanza un error si el código de estado no es 200
                print(f"Respuesta del servidor: {response.text}")
            except requests.exceptions.Timeout:
                print("La solicitud ha tardado demasiado. Verifica si el servidor está disponible.")
            except requests.exceptions.ConnectionError:
                print("Error de conexión. El servidor puede estar caído o inaccesible.")
            except requests.exceptions.HTTPError as err:
                print(f"Error HTTP: {err}")
            except requests.exceptions.RequestException as e:
                print(f"Error en la solicitud: {e}")

    def run(self):
        """
        Captura el flujo de video y muestra el grid.
        """
        cv2.namedWindow("Vista con Grid")
        cv2.setMouseCallback("Vista con Grid", self.mouse_callback)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error al acceder a la cámara.")
                break

            self.create_grid(frame)

            cv2.imshow("Vista con Grid", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Presionar 'ESC' para salir
                break

        self.cap.release()
        cv2.destroyAllWindows()

# Crear una instancia de la clase y ejecutar
if __name__ == "__main__":
    detector = DeteccionObjetos()
    detector.run()
