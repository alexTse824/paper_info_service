# coding=utf-8
import setting
from pyvirtualdisplay import Display
from server import run_server


def main():
    if setting.VIRTUAL_DISPLAY:
        display = Display(visible=0, size=(900, 800))
        display.start()
    
    run_server()


if __name__ == "__main__":
    main()