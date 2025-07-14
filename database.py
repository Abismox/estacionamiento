from sqlmodel import create_engine, SQLModel

engine = create_engine("sqlite:///./data/estacionamiento.db", echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)    