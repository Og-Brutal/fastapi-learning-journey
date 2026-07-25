from ast import Lambda

from fastapi import FastAPI,Path,HTTPException, Query, responses
import json 
from fastapi.responses import JSONResponse


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
