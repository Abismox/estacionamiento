# routers/entrada.py

from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from datetime import datetime
import uuid

from database import engine
from models import Sesion, Ticket, Vehiculo, EntradaCreate
from crud import obtener_vehiculo_por_placa, crear_vehiculo

router = APIRouter()

@router.post("/", response_model=Ticket)
def registrar_entrada(data: EntradaCreate):
    """
    Registra la entrada de un vehículo:
    1) Busca o crea el vehículo en la tabla Vehiculo.
    2) Crea una Sesion con la plaza y la tarifa por defecto.
    3) Genera un Ticket con un UUID como código para QR/barcode.
    4) Devuelve el ticket creado.
    """
    with Session(engine) as session:
        # 1) Vehículo: buscar por placa; si no existe, crearlo
        veh = obtener_vehiculo_por_placa(session, data.placa)
        if not veh:
            veh = crear_vehiculo(session, data)

        # 2) Crear la sesión de estacionamiento
        sesion = Sesion(
            vehiculo_id=veh.vehiculo_id,
            plaza_id=data.plaza_id,
            tarifa_id=1,               # aquí usas la tarifa normal (ID = 1)
            entrada=datetime.utcnow()
        )
        session.add(sesion)
        session.commit()
        session.refresh(sesion)

        # 3) Generar el ticket vinculado a la sesión
        codigo_qr = str(uuid.uuid4())
        ticket = Ticket(
            codigo=codigo_qr,
            sesion_id=sesion.sesion_id,
            generado=datetime.utcnow()
        )
        session.add(ticket)
        session.commit()
        session.refresh(ticket)

        # 4) devolver el ticket (JSON)
        return ticket
