import time
from tinydb import TinyDB, Query
TAIKANUMERO = 60

class Data:
    def __init__(self,name, pointer):
        self.name = name
        self.db = TinyDB(name+'.json')
        self.command = pointer
        self.now = 0.0
        self.minute=[]
    
    def update(self):
        self.now = self.command()
        self.minute.insert(0, (time.strftime("%Y-%m-%d %H:%M"),self.now))

    def delta_short(self):
        length =len(self.minute)
        if length >= 5:
            delta = self.minute[0][1]-self.minute[4][1]
            return delta/5
        else:
            delta = self.minute[0][1]-self.minute[length-1][1]
            return delta/length


    def delta_long(self):
        length =len(self.minute)
        if length >= 60:
            delta = self.minute[0][1]-self.minute[60][1]
            return delta*60/60
        else:
            delta = self.minute[0][1]-self.minute[length-1][1]
            return delta*60/length

    def save(self):
        while (len(self.minute))>TAIKANUMERO:
            last = self.minute.pop()
            self.db.insert({'time': last[0], 'value': last[1]})
            
    def dumpall(self):
        while (self.minute):
            last = self.minute.pop()
            self.db.insert({'time': last[0], 'value': last[1]})