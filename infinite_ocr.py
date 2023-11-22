from pathlib import Path
from fastapi import FastAPI, UploadFile, File
import uvicorn
import os
from typing import List
import json
import re
import shutil
import easyocr

app = FastAPI()
    
BASIC_GOALS_PATH = './basic_candidate_images'
EXTREME_GOALS_PATH = './extreme_candidate_images'
os.makedirs(BASIC_GOALS_PATH, exist_ok=True)
os.makedirs(EXTREME_GOALS_PATH, exist_ok=True)
os.makedirs('./images-uploaded', exist_ok=True)
os.makedirs('./ready-to-ocr', exist_ok=True)


def check_goal(txts):
    concated = ' '.join(txts)
    pattern = r'[A-Za-z1-9]{10}'
    matches = re.findall(pattern, concated)
    return matches != []



def check_extreme_goal(txts):
    concated = ' '.join(txts)
    pattern = r'\b[A-Za-z1-9]{10}\b'
    matches = re.findall(pattern, concated)
    #10 sequence
    return matches != [] and concated[1:].lower() != concated[1:] and any(num in concated for num in list('1234567890'))
        


def batcher(iterable, batch_size=1):
    l = len(iterable)
    for ndx in range(0, l, batch_size):
        yield iterable[ndx:min(ndx + batch_size, l)]

def get_batch_ocr(all_images):
    result =  ocr_model.readtext_batched(all_images, n_width=800, n_height=600, detail = 0)
    return result    

global ocr_model, seen_ids, image2txt
ocr_model = easyocr.Reader(['fa','en'], cudnn_benchmark=True) # this needs to run only once to load the model into memory

import glob
if __name__ == "__main__":
    seen_path_file = Path('seen_path.txt')
    image2txt_file = Path('image2txt.jsonl')
    seen_path_file.touch(exist_ok=True) 
    image2txt_file.touch(exist_ok=True) 
    seen_path = set(open('seen_path.txt').read().splitlines())
    image2txt = {}
    for line in open('image2txt.jsonl'):
        item = json.loads(line)
        image2txt[item['image']] = item['text']
    while True:
        ready_for_ocr = []
        for path in glob.iglob('./ready-to-ocr/*'):
            if path not in seen_path:
                    batch.append(ready_for_ocr)
            
        
        for batch in batcher(ready_for_ocr, 8):
            results = get_batch_ocr(batch)
            for path, texts in zip(ready_for_ocr, results):
                image2txt[path] = ' '.join(texts)
                if check_goal(texts):
                    shutil.copy(path, BASIC_GOALS_PATH)
                if check_extreme_goal(texts):
                    print(texts)
                    shutil.copy(batch, EXTREME_GOALS_PATH)

