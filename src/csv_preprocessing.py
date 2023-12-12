import os
from utils import *

def translating_hindi_csvs(file):
    df=pd.read_csv(file)
    df = df.rename(columns={'content': 'originalLanguageChunk','heading':'originalLanguageHeading'})
    print('translating',file)
    df['content'] = df.apply(lambda row: translate_text_bhashini(row['originalLanguageChunk'])[0] if row['contentType'] != 'table' else row['originalLanguageChunk'], axis=1)
    df['heading'] = df.apply(lambda row: translate_text_bhashini(row['originalLanguageHeading'])[0] if row['contentType'] != 'table' else row['originalLanguageHeading'], axis=1)
    df=df[['chunkId','content','heading','originalLanguageChunk','StartPage','EndPage','originalLanguageHeading','ContentWordCount','pdfName','contentType','image','summary']]
    df.to_csv(file)
    print('translating done')

if __name__ == '__main__':
    
    hindi_files=[]
    english_files=[]
    for folder, subfolders, files in os.walk('output/hindi'):
        full_file_paths = [os.path.join(folder, file) for file in files]
        hindi_files.extend(full_file_paths)

    for folder, subfolders, files in os.walk('output/english'):
        full_file_paths = [os.path.join(folder, file) for file in files]
        english_files.extend(full_file_paths)

    all_files=hindi_files+english_files

    for file in hindi_files:
        translating_hindi_csvs(file)
    
    for file in all_files:
        