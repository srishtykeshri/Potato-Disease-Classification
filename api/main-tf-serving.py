import numpy as np
from fastapi import FastAPI, File, UploadFile
import uvicorn
from io import BytesIO
from PIL import Image
import tensorflow as tf
import requests

app = FastAPI()

endpoint = "http://localhost8501/v1/models/potatoes_model:predict"

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

    json_data = {
        "instances": img_batch.tolist()
    }


    response = requests.post(endpoint, json=json_data)
    pass

if __name__ == "_main_":
    uvicorn.run(app, host='localhost', port=8000)


















# import numpy as np
# from fastapi import FastAPI, File, UploadFile
# import uvicorn
# from io import BytesIO
# from PIL import Image
# import requests

# app = FastAPI()

# # Ensure the correct endpoint
# endpoint = "http://localhost:8501/v1/models/potatoes_model:predict"

# CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

# DISEASE_INFO = {
#     "Early Blight": {
#         "description": "Early Blight is caused by *Alternaria solani*. It results in dark spots with concentric rings on the leaves, leading to defoliation and yield loss.",
#         "solution": "Apply fungicides like chlorothalonil or copper-based sprays. Practice crop rotation and ensure field sanitation."
#     },
#     "Late Blight": {
#         "description": "Late Blight is caused by *Phytophthora infestans*. It spreads quickly in wet and cool conditions, causing dark lesions on leaves and stems.",
#         "solution": "Apply fungicides such as metalaxyl or mancozeb. Remove infected plants to prevent further spread."
#     },
#     "Healthy": {
#         "description": "No signs of disease detected. The plant appears healthy.",
#         "solution": "Maintain good agricultural practices to ensure plant health."
#     }
# }

# @app.get("/ping")
# async def ping():
#     return "Hello, I am alive"

# def read_file_as_image(data) -> np.ndarray:
#     try:
#         image = Image.open(BytesIO(data)).convert("RGB")
#         image = image.resize((224, 224))
#         image = np.array(image) / 255.0
#         return image
#     except Exception as e:
#         print(f"Error reading image: {e}")
#         return None

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     try:
#         image = read_file_as_image(await file.read())
#         if image is None:
#             return {"error": "Failed to process image"}

#         img_batch = np.expand_dims(image, 0)
#         json_data = {"instances": img_batch.tolist()}

#         # Send the request to TensorFlow Serving
#         response = requests.post(endpoint, json=json_data)

#         if response.status_code != 200:
#             print(f"Error from TensorFlow Serving: {response.text}")
#             return {"error": "Failed to get prediction from model"}

#         prediction_data = response.json()
#         predictions = prediction_data.get('predictions', [[]])[0]

#         predicted_class = CLASS_NAMES[np.argmax(predictions)]
#         confidence = np.max(predictions[0])
#        # conf=str(confidence)

#         return {
#             'class': predicted_class,
#             'confidence': confidence,
#             'description': DISEASE_INFO[predicted_class]['description'],
#             'solution': DISEASE_INFO[predicted_class]['solution']
#         }
#     except Exception as e:
#         print(f"Error during prediction: {e}")
#         return {"error": str(e)}

# if __name__ == "__main__":
#     uvicorn.run(app, host='localhost', port=8000)

