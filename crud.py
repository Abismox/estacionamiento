# --- crud.py ---
from sqlmodel import Session, select
from datetime import datetime

from database import engine
from models import Vehiculo, Sesion, Ticket, Pago, Suscripcion, EntradaCreate

# Vehículos

def obtener_vehiculo_por_placa(session: Session, placa: str) -> Vehiculo:
    stmt = select(Vehiculo).where(Vehiculo.placa == placa)
    result = session.exec(stmt).first()
    return result

def crear_vehiculo(session: Session, data: EntradaCreate) -> Vehiculo:
    veh = Vehiculo(
        placa=data.placa,
        marca=data.marca,
        modelo=data.modelo,
        color=data.color,
        tipo=data.tipo,
    )
    session.add(veh)
    session.commit()
    session.refresh(veh)
    return veh

# Sesiones y Tickets

def crear_sesion(session: Session, vehiculo_id: int, plaza_id: int, tarifa_id: int) -> Sesion:
    sesion = Sesion(
        vehiculo_id=vehiculo_id,
        plaza_id=plaza_id,
        tarifa_id=tarifa_id,
        entrada=datetime.utcnow()
    )
    session.add(sesion)
    session.commit()
    session.refresh(sesion)
    return sesion

def crear_ticket(session: Session, sesion_id: int) -> Ticket:
    import uuid
    codigo_qr = str(uuid.uuid4())
    ticket = Ticket(
        sesion_id=sesion_id,
        codigo=codigo_qr,
        generado=datetime.utcnow()
    )
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

# Consultas de sesión

def obtener_sesion_por_codigo(session: Session, codigo: str) -> Sesion:
    stmt = (
        select(Sesion, Ticket)
        .join(Ticket, Ticket.sesion_id == Sesion.sesion_id)
        .where(Ticket.codigo == codigo)
        .where(Ticket.estado == 'activo')
    )
    result = session.exec(stmt).first()
    # devuelve una tupla (Sesion, Ticket)
    return result

# Pagos

def procesar_pago(session: Session, sesion: Sesion, ticket: Ticket, monto: float, metodo: str) -> Pago:
    # 1) Crear pago
    pago = Pago(
        sesion_id=sesion.sesion_id,
        monto=monto,
        fecha_pago=datetime.utcnow(),
        metodo=metodo,
    )
    session.add(pago)
    # 2) Actualizar ticket como pagado
    ticket.estado = 'pagado'
    session.add(ticket)
    # 3) Cerrar la sesión
    sesion.salida = datetime.utcnow()
    session.add(sesion)

    session.commit()
    session.refresh(pago)
    return pago

# Suscripciones (pensiones)

def crear_suscripcion(session: Session, vehiculo_id: int, fecha_inicio, fecha_fin, monto_mes: float) -> Suscripcion:
    subs = Suscripcion(
        vehiculo_id=vehiculo_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        monto_mes=monto_mes,
        estado='activa'
    )
    session.add(subs)
    session.commit()
    session.refresh(subs)
    return subs
