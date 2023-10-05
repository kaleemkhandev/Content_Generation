import requests

def generate_text_CP_one(query):
    # Replace "YOUR_GENERATE_FOR_ALL_API_URL" with the URL of your generate-for-all API
    api_url = "http://143.110.225.38:8000/custom_prompt"
    # api_url = "http://0.0.0.0:8000/custom_prompt"
    print(query)
    response = requests.post(api_url, json={"query":[query]})
    if response.status_code == 200:
        return response.json()["text"]
    else:
        return "Error generating text."
    
# Function to call the API and get the generated text based on persona name
def generate_text_for_one(persona, no_of_paragraphs):
    # Replace "YOUR_GENERATE_API_URL" with the URL of your generate API
    api_url = "http://143.110.225.38:8000/generate_text"
    # api_url = "http://0.0.0.0:8000/generate_text"
    print(persona, no_of_paragraphs)
    response = requests.post(api_url, json={"personas": persona,"no_of_paragraphs":[no_of_paragraphs]})
    if response.status_code == 200:
        return response.json()["text"], response.json()["prompt"]
    else:
        return "Error generating text."

# Function to call the API and get the generated text for all personas
def generate_text_for_all(personas,no_of_paragraphs):
    # Replace "YOUR_GENERATE_FOR_ALL_API_URL" with the URL of your generate-for-all API
    api_url = "http://143.110.225.38:8000/generate_text_all"
    # api_url = "http://0.0.0.0:8000/generate_text_all"
    print(personas)
    response = requests.post(api_url, json={"personas": personas,"no_of_paragraphs":[no_of_paragraphs]})
    if response.status_code == 200:
        return response.json()["text"], 
    else:
        return "Error generating text for all personas."

# Function to call the API and get the generated text by merging two personas
def merge_two(personas,no_of_paragraphs,weight):
    # Replace "YOUR_GENERATE_FOR_ALL_API_URL" with the URL of your generate-for-all API
    api_url = "http://143.110.225.38:8000/merge_two"
    # api_url = "http://0.0.0.0:8000/merge_two"
    # print(personas)
    response = requests.post(api_url, json={"personas": personas,"no_of_paragraphs":[no_of_paragraphs],"w1":weight})
    if response.status_code == 200:
        return response.json()["text"]
    else:
        return "Error generating text for all personas."


# Function to call the API and get the generated text by merging it with the main pdf file
def merge_with_main(personas,no_of_paragraphs,weight):
    # Replace "YOUR_GENERATE_FOR_ALL_API_URL" with the URL of your generate-for-all API
    api_url = "http://143.110.225.38:8000/merge_with_main"
    # api_url = "http://0.0.0.0:8000/merge_with_main"
    print(personas)
    response = requests.post(api_url, json={"personas": personas,"no_of_paragraphs":[no_of_paragraphs],"w1":weight})
    if response.status_code == 200:
        return response.json()["text"]
    else:
        return "Error generating text for all personas."