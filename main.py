from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from upload import save_uploaded_file
from models.predictor import predict_desertion
from datetime import datetime
from sqlalchemy.orm import Session
from models.tiempo_inferencia_model import TiempoInferencia
from config import SessionLocal, Base, engine
import os

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://edu-forge-psi.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Servidor activo en la raíz."}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = await save_uploaded_file(file)
        return {
            "success": True,
            "message": f"Archivo '{file.filename}' guardado correctamente",
            "filename": file.filename,
            "filepath": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")


@app.post("/predict")
async def predict(filename: str):
    db: Session = SessionLocal()
    try:
        tiempo_inicio = datetime.utcnow()

        upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "uploads"))
        file_path = os.path.join(upload_dir, filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {file_path}")

        predictions = predict_desertion(file_path)

        tiempo_fin = datetime.utcnow()
        duracion = (tiempo_fin - tiempo_inicio).total_seconds()

        # Guardar en BD
        registro = TiempoInferencia(tiempo_inicio=tiempo_inicio, tiempo_fin=tiempo_fin, duracion=duracion)
        db.add(registro)
        db.commit()

        return {
            "predictions": predictions,
            "tiempo_inferencia": f"{duracion:.3f} segundos"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()