import cv2
import os
import sqlite3

# 1. Configuración inicial
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

if not os.path.exists('dataset'):
    os.makedirs('dataset')

user_id = input("Ingrese ID numérico: ")
user_nombre = input("Ingrese Nombre: ")
user_apellido = input("Ingrese Apellido: ")

# Conectar a la base de datos y guardar el usuario
conn = sqlite3.connect('smart_gate.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                  (id INTEGER PRIMARY KEY, nombre TEXT, apellido TEXT)''')
cursor.execute('''INSERT OR REPLACE INTO usuarios (id, nombre, apellido) 
                  VALUES (?, ?, ?)''', (int(user_id), user_nombre, user_apellido))
conn.commit()
conn.close()

# Limpiar fotos previas de ese ID
for f in os.listdir('dataset'):
    if f.startswith(f"User.{user_id}."):
        os.remove(os.path.join('dataset', f))

# 2. Iniciar Cámara
cap = cv2.VideoCapture(0)

# OPCIONAL: Forzar tamaño de ventana para asegurar que se cree
cap.set(3, 640) # Ancho
cap.set(4, 480) # Alto

count = 0
print("\n>>> Capturando... La ventana debería abrirse ahora.")

# Ayuda a prevenir que la ventana se congele en algunos sistemas
cv2.startWindowThread() 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostros = face_cascade.detectMultiScale(gris, 1.3, 5)

    for (x, y, w, h) in rostros:
        count += 1
        cv2.imwrite(f"dataset/User.{user_id}.{count}.jpg", gris[y:y+h, x:x+w])
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"Capturando {count}/50", (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Mostrar la imagen
    cv2.imshow('Ventana de Registro', frame)
    
    # IMPORTANTE: Subimos a 30ms para dar tiempo al procesador de dibujar la ventana
    if cv2.waitKey(30) & 0xFF == ord('q') or count >= 50:
        break

print(f">>> Finalizado. Revisa la carpeta dataset.")
cap.release()
cv2.destroyAllWindows()
# Dos waitKeys extras a veces ayudan a cerrar ventanas rebeldes en Windows
cv2.waitKey(1)