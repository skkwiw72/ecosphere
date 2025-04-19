import cv2
import numpy as np
from keras.models import load_model

# Cargar modelo
model = load_model("C:/Users/roberto/Desktop/waste_AG_model.h5")

# Diccionario de clases
classes = ["Organico", "Plastico", "Carton", "Vidrio", "Otro"]  # Ajusta según tu modelo

# Iniciar cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Redimensionar a 64x64
    img = cv2.resize(frame, (64, 64))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    # Predecir
    predictions = model.predict(img)
    class_index = np.argmax(predictions)
    label = f"{classes[class_index]} ({predictions[0][class_index]*100:.1f}%)"

    # Mostrar etiqueta
    cv2.rectangle(frame, (10, 10), (300, 50), (0, 0, 0), -1)
    cv2.putText(frame, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar imagen en ventana
    cv2.imshow("Waste Classifier", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
