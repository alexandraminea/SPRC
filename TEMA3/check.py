import datetime
import random
from random import randrange

s = "2019-11-27 20:35:57+02:00"
print(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S%z"))
print(datetime.datetime.utcnow())

{
"BAT" : 99 ,
"HUMID" : 40,
"PRJ" : "SPRC",
"TMP" : 25.3,
"status" : "OK",
"timestamp" : "2019-11-26 03:54:20+03:00"
}

for i in range(0, 10):
    td = random.random() * datetime.timedelta(days=1)
    avgString = str(td).split(".")[0]
    timestamp = "2021-01-06T" + avgString + "+02:00"
    dd = "{\"BAT\":" + str(randrange(100)) + ", " + "\"timestamp\":\"" + timestamp + "\"}"
    d = {"BAT": randrange(100), "timestamp" : timestamp}
    print(dd)