from fastapi import FastAPI, UploadFile, File,Query,Body
import numpy as np
from typing import List,Dict
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles
import shutil
import os
from main import main,load_merge_2persons,load_merge_master, custom_prompt,csv_to_db,persona_names, save_snippets_tocsv,csv_to_pdf_master,get_snippets_of_persona,replace_edited_persona,update_content


class InputData(BaseModel):
    personas: List[str]
    no_of_paragraphs: List[int]
    temp:float

class InputDataOne(BaseModel):
    personas: List[str]
    no_of_paragraphs: List[int]
    w1: int
    temp:float

class InputDataCustom(BaseModel):
    query: List[str]
    temp:float

class InputDataCsv(BaseModel):
    file_path:str

class InputPersonaSave(BaseModel):
    snippets_list:List[dict]

class InputDelPersona(BaseModel):
    personas:List[str]

class InputgetSnippets(BaseModel):
    persona : str

class InputreplaceSnippets(BaseModel):
    snippets_list:List[str]
    persona : str




app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]  # You can specify the allowed origins here

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify the allowed HTTP methods (e.g., ["GET", "POST"])
    allow_headers=["*"],  # You can specify the allowed headers here
)

@app.post("/api/custom_prompt")
async def generate_text_custom_prompt_one(data:InputDataCustom):
    try:
        query = data.query[0]
        temp = data.temp
        response,persona_names = custom_prompt(query,temp)
        paragraphs = response.split('\n')[:]
        filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]

        return {"personas":persona_names,"response":filtered_paragraphs,"w1":None}

    except Exception as e:
        return {"text":e}


@app.post("/api/generate_text")
async def generate_text(data:InputData):
    try:
        char_list = os.listdir('vector_db')
        identifier = data.personas[0]
        para_no = data.no_of_paragraphs[0]
        temp = data.temp
        
        if identifier not in char_list:
            return {"response":"Persona not found."}
        
        response = main(identifier, para_no,temp)

        paragraphs = response.split('\n')[:]
        filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
        resp = []
        for para in filtered_paragraphs:
            resp.append({"persona":identifier,"snippet":para})
        return {"response":resp,"w1":None}

    except Exception as e:
        print(e)
        return {"text":e}


@app.post("/api/generate_text_all")
async def generate_text_all(data:InputData):
    resp = []
    try:
        identifier = data.personas
        para_no = data.no_of_paragraphs[0]
        temp = data.temp
        for i,char in enumerate(identifier):
            # print(identifier[i+1])
            text = main(char, para_no,temp)
            indv_paras = text.split('\n')[:]
            # print(text)
            # print(indv_paras)
            filtered_paragraphs = [paragraph.strip() for paragraph in indv_paras if paragraph.strip()]
            
            # print(filtered_paragraphs)
            for para in filtered_paragraphs:
                resp.append({"persona":char,"snippet":para}) 
                # print(resp)
        return {"response":resp,"w1":None}
        # formatted_text = "\n".join([f"{i}. {paragraph}" for i, paragraph in enumerate(response_list, 1)])
        # paragraphs = formatted_text.split('\n')[:]
        # filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
        # return {"personas": ["All personas"],"response":filtered_paragraphs,"w1":None}
    
    except Exception as e:
        print(e)
        return {"response":resp,"w1":None}

@app.post("/api/merge_two")
async def merge_two(data:InputDataOne):
    try:
        print("generate_merged_text")
        identifier_list = data.personas
        para_no = data.no_of_paragraphs[0]
        w1 = data.w1
        temp = data.temp
        if w1>=50:
            identifier = identifier_list[0]
        else:
            identifier = identifier_list[1]
        response = load_merge_2persons(identifier_list, para_no,w1,temp)
        paragraphs = response.split('\n')[:]
        filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
        resp = []
        for para in filtered_paragraphs:
            resp.append({"persona":identifier,"snippet":para})
        return {"response":resp,"w1":w1}
        # return {"personas": data.personas,"response":filtered_paragraphs,"w1":w1}
    
    except Exception as e:
        return {"text":e}

@app.post("/api/merge_with_main")
async def merge_with_main(data:InputDataOne):
    try:
        identifier_list = data.personas
        para_no = data.no_of_paragraphs[0]
        w1 = data.w1
        temp = data.temp
        response = load_merge_master(identifier_list, para_no,w1,temp)
        paragraphs = response.split('\n')[:]
        filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
        resp = []
        for para in filtered_paragraphs:
            resp.append({"persona":identifier_list[0],"snippet":para})
        return {"response":resp,"w1":w1}
        # return {"personas": data.personas,"response":filtered_paragraphs,"w1":w1}
    

    except Exception as e:
        print(e)
        return {"text":e}

@app.post("/api/upload_persona")
async def upload_new_persona(data:InputDataCsv):
    try:
        file_name = data.file_path
        csv_to_db(file_name)
        return {"response":"Personas uploaded successfully"}
    except Exception as e:
        return {"text":e}

@app.get("/api/get_personas")
async def get_personas_names():
    try:
        personas_list = persona_names()
        return {"personas_list":personas_list}
    except Exception as e:
        return {"exception":e}

@app.post("/api/save_snippets")
async def save_gen_snippets(data:InputPersonaSave):
    try:
        if len(data.snippets_list)<1:
            return {"response":"No snippet is selected"}
        else:
            list_of_obj = data.snippets_list
            # Create a dictionary to store personas as keys and lists of snippets as values
            result_dict = {}
            for item in list_of_obj:
                persona = item["persona"]
                snippet = item["snippet"]
                # If the persona is not in the result_dict, add it with an empty list
                if persona not in result_dict:
                    result_dict[persona] = []
                # Append the snippet to the persona's list of snippets
                result_dict[persona].append(snippet)
            # Convert the result_dict to a list of dictionaries
            list_of_obj = [{"persona": persona, "snippets": snippets} for persona, snippets in result_dict.items()]
            for obj in list_of_obj:
                persona_name = obj["persona"]
                snippets = obj["snippets"]
                response = save_snippets_tocsv(persona_name,snippets)
                # print(response)
            csv_file = "docs/csv/training - Sheet1.csv"
            csv_to_pdf_master(csv_file,"master.pdf")
            return response
    except Exception as e:
        print(e)
        return {"response":"Exception Occurred."}
    
@app.get("/api/download_csv")
async def download_csv():
    file_path = "database.csv"  # Update with the actual path
    if os.path.exists(file_path):
        return FileResponse(file_path, headers={"Content-Disposition": "attachment; filename=database.csv"})
    else:
        return {"error": "File not found"}

@app.post("/api/delete_csv")
async def del_csv():
    file_path = "database.csv"
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"response":"File deleted"}
    else:
        return {"response":"File not found"}

@app.post("/api/upload_csv")
async def upload_csv(file: UploadFile):
    try:
        file_name = f"uploaded_files/{file.filename}"
        print(file_name)
        # Save the uploaded CSV file to the server
        with open(file_name, "wb") as csv_file:
            csv_file.write(file.file.read())  
        
        csv_to_db(file_name) 
        os.remove(file_name)
        # Perform preprocessing on the uploaded CSV file
        response = {"response": "CSV file uploaded and processed successfully."}
        return response
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/delete_persona")
async def del_persona(data:InputDelPersona):
    try:
        for folder in data.personas:
            folder_dir = f"vector_db/{folder}"
            if os.path.isdir(folder_dir):
                shutil.rmtree(folder_dir)
        return{"response":"operation successfull."}
    except Exception as e:
        print(e)
        return {"response":"Exception occured"}

@app.post("/api/get_snippets")
async def get_snippets(data:InputgetSnippets):
    try:
        csv_file = "docs/csv/training - Sheet1.csv"
        persona = data.persona
        response = get_snippets_of_persona(csv_file,persona)
        return {"response":response,"persona":persona}
    except Exception as e:
        print(e)
        return {"response":"Exception Occurred."}


@app.post("/api/save_edited_persona")
async def save_edited_persona(data:InputreplaceSnippets):
    try:
        print(data)
        snippets_list = data.snippets_list
        persona = data.persona
        csv_file = "docs/csv/training - Sheet1.csv"
        response = replace_edited_persona(csv_file,persona,snippets_list)

        if response == True:
            update_db = update_content(persona,snippets_list)
            csv_to_pdf_master(csv_file,"master.pdf")
            return {"response":"Operation successfull"}
        elif response == False:
            return {"reponse":"Operation Unsuccessfull. Persona isn't found."}
        else:
            return {"reponse":"File not found"}
    except Exception as e:
        print(e)
        return {"reponse":"Exception occurred."}

@app.get("/api")
async def test():
	return "hello g"

# Serve React App
@app.get("/")
@app.get("/{path:path}")
async def serve_index():
    return FileResponse("static/index.html")

if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)