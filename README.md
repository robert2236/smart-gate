# 🛡️ Smart-Gate: Control de Acceso Biométrico con IA

**Smart-Gate** es un sistema de seguridad avanzado que utiliza visión artificial para gestionar accesos mediante reconocimiento facial. El proyecto integra el procesamiento de imágenes en tiempo real con una base de datos relacional para garantizar la persistencia de cada evento.

## ⚙️ Funcionamiento del Proyecto

Según el flujo establecido en la documentación técnica, el sistema opera en las siguientes etapas:

### 1. Registro y Captura de Rostros (`captura.py`)
En esta fase inicial, se vincula la identidad legal del usuario con su identidad biométrica.
* **Entrada de Datos:** El script solicita vía terminal el ID numérico, Nombre y Apellido del usuario.
* **Proceso de Captura:** Una vez detectado el rostro, el sistema captura automáticamente **50 fotografías**.
* **Almacenamiento:** Las imágenes se guardan en escala de grises dentro de la carpeta `/dataset` con el formato `User.ID.Count.jpg`.

### 2. Entrenamiento del Modelo (`training.py`)
Tras generar el dataset, se procesan las imágenes para crear el motor de reconocimiento.
* **Algoritmo:** Utiliza **LBPH** (Local Binary Patterns Histograms) para analizar la estructura local del rostro.
* **Resultado:** Se genera el archivo `trainer.yml`, que contiene los patrones aprendidos para la validación.

### 3. Validación y Acceso (Persistencia de Datos)
El sistema compara el rostro capturado por la cámara con el modelo entrenado para determinar el acceso.
* **Umbral de Confianza:** El sistema trabaja con un valor de confianza de 0 a 100. Se considera éxito cuando el valor se mantiene dentro del umbral configurado (60-70).
* **Interfaz Dual:** Los resultados pueden visualizarse mediante logs en la terminal o a través de una **interfaz web** (`http://localhost:5000`) que indica si el acceso es **PERMITIDO** o **DENEGADO**.

## 🚨 Protocolo de Intrusos
Si el rostro no es reconocido o el nivel de confianza es insuficiente, se activa el protocolo de seguridad:
* **Captura de Evidencia:** Se toma una foto del intruso y se guarda en la carpeta `/intrusos`.
* **Registro SQL:** El intento se guarda en la base de datos con el estado "DENEGADO" y el ID "DESCONOCIDO" para auditoría posterior.

## 🛠️ Tecnologías y Herramientas
* **Lenguaje:** Python 3.13.5.
* **Librerías:** OpenCV, SQLite3 y Pillow.
* **Gestión de Datos:** DBeaver para la auditoría de la base de datos `smart_gate.db`.

---
**Repositorio:** [https://github.com/robert2236/smart-gate.git](https://github.com/robert2236/smart-gate.git)
