# routers/cobro.py

from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from datetime import datetime
import math

from database import engine
from models import Pago, Sesion, Ticket, Tarifa
from crud import obtener_sesion_por_codigo, procesar_pago

router = APIRouter()

# Modelo simple para validar la petición
from pydantic import BaseModel
class CobroRequest(BaseModel):
    codigo: str    # código UUID del ticket (QR/barcode)
    metodo: str    # método de pago, e.g. "efectivo", "tarjeta"

@router.post("/", response_model=Pago)
def cobrar_ticket(data: CobroRequest):
    """
    1) Busca la sesión activa asociada al código del ticket.
    2) Calcula el monto con 10 minutos de cortesía.
    3) Registra el pago, cierra la sesión y marca el ticket como pagado.
    4) Devuelve el objeto Pago.
    """

    with Session(engine) as session:
        # 1) Obtener (Sesion, Ticket) para ese código
        resultado = obtener_sesion_por_codigo(session, data.codigo)
        if not resultado:
            raise HTTPException(status_code=404, detail="Ticket no encontrado o ya pagado")
        sesion, ticket = resultado

        # 2) Recuperar la tarifa asociada
        tarifa = session.get(Tarifa, sesion.tarifa_id)
        precio_hora = tarifa.precio_por_hora

        # 3) Calcular tiempo transcurrido en minutos
        minutos_totales = (datetime.utcnow() - sesion.entrada).total_seconds() / 60.0

        # 4) Aplicar 10 minutos de cortesía
        minutos_facturables = max(0, minutos_totales - 10)

        # 5) Calcular bloques de cobro de 60 min, redondeando hacia arriba
        bloques = math.ceil(minutos_facturables / 60.0) if minutos_facturables > 0 else 0
        bloques = max(bloques, 1)  # al menos 1 hora

        monto = bloques * precio_hora

        # 6) Registrar el pago y cerrar la sesión
        pago = procesar_pago(session, sesion, ticket, monto, data.metodo)

        return pago
