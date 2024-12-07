import torch
import torchvision.transforms as transforms
from PIL import Image
import os
import random

# Load the image
#image_path = 'orig_img.jpg'
#image = Image.open(image_path)

# Define the transformations





original_path='../data/~~/cropped_images/'

# Directory to save augmented images
output_path = '../data/~~/augmented_images_2/'
os.makedirs(output_path, exist_ok=True)

classes=[1, 10, 50,100]

for label in classes:
    print(label)
    original_class_path = original_path+f'{label}/'
    image_list = os.listdir(original_class_path)

    output_path_class = output_path+f'{label}/'
    os.makedirs(output_path_class, exist_ok=True)

    # Apply transformations and save augmented images
    num_augmented_images = 10
    
    for image_path in image_list:
        image = Image.open(original_class_path + image_path)    
        
        for i in range(num_augmented_images):
            resize_factor = 0.3+random.random()*0.7
            transform = transforms.Compose([
            transforms.RandomRotation(random.random()*359),  # Randomly rotate images by up to 30 degrees
            transforms.RandomResizedCrop(size=(image.size[1], image.size[0]), scale=(resize_factor, resize_factor)),  # Randomly crop and resize
            transforms.RandomHorizontalFlip(p=0.5),  # Randomly flip images horizontally
            transforms.RandomAffine(degrees=random.random()*180, translate=(random.random()*0.1,  random.random()*0.1)),
            #transforms.ColorJitter(brightness=random.random(), contrast=random.random(), saturation=random.random(), hue=random.random()),  # Random color jitter
            #transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalize
            transforms.ToTensor()  # Convert the image to a tensor
            
             ])

            augmented_image = transform(image)

            augmented_image_pil = transforms.ToPILImage()(augmented_image)
            #augmented_image_pil.save(os.path.join(output_path, f'aug_{i}.jpeg'))
            augmented_image_pil.save(os.path.join(output_path_class, f'{image_path}_aug_{i}.jpeg'))

print("Image augmentation completed and saved to the specified folder.")
