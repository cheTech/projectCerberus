from PIL import Image
import numpy as np
import base64
import io
import json
import cv2
import dlib


def fromBase64imgToFile(str, filename):
    Image.open(io.BytesIO(base64.b64decode(str.split(",")[1]))).save(filename)

    return True


def normalizeEncoding(encoding):
    return json.dumps(encoding.tolist())


def processFaceImage(img, face_location):
    top, right, bottom, left = face_location
    crop_img = img[int(top / 1.2):int(bottom * 1.2), int(left / 1.2):int(right * 1.2)]
    crop_img = image_resize(crop_img, width=100)
    return crop_img


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    try:
        dim = None
        (h, w) = image.shape[:2]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        resized = cv2.resize(image, dim, interpolation=inter)

        return resized
    except:
        print(h, w)
