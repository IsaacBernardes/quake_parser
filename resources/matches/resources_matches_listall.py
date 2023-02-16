import json
from configparser import ConfigParser


def listall_handler(request=None):

    try:
        settings = ConfigParser()
        settings.read("settings.ini")
    except Exception as ex:
        return 400, {"message": "An error occurred while reading the settings file", "error": str(ex)}

    try:
        data_file = open(settings["data"]["output_file"], "r")
        data = json.loads('\n'.join(data_file.readlines()))
        data_file.close()
    except Exception as ex:
        return 400, {"message": "An error occurred while reading the data file", "error": str(ex)}

    if request is not None:
        match_id = request.get("match_id")
        if match_id is not None:
            data = data.get(match_id, {})

    return 200, data
