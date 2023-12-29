import os
from utils import *
from translate import *
from split_chunks import *
from gpt_response import get_gpt_response
import re
import time


def translating_hindi_csvs(file,source):
    df=pd.read_csv(file)
    df = df.rename(columns={'content': 'originalLanguageChunk','heading':'originalLanguageHeading'})
    print('translating',file)
    df['content'] = df.apply(lambda row: translate_text_bhashini(row['originalLanguageChunk'],source=source)[0] , axis=1)
    df['heading'] = df.apply(lambda row: translate_text_bhashini(row['originalLanguageHeading'],source=source)[0], axis=1) 
    df=df[['chunkId','content','heading','originalLanguageChunk','StartPage','EndPage','originalLanguageHeading','ContentWordCount','pdfName','contentType','image','summary']]
    df.to_csv(file)
    print('translating done')

def summary(file):
    system_prompt = """You are an AI bot that summarises user provided content in 5 sentences.
The content that you are shared is part of the Samagra Processes and Policy Corpus. The data was extracted from the PDF and has two sections - Heading and Content.
These will be provided to you to summarize in the folloowing format

Heading: <Heading>
Content: <Content>

You dont say anything else apart from the 5 sentence summary. Do not reproduce either the Heading or Content.
"""
    df = pd.read_csv(file)
    df['summary'] = ''
    for i in range(df.shape[0]):
        if df.loc[i,'contentType']!='heading':
            content = "Heading:" + str(df.loc[i,'heading']) + "\n" + "Content: " + str(df.loc[i,'content'])        
            df.loc[i,'summary'] =  get_gpt_response(system_prompt,content)
    df.to_csv(file)

def driver(file):

    # if language!='english':      
    if 'hindi' in file:     
        translating_hindi_csvs(file,source='hi')
    # if language=='english':
    if 'english' in file:     
        df=pd.read_csv(file)
        df['originalLanguageChunk']=''
        df['originalLanguageHeading']=''
        df=df[['chunkId','content','heading','originalLanguageChunk','StartPage','EndPage','originalLanguageHeading','ContentWordCount','pdfName','contentType','image','summary']]
        df.to_csv(file)

    print('on file', file)
    df=pd.read_csv(file)
    df_filtered = df[df['contentType'] != 'heading']
    df_filtered = df_filtered[df_filtered['ContentWordCount']!=0]     

    print('combining',file)
    combined_df=merge_small_chunks(df_filtered)
    
    print('splitting',file)
    splitted_df=split_chunks(combined_df)

    new_df = splitted_df[splitted_df['ContentWordCount']!=0]
    new_df.to_csv(file,index=False)

    # try:
    #     print('summarizing',file)
    #     summary(file)
    # except Exception as e:
    #     print('Error: ',e)
    
if __name__ == '__main__':
    
    hindi_files=[]
    english_files=[]

    # Getting hindi files
    for folder, subfolders, files in os.walk('output/hindi'):
        full_file_paths = [os.path.join(folder, file) for file in files]
        hindi_files.extend(full_file_paths)
    # getting english files
    for folder, subfolders, files in os.walk('output/english'):
        full_file_paths = [os.path.join(folder, file) for file in files]
        english_files.extend(full_file_paths)

    all_files=hindi_files+english_files

    for file in all_files:
        driver(file)