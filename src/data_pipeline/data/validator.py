from pydantic import BaseModel


class IrisDatasetValidator(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float
    Species: str
