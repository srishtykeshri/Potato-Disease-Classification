"""import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
MODEL_PATH = "./saved_models/1.h5"  # Adjust this path if needed
MODEL = tf.keras.models.load_model(MODEL_PATH)
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence' : float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)"""



import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "./saved_models/1.h5"
MODEL = tf.keras.models.load_model(MODEL_PATH)
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

DISEASE_INFO = {
    "Early Blight": {
        "description": "Early Blight is caused by *Alternaria solani*. It results in dark spots with concentric rings on the leaves, leading to defoliation and yield loss.",
        "solution": "Apply fungicides like chlorothalonil or copper-based sprays. Practice crop rotation and ensure field sanitation."
    },
    "Late Blight": {
        "description": "Late Blight is caused by *Phytophthora infestans*. It spreads quickly in wet and cool conditions, causing dark lesions on leaves and stems.",
        "solution": "Apply fungicides such as metalaxyl or mancozeb. Remove infected plants to prevent further spread."
    },
    "Healthy": {
        "description": "No signs of disease detected. The plant appears healthy.",
        "solution": "Maintain good agricultural practices to ensure plant health."
    }
}

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence' : float(confidence),
        'description': DISEASE_INFO[predicted_class]['description'],
       'solution': DISEASE_INFO[predicted_class]['solution']
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
