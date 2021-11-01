from gpsdclient import GPSDClient

client = GPSDClient(host="127.0.0.1")

# get your data as json strings:
for result in client.json_stream():
    print(result)

# or as python dicts (optionally convert time information to `datetime` objects)
for result in client.dict_stream(convert_datetime=True):
    if result["class"] == "TPV":
        print("Latitude: %s" % result.get("lat", "n/a"))
        print("Longitude: %s" % result.get("lon", "n/a"))
