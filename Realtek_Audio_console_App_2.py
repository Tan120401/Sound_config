from time import sleep

import pyautogui
from pywinauto import Application, Desktop

from common_lib import click_object, write_log, close_app


def Realtek_Audio_console_App_2(detail_testcase, log_file_name):

    try:
        detail_testcase = detail_testcase.split('/')

        # The List contains the pass fail objects
        pass_list = []
        fail_list = []

        #Search app
        pyautogui.hotkey('win', 's')

        pyautogui.hotkey('ctrl', 'a')

        pyautogui.write('Realtek Audio Console', interval=0.05)
        sleep(1)

        #Connect to search window
        app = Application(backend='uia').connect(title_re='Search')
        target_window = app.window(title_re='Search')

        is_open = click_object(target_window, "Open", "pp_S_Open", "ListItem")
        if is_open:
            pass_list.append(detail_testcase[0])
        else:
            fail_list.append(detail_testcase[0])

        #Connect to Realtek Audio Console app
        app1 = Application(backend='uia').connect(title_re='Realtek Audio Console')
        realtek_window = app1.window(title_re='Realtek Audio Console')
        sleep(1)
        if realtek_window:
            pass_list.append(detail_testcase[1])
        else:
            fail_list.append(detail_testcase[1])

        #Write log
        write_log('Realtek_Audio_console_App_2', pass_list, fail_list, log_file_name)
        if len(fail_list) > 0:
            return False
        elif len(pass_list) > 0:
            return True
    except Exception as e:
        print(f'write log error: {e}')

