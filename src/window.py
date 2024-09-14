import ctypes
import tkinter
from threading import Thread
from tkinter.filedialog import *
from tkinter.simpledialog import *

from ttkbootstrap import *
from src.lang import load_lang
from src.constants import *

LANG = load_lang()

winapi = ctypes.windll.user32
trueWidth = winapi.GetSystemMetrics(0)

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ZOOM = round((winapi.GetSystemMetrics(0) / trueWidth) + (0.1 * ((winapi.GetSystemMetrics(0) / trueWidth) / 2)), 1)

import src.downloader as downloader


class Application(Window):
    def __init__(self):
        Window.__init__(self)
        self.withdraw()
        self.textable = {}

        windowInit(self, 310, 160, False, LANG["main.name"], "src\\resources\\icon.ico")
        middle(self, zoom(310), zoom(160))
        self.protocol("WM_DELETE_WINDOW", self.close)

        success_pic = Image.open("src\\resources\\success.png").resize((zoom(60), zoom(60)))
        self.success_pic = ImageTk.PhotoImage(success_pic)
        warning_pic = Image.open("src\\resources\\warning.png").resize((zoom(60), zoom(60)))
        self.warning_pic = ImageTk.PhotoImage(warning_pic)

        self.Style = Style()
        self.Style.configure("green.success.Roundtoggle.Toolbutton", font=("arial", "12"))
        self.Style.configure("normal.primary.Outline.TButton", font=("arial", "12", "bold"))
        self.Style.configure("normal.secondary.Outline.TButton", font=("arial", "9"))

        self.check_frame = LabelFrame(self, text=LANG["main.active"])
        self.textable[self.check_frame] = "main.active"

        self.basic_variable = BooleanVar(self, name="basic")
        self.addon_variable = BooleanVar(self, name="addon")
        self.optim_variable = BooleanVar(self, name="optimization")
        self.shader_variable = BooleanVar(self, name="shader")

        self.basic_variable.set(str_to_boolean(CONFIG["SELECTION"]["basic"]))
        self.addon_variable.set(str_to_boolean(CONFIG["SELECTION"]["addon"]))
        self.optim_variable.set(str_to_boolean(CONFIG["SELECTION"]["optim"]))
        self.shader_variable.set(str_to_boolean(CONFIG["SELECTION"]["shader"]))

        self.basic_check = Checkbutton(self.check_frame, style="success.Roundtoggle.Toolbutton",
                                       text=LANG["type.basic"], variable=self.basic_variable, command=self.update_check)
        self.addon_check = Checkbutton(self.check_frame, style="success.Roundtoggle.Toolbutton",
                                       text=LANG["type.addon"], variable=self.addon_variable, command=self.update_check)
        # self.hdisc_check = Checkbutton(self.check_frame, style="green.success.Roundtoggle.Toolbutton",
        #                                text=LANG["type.hdisc"])
        self.optim_check = Checkbutton(self.check_frame, style="success.Roundtoggle.Toolbutton",
                                       text=LANG["type.optimization"],
                                       variable=self.optim_variable, command=self.update_check)
        self.shader_check = Checkbutton(self.check_frame, style="success.Roundtoggle.Toolbutton",
                                        text=LANG["type.shader"],
                                        variable=self.shader_variable, command=self.update_check)
        self.textable[self.basic_check] = "type.basic"
        self.textable[self.addon_check] = "type.addon"
        # self.textable[self.hdisc_check] = "type.hdisc"
        self.textable[self.optim_check] = "type.optimization"
        self.textable[self.shader_check] = "type.shader"

        self.lang_selector = Combobox(self, state="readonly", values=list(LANG_DICT.keys()))
        self.lang_selector.bind("<<ComboboxSelected>>", self.change_lang)
        self.lang_selector.current(list(LANG_DICT.keys()).index(LANG["language_name"]))
        self.sync_btn = Button(self, style="normal.primary.Outline.TButton",
                               text=LANG["main.sync"], command=self.sync_mods)
        self.sync_btn_f = Button(self, style="normal.secondary.Outline.TButton",
                                 text=LANG["main.force_update"], command=self.sync_mods_f)
        self.path_tip = Label(self, text=LANG["main.select_path"])
        self.path_btn = Button(self, style="normal.secondary.Outline.TButton",
                               text=CONFIG["CONFIG"]["mc_path"], command=self.setpath)
        self.textable[self.sync_btn] = "main.sync"
        self.textable[self.sync_btn_f] = "main.force_update"
        self.textable[self.path_tip] = "main.select_path"

        self.check_frame.place(x=zoom(5), y=zoom(5), width=zoom(200), height=zoom(100))
        self.basic_check.grid(row=0, column=0, sticky="w")
        self.addon_check.grid(row=1, column=0, sticky="w")
        # self.hdisc_check.grid(row=0, column=0, sticky="w")
        self.optim_check.grid(row=2, column=0, sticky="w")
        self.shader_check.grid(row=3, column=0, sticky="w")

        self.path_tip.place(x=zoom(5), y=zoom(105), width=zoom(200), height=zoom(25))
        self.path_btn.place(x=zoom(5), y=zoom(130), width=zoom(200), height=zoom(25))

        self.lang_selector.place(x=zoom(205), y=zoom(5), width=zoom(100), height=zoom(25))
        self.sync_btn.place(x=zoom(205), y=zoom(105), width=zoom(100), height=zoom(50))
        self.sync_btn_f.place(x=zoom(205), y=zoom(75), width=zoom(100), height=zoom(25))


        self.deiconify()

    def setpath(self, event=None):
        self.focus_set()
        path = askdirectory()
        if path.endswith("mods"):
            CONFIG["CONFIG"]["mc_path"] = path
        save_config()
        self.path_btn.config(text=CONFIG["CONFIG"]["mc_path"])

    def update_check(self):
        self.focus_set()
        basic = self.basic_variable.get()
        addon = self.addon_variable.get()
        optim = self.optim_variable.get()
        shader = self.shader_variable.get()

        if optim:
            self.shader_variable.set(True)
            self.shader_check.update()
            shader = True
        if not basic:
            self.basic_variable.set(True)
            self.basic_check.update()
        if not CONFIG.has_section("SELECTION"):
            CONFIG.add_section("SELECTION")
            CONFIG.set("SELECTION", "basic", boolean_to_str(basic))
            CONFIG.set("SELECTION", "addon", boolean_to_str(addon))
            CONFIG.set("SELECTION", "optim", boolean_to_str(optim))
            CONFIG.set("SELECTION", "shader", boolean_to_str(shader))
        else:
            CONFIG.set("SELECTION", "basic", boolean_to_str(basic))
            CONFIG.set("SELECTION", "addon", boolean_to_str(addon))
            CONFIG.set("SELECTION", "optim", boolean_to_str(optim))
            CONFIG.set("SELECTION", "shader", boolean_to_str(shader))
        save_config()

        return 0

    def change_lang(self, event=None, langs=None):
        global LANG
        self.focus_set()
        if langs is None:
            langs = self.lang_selector.get()

        CONFIG["CONFIG"]["lang"] = LANG_DICT[langs]
        save_config()

        LANG = load_lang()
        for i in self.textable.keys():
            i.configure(text=LANG[self.textable[i]])

        self.title(LANG["main.name"])

    def close(self, event=None):
        for i in THREADS:
            if i.is_alive():
                return 0
        self.destroy()
        os._exit(0)

    def sync_mods(self, event=None):
        self.focus_set()
        options = [self.basic_variable, self.addon_variable, self.optim_variable, self.shader_variable]
        updater = ProgressWindow(self)

        def do(controller: ProgressWindow):
            try:
                downloader.check_version(controller)

                for i in options:
                    if i.get():
                        downloader.adder(str(i), controller)
                    else:
                        downloader.remover(str(i), controller)

                controller.attributes('-topmost', False)

                msg = InfoWindow(self, title=LANG["main.succeed"], message=LANG["main.succeed"],
                                 icon="src\\resources\\icon.ico",
                                 bitmap=self.success_pic, alert=True, buttonType=["OK : success"],
                                 buttonCommands=[controller.close])
                msg.show()

            except PermissionError as e:
                LOGGER.warning(str(e), f"{create_log_time()} [WINDOW]")
                controller.attributes('-topmost', False)
                msg = InfoWindow(self, title=LANG["main.failed"], message=LANG["sync.access_denied"],
                                 icon="src\\resources\\icon.ico",
                                 bitmap=self.warning_pic, alert=True, buttonType=["OK : success"],
                                 buttonCommands=[controller.close])
                msg.show()

        sync = Thread(target=do, args=(updater,))
        sync.start()
        THREADS.append(sync)

    def sync_mods_f(self, event=None):
        self.focus_set()
        options = [self.basic_variable, self.addon_variable, self.optim_variable, self.shader_variable]
        updater = ProgressWindow(self)

        def do(controller: ProgressWindow):
            try:
                downloader.check_version(controller, force=True)

                for i in options:
                    if i.get():
                        downloader.adder(str(i), controller)
                    else:
                        downloader.remover(str(i), controller)

                controller.attributes('-topmost', False)

                msg = InfoWindow(self, title=LANG["main.succeed"], message=LANG["main.succeed"],
                                 icon="src\\resources\\icon.ico",
                                 bitmap=self.success_pic, alert=True, buttonType=["OK : success"],
                                 buttonCommands=[controller.close])
                msg.show()

            except PermissionError as e:
                LOGGER.warning(str(e), f"{create_log_time()} [WINDOW]")
                controller.attributes('-topmost', False)
                msg = InfoWindow(self, title=LANG["main.failed"], message=LANG["sync.access_denied"],
                                 icon="src\\resources\\icon.ico",
                                 bitmap=self.warning_pic, alert=True, buttonType=["OK : success"],
                                 buttonCommands=[controller.close])
                msg.show()

        sync = Thread(target=do, args=(updater,))
        sync.start()
        THREADS.append(sync)


class ProgressWindow(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.withdraw()
        self.grab_set()
        self.mainframe = Frame(self)
        self.protocol("WM_DELETE_WINDOW", noFun)
        windowInit(self, 300, 75, False, LANG["main.syncer"], "src\\resources\\icon.ico")
        middle(self, zoom(300), zoom(150))

        self.progress = Progressbar(self.mainframe, mode='determinate', style="info.Striped.Horizontal.TProgressbar")
        self.title_bar = Label(self.mainframe)
        self.progress_text = Label(self.mainframe)

        self.mainframe.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())

        self.total_progress = 0
        self.finished_progress = 0

        self.progress_text.configure(text=f"{self.finished_progress} / {self.total_progress}"
                                          f"----{division(self.finished_progress,self.total_progress)*100:.2f}%")

        self.title_bar.place(x=0, y=0, width=self.winfo_width(), height=zoom(25))
        self.progress.place(x=0, y=zoom(25), width=self.winfo_width(), height=zoom(25))
        self.progress_text.place(x=0, y=zoom(50), width=self.winfo_width(), height=zoom(25))

        self.deiconify()
        self.attributes('-topmost', True)
        self.lift()

    def update_progress(self, value):
        self.finished_progress += value
        self.progress["value"] = self.finished_progress
        self.progress_text.configure(text=f"{self.finished_progress} / {self.total_progress}"
                                          f"----{division(self.finished_progress,self.total_progress)*100:.2f}%")

    def set_progress(self, value):
        self.total_progress = value
        self.finished_progress = 0
        self.progress["maximum"] = self.total_progress
        self.update_progress(0)

    def finish_progress(self):
        self.finished_progress = self.total_progress
        self.update_progress(0)

    def set_title(self, title: str):
        self.title_bar.configure(text=title+"...")

    def close(self, event=None):
        self.grab_release()
        self.destroy()


class InfoWindow(Toplevel):

    def __init__(self, master, title="Info", message="", alert=True, icon=None, bitmap=None,
                 buttonType=("Cancel : danger", "OK : success"), buttonCommands=None):
        super().__init__(master)
        self.transient(master)
        self.withdraw()
        self.buttons = []
        self.buttons2 = []
        self.protocol("WM_DELETE_WINDOW", self.delete)
        windowInit(self, 250, 150, False, title=title, icon=icon)
        middle(self, zoom(250), zoom(150))
        if buttonCommands is None:
            self.buttonCommands = (self.destroy, self.destroy)
        else:
            self.buttonCommands = buttonCommands
        self.title(title)
        self.iconbitmap(icon)
        self.button_type = buttonType
        self.master = master
        self.alert = alert
        messageLabel = ttk.Label(self, text=message)
        picLabel = ttk.Label(self, image=bitmap)
        picLabel.place(x=zoom(10), y=zoom(30), width=zoom(60), height=zoom(60))
        messageHeight = messageLabel.winfo_height()
        y = (zoom(150) - zoom(messageHeight)) / 2
        messageLabel.place(x=zoom(75), y=y - zoom(20))
        self.createButton()

    def createButton(self):
        buttonFrame = ttk.Frame(self)
        times = 0
        self.buttons = []
        self.buttons2 = []
        for i in self.button_type:
            string = i.split(" : ")[0]
            _style = i.split(" : ")[1]
            command = self.buttonCommands[times]
            self.buttons.append(ttk.Button(buttonFrame, text=string, style=_style))
            self.buttons[-1].place(x=zoom(times * 60), y=0, width=zoom(60), height=zoom(30))
            self.buttons[-1].configure(command=lambda b=self.buttons[-1]: self.press_button(b))
            self.buttons2.append(command)
            times += 1
        frameWidth = zoom(60 * len(self.button_type))
        frameHeight = zoom(30)
        x = max(zoom(0), (zoom(250) - frameWidth) - zoom(10))
        buttonFrame.place(x=x + zoom(5), y=zoom(115), width=frameWidth, height=frameHeight)
        # buttonFrame.bind("<ButtonRelease>", self.press_button)

    def delete(self):
        try:
            self.buttons2[-1]()
        except Exception as e:
            LOGGER.warning(str(e), f"{create_log_time()} [WINDOW]")
        self.destroy()

    def show(self):
        self.withdraw()
        self.deiconify()
        self.attributes('-topmost', True)
        self.lift()
        if self.alert:
            self.bell()
        self.grab_set()
        # self.mainloop()

    def press_button(self, event=None):
        if self.buttons2[self.buttons.index(event)] is not None:
            self.buttons2[self.buttons.index(event)]()
        self.destroy()


def zoom(integer):
    return round(integer * ZOOM)


def windowInit(master, width: int, height: int, canResize: bool, title: str, icon: str):
    master.config(width=zoom(width), height=zoom(height))
    if not canResize:
        master.resizable(width=False, height=False)
    master.title(title)
    master.iconbitmap(icon)


def middle(master, width=None, height=None):
    winapi = ctypes.windll.user32
    winX = width
    winY = height
    maxX = winapi.GetSystemMetrics(0)
    maxY = winapi.GetSystemMetrics(1)
    if winX is None:
        winX = master.winfo_width()
        winY = master.winfo_height()
    x = maxX // 2 - winX // 2
    y = maxY // 2 - winY // 2
    master.geometry(f"+{int(x)}+{int(y)}")


def noFun(*args):
    pass
