# Heart of the data infrastructure.

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# DB adress
URL_DATA_BASE = "sqlite:///./inventory.db"

# Engine maker
engine = create_engine(
    URL_DATA_BASE,
    connect_args={"check_same_thread": False}
)

# Session maker
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()