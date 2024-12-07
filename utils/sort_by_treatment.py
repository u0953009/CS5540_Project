'''
Place this in the parent folder of Analyzed_Levas
Place FINAL_SCANDATA.xlsx in the same folder as this python file is
Remove all other files which are not images in Analyzed_Levas folder
'''

import os
import pandas as pd
import sys
import shutil


image_folder = 'Analyzed_Leaves/'
excel_file_name = 'FINAL_SCANDATA.xlsx'
sorted_folder_name = 'sorted_images'  # make folders by treatment


# maker folders to put sorted images
os.mkdir(sorted_folder_name)
os.mkdir(sorted_folder_name+'/1')
os.mkdir(sorted_folder_name+'/10')
os.mkdir(sorted_folder_name+'/50')
os.mkdir(sorted_folder_name+'/100')



# read excel data file
df  = pd.read_excel(excel_file_name)


# plant id dictionary
plant_id_d ={}
for idx in range(len(df['Plant ID'])):
    plant_id_d[df['Plant ID'][idx].split('-')[1]] = df['Treatment'][idx]




# image file name list
image_file_name_list = os.listdir('./'+image_folder)

# sort iamges
for image_name in image_file_name_list:
    if image_name.split('.')[-1]=='jpg':
        if image_name.split('-')[1] in plant_id_d:
            treatment=plant_id_d[image_name.split('-')[1]]
            destination_folder_name = sorted_folder_name+'/'+str(treatment)+'/'
            shutil.copy(image_folder+image_name, destination_folder_name+image_name)
        
    
