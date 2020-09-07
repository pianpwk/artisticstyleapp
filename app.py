from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
import json
import requests
from io import BytesIO
import imageio
from PIL import Image
import base64
import time
import numpy as np
import pandas as pd

import torch
import torchvision
import os
import matplotlib.pyplot as plt
import sys
import imageio
import shutil
import math
import random
import string
import pickle

import torch.nn as nn
from torchvision import transforms
from torchvision.utils import save_image

# PROGRESS
PROGRESS = {
    'image_upload': {},
    'style_transfer': {}
}

# # style transfer
# sys.path.insert(0, 'assets/pytorch-AdaIN')
# from pathlib import Path
# import net
# from function import adaptive_instance_normalization, coral

def test_transform(size, crop):
    transform_list = []
    if size != 0:
        transform_list.append(transforms.Resize(size))
    if crop:
        transform_list.append(transforms.CenterCrop(size))
    transform_list.append(transforms.ToTensor())
    transform = transforms.Compose(transform_list)
    return transform

def _style_transfer(token, vgg, decoder, content, style, alpha=1.0,
                   interpolation_weights=None):
    assert (0.0 <= alpha <= 1.0)
    content_f = vgg(content)
    PROGRESS['style_transfer'][token] = 'content feature'
    style_f = vgg(style)
    PROGRESS['style_transfer'][token] = 'style feature'
    if interpolation_weights:
        _, C, H, W = content_f.size()
        feat = torch.FloatTensor(1, C, H, W).zero_().to(device)
        base_feat = adaptive_instance_normalization(content_f, style_f)
        for i, w in enumerate(interpolation_weights):
            feat = feat + w * base_feat[i:i + 1]
        content_f = content_f[0:1]
    else:
        feat = adaptive_instance_normalization(content_f, style_f)
    feat = feat * alpha + content_f * (1 - alpha)
    PROGRESS['style_transfer'][token] = 'decoding'
    return decoder(feat)

# decoder = net.decoder
# decoder.load_state_dict(torch.load('assets/pytorch-AdaIN/models/decoder.pth'))
# vgg = net.vgg
# vgg.load_state_dict(torch.load('assets/pytorch-AdaIN/models/vgg_normalised.pth'))
# vgg = nn.Sequential(*list(vgg.children())[:31])

# content_tf = test_transform(512, False)

class RN18FE:
    
    def __init__(self, pth=None, n_classes=93):
        
        net = torchvision.models.resnet18(pretrained=False)
        if not pth is None:
            net.fc = nn.Linear(net.fc.in_features, n_classes, bias=True)
            net.load_state_dict(torch.load(pth, map_location=torch.device('cpu')))
        net.eval()
        
        self.net = net
        
    def extract(self, X):
        with torch.no_grad():
            X = self.net.conv1(X)
            X = self.net.bn1(X)
            X = self.net.relu(X)
            X = self.net.maxpool(X)

            X = self.net.layer1(X)
            X = self.net.layer2(X)
            X = self.net.layer3(X)
            X = self.net.layer4(X)
        return X
    
    def lastlayer(self, X):
        with torch.no_grad():
            X = self.net.avgpool(X)
            X = torch.flatten(X, 1)
            X = self.net.fc(X)
        return X

def torch_preprocess():
    
    return transforms.Compose([
        transforms.Resize(512),
        transforms.CenterCrop(512),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

# pca_model = pickle.load(open('assets/models/pca.pkl','rb'))
# data_features = np.load('assets/data/outputs/pca_features.npy')
data_filenames = []
for x_ in ['europeana','met','rijksmuseum']:
    f = open('assets/data/outputs/{}_filenames.txt'.format(x_),'r')
    for r in f:
        data_filenames.append(r.strip())
    f.close()
data_filenames = np.array(data_filenames)
model = RN18FE('assets/models/model_content_v2.pth')
urls = pd.read_csv('assets/data/all_urls.csv')
urls = {(row['dataset'],row['id']) : row['url'] for _,row in urls.iterrows()}
metadata = pd.read_csv('assets/data/metadata.csv')
metadata = {(row['dataset'],row['id']) : {
    'title':row['title'],
    'artist':row['artist'],
    'date':row['date']
} for _,row in metadata.iterrows()}

def read_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    return img

def normalize_avgpool(X):
    X = X.mean(dim=(2,3))
    mean,std = X.mean(dim=1).view(-1,1),X.std(dim=1).view(-1,1)
    return (X-mean)/std

def extract_feature(img, model):
    x = torch_preprocess()(img).unsqueeze(0)
    x = model.extract(x)
    x = normalize_avgpool(x)
    x = x.detach().cpu().numpy()
    return pca_model.transform(x)

def eucl_dist(X,Y):
    return np.sum(X*X,axis=1).reshape([-1,1]) - 2*np.matmul(X,Y.T) + np.sum(Y*Y,axis=1)

# configuration
DEBUG = False

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def helloWorld():
    return "Hello"

@app.route('/ping', methods=['GET'])
def ping():
    return 'OK'

# generate random string
def random_string(n):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(n))

@app.route('/progress_image_upload', methods=['POST'])
def progress_image_upload():
    token = json.loads(request.get_data())['token']
    if not token in PROGRESS['image_upload']:
        return 'not available'
    return PROGRESS['image_upload'][token]

@app.route('/progress_style_transfer', methods=['POST'])
def progress_style_transfer():
    token = json.loads(request.get_data())['token']
    if not token in PROGRESS['style_transfer']:
        return 'not available'
    return PROGRESS['style_transfer'][token]

@app.route('/request_image_upload', methods=['POST'])
def request_image_upload():
    token = random_string(16)
    while token in PROGRESS['image_upload']:
        token = random_string(16)
    return jsonify({'token': token})

@app.route('/image_upload', methods=['POST'])
def image_upload():
    data = json.loads(request.get_data())
    token = data['token']
    data = data['data'][5:]

    mimetype, imgstr = data.split(';base64,')
    img_bytes = imgstr.encode('utf-8')
    img = base64.decodebytes(img_bytes)

    img = Image.open(BytesIO(img)).convert('RGB')
    print("Image received")

    PROGRESS['image_upload'][token] = 'processing'

    x = extract_feature(img, model)
    print("Feature extracted")
    dists = eucl_dist(x, data_features)
    order = np.argsort(dists[0])
    print("Order determined")

    PROGRESS['image_upload'][token] = 'analyzed'

    def fillna(d):
        for k in d:
            if d[k] is None or (type(d[k]) is float and np.isnan(d[k])):
                d[k] = ''
        return d

    idx = 0
    result = []
    while len(result) < 6:
        # print('../data/small_images/'+data_filenames[order[idx]])
        img_ds,img_id = data_filenames[order[idx]].split('/')[-2:]
        k = (img_ds, img_id[:-4])
        try: # test if url is available and can be downloaded
            if k in urls and k in metadata:
                img = read_image(urls[k])
                shape = np.array(img).shape
                if shape[0] > 300 or shape[1] > 300:
                    result.append(fillna({
                        'url': urls[k],
                        'title': metadata[k]['title'],
                        'artist': metadata[k]['artist'],
                        'date': metadata[k]['date']
                    }))
                    PROGRESS['image_upload'][token] = 'done{}'.format(len(result))
        except:
            pass
        idx += 1
    print(result)
    del PROGRESS['image_upload'][token]
    return jsonify(result)

@app.route('/request_style_transfer', methods=['POST'])
def request_style_transfer():
    token = random_string(16)
    while token in PROGRESS['style_transfer']:
        token = random_string(16)
    return jsonify({'token': token})

@app.route('/upload_style_transfer', methods=['POST'])
def style_transfer():
    data = json.loads(request.get_data())
    token = data['token']
    PROGRESS['style_transfer'][token] = 'received'
    content_data,style_data = data['data']
    content_bytes = content_data.split(';base64,')[-1].encode('utf-8')
    style_bytes = style_data.split(';base64,')[-1].encode('utf-8')
    content_img = Image.open(BytesIO(base64.decodebytes(content_bytes))).convert('RGB')
    style_img = Image.open(BytesIO(base64.decodebytes(style_bytes))).convert('RGB')

    img = _style_transfer(
        token, vgg, decoder,
        content_tf(content_img).unsqueeze(0),
        content_tf(style_img).unsqueeze(0)
    )
    PROGRESS['style_transfer'][token] = 'finalizing'
    img = img.squeeze(0).permute(1,2,0)
    img = img.detach().cpu().numpy()
    img = img - np.min(img, axis=(0,1))
    img = img/np.max(img, axis=(0,1))
    img = np.array(img*255, dtype=np.uint8)
    PROGRESS['style_transfer'][token] = 'preparing'

    del PROGRESS['style_transfer'][token]
    imageio.imsave("assets/style_test.png", img)
    with open('assets/style_test.png', 'rb') as imf:
        b = imf.read()
        estr = base64.b64encode(b)
        return jsonify(str(estr)[2:-1])

if __name__ == '__main__':
    app.run()