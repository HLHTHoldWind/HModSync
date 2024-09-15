"""HCollection Minecraft Server mod synchronizer"""

from src.downloader import *


def main():
    try:
        logs = os.listdir('logs')
        if len(logs) > 20:
            while len(logs) > 20:
                os.remove(f"logs\\{logs.pop(0)}")
        root = Application()
        root.mainloop()
    except Exception as exception:
        LOGGER.critical(str(exception), f"{create_log_time()} [MAIN]")
        raise exception


if __name__ == "__main__":
    main()
