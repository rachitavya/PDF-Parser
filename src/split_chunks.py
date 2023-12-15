import pandas as pd
import re

def split_chunks(df, upper_limit=200):
    new_rows = []
    count=0
    for index, row in df.iterrows():
        
    
        word_count = row['ContentWordCount']
        content = row['content']
        
        if int(word_count) > upper_limit and (row['contentType']=='para' or row['contentType']=='list'):
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|;|\?)\s', content)
            
            
            chunks = []
            current_chunk = []
            for sentence in sentences:
                # print(sentence)
                
                temp=' '.join(current_chunk + [sentence])
                if len(temp.split()) <= upper_limit:
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

def merge_small_chunks(df,lowerLimit=20):
    df['status']='visited'
    rows = df.to_dict(orient='records')
    size=len(rows)
    i=0
    lowerLimit=40
    while i<size:
        
        row=rows[i]
        if row['contentType']=='table':
            i+=1
            continue
        if row['status']=='unvisited':
            i+=1
            continue
        # print(row['chunkId'])
        
        stat=(i/size)*100
        print(stat,'% done',end='\r')
        prev_row=rows[i-1] if i>0 else None
        next_row=rows[i+1] if i<size-1 else None
        
        # if type(str(next_row))=='pandas.core.series.Series':

        # merged_rows = []
        # current_row = None
        temp=1
        while row['ContentWordCount']<lowerLimit:
            print('here')
            
            if isinstance(next_row, dict):
                
                same_type=(row['contentType']==next_row['contentType'])
                same_heading=row['heading']==next_row['heading']
                valid_word_count=row['ContentWordCount']+next_row['ContentWordCount']<200 
            else:
                same_type=same_heading=valid_word_count=False            
            if isinstance(prev_row, dict):
                psame_type=(row['contentType']==prev_row['contentType'])
                psame_heading=(row['heading']==prev_row['heading'])
                pvalid_word_count=row['ContentWordCount']+prev_row['ContentWordCount']<200
            else:
                psame_type=psame_heading=pvalid_word_count=False
        
            if  same_type and same_heading and valid_word_count:
                print('here')
                row['content']+=next_row['content']
                row['ContentWordCount']+=next_row['ContentWordCount']
                next_row['status']='unvisited'
                
            # elif same_type and not same_heading:
            elif psame_type and psame_heading and pvalid_word_count:
                row['content']+=prev_row['content']
                row['ContentWordCount']+=prev_row['ContentWordCount']
                prev_row['status']='unvisited'

            elif valid_word_count and same_heading:
                row['content']+=str(next_row['content'])
                row['ContentWordCount']+=next_row['ContentWordCount']
                next_row['status']='unvisited'

            elif pvalid_word_count and psame_heading:
                row['content']+=prev_row['content']
                row['ContentWordCount']+=prev_row['ContentWordCount']
                prev_row['status']='unvisited'

            elif valid_word_count:
                row['content']+=next_row['content']
                row['ContentWordCount']+=next_row['ContentWordCount']
                next_row['status']='unvisited'
                merged=str(row['heading'])+','+str(next_row['heading'])
                merged=list(set(merged.split(',')))
                
                row['heading']=','.join(merged)
            
            elif pvalid_word_count:
                row['content']+=prev_row['content']
                row['ContentWordCount']+=prev_row['ContentWordCount']
                prev_row['status']='unvisited'
                merged=str(row['heading'])+','+str(prev_row['heading'])
                merged=list(set(merged.split(',')))
                # row['heading']=','.join(list(set([(row['heading']+','+prev_row['heading'])].split(','))))

            else:
                print('reached')
                temp+=1
                
                prev_row=rows[i-temp] if i>temp-1 else None
                # print(prev_row)
                # break
                next_row=rows[i+temp] if i<size-temp else None
                # print(prev_row)
                
        # break
                # temp+=1
                # if i>temp-1:
                #      prev_row=rows[i-temp]
                # else:
                #     prev_row=None
                # next_row=rows[i+temp] if i<size-temp else None

        i+=1

    columns = ['chunkId', 'content', 'heading', 'originalLanguageChunk', 'StartPage', 'EndPage', 'originalLanguageHeading', 'ContentWordCount', 'pdfName', 'contentType', 'image', 'summary', 'status']

    new_df = pd.DataFrame(rows, columns=columns)
    new_df = new_df[new_df['status']=='visited']
    new_df=new_df.drop(columns=['status'])
    return new_df