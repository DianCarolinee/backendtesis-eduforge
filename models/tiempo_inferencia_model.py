from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from config import Base  # o desde config si lo tienes global

class TiempoInferencia(Base):
    __tablename__ = "tiempos_inferencia"

    id = Column(Integer, primary_key=True, index=True)
    tiempo_inicio = Column(DateTime, default=datetime.utcnow)
    tiempo_fin = Column(DateTime)
    duracion = Column(Float)  # en segundos