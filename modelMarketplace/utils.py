import os
import yaml
import boto3
import shutil
import subprocess
import environ
from aiEngine.settings import DATA_DIRECTORY, MODEL_DIRECTORY, \
                                AWS_STORAGE_BUCKET_NAME, \
                                AWS_ACCESS_KEY_ID, \
                                AWS_SECRET_ACCESS_KEY

env = environ.Env()
environ.Env.read_env()

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def download_directory_from_s3(bucket, s3_directory, local_directory):
    
    paginator = s3.get_paginator('list_objects_v2')

    for result in paginator.paginate(Bucket=bucket, Prefix=s3_directory):
        if 'Contents' in result:
            for file_info in result['Contents']:
                s3_key = file_info['Key']
                local_path = os.path.join(local_directory, os.path.relpath(s3_key, s3_directory))
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                s3.download_file(bucket, s3_key, local_path)

    return True

def generate_yaml(data):
    file_path = 'yolo/yolov5/data.yaml'
    if not os.path.exists(file_path):
        with open('yolo/yolov5/data.yaml', 'w') as file:
            yaml.dump(data, file)
        return True
    
    else:
        print("File already exists!")
        return False

def prepare_data(datasetConfig):
    folder = datasetConfig.parent_folder.folder_path
    data_folder = folder + "/data/"
    
    download_result = download_directory_from_s3(AWS_STORAGE_BUCKET_NAME,
                               data_folder,
                               DATA_DIRECTORY)
    
    with open(DATA_DIRECTORY+'/classes.txt', 'r') as f:
        lines = f.readlines()
    names = [line.strip() for line in lines]
    
    CONFIG = {
        'path': f'{DATA_DIRECTORY}',
        'train': f'{DATA_DIRECTORY}/images/training',
        'val': f'{DATA_DIRECTORY}/images/validation',

        'nc': len(names),
        'names': names
    }
    yaml_result = generate_yaml(CONFIG)
    
    if download_result and yaml_result:
        return True
    else: 
        return False

def train_yolo(modelConfig, datasetConfig):
    train_command = f"python yolo/yolov5/train.py  \
                    --epochs {modelConfig.num_of_epochs} \
                    --data yolo/yolov5/data.yaml  \
                    --batch-size {modelConfig.batch_size}  \
                    --img-size {modelConfig.img_size}  \
                    --optimizer {modelConfig.optimizer}  \
                    --weights yolo/models/{modelConfig.yolo_choice}.pt"
    
    try:
        # Execute the training command using subprocess
        subprocess.check_output(train_command, shell=True, stderr=subprocess.STDOUT)
        result_path = datasetConfig.parent_folder.folders.get(folder_name='model').folder_path
        upload_folder_to_s3(AWS_STORAGE_BUCKET_NAME, result_path)
        clear_data()
        return True
    except subprocess.CalledProcessError as e:
        error_message = f"Training process failed with error: {e.output.decode('utf-8')}"
        print(error_message)
        clear_data()
        return False

def unique_index(s3_bucket, s3_folder_path):
    existing_folders = []
    s3_folder_path = s3_folder_path + "/exp"
    response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_folder_path, Delimiter='/')

    for prefix in response.get('CommonPrefixes', []):
        folder_name = prefix['Prefix'].strip('/')
        existing_folders.append(folder_name)

    try:
        last_folder_index = int(existing_folders[-1][-1]) + 1
    except IndexError:
        last_folder_index = 1

    return last_folder_index

def upload_folder_to_s3(s3_bucket, s3_folder_path):
    results_path = "yolo/yolov5/runs/train"

    last_folder_index = unique_index(s3_bucket, s3_folder_path)

    os.rename(results_path+"/exp", results_path+f"/exp{last_folder_index}")
    for root, dirs, files in os.walk(results_path):

        for file in files:
            local_file_path = os.path.join(root, file)
            s3_file_path = os.path.join(s3_folder_path, os.path.relpath(local_file_path, results_path))
            s3.upload_file(local_file_path, s3_bucket, s3_file_path)

def clear_data():
    file_path = 'yolo/yolov5/data.yaml'
    runs_path = 'yolo/yolov5/runs'
    for item in os.listdir(DATA_DIRECTORY):
        item_path = os.path.join(DATA_DIRECTORY, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(runs_path):
        shutil.rmtree(runs_path)
    if os.path.exists(MODEL_DIRECTORY):
        if len(os.listdir(MODEL_DIRECTORY)) > 0:
            for file in os.listdir(MODEL_DIRECTORY):
                os.remove(f'{MODEL_DIRECTORY}/{file}')
    