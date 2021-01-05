import datetime

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