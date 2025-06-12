# src/api/routes/prediction_calculations.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.prediction_service import predict_dropout  # Asegúrate de que la importación esté aquí
from api.models.tiempo_inferencia_model import TiempoInferencia

router = APIRouter()

# Definimos el modelo de datos para la entrada
class StudentData(BaseModel):
    calificacion: float
    asistencia: float
    conducta: str

# Endpoint para realizar la predicción de deserción
@router.post("/predict_dropout")
async def predict_dropout_api(student: StudentData):
    db: Session = SessionLocal()
    try:
        tiempo_inicio = datetime.utcnow()

        result = predict_dropout(student.calificacion, student.asistencia, student.conducta)

        tiempo_fin = datetime.utcnow()
        duracion = (tiempo_fin - tiempo_inicio).total_seconds()

        # Guardar en BD
        registro = TiempoInferencia(tiempo_inicio=tiempo_inicio, tiempo_fin=tiempo_fin, duracion=duracion)
        db.add(registro)
        db.commit()

        return {
            **result,
            "tiempo_inferencia": f"{duracion:.3f} segundos"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al realizar la predicción: {e}")
    finally:
        db.close()