import ctypes
import locale
import os
import configparser
import json
import logging
import time
WORK_PATH = os.getcwd()
USER_PATH = os.path.expanduser('~')
CONFIG = configparser.ConfigParser()
THREADS = []
LOGGER = logging.getLogger("[ModSync]")
log_name = time.time()
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=f'logs\\log_{str(log_name).replace(".", "_")}.log',
                    filemode='w', level=logging.DEBUG)


def create_log_time():
    timestamp = time.localtime(time.time())
    time_y = str(timestamp.tm_year)
    time_M = str(timestamp.tm_mon)
    time_d = str(timestamp.tm_mday)
    time_h = str(timestamp.tm_hour).rjust(2, '0')
    time_m = str(timestamp.tm_min).rjust(2, '0')
    time_s = str(timestamp.tm_sec).rjust(2, '0')
    date_text = f"{time_y}/{time_M}/{time_d}"
    time_text = f"{time_h}:{time_m}:{time_s}"
    return f"[{date_text} {time_text}]"


class Color:

    def __init__(self, color, name, code):
        self.color = color
        self.name = name
        self.color_code = code


class COLORS:
    PINK = Color('[95m', "INFO", "#e4007f")
    BLUE = Color('[94m', "INFO", "#00a0e9")
    CYAN = Color('[96m', "INFO", "#00f0e8")
    GREEN = INFO = SUCCESS = Color('[92m', "INFO", "#4add43")
    YELLOW = WARNING = Color('[93m', "WARNING", "#ffff00")
    RED = ERROR = Color('[91m', "ERROR", "#ff0000")
    LIGHT_GRAY = Color('[37m', "COMMAND", "#c8c3bc")
    NONE = Color('[0m', "INFO", "#ffffff")
    BOLD = Color('[1m', "INFO", "#fffffe")
    UNDERLINE = Color('[4m', "INFO", "#fffffd")
    LIGHT_BLUE = Color('[4m', "INFO", "#a0c3fb")
    LIGHT_GREEN = Color('[4m', "INFO", "#41ff41")
    LIGHT_YELLOW = Color('[4m', "INFO", "#ffdf94")
    colors = [PINK, BLUE, CYAN, GREEN, YELLOW, RED, LIGHT_GRAY,
              NONE, BOLD, UNDERLINE, LIGHT_BLUE, LIGHT_GREEN, LIGHT_YELLOW]


if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32
    kernel32.GetUserDefaultUILanguage()
    default_lang = locale.windows_locale[kernel32.GetUserDefaultUILanguage()]

else:
    default_lang = locale.getdefaultlocale()[0]

language_lib = []

for file in os.listdir(f"{WORK_PATH}\\languages"):
    if file.endswith(".json"):
        language_lib.append(os.path.basename(file).replace(".json", "").lower())

if default_lang.lower() not in language_lib:
    default_lang = "en_us"

LANG_DICT = {}

for lang_file in os.listdir(f"{WORK_PATH}\\languages"):
    if lang_file.endswith(".json"):
        with open(f"{WORK_PATH}\\languages\\{lang_file}", 'rb') as file:
            # print(file.read())
            content = json.load(file)
            lang_code = lang_file.lower().replace(".json", "")
            LANG_DICT[content["language_name"]] = f"{lang_code}"

TEMP_PATH = f"{USER_PATH}\\AppData\\Local\\Temp"
LOCAL_PATH = f"{USER_PATH}\\AppData\\Local\\HLHT\\ModSync"


def init_config():
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH, exist_ok=True)
    if not os.path.exists(LOCAL_PATH):
        os.makedirs(LOCAL_PATH, exist_ok=True)
    with open(f"{LOCAL_PATH}\\config.ini", "w") as configfile:
        CONFIG["CONFIG"] = {
            "lang": default_lang,
            "mc_path": ".minecraft\\mods"
        }
        CONFIG["SELECTION"] = {
            "basic": "true",
            "addon": "false",
            "optim": "false",
            "shader": "false"
        }
        CONFIG.write(configfile)
    CONFIG.read(f"{LOCAL_PATH}\\config.ini")


def test_config():
    try:
        CONFIG.read(f"{LOCAL_PATH}\\config.ini")
        awa = CONFIG["CONFIG"]["lang"]
        awa = CONFIG["CONFIG"]["mc_path"]
    except KeyError as e:
        LOGGER.warning(str(e), f"{create_log_time()} [CONFIG]")
        init_config()


def save_config(*args):
    with open(f"{LOCAL_PATH}\\config.ini", "w") as config_f:
        CONFIG.write(config_f)


def boolean_to_str(boolean):
    if boolean:
        return "true"
    else:
        return "false"


def str_to_boolean(string):
    if string == "true":
        return True
    else:
        return False


def division(x, y):
    if 0 not in (x, y):
        return x / y
    else:
        return 0


test_config()
