import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use DATABASE_URL from environment (Render)
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:%23Usman20069292006@db.ppklfyvxxtjwnrweuihk.supabase.co:5432/postgres"
)

# Create database engine
engine = create_engine(DATABASE_URL, echo=False)

# Setup base and session
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Define table structure
class StockSnapshot(Base):
    __tablename__ = "stock_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    date = Column(Date, default=datetime.date.today)
    market_price = Column(Float)
    ma_10 = Column(Float)
    ma_30 = Column(Float)
    ma_60 = Column(Float)
    rsi = Column(Float)
    macd_daily = Column(String)
    macd_weekly = Column(String)
    support1 = Column(Float)
    support2 = Column(Float)
    resistance1 = Column(Float)
    resistance2 = Column(Float)

# Create the table (if not exists)
Base.metadata.create_all(engine)
