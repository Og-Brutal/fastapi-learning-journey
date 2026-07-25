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