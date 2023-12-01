import avro.schema
import time
import random

from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

def ef():
    "eleven random floats"
    return [float(random.random()) for f in range(11)] 

schema = avro.schema.parse(open("raw-alert.avsc", "rb").read())

writer = DataFileWriter(open("raw-alerts.avro", "wb"), DatumWriter(), schema)
writer.append(
    {"Telescope": "SPLAT",
     "flux90": 10.0,
     "flux150": 150.0,
     "ra" : 90.0,
     "dec" : -60.0,
     "time" : time.time(),
     "cutout90" :  [ ef(), ef(),  ef(), ef(), ef(), ef(),  ef(), ef(), ef(), ef(),  ef()  ],
     "cutout150" : [ ef(), ef(),  ef(), ef(), ef(), ef(),  ef(), ef(), ef(), ef(),  ef()  ]
     })
writer.close()

reader = DataFileReader(open("raw-alerts.avro", "rb"), DatumReader())
for alert in reader:
    print (alert)
reader.close()

print (f"payload is {5*4 + 11*11*2*4 + 5}")
