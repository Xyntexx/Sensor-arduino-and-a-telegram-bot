import time
from tinydb import TinyDB, Query
TAIKANUMERO = 10080 #astetta

class Data:
    def __init__(self,name, pointer):
        self.name = name
        self.db = TinyDB(name+'.json')
        self.command = pointer
        self.now = 0.0
        self.minute=[]
        self.new = 0
        for i in self.db:
            self.minute.append((i["time"],i["value"]))

    def update(self):
        self.new += 1
        self.now = self.command()
        self.minute.append((time.strftime("%Y-%m-%d %H:%M"),self.now))

    def delta_short(self):
        length =len(self.minute)
        if length >= 5:
            delta = self.minute[-1][1]-self.minute[-5][1]
            return delta/5
        else:
            delta = self.minute[-1][1]-self.minute[0][1]
            return delta/length


    def delta_long(self):
        length =len(self.minute)
        if length >= 60:
            delta = self.minute[-1][1]-self.minute[-60][1]
            return delta*60/60
        else:
            delta = self.minute[-1][1]-self.minute[0][1]
            return delta*60/length

    def save(self):
        while self.new:
            self.db.insert({'time': self.minute[-self.new][0], 'value': self.minute[-self.new][1]})
            self.new -= 1
    
    def day()

    def week()