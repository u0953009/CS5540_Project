# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 15:44:19 2024

@author: Yoonki
"""

#from bs4 import BeautifulSoup
import xmltodict
import cv2
import numpy as np

import os
import pandas as pd
import sys
import shutil
#%%



'''
count=0


for k in dd['dataset']['images']['image']:
    #ab=dd['dataset']['images']['image'][k]
    
    
    if 'box' not in k:
        break
    if len(k['box'])>0:
        count+=1
    print(k['@file'])
    print(len(k['box']))

print(count)
'''

# %%

'''
folder_path = "../sorted_images/50/"


for k in dd['dataset']['images']['image']:
    #ab=dd['dataset']['images']['image'][k]
    
    
    if 'box' not in k:
        break
    if len(k['box'])>0:
        count+=1
    print(k['@file'])
    print(len(k['box']))
    print(k)


file_name =      dd['dataset']['images']['image'][0]['@file']
boxes= dd['dataset']['images']['image'][0]['box']


file_path = folder_path+file_name

img=cv2.imread(file_path)
'''
# %%%%%%





def load_xml(file_path, to_image_list=True):
    with open(file_path, 'r') as f:
        data= f.read()
    
    if to_image_list:
        return xmltodict.parse(data)['dataset']['images']['image']
    return xmltodict.parse(data)

def convert_boxes(boxes):
    # convert info about boxes for one image in dictionary to int list
    #boxes - list of dictionary 
    #{'@top': string, '@left':string, '@width':string, '@height': str}
    
    result=[]
    for i in range(len(boxes)):
        box_d = boxes[i]
        box = [int(box_d['@top']), int(box_d['@left']), int(box_d['@width']), int(box_d['@height']) ]
        result.append(box)
    
    # list of [top, left, width, height]
    return result

def get_image_name_and_boxes(data_list):
    
    file_name = []
    boxes=[]

    for image in data_list:
        if 'box' in image:
            file_name.append(image['@file'])
            if type(image['box']) != list:
                boxes.append(convert_boxes([image['box']] ))    
            else:
                boxes.append(convert_boxes(image['box']))
        else:
            print(image['@file'])
    
    return file_name, boxes


def crop_with_boxes(original_img, original_img_name, boxes, save_folder='', new_img_size=2000):
    # crop an image
    #original_image height x width x rgb
    #boxes - list of [top, left, width, height] (int)
    
    img_count=0
    img_name = original_img_name.split('.')[0]
    
    # iterate boxes and crop
    for i in range(len(boxes)):
        box=boxes[i]
        top,left,width, height = box[0], box[1], box[2], box[3]
        
        
        if top<0:
            top=0
        if left<0:
            left=0
        
            
            
        
        cropped_img = original_img[top:top+height, left:left+width, :]
        
        tmp_size =-99
        if width>new_img_size or height>new_img_size:
            
            new_img_size = width
            if height>width:
                new_img_size=height
            new_img = np.full((new_img_size, new_img_size,3), 255)
        else:
            new_img = np.full((new_img_size, new_img_size,3), 255)
        
        new_top = int(new_img_size/2 - height/2)
        new_left = int(new_img_size/2 - width/2 )
        
        new_img[new_top:new_top+height, new_left:new_left+width, :] = cropped_img
                               
        new_img_name = save_folder+img_name+'_'+str(img_count)+'.jpg'
        cv2.imwrite(new_img_name, new_img)
        img_count+=1
        
        if tmp_size>=0:
            new_img_size=tmp_size
    return 0
# %%

# cro piamges for 50
label='100'

folder_path= '../cropped_images/' +label+'/'
folder_path = "C:/Users/Yoonki/Desktop/Fall 2024/CS5540 Advanced Machine Learning/project/data/cropped_images/"+label+"/"
test_folder_path ="C:/Users/Yoonki/Desktop/Fall 2024/CS5540 Advanced Machine Learning/project/data/cropped_images_test/"+label+"/"
image_file_name_list = os.listdir(folder_path)

image_count=len(image_file_name_list)

index_to_pick= np.random.choice(image_count, int(image_count/10), replace=False)

file_names_for_test = np.array(image_file_name_list)[index_to_pick]

#full_path = np.array([folder_path])+file_names_for_test

for file_name in file_names_for_test:
    full_path = folder_path+file_name
    full_path_target = test_folder_path+file_name
    os.rename(full_path, full_path_target)


#%%
    


