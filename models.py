from sqlmodel import Field, SQLModel
from datetime import datetime, date

class Vehiculo(SQLModel, table=True):
    vehiculo_id: int = Field(default=None, primary_key=True)
    placa: str = Field(index=True, unique=True, nullable=False)
    marca: str
    modelo: str
    color: str
    tipo: str  # auto, moto, camión...

class Plaza(SQLModel, table=True):
    plaza_id: int = Field(default=None, primary_key=True)
    numero: str = Field(unique=True, nullable=False)
    sector: str = None
    estado: str = Field(default="libre")  # libre / ocupada

class Tarifa(SQLModel, table=True):
    tarifa_id: int = Field(default=None, primary_key=True)
    descripcion: str
    precio_por_hora: float
    precio_minimo: float = 0.0

class Sesion(SQLModel, table=True):
    sesion_id: int = Field(default=None, primary_key=True)
    vehiculo_id: int
    plaza_id: int
    tarifa_id: int
    entrada: datetime = Field(default_factory=datetime.utcnow)
    salida: datetime = None

class Ticket(SQLModel, table=True):
    ticket_id: int = Field(default=None, primary_key=True)
    codigo: str = Field(unique=True, nullable=False)
    sesion_id: int
    generado: datetime = Field(default_factory=datetime.utcnow)
    estado: str = Field(default="activo")  # activo / pagado / anulado

class Pago(SQLModel, table=True):
    pago_id: int = Field(default=None, primary_key=True)
    sesion_id: int
    monto: float
    fecha_pago: datetime = Field(default_factory=datetime.utcnow)
    metodo: str

class Suscripcion(SQLModel, table=True):
    subs_id: int = Field(default=None, primary_key=True)
    vehiculo_id: int
    fecha_inicio: date
    fecha_fin: date
    monto_mes: float
    estado: str  # activa / vencida