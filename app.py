from fastapi import FastAPI, HTTPException
import numpy as np
from keras.models import model_from_json

app = FastAPI()


loaded_model = None

# Cargar el modelo al iniciar la aplicación
def load_model():
    global loaded_model
    json_file = open("model.json", 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model.h5")
    print("Modelo cargado en el disco")

app.add_event_handler("startup", load_model)

# Ruta de inicio
@app.get("/")
async def read_root():
    return {"message": "¡Bienvenido a la API de predicción! Visita /docs para ver la documentación."}

# Ruta de predicción
@app.get("/predict/{x0}/{x1}/{x2}/{x3}/{x4}")
async def predict(x0: float, x1: float, x2: float, x3: float, x4: float):
    global loaded_model
    if loaded_model is None:
        raise HTTPException(status_code=500, detail="El modelo no está cargado.")
    try:
        # Convertir los datos de entrada a un array de NumPy para la predicción
        input_data = np.array([[x0, x1, x2, x3, x4]])
        prediction = loaded_model.predict(input_data).round()
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
