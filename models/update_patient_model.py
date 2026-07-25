from pydantic import BaseModel,Field,field_validator,computed_field
from typing import Literal,Optional



class UpdatedPatient(BaseModel):

    name: Optional[str] = Field(default=None,description="name of patient !")
    city: Optional[str] = Field(default=None,description="city name of patient !")
    age: Optional[int] = Field(default=None,gt=0,description="age of user ")
    gender: Optional[Literal["male","female","others"]] = Field(default=None,description="gender of pateint !")
    height: Optional[float] = Field(default=None,gt=0,description="height of user")
    weight: Optional[float] = Field(defualt=None,gt=0,description="weight of patient !")
