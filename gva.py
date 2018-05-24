from sys import argv
from os import makedirs
import os
from os.path import join, basename
import json
import requests
from base64 import b64encode
import sys

#from google.cloud import vision as GVA
#from google.cloud.vision import types

#GVA.text_detection()

APPKEY ="AIzaSyC90yKoswLGpPFMq0D0ni_n0Oh6Ty0fNqc"
ENDPOINT_URL = "https://vision.googleapis.com/v1/images:annotate"
RESULTS_DIR = "jsons"
makedirs(RESULTS_DIR,exist_ok=True)
ROOT = "../tmp"

pixel = 5

def make_image_data_list(input):
    """
    image_filenames is a list of filename strings
    Returns a list of dicts formatted as the Vision API
        needs them to be
    """
    #print(folder)
    img_requests = []


    with open(input, 'rb') as f:
            ctxt = b64encode(f.read()).decode()
            img_requests.append({
                     'image': {'content': ctxt},
                     'features': [{
                            'type': 'DOCUMENT_TEXT_DETECTION',
                           'maxResults': 1
                        }]
             })
    return img_requests

def make_image_data(input):
    """Returns the image data lists as bytes"""
    imgdict = make_image_data_list(input)
    return json.dumps({"requests": imgdict }).encode()


def request_ocr(api_key,input):
    response = requests.post(ENDPOINT_URL,
                             data=make_image_data(input),
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
    return response


if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    result = open(output_path, 'w')
    api_key= APPKEY
    folder = input_path
    if not api_key or not folder:
        print("""
            Please supply an api key, then one or more image filenames
            $ python cloudvisreq.py api_key image1.jpg image2.png""")
    else:
        response = request_ocr(api_key,input_path)
        if response.status_code != 200 or response.json().get('error'):
            print(response.text)
        else:
            for idx, resp in enumerate(response.json()['responses']):
                # save to JSON file
                imgname = folder[idx]
                jpath = join(RESULTS_DIR, basename(imgname) + '.json')
                with open(jpath, 'w') as f:
                    datatxt = json.dumps(resp, indent=2)
                    f.write(datatxt)
                t = resp['textAnnotations'][0]
                result.write(t['description'])
    n1 = 0
    lines = []
    with open(output_path, 'r+') as f:
        while True:
            line = f.readline()
            if not line: break
            for i in range(len(line) - 1):
                if line[i] == "{":
                    n1 += 1
                if line[i] == ':':
                    line = line[:i] + '=' + line[i + 1:]
            lines.append(line)
        f.seek(0)
        f.writelines(lines)
        f.close()

    with open(output_path, 'a') as f:
        while (n1 > 0):
            f.write("\n}")
            n1 -= 1

    with open(output_path, 'r') as f:
        while True:
            line = f.readline()
            if not line: break
            print(line, end='')
