# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 15:44:19 2024

@author: Yoonki
"""

#from bs4 import BeautifulSoup
import xmltodict
import cv2
import numpy as np





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


def crop_with_boxes(original_img, original_img_name, boxes, save_folder='', new_img_size=2000, background=False):
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
        if width<=0:
            width=2
        if height<=0:
            height=2
        
            
            
        
        cropped_img = original_img[top:top+height, left:left+width, :]
        
        if background:
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
        else:
            new_img_name = save_folder+img_name+'_'+str(img_count)+'.jpg'
            cv2.imwrite(new_img_name, cropped_img)
            img_count+=1
            
    return 0
# %%

# cro piamges for 50
label='1'
data_list = load_xml(label+'.xml')        
file_name, boxes = get_image_name_and_boxes(data_list)


# %%
folder_path= '../sorted_images/' +label+'/'
#for idx in range(len(file_name)):
for idx in range(44, len(file_name)):

    
    image_name = file_name[idx]
    image = cv2.imread(folder_path+image_name) 
    crop_with_boxes(image, image_name, boxes[idx], save_folder='../cropped_images/'+label+'/', new_img_size=2000,background=False)
    print(idx, 'done')




    



# %%

# cro piamges for 100
label='100'
data_list = load_xml(label+'.xml')        
file_name, boxes = get_image_name_and_boxes(data_list)


# %%
folder_path= '../sorted_images/' +label+'/'
for idx in range(len(file_name)):
#for idx in range(0, 44):

    
    image_name = file_name[idx]
    image = cv2.imread(folder_path+image_name) 
    crop_with_boxes(image, image_name, boxes[idx], save_folder='../cropped_images/'+label+'/', new_img_size=2000,background=False)
    print(idx, 'done')
