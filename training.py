import cv2
import os
import numpy as np
from PIL import Image

def entrenar_modelo():
    path = 'dataset'
    reconocedor = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
    rostros, ids = [], []

    for path_imagen in image_paths:
        img_pil = Image.open(path_imagen).convert('L')
        img_numpy = np.array(img_pil, 'uint8')
        id_user = int(os.path.split(path_imagen)[-1].split(".")[1])
        rostros.append(img_numpy)
        ids.append(id_user)

    reconocedor.train(rostros, np.array(ids))
    reconocedor.save('trainer.yml')
    print(">>> Modelo 'trainer.yml' creado con éxito.")

if __name__ == "__main__":
    entrenar_modelo()