from sqlalchemy import Column, Integer, String, Float, Date
from config import Base

class StudentData(Base):
    __tablename__ = "student_data"  # Asegúrate de que coincida con la tabla real en PostgreSQL

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, index=True)  # Para búsquedas por estudiante
    fecha = Column(Date)  # Fecha de la asistencia
    asistencia = Column(Float)  # Porcentaje de asistencia
    inasistencia = Column(Float)  # Porcentaje de inasistencia
    nota_final = Column(Float)
    conducta = Column(String)  # puede ser 'positivo', 'neutral', 'agresivo'
