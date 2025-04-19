import cv2
import numpy as np
from keras.models import load_model
import base64
from io import BytesIO
from PIL import Image

# Load model once at module level instead of in function
model = load_model("C:/Users/PC/Desktop/waste_AG_model.h5")
classes = ["Organico", "Plastico", "Carton", "Vidrio", "Otro"]

def detect_waste(image_data):
    # Convert image to numpy array and correct color
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Preprocess image exactly like in your working script
    img = cv2.resize(frame, (64, 64))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict
    predictions = model.predict(img)
    class_index = np.argmax(predictions)
    confidence = predictions[0][class_index] * 100

    label = f"{classes[class_index]} ({confidence:.1f}%)"
    return {
        'class': classes[class_index],
        'confidence': float(confidence),
        'label': label
    }
