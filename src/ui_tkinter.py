# -*- coding: utf-8 -*-
import util, os

ErrorsLocal = []

try:    import tkinter as Tkinter
except ImportError: ErrorsLocal.append("install.missing.module_tkinter")

try:    from PIL import Image
except ImportError: ErrorsLocal.append("install.missing.module_pillow")

try:    from PIL import ImageTk
except ImportError: ErrorsLocal.append("install.missing.package_ImageTk")

def window_main(Prg):
    # I collect the msg NOT in the if because if one of them is missing, it causes Error
    for ErrTxtKey in ErrorsLocal:
        Prg["Errors"].append(util.ui_msg(Prg, ErrTxtKey))

    if Prg["Errors"]: return

    print("Tkinter ui main interface")
    MainWidth = 1200
    MainHeight = 800

    Window = window_new(Prg, "window.main.title")
    Window.geometry('{}x{}'.format(MainWidth, MainHeight))


    SourceWidth = 300
    OnePageWidth = 600
    TextRecognisedWidth = MainWidth - SourceWidth - OnePageWidth
    Pady = 3

    FrameSourcePages = Tkinter.Frame(Window, bg='cyan', width=SourceWidth, height=MainHeight, pady=Pady)
    FrameSourcePages.grid(row=0, column=0, rowspan=3)

    FrameOnePage = Tkinter.Frame(Window, bg='purple', width=OnePageWidth, height=MainHeight, pady=Pady)
    FrameOnePage.grid(row=0, column=1, rowspan=3)

    FrameTextRecognised = Tkinter.Frame(Window, bg='green', width=TextRecognisedWidth, height=MainHeight,pady=Pady)
    FrameTextRecognised.grid(row=0, column=2, rowspan=3)

    Img = image_file_load_to_tk(Prg, "resources/deepcopy_logo_64.png")
    if Img:
        Panel = Tkinter.Label(FrameSourcePages, image=Img)
        Panel.grid(row=0, column=0)

        Panel2 = Tkinter.Label(FrameSourcePages, image=Img)
        Panel2.grid(row=1, column=1)

        Panel3 = Tkinter.Label(FrameSourcePages, image=Img)
        Panel3.grid(row=2, column=2)

        Tkinter.Label(FrameOnePage, text="Frame One Page").grid(row=0, column=1)
        Tkinter.Label(FrameOnePage, text="2222").grid(row=1, column=1)
        Tkinter.Label(FrameTextRecognised, text="Text Recognised").grid(row=0, column=2)

    # top_frame = Frame(root, bg='cyan', width = 450, height=50, pady=3).grid(row=0, columnspan=3)
    # FrameSourcePages.grid(row=0, column=0, sticky='e')

    Window.mainloop()

def window_new(Prg, TitleKey=""):
    Window = Tkinter.Tk()
    if TitleKey:
        Window.title(util.ui_msg(Prg, TitleKey))
    return Window

def image_file_load_to_tk(Prg, Path):
    if not os.path.isfile(Path):
        Msg = util.ui_msg(Prg, "file_operation.file_missing", PrintInTerminal=True)
        Prg["Warning"].append(Msg)
        return False

    Load = Image.open(Path)
    return ImageTk.PhotoImage(Load)

