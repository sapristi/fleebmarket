import requests
import json

def get_palettes_raw():
    response = requests.post("https://colorhunt.co/hunt.php", data={"step": 0, "sort": "popular"})
    return response.content

def get_palettes(data_raw):
    indices = (
        data_raw.index(b"["),
        # data_raw.rindex(b"]")
        data_raw.rindex(b",")
    )
    array_raw = data_raw[indices[0]:indices[1]]
    array = json.loads(array_raw + b"]")
    palettes = [
        (p['code'][0:6], p['code'][6:12], p['code'][12:18], p['code'][18:24])
        for p in array
    ]

    return palettes
