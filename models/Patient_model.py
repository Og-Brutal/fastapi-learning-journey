from pydantic import BaseModel,Field,field_validator,computed_field
from typing import Literal



class Patient(BaseModel):

    id: str=Field(...,description="Unique ID of patient .",examples=["POO1"])
    name: str=Field(...,description="name of patient .")
    city: str=Field(...,description="city of patient .")
    age: int=Field(...,gt=0,le=120,description="age of patient .")
    gender: Literal["male","female","other"]=Field(...,description="gender of patient .")
    height: float=Field(...,description="height of patient .")
    weight: float=Field(...,description="weight of patient .")

    @field_validator("name")
    def captilize_name(cls,value):
        return value.upper()

    @computed_field
    @property
    def bmi(self) -> float :
        return round(self.weight/(self.height**2),2)

    @computed_field
    @property
    def verdict(self) -> str:
        bmi=self.bmi
        if bmi < 18.5 :
            return "Underwight"
        elif bmi < 30 :
            return "Normal"
        else:
            return "obese"




        
