import json


def read_config():
    with open("config.json") as f:
        data = json.load(f)
        return data


def format_session(session, parts):
    date = parts[2]
    start = parts[4]
    end = parts[5]
    current = date + ", " + start + "-" + end + ", session: " + session
    current = current.strip().replace('"', '')
    return current


