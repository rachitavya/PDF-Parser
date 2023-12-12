import pandas as pd
import re

def split_chunks(df):
    new_rows = []
    count=0
    for index, row in df.iterrows():
        
    
        word_count = row['ContentWordCount']
        content = row['content']
        
        if int(word_count) > 300 and row['contentType']=='para':
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', content)
            
            
            chunks = []
            current_chunk = []
            for sentence in sentences:
                # print(sentence)
                
                temp=' '.join(current_chunk + [sentence])
                if len(temp.split()) <= 300:
                    current_chunk.append(sentence)
                    # print(current_chunk)
                    
                else:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [sentence]
            
            if current_chunk:
                chunks.append(' '.join(current_chunk))
    
            
            
            for chunk in chunks:
                count+=1
                new_row = {
                    'chunkId': index,  
                    'content': chunk,
                    'heading': row['heading'],
                    'originalLanguageChunk': row['originalLanguageChunk'],
                    'StartPage': row['StartPage'],
                    'EndPage': row['EndPage'],
                    'originalLanguageHeading': row['originalLanguageHeading'],
                    'ContentWordCount': len(chunk.split()),
                    'pdfName': row['pdfName'],
                    'contentType': row['contentType'],
                    'image': row['image'],
                    'summary': row['summary']
                }
                new_rows.append(new_row)
        else:
           
            count+=1
            new_rows.append({
                    'chunkId': count,
                    'content': content,
                    'heading': row['heading'],
                    'originalLanguageChunk': row['originalLanguageChunk'],
                    'StartPage': row['StartPage'],
                    'EndPage': row['EndPage'],            
                    'originalLanguageHeading': row['originalLanguageHeading'],
                    'ContentWordCount': word_count,
                    'pdfName': row['pdfName'],
                    'contentType': row['contentType'],
                    'image': row['image'],
                    'summary': row['summary']
            })


    new_df = pd.DataFrame(new_rows)
    return new_df