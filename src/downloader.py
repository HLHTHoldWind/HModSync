import zipfile
import os
import shutil
import urllib.request
from src.window import *
from src.constants import *

URL = "http://archives.hlhtstudios.com:3399/minecraft"


def check_version(master, force=False):
    master.set_title(LANG["sync.check_update"])
    master.set_progress(1)
    if not os.path.exists(f'{LOCAL_PATH}\\version.txt'):
        update = True
        urllib.request.urlretrieve(f"{URL}/hversion.txt",
                                   f"{LOCAL_PATH}\\version2.txt")
        with open(f'{LOCAL_PATH}\\version2.txt', 'r') as f:
            version2 = int(f.readline().strip())

    else:
        try:
            with open(f'{LOCAL_PATH}\\version.txt', 'r') as f:
                version = int(f.readline().strip())
            urllib.request.urlretrieve(f"{URL}/hversion.txt",
                                       f"{LOCAL_PATH}\\version2.txt")
            with open(f'{LOCAL_PATH}\\version2.txt', 'r') as f:
                version2 = int(f.readline().strip())

            if version != version2:
                update = True
            else:
                update = False
        except (ValueError, FileNotFoundError) as e:
            LOGGER.warning(str(e), f"{create_log_time()} [DOWNLOADER]")
            update = True
            urllib.request.urlretrieve(f"{URL}/hversion.txt",
                                       f"{LOCAL_PATH}\\version2.txt")
            with open(f'{LOCAL_PATH}\\version2.txt', 'r') as f:
                version2 = int(f.readline().strip())

    if force:
        update = True

    if update:
        if os.path.exists("mods2"):
            for path, dirs, files in os.walk("mods2"):
                for filename in files:
                    os.remove(f"{path}\\{filename}")

            for path, dirs, files in os.walk("mods2"):
                try:
                    os.rmdir(f"{path}")
                except OSError as e:
                    LOGGER.warning(str(e), f"{create_log_time()} [DOWNLOADER]")
            try:
                os.removedirs("mods2")
            except PermissionError as exception:
                LOGGER.critical(str(exception), f"{create_log_time()} [DOWNLOADER]")
                raise exception
        if os.path.exists("mods"):
            os.rename("mods", "mods2")
        master.update_progress(1)
        master.finish_progress()
        master.set_title(LANG["sync.download"])
        master.set_progress(5)
        urllib.request.urlretrieve(f"{URL}/basic.zip", "basic.zip")
        master.update_progress(1)
        urllib.request.urlretrieve(f"{URL}/addon.zip", "addon.zip")
        master.update_progress(1)
        # urllib.request.urlretrieve(f"{URL}/hdisc.zip", "hdisc.zip")
        master.update_progress(1)
        urllib.request.urlretrieve(f"{URL}/optimization.zip", "optimization.zip")
        master.update_progress(1)
        urllib.request.urlretrieve(f"{URL}/shader.zip", "shader.zip")
        master.update_progress(1)
        master.finish_progress()

        master.set_title(LANG["sync.extract"])
        master.set_progress(5)
        zipfile.ZipFile("basic.zip").extractall("mods\\basic")
        master.update_progress(1)
        zipfile.ZipFile("addon.zip").extractall("mods\\addon")
        master.update_progress(1)
        zipfile.ZipFile("optimization.zip").extractall("mods\\optimization")
        master.update_progress(1)
        zipfile.ZipFile("shader.zip").extractall("mods\\shader")
        master.update_progress(1)
        # zipfile.ZipFile("hdisc.zip").extractall("mods\\hdisc")
        master.update_progress(1)
        master.finish_progress()

        with open(f'{LOCAL_PATH}\\version.txt', 'w') as f:
            f.write(str(version2))

        master.set_title(LANG["sync.clean_cache"])
        master.set_progress(5)
        os.remove('basic.zip')
        master.update_progress(1)
        os.remove('addon.zip')
        master.update_progress(1)
        os.remove('optimization.zip')
        master.update_progress(1)
        os.remove('shader.zip')
        master.update_progress(1)
        # os.remove('hdisc.zip')
        master.update_progress(1)
        master.finish_progress()
        deleter(master)
    else:
        master.update_progress(1)
        master.finish_progress()

    if os.path.exists(f'{LOCAL_PATH}\\version2.txt'):
        os.remove(f'{LOCAL_PATH}\\version2.txt')


def adder(name: str, master):
    master.set_title(LANG["sync.sync_to_mods"].format(LANG[f"type.{name}"]))
    mod_path = CONFIG["CONFIG"]["mc_path"]
    cfg_path = os.path.dirname(CONFIG["CONFIG"]["mc_path"])+"\\config"

    mods = os.listdir(f"mods\\{name}")
    master.set_progress(len(mods)+2)

    os.makedirs(mod_path, exist_ok=True)
    os.makedirs(cfg_path, exist_ok=True)

    shutil.copy(f"{WORK_PATH}\\src\\resources\\createfood.json5", cfg_path)
    master.update_progress(1)

    for i in mods:
        shutil.copy(f"mods\\{name}\\{i}", mod_path)
        master.update_progress(1)
    master.finish_progress()


def remover(name: str, master):
    master.set_title(LANG["sync.sync_to_mods"].format(LANG[f"type.{name}"]))
    mod_path = CONFIG["CONFIG"]["mc_path"]

    delete_list = os.listdir(f"mods\\{name}")
    master.set_progress(len(delete_list)+1)

    for i in os.listdir(mod_path):
        if i in delete_list:
            os.remove(f"{mod_path}\\{i}")
            master.update_progress(1)
    master.finish_progress()


def deleter(master):
    master.set_title(LANG["sync.clean"])
    mod_path = CONFIG["CONFIG"]["mc_path"]
    master.set_progress(len(os.listdir(mod_path))+1)

    if not os.path.isdir("mods2"):
        for i in os.listdir(mod_path):
            if os.path.isfile(f"{mod_path}\\{i}") and i.endswith(".jar"):
                os.remove(f"{mod_path}\\{i}")
            master.update_progress(1)
        master.finish_progress()
    else:
        mods2_list = []
        for path, dirs, files in os.walk("mods2"):
            for filename in files:
                mods2_list.append(filename)

        for i in os.listdir(mod_path):
            if i in mods2_list:
                os.remove(f"{mod_path}\\{i}")
            master.update_progress(1)
        master.finish_progress()


def safeDeleteDirs(dirs):
    def delete():
        nonlocal dirs
        total_dir = []
        for path, dirs, files in os.walk(dirs):
            total_dir.append(f"{path}")
        total_dir.reverse()
        for i in total_dir:
            try:
                os.rmdir(i)
            except Exception as e:
                LOGGER.warning(str(e), f"{create_log_time()} [DOWNLOADER]")

