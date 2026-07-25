from ast import Lambda

from fastapi import FastAPI,Path,HTTPException, Query, responses
import json 
from fastapi.responses import JSONResponse
from models.Patient_model import Patient
from models.update_patient_model import UpdatedPatient
app = FastAPI()

def loadData():
    with open("patients.json") as f:
        data = json.load(f)
    return data

def saveData(data):
    with open("patients.json","w") as f:
        json.dump(data,f)



@app.get("/",tags=["Health"])
def hello_world_api():
    return {"message": "Hello, World!"}

@app.get("/about",tags=["Health"])
def about():
    return {"message":" Hey i am learning fastapi and i am enjoying it !!!"}


@app.get("/patients/view",tags=["Patients"])
def view_patients():
    return loadData()

@app.get("/patients/view/{patient_id}")
def view_particular_patient(patient_id:str = Path(...,description="The ID of the patient you want to view",example="P001")):

    data=loadData()

    patient_id=patient_id.upper()

    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404,detail=f"Patient with ID {patient_id} not found")

@app.get("/sort")
def sort_patients(sort_by:str =Query(...,description="The field by which you want to sort the patients",example="age"),
                  order:str= Query("asc",description="The order in which you want to sort the patients",example="asc")):
    
    if sort_by not in ['bmi','age','height','weight']:
       raise HTTPException(status_code=400,detail=f"Invalid sort_by value. Must be one of ['bmi','age','height','weight']")
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f"Invalid order value. Must be one of ['asc','desc']")
    
    data=loadData()

    sorted_data=sorted(data.values(),key=lambda x:x[sort_by],reverse=(order=="desc"))   
    return sorted_data


@app.get("/patient/{patient_id}")
def get_patient_field(patient_id:str =Path(...,description="The ID of the patient you want to view",example="P001"),
                      field:str =Query(...,description="The field you want to view for the patient",example="age")):
    
    if field not in ['name','age','height','weight','bmi','verdict','city','gender']:
        raise HTTPException(status_code=400,detail=f"Invalid field value. Must be one of ['name','age','height','weight','bmi','verdict','city','gender']")
    data=loadData()

    field_value=data[patient_id.upper()][field]

    return {field:field_value}


### in fast api when a http request occur it reads the associated fucntion and if in function defincation it found a pydantic object
### then it check request body becuase it knows that if in signatute there is pydantic model then there should be something in 
### request body and then fast api on his own parse json body and create a Pateint model if it is created successfully then
### then pass pydantic model as argument but if any validation error occur it automatically raise erorr 422 unprocessable entity 


@app.post("/patient/create")
def create_patient(patient:Patient):

    data =loadData()

    if patient.id in data:
        raise HTTPException(status_code=400,detail="Pateint already exist !")

    data[patient.id]=patient.model_dump(exclude=["id"])

    saveData(data)

    return JSONResponse(status_code=201,content={"message": "Patient created successfully !!!"})


@app.put("/patient/update/{patient_id}")
def update_patient(updatedDetail : UpdatedPatient 
                   ,patient_id: str= Path(...,description="patient id of patient whom you want to update !",example="P001")):

    data=loadData()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found !")

    oldPatientDetails=data[patient_id]
    updatedDetails=updatedDetail.model_dump(exclude_unset=True)

    merged_new_updaetd_patient={**oldPatientDetails,**updatedDetails} # this line merge two dicts key_value pairs and if two dict have same keys then the later one key's value remains 

    merged_new_updaetd_patient["id"]=patient_id
    new_validated_Pateint=Patient(**merged_new_updaetd_patient)

    patient_dict=new_validated_Pateint.model_dump(exclude="id")

    data[patient_id]=patient_dict

    saveData(data)

    return JSONResponse(status_code=200,content={"message":"Pateint updated successfully !!"})


@app.delete("/patient/delete/{patient_id}")
def delete_patient(patient_id:str= Path(...,description="give id of patient whom you want to delete !",expample="P001")):
    data=loadData()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found !")


    del data[patient_id]

    saveData(data)

    return JSONResponse(status_code=200,content={"message":f"{patient_id} deleted successfully !"})