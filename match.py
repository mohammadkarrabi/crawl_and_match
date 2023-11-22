import cv2
import numpy as np
import time
import os
import shutil
#load image into variable
from tqdm import tqdm
template = cv2.imread('template.jpg')
w, h = template.shape[0], template.shape[1]

def main(im_list,outlist):
  seen = {}
  while True:
    no_new_image = True
    for im in tqdm(os.listdir(im_list), total=len(os.listdir(im_list))):
      if im not in seen:
        no_new_image = False
        img_rgb = cv2.imread(im_list+"/"+im)
        seen[im] = True
        #load template

        #read height and width of template image
        
        try:
          res = cv2.matchTemplate(img_rgb,template,cv2.TM_CCOEFF_NORMED)
          threshold = 0.8
          loc = np.where( res >= threshold)
          if len(loc[0])!=0:
            shutil.copy(im_list+"/"+im,outlist+"/"+im)
        except:
          continue
    print('end!')
    if no_new_image:
      time.sleep(5)     

os.makedirs('./images', exist_ok=True)
os.makedirs('./images/matched', exist_ok=True)
os.makedirs('./images/candidate', exist_ok=True)
main("./images/candidates","./images/matched")