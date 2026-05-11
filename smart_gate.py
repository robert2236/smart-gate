import cv2
import sqlite3
import time
from datetime import datetime

class SmartGate:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        # Cargar el reconocedor entrenado
        self.reconocedor = cv2.face.LBPHFaceRecognizer_create()
        self.reconocedor.read('trainer.yml')
        
        # Base de Datos
        self.conn = sqlite3.connect('smart_gate.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accesos 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, usuario_id TEXT, estado TEXT)''')
        
        # Configuración de Cooldown (Evitar spam de registros)
        self.ultimo_registro = 0
        self.cooldown_segundos = 5 

    def registrar_acceso(self, user_id, estado):
        ahora_unix = time.time()
        if ahora_unix - self.ultimo_registro > self.cooldown_segundos:
            fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO accesos (fecha, usuario_id, estado) VALUES (?, ?, ?)", 
                                (fecha_str, user_id, estado))
            self.conn.commit()
            self.ultimo_registro = ahora_unix
            print(f"[{estado}] Usuario: {user_id} a las {fecha_str}")

    def protocolo_intruso(self, frame_gris, x, y, w, h):
        """Captura foto de quien no tiene acceso"""
        fecha_foto = datetime.now().strftime("%Y%m%d_%H%M%S")
        rostro_recortado = frame_gris[y:y+h, x:x+w]
        cv2.imwrite(f"intrusos/INTRUSO_{fecha_foto}.jpg", rostro_recortado)
        self.registrar_acceso("DESCONOCIDO", "DENEGADO")

    def obtener_nombre_usuario(self, user_id):
        self.cursor.execute("SELECT nombre, apellido FROM usuarios WHERE id = ?", (user_id,))
        resultado = self.cursor.fetchone()
        if resultado:
            return f"{resultado[0]} {resultado[1]}"
        return f"ID: {user_id}"

    def procesar_frame(self, frame):
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostros = self.face_cascade.detectMultiScale(gris, 1.3, 5)

        self.estado_actual = {"estado": "ESPERANDO", "nombre": ""}

        for (x, y, w, h) in rostros:
            id_predicho, confianza = self.reconocedor.predict(gris[y:y+h, x:x+w])

            if confianza < 85:
                nombre_completo = self.obtener_nombre_usuario(id_predicho)
                nombre_label = nombre_completo
                color = (0, 255, 0) # Verde
                self.registrar_acceso(nombre_completo, "AUTORIZADO")
                self.estado_actual = {"estado": "AUTORIZADO", "nombre": nombre_completo}
            else:
                nombre_label = "DESCONOCIDO"
                color = (0, 0, 255) # Rojo
                self.protocolo_intruso(gris, x, y, w, h)
                self.estado_actual = {"estado": "DENEGADO", "nombre": "Desconocido"}

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"{nombre_label} ({round(confianza)})", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                        
        return frame

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        frame = cv2.flip(frame, 1)
        frame = self.procesar_frame(frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

    def iniciar(self):
        print("Smart-Gate Activo. Presione 'q' para finalizar.")
        
        while True:
            ret, frame = self.cap.read()
            if not ret: break
            
            frame = cv2.flip(frame, 1)
            frame = self.procesar_frame(frame)

            cv2.imshow('Smart-Gate: Control Biometrico', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        self.cap.release()
        cv2.destroyAllWindows()
        self.conn.close()

if __name__ == "__main__":
    sistema = SmartGate()
    sistema.iniciar()