from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# sofang
SofangDB = client.SofangDB

# fang
FangDB = client.FangDB
GFsundeES = FangDB.get_collection('GFsundeES')
GFsundeXQ = FangDB.get_collection('GFsundeXQ')
GDSZES = FangDB.get_collection('GDSZES')

# anjuke
AnjukeDB = client.AnjukeDB

# housing
HousingDB = client.HousingDB

# fangjia
FangjiaDB = client.FangjiaDB
