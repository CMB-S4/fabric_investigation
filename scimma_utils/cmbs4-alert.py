"""

   Prototype Formating, publishing and cataloging  alerts

   Goals:
      social 
      - Produce some sort fo exampel of what wild be in a published alert.
      - Get peopel Clucking.
      - PRovide a BOE for a real work item

      techincal 
      - Add invariant information to alert (support low bandwidth link).
      - Format alert consisent with pracices on broker.
      - Catalog every undecorated alert.
      - Catalog  every published alert.
      - Make liveness of agent mesureable.
      - Log significant actions.
"""
import sqlite3
import logging
import random
import time
import datetime
import numpy as np

class Catalogger:
    """
    Catalog an Alert

    While the final alert catalog is managed by data movement,
    with TBD interface, as an interim measure put the data in
    an sqlite database.
    """

    def __init__(self, db_file="pulished.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        sql = """
           CREATE TABLE IF NOT EXISTS alert (
                  id         INTEGER,
                  telescope  TEXT,
                  ra         FLOAT,
                  dec        FLOAT,
                  time       DATETIME,
                  cutout90   TEXT,
                  cutout150  TEXT
        )
        """
        self.conn.execute(sql)
        self.conn.commit()

    def save(self, undecorated):
        pass

class Undecorated_alert:
    """
    For now just make a mock alert
    Its imagined that the recieved undecorated alerts wlll
    be a in  compact binary form, given the limited baseline
    networking.
    """
    def __init__(self):
        self.ra   = -50.0       # float
        self.dec  = 40.0      # float
        self.telescope =  'CHLAT1'
        self.flux90MJy = 30
        self.flux150MJy = 10
        self.time = time.time()       # unix time in seconds
        self.cutout_rows = 10
        # 100 floats in rwo-major form just junk right now.
        self.cutout90 = np.random.uniform(low=0.10, high=40.0, size=100) 
        self.cutout150 =  np.random.uniform(low=0.10, high=40.0, size=100) 

    
class Scimma_alert:
    def __init__(self, undecorated_alert, salt):

        ua = undecorated_alert
        alert = {}
        alert['issuer'] = 'CMB-S4'
        alert['version'] = 1
        alert['alert-type'] = 'intial-detection'
        # time + this id uniquely identifies this alert 
        alert['id-salt'] = salt
        detection  = {}
        alert['detection'] = detection
        detection['Telescope']  = ua.telescope 
        detection['RA']         = ua.ra
        detection['DEC']        = ua.dec 
        detection['flux90MJy']  = ua.flux90MJy 
        detection['flux150MJy'] = ua.flux150MJy 
        detection['time']       = datetime.datetime.utcfromtimestamp(ua.time).isoformat() 
        detection['cutout_size']=  '10x10'
        detection['cutout90']   =  ua.cutout90.np.around(x,decimals=2))reshape(10,10).tolist()
        detection['cutout150']  =  ua.cutout150.reshape(10, 10).tolist()
        self.alert = alert
        
    def send(self):
        """
        publish alert to community
        """
        import pprint
        pprint.pprint(self.alert, compact=True, width=200)


ua = Undecorated_alert()
salt =  int(random.random()*1E4)
sa = Scimma_alert(ua, salt)
sa.send() 
