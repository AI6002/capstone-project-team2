# Datasets VQA-2

Since the Dataset is So Huge we have added the download and Extract python file Setup Database as required.

## Directory and File Structure
```
.
+-- datasests/
|   +-- images/
|       +-- test2015/
|       +-- train2014/
|		+-- val2014/
|   +-- Annotations/
|		+-- <annotations>.json
| 	+-- Questions/
|       +-- <questions>.json
|   
```

## Download and unzip the dataset from official url of VQA: https://visualqa.org/download.html.
We have used VQA2 in for this project
```bash
python download_dataset.py
```
