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
            current_para=current_para.strip()
            return (current_para,(index+i))            
        elif inside_para:
            if chunk[0] not in temp:
                inside_para=True
                current_para=current_para+' '+chunk
            else:
                current_para=current_para.strip()
                # if len(current_para)==0:
                #     return(current_para,'flag')
                return (current_para,(index+i))            
        elif (chunk[0] not in temp) or chunk!='|':
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

