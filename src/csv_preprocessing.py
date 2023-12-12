import os
from utils import *
from translate import *
from split_chunks import *
from gpt_response import get_gpt_response
import re


def translating_hindi_csvs(file):
    df=pd.read_csv(file)
    df = df.rename(columns={'content': 'originalLanguageChunk','heading':'originalLanguageHeading'})
    print('translating',file)
    df['content'] = df.apply(lambda row: translate_text_bhashini(row['originalLanguageChunk'])[0] if row['contentType'] != 'table' else row['originalLanguageChunk'], axis=1)
    df['heading'] = df.apply(lambda row: translate_text_bhashini(row['originalLanguageHeading'])[0] if row['contentType'] != 'table' else row['originalLanguageHeading'], axis=1)
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

    # translating hindi files
    # for file in hindi_files:
    #     translating_hindi_csvs(file)

    #creating empty columns to match hindi structure
    for file in english_files:
        df=pd.read_csv(file)
        df['originalLanguageChunk']=''
        df['originalLanguageHeading']=''
        df=df[['chunkId','content','heading','originalLanguageChunk','StartPage','EndPage','originalLanguageHeading','ContentWordCount','pdfName','contentType','image','summary']]
        df.to_csv(file)
    
    for file in english_files:
        df=pd.read_csv(file)
        print('splitting',file)
        split_chunks(df).to_csv(file) #split chunks
        # print('summarizing',file)
        # summary(file)


        