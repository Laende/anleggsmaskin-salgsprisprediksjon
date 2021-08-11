from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, Date
from sqlalchemy.sql.sqltypes import Boolean

from app.db.base_class import Base


class Sales(Base):
    id = Column(Integer, primary_key=True)
    saleprice = Column(Integer, nullable=True)
    model_id = Column(Integer, nullable=True)
    data_source = Column(Integer, nullable=True)
    auctioneer_id = Column(String, nullable=True)

    year_made = Column(Integer, nullable=True, default=1996)

    machine_hours_current_meter = Column(Integer, nullable=True, default=3213)

    saledate = Column(Date, nullable=False)

    fi_model_desc = Column(String, nullable=True)
    fi_base_model = Column(String, nullable=True)
    fi_secondary_desc = Column(String, nullable=True)
    fi_model_series = Column(String, nullable=True)
    fi_model_descriptor = Column(String, nullable=True)

    product_size = Column(String, nullable=True)
    state = Column(String, nullable=True)
    product_group = Column(String, nullable=True)
    product_group_desc = Column(String, nullable=True)
    
    drive_system = Column(String, nullable=True)
    enclosure = Column(String, nullable=True)
    ride_control = Column(String, nullable=True)
    stick = Column(String, nullable=True)
    transmission = Column(String, nullable=True)
    engine_horsepower_desc = Column(String, nullable=True)
    hydraulics = Column(String, nullable=True)
    ripper = Column(String, nullable=True)
    tire_size = Column(Float, nullable=True)
    coupler = Column(String, nullable=True)
    hydraulics_flow = Column(String, nullable=True)
    track_type = Column(String, nullable=True)
    undercarriage_pad_width = Column(Float, nullable=True)
    stick_length = Column(String, nullable=True)
    grouser_type = Column(String, nullable=True)
    blade_type = Column(String, nullable=True)
    differential_type = Column(String, nullable=True)
    steering_controls = Column(String, nullable=True)
    engine_horsepower = Column(Float, nullable=True)
    is_new = Column(Boolean, default=False)

        
