import json
import os
import locale
import ctypes
from src.constants import *
import configparser

config = configparser.ConfigParser()

if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32
    kernel32.GetUserDefaultUILanguage()
    default_lang = locale.windows_locale[kernel32.GetUserDefaultUILanguage()]

else:
    default_lang = locale.getdefaultlocale()[0]


if not os.path.exists(f"{LOCAL_PATH}\\config.ini"):
    with open(f"{LOCAL_PATH}\\config.ini", "w") as configfile:
        config["CONFIG"] = {"lang": default_lang}
        config.write(configfile)


def load_lang():
    while True:
        try:

            config.read(f"{LOCAL_PATH}\\config.ini")

            if os.path.exists("languages\\" + config["CONFIG"]["lang"].lower() + ".json"):
                with open("languages\\" + config["CONFIG"]["lang"].lower() + ".json", "rb") as _file:
                    _LANG = json.load(_file)
            else:
                with open("languages\\en_us.json", "rb") as _file:
                    _LANG = json.load(_file)
            return _LANG

        except KeyError as e:
            LOGGER.warning(str(e), f"{create_log_time()} [CONFIG]")
            init_config()
            continue


LANG = load_lang()
