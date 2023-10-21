import os
import urllib.request
import zipfile

# Create the directories
DATASETS_DIR = "../datasets"
ANNOTATIONS_DIR = os.path.join(DATASETS_DIR, "Annotations")
QUESTIONS_DIR = os.path.join(DATASETS_DIR, "Questions")
IMAGES_DIR = os.path.join(DATASETS_DIR, "Images")

os.makedirs(DATASETS_DIR, exist_ok=True)
os.makedirs(ANNOTATIONS_DIR, exist_ok=True)
os.makedirs(QUESTIONS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Download datasets from VQA official URL
# VQA Annotations
urllib.request.urlretrieve("https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Annotations_Train_mscoco.zip", os.path.join(ANNOTATIONS_DIR, "v2_Annotations_Train_mscoco.zip"))
urllib.request.urlretrieve("https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Annotations_Val_mscoco.zip", os.path.join(ANNOTATIONS_DIR, "v2_Annotations_Val_mscoco.zip"))

# VQA Input Questions
urllib.request.urlretrieve("https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Questions_Train_mscoco.zip", os.path.join(QUESTIONS_DIR, "v2_Questions_Train_mscoco.zip"))
urllib.request.urlretrieve("https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Questions_Val_mscoco.zip", os.path.join(QUESTIONS_DIR, "v2_Questions_Val_mscoco.zip"))
urllib.request.urlretrieve("https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Questions_Test_mscoco.zip", os.path.join(QUESTIONS_DIR, "v2_Questions_Test_mscoco.zip"))

# VQA Input Images (COCO)
urllib.request.urlretrieve("http://images.cocodataset.org/zips/train2014.zip", os.path.join(IMAGES_DIR, "train2014.zip"))
urllib.request.urlretrieve("http://images.cocodataset.org/zips/val2014.zip", os.path.join(IMAGES_DIR, "val2014.zip"))
urllib.request.urlretrieve("http://images.cocodataset.org/zips/test2015.zip", os.path.join(IMAGES_DIR, "test2015.zip"))

# Unzip the downloaded files
with zipfile.ZipFile(os.path.join(ANNOTATIONS_DIR, "v2_Annotations_Train_mscoco.zip"), 'r') as zip_ref:
    zip_ref.extractall(ANNOTATIONS_DIR)
with zipfile.ZipFile(os.path.join(ANNOTATIONS_DIR, "v2_Annotations_Val_mscoco.zip"), 'r') as zip_ref:
    zip_ref.extractall(ANNOTATIONS_DIR)

with zipfile.ZipFile(os.path.join(QUESTIONS_DIR, "v2_Questions_Train_mscoco.zip"), 'r') as zip_ref:
    zip_ref.extractall(QUESTIONS_DIR)
with zipfile.ZipFile(os.path.join(QUESTIONS_DIR, "v2_Questions_Val_mscoco.zip"), 'r') as zip_ref:
    zip_ref.extractall(QUESTIONS_DIR)
with zipfile.ZipFile(os.path.join(QUESTIONS_DIR, "v2_Questions_Test_mscoco.zip"), 'r') as zip_ref:
    zip_ref.extractall(QUESTIONS_DIR)

with zipfile.ZipFile(os.path.join(IMAGES_DIR, "train2014.zip"), 'r') as zip_ref:
    zip_ref.extractall(IMAGES_DIR)
with zipfile.ZipFile(os.path.join(IMAGES_DIR, "val2014.zip"), 'r') as zip_ref:
    zip_ref.extractall(IMAGES_DIR)
with zipfile.ZipFile(os.path.join(IMAGES_DIR, "test2015.zip"), 'r') as zip_ref:
    zip_ref.extractall(IMAGES_DIR)

# Remove unnecessary zip files
os.remove(os.path.join(ANNOTATIONS_DIR, "v2_Annotations_Train_mscoco.zip"))
os.remove(os.path.join(ANNOTATIONS_DIR, "v2_Annotations_Val_mscoco.zip"))

os.remove(os.path.join(QUESTIONS_DIR, "v2_Questions_Train_mscoco.zip"))
os.remove(os.path.join(QUESTIONS_DIR, "v2_Questions_Val_mscoco.zip"))
os.remove(os.path.join(QUESTIONS_DIR, "v2_Questions_Test_mscoco.zip"))

os.remove(os.path.join(IMAGES_DIR, "train2014.zip"))
os.remove(os.path.join(IMAGES_DIR, "val2014.zip"))
os.remove(os.path.join(IMAGES_DIR, "test2015.zip"))