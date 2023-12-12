import requests
import json
import pandas as pd
import time

def table_parser(chunks,index):
    inside_table = False
    current_table = ''

    for i,chunk in enumerate(chunks):
        if inside_table:
            # Check if the current chunk is the end of the tablere
            if chunk.startswith('|') and len(chunk)!=1:
                inside_table = True
                current_table=current_table+'\n'+chunk
            else:
                
                return current_table,(index+i)
        elif chunk.startswith('|'):
            inside_table = True
            current_table=chunk
    #     elif chunk=='':
    #         continue
#         else:
#             print('post',(index+i))
#             return combined_chunks,(index+i)
    return 0

def para_parser(chunks,index):
    inside_para=False
    current_para=''
    temp=['#','## ','### ','#### ','##### ','###### ','-','|']
    for i,chunk in enumerate(chunks):
        if chunk=='':
            i=i+1            
        elif inside_para:
            if chunk[0] not in temp:
                inside_para=True
                current_para=current_para+' '+chunk
            else:
                current_para=current_para.strip()
                # if len(current_para)==0:
                #     return(current_para,'flag')
                return (current_para,(index+i))            
        elif chunk[0] not in temp:
            inside_para=True
            current_para=chunk
            
    return (current_para,(index+i))

def list_parser(chunks,index):
    inside_list=False
    current_list=''
    temp=['#','## ','### ','#### ','##### ','###### ','-','|']
    for i,chunk in enumerate(chunks):
        if inside_list:
            if chunk=='' or chunk.startswith('- ') or chunk.startswith('* '):
                return (current_list,(index+i))
            if chunk[0] not in temp:
                current_list=current_list+'\n'+chunk
        elif chunk.startswith('-') or chunk.startswith('* '):
            current_list=chunk
            inside_list=True
            
    return (current_list,(index+i))   

def translate_text_bhashini(input_text):
    url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

    payload = json.dumps({
        "pipelineTasks": [
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": "hi",
                        "targetLanguage": "en"
                    },
                    "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
                }
            }
        ],
        "inputData": {
            "input": [
                {
                    "source": input_text
                }
            ]
        }
    })
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Thunder Client (https://www.thunderclient.com)',
        'Authorization': 'sLAFJehUCZQ72NIM4nDZNCya7TQVzittLgJEU0vIf-69rp0gFUcGu5sjwAaOSUfa',
        'Content-Type': 'application/json'
    }

    retries = 0
    max_retries = 5
    start_time = time.time()
    while retries < max_retries:
        try:
            response = requests.post(url, headers=headers, data=payload)
            # Check if the request was successful
            if response.status_code == 200:
                translated_output = json.loads(response.text)['pipelineResponse'][0]['output'][0]['target']
                end_time = time.time()
                return translated_output, retries, end_time - start_time
            else:
                print(f"Request failed with status code {response.status_code}. Retrying...")
                retries += 1
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            retries += 1

    end_time = time.time()
    return "Translation failed after maximum retries.", max_retries, end_time - start_time