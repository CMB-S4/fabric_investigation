"""
This code mocks an alert detcton

It   sends an alert to the alter publisher
"""

import requests
import avro.schema
import time
import random
import io 
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter, BinaryEncoder, BinaryDecoder


url = "http://localhost:8000/upload_raw"


files = {"file": ("image.jpg", open("image.jpg", "rb"), "image/jpeg")}

def ef():
    "eleven random floats"
    return [float(random.random()) for f in range(11)]

schema = avro.schema.parse(open("raw-alert.avsc", "rb").read())


writer = DatumWriter(schema)
bytes_writer = io.BytesIO()
encoder = BinaryEncoder(bytes_writer)
writer.write (
    {"Telescope": "SPLAT",
     "flux90": 10.0,
     "flux150": 150.0,
     "ra" : 90.0,
     "dec" : -60.0,
     "time" : time.time(),
     "cutout90" :  [ ef(), ef(),  ef(), ef(), ef(), ef(),  ef(), ef(), ef(), ef(),  ef()  ],
     "cutout150" : [ ef(), ef(),  ef(), ef(), ef(), ef(),  ef(), ef(), ef(), ef(),  ef()  ]
     }, encoder)
bytes_writer.seek(0)

response = requests.post(url, files={'file': ('filename', bytes_writer , "application/octet-stream")})

print(response.json())
