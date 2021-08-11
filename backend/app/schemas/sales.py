from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class SalesBase(BaseModel):
    saleprice: Optional[int] = None
    model_id: Optional[int] = None
    data_source: Optional[int] = None
    auctioneer_id: Optional[str] = None

    year_made: Optional[int] = 1996  # Median of yearmade in the dataset

    machine_hours_current_meter: Optional[
        int
    ] = 3213  # Median of MachineHoursCurrentMeter in the dataset

    saledate: Optional[date] = datetime.now().date()

    fi_model_desc: Optional[str] = None
    fi_base_model: Optional[str] = None
    fi_secondary_desc: Optional[str] = None
    fi_model_series: Optional[str] = None
    fi_model_descriptor: Optional[str] = None

    product_size: Optional[str] = None
    state: Optional[str] = None
    product_group: Optional[str] = None
    product_group_desc: Optional[str] = None

    drive_system: Optional[str] = None
    enclosure: Optional[str] = None
    ride_control: Optional[str] = None
    stick: Optional[str] = None
    transmission: Optional[str] = None
    engine_horsepower_desc: Optional[str] = None

    hydraulics: Optional[str] = None
    ripper: Optional[str] = None
    tire_size: Optional[float] = 20.0  # Median of Tire_Size in the dataset
    coupler: Optional[str] = None
    hydraulics_flow: Optional[str] = None
    track_type: Optional[str] = None
    undercarriage_pad_width: Optional[
        float
    ] = 30.0  # Median of Undercarriage_Pad_Width in the dataset
    stick_length: Optional[str] = None
    grouser_type: Optional[str] = None
    blade_type: Optional[str] = None
    differential_type: Optional[str] = None
    steering_controls: Optional[str] = None
    engine_horsepower: Optional[float] = None
    is_new: Optional[bool] = True


class SalesCreate(SalesBase):
    """
    Required fields for predictions, based on feature importance graph
    """

    saledate: date
    model_id: int
    fi_base_model: str
    year_made: int
    product_group: str
    state: str


class SalesShow(SalesBase):
    saleprice: Optional[int]
    saledate: date
    state: str

    model_id: int
    fi_model_desc: Optional[str]

    year_made: int
    machine_hours_current_meter: Optional[int]

    product_group: str
    product_size: Optional[str]
    enclosure: Optional[str] = None
    engine_horsepower: Optional[float] = None

    class Config:
        orm_mode = True
