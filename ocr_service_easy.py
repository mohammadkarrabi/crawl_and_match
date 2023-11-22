from fastapi import FastAPI, UploadFile, File
import uvicorn
import os
from typing import List
import json
import re
import shutil
import easyocr


app = FastAPI()


def get_ocr(image_path):
    return ocr_model.readtext(image_path, detail = 0)

BASIC_GOALS_PATH = './basic_candidate_images'
EXTREME_GOALS_PATH = './extreme_candidate_images'
os.makedirs(BASIC_GOALS_PATH, exist_ok=True)
os.makedirs(EXTREME_GOALS_PATH, exist_ok=True)


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
        

@app.post("/ocr")
async def perform_ocr(file: UploadFile = File(...)):
    # Save the uploaded image to a specific path
    file_path = f"./images-uploaded/{file.filename}"
    with open(file_path, "wb") as image_file:
        image_file.write(await file.read())

    # Perform OCR on the saved image using your OCR function
    result = ocr_model.ocr(file_path, cls=False)
    texts = [item[1][0][::-1] for item in result[0]]
    return {"texts": texts}


@app.post("/batch-ocr")
async def batch_ocr(files: List[UploadFile] = File(...)):
    seen_ids = set(open('seen-ids.txt').read().splitlines())
    final_out = {}
    for file in files:
        # Save each uploaded image to a specific path
        if file.filename not in seen_ids:
            file_path = f"./images-uploaded/{file.filename}"
            
            with open(file_path, "wb") as image_file:
                image_file.write(await file.read())
            texts =get_ocr(file_path)
            final_out[file.filename] = texts
            image2txt[file.filename] = ' '.join(texts)
            if check_goal(texts):
                 shutil.copy(file_path, BASIC_GOALS_PATH)
            if check_extreme_goal(texts):
                 print(texts)
                 shutil.copy(file_path, EXTREME_GOALS_PATH)

            with open('image2txt.jsonl', 'a') as out:
                new_item = {'image':file.filename, 'text':texts}
                out.write(json.dumps(new_item))
                out.write('\n')
            with open('seen-ids.txt', 'a') as f:
                f.write(file.filename)
                f.write('\n')
            
    return {"texts": final_out}
    

global ocr_model, seen_ids, image2txt
ocr_model = easyocr.Reader(['fa','en']) # this needs to run only once to load the model into memory
seen_ids = set(open('seen-ids.txt').read().splitlines())
image2txt = {}
for line in open('image2txt.jsonl'):
    item = json.loads(line)
    image2txt[item['image']] = item['text']

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8484)

