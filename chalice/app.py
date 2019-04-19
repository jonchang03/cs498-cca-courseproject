from chalice import Chalice
from chalice import BadRequestError
import base64, os, boto3, ast
import numpy as np
import os
import cv2
from PIL import Image
import requests
import boto3
import h5py
import json
from io import BytesIO

app = Chalice(app_name='chalice')
app.debug = True

s3 = boto3.resource('s3')
bucket = s3.Bucket('test-bucket')
file_name = 's3://malariaimages498/cell_images/Parasitized/C100P61ThinF_IMG_20150918_144104_cell_168.png'
endpoint_name = 'sagemaker-tensorflow-2019-04-13-16-22-06-941'
#s3://sagemaker-us-east-1-554240446913/model/model.tar.gz
#s3://sagemaker-us-east-1-554240446913/model/test_X.h5

#h5f = h5py.File('s3://sagemaker-us-east-1-554240446913/model/test_X.h5','r')
s3client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
my_bucket = resource.Bucket('sagemaker-us-east-1-554240446913') #subsitute this for your s3 bucket name.
obj = s3client.get_object(Bucket='sagemaker-us-east-1-554240446913', Key='model/test_X.h5')
h5f = h5py.File(BytesIO(obj['Body'].read()))

test_X = h5f['test_X'][:]
h5f.close()

N = 0
data = test_X[0].reshape((1,64,64,3)).tolist()

client = boto3.client('runtime.sagemaker')

response = client.invoke_endpoint(EndpointName=endpoint_name, Body=json.dumps(data))
response_body = response['Body']
print(response_body.read())
