import openai
import pandas as pd
import math
import os

openai.api_key = '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'

def get_completion(prompt, model, temperature):

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(

    model=model,

    messages=messages,

    temperature=temperature,

    )

    return response.choices[0].message["content"]

def sample_list(samples):
    sample_string = """ """
    for s in samples:
        try:
            sample_string = sample_string + s + "\n"
        except:
            continue
    return sample_string

def create_numbered_list(strings):
    numbered_list = """\n""".join([f"{i + 1}. {string}" for i, string in enumerate(strings)])
    return numbered_list

def remove_nan_values(input_list):
    cleaned_list = [x for x in input_list if not (isinstance(x, float) and math.isnan(x))]
    return cleaned_list

def textgen(identifier:str,no_of_paragraphs:int,temp:float):
    
    df = pd.read_csv('docs/csv/training - Sheet1.csv')
    samples = df[identifier].tolist()

    samples = remove_nan_values(samples)
    ss = create_numbered_list(samples)
    
    n = no_of_paragraphs
    temperature = temp

    prompt = f"""
    Following are sample snippets of text from a specific writer:

    {ss}


    I want you to produce only {n} New snippets of text as if they are created by the same writer in the same writing style and tone. Every snippet of text should at max be of 250 characters.
    

    
    Strictly follow the following instructions:
    Remember to stay within the token limit.
    Do not give numbering to the generated snippets.
    Do not generate more than {n} snippets.
    Give each snippet in a new line Following this format;
    <The snippet> 
        
    """ 
    output = get_completion(prompt,"gpt-3.5-turbo", temperature)
    return output
    # gen = output.split("\n")
    # for g in gen:
    #     print(g + "\n")


if __name__ == "__main__":
    identifier = "hearstdarling"
    no_of_paragraphs = 4
    temp = 1.2
    response = textgen(identifier,no_of_paragraphs,temp)
    print(response)
    paragraphs = response.split('\n')[:]
    print(paragraphs)
    filtered_paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
    print(filtered_paragraphs)