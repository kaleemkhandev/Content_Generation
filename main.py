import os
import tiktoken
import pandas as pd
import numpy as np
from utils import pdf_doc_loader, pdf_dir_loader
from utils import vector_database_creation
from utils import save_db, load_db, merge_db
from utils import query_database, query_database_personas , query_database_master_persona, query_custom_prompt
from utils_ind import textgen
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Spacer

def load_merge_2persons(identifier:list, no_para:int, w1:int,temp:float):
    merge_dbs = merge_db(db1_path=f"vector_db/{identifier[0]}", 
                         db2_path=f"vector_db/{identifier[1]}")
    text = query_database_personas(db=merge_dbs, identifier=identifier, no_of_paragraphs=no_para, w1=w1,temp=temp)
    
    return text

def load_merge_master(identifier:list, no_para:int, w1:int,temp:float):
    merge_dbs = merge_db(db1_path=f"vector_db/{identifier[0]}", 
                         db2_path=f"vector_db/master")
    text = query_database_master_persona(db=merge_dbs, identifier=identifier, no_of_paragraphs=no_para, w1=w1,temp=temp)
    
    return text

def custom_prompt(query,temp):
    char_list = os.listdir('vector_db')
    final_db = None
    persona_names = []
    for char in char_list:
        if char in query:
            persona_names.append(char)
            load_path = f"vector_db/{char}"
            db = load_db(path_to_db=load_path)

            if not final_db:
                final_db = db
            else:
                final_db.merge_from(db)
    if final_db is None:
        return "Please mention the name of the character and if already mentioned check your spellings..."
    
    text = query_custom_prompt(final_db, query,temp)

    return text,persona_names

def main(character, para_no,temp):
    text = textgen(identifier=character, no_of_paragraphs=para_no, temp=temp)
    return text
    
def csv_to_db(csv_file_prefix):
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file_prefix)

    # Define a style for the heading
    styles = getSampleStyleSheet()
    heading_style = styles["Heading1"]

    # Define a style for the bullet points
    bullet_style = styles["Normal"]
    bullet_style.leading = 12  # Adjust the line spacing for bullet points

    # Iterate through each column in the DataFrame
    db_files = os.listdir('vector_db')
    for column_name in df.columns:
        if column_name not in db_files:
            # Create a PDF file for the current column
            pdf_file = f"{column_name}.pdf"
            doc = SimpleDocTemplate(pdf_file, pagesize=letter)

            # Define a list to hold the content (Paragraphs)
            content = []

            # Add the column name as a heading
            heading = Paragraph('Name: ' + column_name, heading_style)
            content.append(heading)

            # Add each row in the column as a bullet point
            for value in df[column_name]:
                bullet = Paragraph(f"• {value}", bullet_style)
                content.append(bullet)

            # Build the PDF document for the current column
            doc.build(content)
            
            docum = pdf_doc_loader(pdf_file=column_name + '.pdf')
            db = vector_database_creation(pdf_document=docum)
            save_db(docsearch=db, save_path=f'vector_db/{column_name}')
            os.remove(f'{column_name}.pdf')
      
def persona_names():
    names = os.listdir("vector_db/")
    return names

def csv_to_pdf_master(csv_file, pdf_file):
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file)
    # Create a PDF file
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    # Define a list to hold the content (Paragraphs)
    content = []
    # Define a style for the heading
    styles = getSampleStyleSheet()
    heading_style = styles["Heading1"]
    # Define a style for the bullet points
    bullet_style = styles["Normal"]
    bullet_style.leading = 12  # Adjust the line spacing for bullet points
    # Iterate through each column in the DataFrame
    for column_name in df.columns:
        # Add the column name as a heading
        heading = Paragraph("Name: " + column_name, heading_style)
        content.append(heading)
        # Add each row in the column as a bullet point
        for value in df[column_name]:
            bullet = Paragraph(f"• {value}", bullet_style)
            content.append(bullet)
        # Add a spacer to separate columns
        content.append(Spacer(1, 12))
    # Build the PDF document
    doc.build(content)
    docum = pdf_doc_loader(pdf_file='master.pdf')
    db = vector_database_creation(pdf_document=docum)
    save_db(docsearch=db, save_path=f'vector_db/master')
    os.remove('master.pdf')

def update_content(persona:str, content_bot:list):
    # Load the CSV file into a DataFrame
    # csv_file = 'training - Sheet1.csv'  # Replace with your CSV file path
    csv_file = "docs/csv/training - Sheet1.csv"
    df0 = pd.read_csv(csv_file)
    cols = list(df0.columns)
    if persona not in cols:
        return None
    column_name = persona
    for content in content_bot:
        string_to_append = content
        df0.loc[len(df0[persona]), persona] = string_to_append
    df0.to_csv(csv_file, index=False)
    df1 = pd.read_csv(csv_file)

    # Define a style for the heading
    styles = getSampleStyleSheet()
    heading_style = styles["Heading1"]

    # Define a style for the bullet points
    bullet_style = styles["Normal"]
    bullet_style.leading = 12  # Adjust the line spacing for bullet points
    # # Create a PDF file
    pdf_file = f"{persona}.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    # Define a list to hold the content (Paragraphs)
    content = []

    # Add the column name as a heading
    heading = Paragraph('Name: ' + column_name, heading_style)
    content.append(heading)

    # Add each row in the column as a bullet point
    for value in df1[column_name]:
        bullet = Paragraph(f"• {value}", bullet_style)
        content.append(bullet)

    # Build the PDF document for the current column
    doc.build(content)
    # csv_to_pdf_master(csv_file,"master.pdf")

    docum = pdf_doc_loader(pdf_file=column_name + '.pdf')
    db = vector_database_creation(pdf_document=docum)
    save_db(docsearch=db, save_path=f'vector_db/{column_name}')
    os.remove(f'{column_name}.pdf')
    return 1

def save_snippets_tocsv(persona_name:str,snippets_list:list):

    try: 
        liked_paragraphs_df = pd.DataFrame(columns=["handle" ,"text", "medias", "schedule"])
        # If the file doesn't exist, create it with headers
        if not os.path.isfile("database.csv"):
            liked_paragraphs_df.to_csv("database.csv", index=False)
        for snippet in snippets_list:
            new_row = pd.DataFrame({"handle": [persona_name], "text": [snippet],"medias":[""],"schedule":[""]})
            liked_paragraphs_df = pd.concat([liked_paragraphs_df, new_row], ignore_index=True)
        liked_paragraphs_df.to_csv("database.csv", index=False, mode="a", header=False)

        update_db = update_content(persona_name,snippets_list)
        if update_db is not None:
            return {"response":"Snippets saved and persona updated Successfully."}
        else:
            return {"response":"Snippets saved Successfully. Persona couldn't be updated."}
        
    except Exception as e:
        print(e)
        return {"response":"Exception occurred."}

def get_snippets_of_persona(csv_file, writer_name):
    try:
        df = pd.read_csv(csv_file)
        if writer_name in df.columns:
            writer_lines = df[writer_name].tolist()
            writer_lines = [line for line in writer_lines if not pd.isna(line)]
            return writer_lines
        else:
            print(f"The writer '{writer_name}' does not exist in the CSV file.")
            return []
    except FileNotFoundError:
        print("The file does not exist.")
        return []

def replace_edited_persona(csv_file, writer_name, new_lines):
    try:
        df = pd.read_csv(csv_file)
        if writer_name in df.columns:
            # Calculate the number of existing rows
            num_existing_rows = len(df)
            
            # Ensure new_lines has at least as many elements as the number of existing rows
            if len(new_lines) < num_existing_rows:
                new_lines.extend([np.nan] * (num_existing_rows - len(new_lines)))
            
            df[writer_name] = new_lines
            df.to_csv(csv_file, index=False,encoding='utf-8-sig')
            print(f"Lines for '{writer_name}' have been replaced in the CSV file.")
            return True
        else:
            print(f"The writer '{writer_name}' does not exist in the CSV file.")
            return False
    except FileNotFoundError:
        print(f"The file '{csv_file}' does not exist.")
        return None
    
if __name__ == "__main__":

    idt, para_no = ["Planetariuummmm","ameliegatenko", "lordofwaar", "onaworkbreak", 
                    "luma88530516","fermentingdreams","main"], 1
    # response = main(idt)
    response = load_merge_master(identifier=["Planetariuummmm"], no_para=1, w1=60)
    print(response)