import streamlit as st
import requests
from model import *
import pandas as pd
import os
import re
# Placeholder for generated text
# List of personas (You can modify this list as per your requirement)

# Create an empty DataFrame to store liked and edited text
liked_and_edited_df = pd.DataFrame(columns=["Persona", "Text"])

# Check if the CSV file already exists
csv_file = "database.csv"
file_name = "temporary.txt"
symbols_to_remove = "12345"
translator = str.maketrans('', '', symbols_to_remove)
print("here")
if not os.path.isfile(csv_file):
    # If the file doesn't exist, create it with headers
    liked_and_edited_df.to_csv(csv_file, index=False)

personas_dict = {'0venhead': '0venhead',
        '0xsparkling': '0xsparkling',
        '33ttiiffaannyy': '33ttiiffaannyy',
        '911reco911': '911reco911',
        'aboudin__': 'aboudin__',
        'adailyprovision': 'adailyprovision',
        'adaranoor': 'adaranoor',
        'alexandre7577': 'alexandre7577',
        'amblingwalker': 'amblingwalker',
        'ameliegatenko': 'ameliegatenko',
        'amienslogistics': 'amienslogistics',
        'anndronikos': 'anndronikos',
        'aprioribitch': 'aprioribitch',
        'babycigi': 'babycigi',
        'beaustonewall': 'beaustonewall',
        'bigethertrader': 'bigethertrader',
        'blondellnewbold': 'blondellnewbold',
        'bodegaman39': 'bodegaman39',
        'bubblesmcflie': 'bubblesmcflie',
        'buzzardbaxter': 'buzzardbaxter',
        'calmigen': 'calmigen',
        'casadiletto': 'casadiletto',
        'cashjewelsand': 'cashjewelsand',
        'checkthepackage': 'checkthepackage',
        'chowhoundchief': 'chowhoundchief',
        'cigman87': 'cigman87',
        'colorfulhughes': 'colorfulhughes',
        'constance_trebi': 'constance_trebi',
        'crimepaysweII': 'crimepaysweII',
        'debtmaxxxi': 'debtmaxxxi',
        'duro006': 'duro006',
        'eathepoor': 'eathepoor',
        'emcooper777': 'emcooper777',
        'enjoyglobohomo': 'enjoyglobohomo',
        'fermentingdream': 'fermentingdream',
        'fermentingdreams': 'fermentingdreams',
        'foggyneptune': 'foggyneptune',
        'harnomiqa': 'harnomiqa',
        'hearstdarling': 'hearstdarling',
        'ibringtheeheat': 'ibringtheeheat',
        'idkusername3123': 'idkusername3123',
        'ignaciadipper': 'ignaciadipper',
        'imthebaitedfool': 'imthebaitedfool',
        'ingeborg777777': 'ingeborg777777',
        'jakurpanggari': 'jakurpanggari',
        'jamesjenasill': 'jamesjenasill',
        'jufjuflofi': 'jufjuflofi',
        'justsaynotorugs': 'justsaynotorugs',
        'kanishatapping': 'kanishatapping',
        'lana_del_mar': 'lana_del_mar',
        'larainetill': 'larainetill',
        'leothe2ndor3rd': 'leothe2ndor3rd',
        'livelyarchively': 'livelyarchively',
        'lordofwaar': 'lordofwaar',
        'lovinglikelover': 'lovinglikelover',
        'luismartinez958': 'luismartinez958',
        'luma88530516': 'luma88530516',
        'lunadestarz': 'lunadestarz',
        'mamacobbler': 'mamacobbler',
        'marinawitchoxo': 'marinawitchoxo',
        'master': 'master',
        'n3w3ngag3m3nt': 'n3w3ngag3m3nt',
        'nanananalala_': 'nanananalala_',
        'nezbecfruitco': 'nezbecfruitco',
        'onaworkbreak': 'onaworkbreak',
        'outterweb': 'outterweb',
        'parmenide51': 'parmenide51',
        'pendinganotice': 'pendinganotice',
        'perangang': 'perangang',
        'Planetariuummmm': 'Planetariuummmm',
        'pmpkn111': 'pmpkn111',
        'ponziuspilates': 'ponziuspilates',
        'powersnaccc': 'powersnaccc',
        'Pradatada': 'Pradatada',
        'pseudochiller': 'pseudochiller',
        'ramwashburn': 'ramwashburn',
        'referralcode42': 'referralcode42',
        'reinseine': 'reinseine',
        'rifledrum': 'rifledrum',
        'robustrusso': 'robustrusso',
        'saganibo': 'saganibo',
        'sillynotsosilly': 'sillynotsosilly',
        'sittingsofia': 'sittingsofia',
        'supremematchaa': 'supremematchaa',
        'suwadacol': 'suwadacol',
        'TESTNET1': 'TESTNET1',
        'TESTNET2': 'TESTNET2',
        'theambling': 'theambling',
        'thedosahunter': 'thedosahunter',
        'thehumblefog': 'thehumblefog',
        'theroadoutandin': 'theroadoutandin',
        'tiptoeinmynikes': 'tiptoeinmynikes',
        'tomati11a': 'tomati11a',
        'tranquilixol': 'tranquilixol',
        'tuckedinandcozy': 'tuckedinandcozy',
        'twistingarms': 'twistingarms',
        'undisclos3dvibe': 'undisclos3dvibe',
        'unknow': 'unknow',
        'urlhostage': 'urlhostage',
        'wagmisista': 'wagmisista',
        'web2000000000': 'web2000000000',
        'wwwslashhttps': 'wwwslashhttps',
        'yalikeclockwork': 'yalikeclockwork',
        '__shark__fish__': '__shark__fish__'}
liked_paragraphs_df = pd.DataFrame(columns=["Persona", "Text"])
paragraphs_list = [1,2,3,4,5]
filtered_paragraphs = []
text_placeholder_haeding = st.empty()
text_placeholder_haeding.subheader('Generated Text')


with st.sidebar:
    # Streamlit Sidebar heading
    st.title("Generate Text")

    # Input component (Dropdown) for selecting the persona
    selected_persona = st.multiselect("Select a Persona:", personas_dict)
    if len(selected_persona) > 2:
        st.warning("Please select at most two characters.")

    # Input component (Dropdown) for selecting the persona
    no_of_paragraphs = st.selectbox("Select no of Paragraphs:", paragraphs_list)
    selected_weight = st.slider("Select weightage for First Persona", min_value=0, max_value=100, step=1)

    # Check Box for text box
    if st.checkbox("Check to Input Custom Prompt"):
        prompt = st.text_area("New Prompt: ")
        if st.button('Use New Prompt') and prompt is not None:
            generated_text = generate_text_CP_one(query=prompt)
            paragraphs = generated_text.split('\n')[:]
            filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
            with open(file_name, "w") as file:
                for item in filtered_paragraphs:
                    file.write(item + "\n")
        else:
            st.warning('Please Enter Prompt')

    # Buttons for generating text
    if st.button("Single Character"):        
        if len(selected_persona)==1:
            generated_text, prompt = generate_text_for_one(selected_persona, no_of_paragraphs)
            paragraphs = generated_text.split('\n')[:]
            filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
            print("also here")
            print(filtered_paragraphs)
            with open(file_name, "w") as file:
                for item in filtered_paragraphs:
                    file.write(item + "\n")

        else:
            st.warning("Please select ONLY one persona to generate text.")

    if st.button("Merge two Characters"):
        if len(selected_persona)==2 and selected_weight>0:
            print(selected_persona,no_of_paragraphs,selected_weight)
            generated_text = merge_two(selected_persona, no_of_paragraphs,selected_weight)
            paragraphs = generated_text.split('\n')[:]
            filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
            print("also here")
            print(filtered_paragraphs)
            with open(file_name, "w") as file:
                for item in filtered_paragraphs:
                    file.write(item + "\n")
 
        elif len(selected_persona)>2:
            st.warning("Please select maximum two personas to generate text.")
        elif len(selected_persona)<2:
            st.warning("Please select atleast two personas to generate merged context.")
        
        else:
            st.warning("Select a weightage for first character.")

    if st.button("Merge with Master"):

        if len(selected_persona)==1 and selected_weight>0:
            
            generated_text = merge_with_main(selected_persona, no_of_paragraphs,selected_weight)
            paragraphs = generated_text.split('\n')[:]
            filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
            with open(file_name, "w") as file:
                for item in filtered_paragraphs:
                    file.write(item + "\n")
            
        elif len(selected_persona)>1:
            st.warning("Please select only one persona to generate text.")
        else:
            st.warning("Please select a weighatge for persona.")

    if st.button("Generate for All"):
        generated_text_for_all = generate_text_for_all(list(personas_dict.values()),no_of_paragraphs)
        # text_placeholder.subheader("Generated Text for All Personas:")
        # text_placeholder.write(generated_text_for_all)
        paragraphs = generated_text_for_all.split('\n')[:]
        filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
        with open(file_name, "w") as file:
                for item in filtered_paragraphs:
                    file.write(item + "\n")
        selected_persona = []

    # Clear button to clear the generated text
    if st.button("Clear"):
        # text_placeholder.empty()
        if os.path.exists(file_name):
            os.remove(file_name)
        selected_persona = []

if os.path.exists(file_name):
    st.write(f"Name:{str(selected_persona)}")
 
    with open(file_name, "r") as file:
        read_list = [line.strip() for line in file]
    print("----------hello-------------")
    for i in range(1, len(read_list) + 1):
        print(f"---------->>>>>>>>>{i}")
        paragraph_number = i
        paragraph_text = read_list[i - 1]
        # paragraph_text = paragraph_text.translate(translator)
        # paragraph_text = paragraph_text.replace
        st.subheader(paragraph_number)
        st.write(paragraph_text)
        # print("-------",type(selected_persona[0]))
        # Create two columns for like and edit buttons
        col1, col2 = st.columns(2)

        # Like button for the paragraph
        if col1.button(f"Like Paragraph {paragraph_number}"):
            # Here, you can prompt the user to select a persona, and then add the liked paragraph to the DataFrame
            if len(selected_persona)>0:
                new_row = pd.DataFrame({"Persona": [selected_persona[0]], "Text": [paragraph_text]})
            elif len(selected_persona)==0:
                new_row = pd.DataFrame({"Persona": ["Mixed Personas"], "Text": [paragraph_text]})
            liked_paragraphs_df = pd.concat([liked_paragraphs_df, new_row], ignore_index=True)
            col1.success(f"Paragraph {paragraph_number} liked and saved successfully!")
        if col2.button(f"Dislike Paragraph {paragraph_number}"):
            col2.success(f"Paragraph {paragraph_number} disliked.")
        
    # st.write()


if not liked_paragraphs_df.empty:
    # st.subheader("Liked Paragraphs:")
    # st.write(liked_paragraphs_df)

    # Save the liked paragraphs to a CSV file immediately after liking
    
    liked_paragraphs_df.to_csv(csv_file, index=False, mode="a", header=False)

