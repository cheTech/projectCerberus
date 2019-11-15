from PIL import Image
import numpy as np
import base64
import io
import json


def fromBase64imgToFile(str, filename):
    Image.open(io.BytesIO(base64.b64decode(str.split(",")[1]))).save(filename)

    return True


def normalizeEncoding(encoding):
    return json.dumps(encoding.tolist())
