# ------------------------- [ Main Project File | Coding: utf-8 ] ------------------------- #
# Project: AsciCam                                                                          #
# File: main.py                                                                             #
# Python Version: 3.10.2 - Tested: 3.10.2 - All others are untested.                        #
# The libraries should get installed among the integrated libraries: cv2, pillow            #
# ----------------------------------------- [ ! ] ----------------------------------------- #
# This code doesn't have any errors. if you got an error, check syntax and python version.  #
# ----------------------------------------- [ ! ] ----------------------------------------- #
# Author: nihadenes - <nihadenesvideo@gmail.com>                                            #
# Links: <https://github.com/nihadenes>                                                     #
# Date: 3/28/2022                                                                           #
# License: MIT License                                                                      #
# --------------------------------------- [ Enjoy ] --------------------------------------- #

import cv2, os,sys, argparse ,signal  
from PIL import Image 
from enum  import Enum 
from collections  import  namedtuple   


class  AsciCamDefaultPramaters(Enum) :  
    camera     = 0 
    mirrored   = 1
    vertical   = 100 
    fontsize   = 1 
    set_screen = 0   
    char_list = "".join([' ', '.', "'", ',', ':', ';', 'c', 'l', 'x', 'o', 'k', 'X', 'd', 'O', '0', 'K', 'N'])
    
defparams_attributes , defparams_values = (
        AsciCamDefaultPramaters.__members__.keys()  ,
        [  p_value.value for  p_value in  AsciCamDefaultPramaters.__members__.values()] 
        )  

AsciCam = namedtuple("AsciCam" ,defparams_attributes ) 
AsciCam = AsciCam(*defparams_values)  

def setscreen(col, line):
    try:
        os.system(f'mode con: cols={col} lines={line}')
    except:
        print("Failed to set screen.")

def  os_support (supported_osplatform)  : 
    def fcall ( _fcallable )  : 
        def _restrict  (*args , **kwargs ) :  
            if sys.platform.__eq__(supported_osplatform)  : 
                from ctypes import POINTER, WinDLL, Structure, sizeof, byref
                from ctypes.wintypes import BOOL, SHORT, WCHAR, UINT, ULONG, DWORD, HANDLE
                _fcallable(*args ,**kwargs) 

        return  _restrict 
    return fcall 


@os_support("win32")  
def changeFontSize(size=2):  # Changes the font size to *size* pixels (Kind of, but not really.)

    LF_FACESIZE, STD_OUTPUT_HANDLE = 32, -11

    class COORD(Structure):
        _fields_ = [
            ("X", SHORT),
            ("Y", SHORT),
        ]

    class CONSOLE_FONT_INFOEX(Structure):
        _fields_ = [
            ("cbSize", ULONG),
            ("nFont", DWORD),
            ("dwFontSize", COORD),
            ("FontFamily", UINT),
            ("FontWeight", UINT),
            ("FaceName", WCHAR * LF_FACESIZE)
        ]

    kernel32_dll = WinDLL("kernel32.dll")

    get_last_error_func = kernel32_dll.GetLastError
    get_last_error_func.argtypes = []
    get_last_error_func.restype = DWORD

    get_std_handle_func = kernel32_dll.GetStdHandle
    get_std_handle_func.argtypes = [DWORD]
    get_std_handle_func.restype = HANDLE

    get_current_console_font_ex_func = kernel32_dll.GetCurrentConsoleFontEx
    get_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
    get_current_console_font_ex_func.restype = BOOL

    set_current_console_font_ex_func = kernel32_dll.SetCurrentConsoleFontEx
    set_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
    set_current_console_font_ex_func.restype = BOOL

    stdout = get_std_handle_func(STD_OUTPUT_HANDLE)
    font = CONSOLE_FONT_INFOEX()
    font.cbSize = sizeof(CONSOLE_FONT_INFOEX)

    font.dwFontSize.X = size
    font.dwFontSize.Y = size

    set_current_console_font_ex_func(stdout, False, byref(font))


def print_large_block(text):
    print("", end="\r")
    print(text, end="\r")


def get_ascii_from_image(im):
    lines = []
    x_range = range(im.size[0])[::-1] if AsciCam.mirrored else range(im.size[0])
    for y in range(im.size[1]):
        line = []
        for x in x_range:
            pix = sum(im.getpixel((x, y))) / 3
            char_list_pos = int((len(AsciCam.char_list) - 1) * pix / 255)
            line.append(AsciCam.char_list[char_list_pos])
        lines.append(''.join(line))
    return ('\n' + ("\n" if AsciCam.fontsize != 1 else "")).join(lines)


def get_video_frms(path, format="cv2"):
    try  :  
        path =  int(path) 
    except ValueError :  
        #may be is a file  
        if  os.access(path ,os.F_OK | os.R_OK) :...  # ok  
        else  :  
            sys.stderr.write(f"Sorry  cannot open  {path} \nAborting...") 
            signal.raise_signal(signal.SIGABRT) 
             

    cap = cv2.VideoCapture(path, cv2.CAP_DSHOW)
    cap.open(path) 
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            if format == 'PIL':
                yield cv2_to_PIL(frame)
            else:
                yield frame
        else:
            cap.release()
            cv2.destroyAllWindows()
            break


def cv2_to_PIL(frame):
    return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


def print_ascii_from_im(im):
    global AsciCam 
    horizontal = int(AsciCam.vertical * 2 * im.size[0] / im.size[1])
    if AsciCam.set_screen == 0:
        AsciCam =  AsciCam._replace(set_screen = 1)  
        setscreen(horizontal, AsciCam.vertical * (2 if AsciCam.fontsize != 1 else 1))
    im = im.resize((horizontal, AsciCam.vertical))
    print_large_block(get_ascii_from_image(im) + '\n')


def main(): 
    global AsciCam 
    description = "Converts your webcam input to ascii and prints it on the screen."
    stdargs  = argparse.ArgumentParser(description=description  ,prog="AsciCam")  
    stdargs.add_argument("-c" ,"--camera"   , help="Select Camera  device  number or  file if your  are in unix system")
    stdargs.add_argument("-m","--mirrored"  , type=int,  help="")  
    stdargs.add_argument("-f" ,"--fontsize" , type=int ,help="Fontsize of Ascii charaters ") 
    stdargs.add_argument("-v" ,"--vertical" , type=int, help="")  
    stdargs.add_argument("-s" , "--set-screen" ,type=int ,help="")  
    stdargs.add_argument("-V" ,"--version"  , action="store_true" , help=f"Show current  version of AsciCam ")  
    
    args  = stdargs.parse_args()    
    if  args.version :  
        print(f"{description}\nVersion of AsciCam   x.x.x ")  
        sys.exit(0) 

    camera   =  (AsciCam.camera   , args.camera  )[args.camera   is not None] 
    mirrored =  (AsciCam.mirrored , args.mirrored)[args.mirrored is not None]   
    fontsize =  (AsciCam.fontsize , args.fontsize)[args.fontsize is not None] 
    vertical =  (AsciCam.vertical , args.vertical)[args.vertical is not None] 
    set_screen= (AsciCam.set_screen,args.set_screen)[args.set_screen is not None] 

    AsciCam = AsciCam._replace(camera=camera, mirrored=mirrored  , fontsize=fontsize  , vertical=vertical, set_screen=set_screen) 
    
    [print_ascii_from_im(im) for im in get_video_frms(AsciCam.camera, 'PIL')]


if __name__ == '__main__':
    try:
        changeFontSize(size=AsciCam.fontsize)
    except Exception as  Xcption : 
        print(f"{Xcption}") 
        print("Failed to set font size.")

    main()
