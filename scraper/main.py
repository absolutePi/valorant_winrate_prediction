from api import Vlr as vlr

start = vlr()
# print(vlr.vlr_rankings("na"))
print(vlr.vlr_stats(region="na",timespan=30))