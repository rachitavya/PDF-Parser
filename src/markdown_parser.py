from utils import *
import csv
import os

def create_chunks(file_name):
    # file_name='CONTRIBUTING.md'
    md_file=open(file_name,'r',encoding='utf-8')
    md=md_file.read()
    chunks=md.split('\n')
    return chunks


def combine_chunks(chunks):
    i=0
    combined_chunks=[]
    temp=['#','## ','### ','#### ','##### ','###### ','-','*','|']
    while i<len(chunks):
        
        if chunks[i]=='':
            combined_chunks.append({'type':'return','content':chunks[i]})
            i=i+1
        # elif chunks[i].startswith('|'):
        elif chunks[i].startswith('|') and len(chunks[i])!=1:
            chunk,i=table_parser(chunks[i:],i)
            combined_chunks.append({'type':'table','content':chunk})
            
        elif chunks[i].startswith('# ') or chunks[i].startswith('## ') or chunks[i].startswith('### ') or chunks[i].startswith('#### ') or chunks[i].startswith('##### '):
            combined_chunks.append({'type':'heading','content':chunks[i]})
            i=i+1
        
        elif chunks[i].startswith('- ') or chunks[i].startswith('* '):
            chunk,i=para_parser(chunks[i:],i)
            combined_chunks.append({'type':'list','content':chunk})

        # elif chunks[i][0] not in temp and (i+1)!=len(chunks):
        elif (chunks[i][0] not in temp and (i+1)!=len(chunks)) or chunks[i]=='|':
            chunk,i=para_parser(chunks[i:],i)
        
            # chunk=chunks[i].strip()
            if len(chunk)==0:
                i=i+1
                continue
            combined_chunks.append({'type':'para','content':chunk})
            # i=i+1
            
        else:
            i=i+1
        
    combined_chunks = [chunk for chunk in combined_chunks if chunk['type'] != 'return']
    return combined_chunks

def assign_headings(combined_chunks):
    id_counter = {'1': 0, '2': 0, '3': 0,'4':0,'5':0} 
    parent_stack = [] 
    
    for chunk in combined_chunks:
        if chunk['type'] == 'heading':
            level = chunk['content'].count('#')
#             level=count_level(chunk['content'])
#             print('hehe',level)
            id_counter[str(level)] += 1
            chunk['id'] = f'{level}{id_counter[str(level)]}'
            
            if parent_stack==[] or level==1:
                parent_stack = [chunk['id']]
            else:
                buff=int(str(parent_stack[0])[0])-1
                while len(parent_stack)>=(level-buff):
                    parent_stack.pop()
                parent_stack.append(chunk['id'])
            chunk['parents'] = parent_stack[:-1]
#             print(parent_stack)
            
        else:
            chunk['parents'] = parent_stack.copy() if parent_stack else []
    
    return combined_chunks

def get_subheading(final_chunks,index):
    headings={}
    for chunk in final_chunks:
        if chunk['type']=='heading':
            headings[chunk['id']]=chunk['content']
    subheadings=''
    for heading in final_chunks[index]['parents']:
        subheadings+=(' '.join(headings[heading].split()[1:]))+','
    return subheadings[:-1]

#CSV columns: chunkId,content,StartPage,EndPage,heading,ContentWordCount,pdfName,contentType,image,summary
def export_csv(file_name,final_chunks):  
    output_filename=file_name.split('.')[0]+'.csv'
    output_filename=output_filename.replace('input/md','output')
    # print(output_filename)
    with open(output_filename,'w') as file:
        csv_writer = csv.writer(file)
        data=['chunkId','content','StartPage','EndPage','heading','ContentWordCount','pdfName','contentType','image','summary']
        csv_writer.writerow(data)

    for i,chunk in enumerate(final_chunks):
        chunkId=i+1
        content=chunk['content'].strip()
        heading=get_subheading(final_chunks,i)
        contentType=chunk['type']
        ContentWordCount=len(content.split()) if contentType!='table' else len(''.join(content.split('|')).split())
        pdfName=file_name.split('.')[0]+'.pdf'
        data=[chunkId,content,'','',heading,ContentWordCount,pdfName,contentType,'','']
        
        with open(output_filename,'a',encoding='utf-8',newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data)
    


if __name__ == '__main__':
    input_folder='input/md/'
    all_files = []#['input/md/english/RevisedPM-KISANOperationalGuidelines(English).md']

# Iterate through the main folder and its subfolders
    for folder, subfolders, files in os.walk(input_folder):
        full_file_paths = [os.path.join(folder, file) for file in files]
        all_files.extend(full_file_paths)
    
    for file in all_files:
    # file='E:\PDF-Parser\input\md\hindi\Natural_Farming_Kharif_Booklet.md'
        print('Currently on',file)
        chunks=create_chunks(file_name=file)
        combined_chunks=combine_chunks(chunks)
        final_chunks=assign_headings(combined_chunks)
        export_csv(file,final_chunks)
    # print(e)



