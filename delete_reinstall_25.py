from time import sleep

import pyautogui
from pywinauto import Application

from common_lib import click_object, click_object_by_index, write_log, scroll_center, connect_app, find_object, \
    open_app, click_object_ad

def delete_reinstall(detail_testcase, log_file_name):
    try:
        detail_testcase = detail_testcase.split('/')
        # The List contains the pass fail objects
        pass_list = []
        fail_list = []

        # Search app
        pyautogui.hotkey('win', 's')

        pyautogui.hotkey('ctrl', 'a')

        pyautogui.write('Dolby Access', interval=0.05)
        sleep(1)

        pyautogui.hotkey('enter')

        #Connect dolby access window
        for i in range(10):
            dolby_window =  connect_app('Dolby Access')
            if dolby_window:
                break
            sleep(2)

        dolby_window.close()
        pass_list.append('Close Dolby Atmos normally')

        # Write log
        write_log('Dolby_Atmos_For_Built', pass_list, fail_list, log_file_name)
        if len(fail_list) > 0:
            return False
        elif len(pass_list) > 0:
            return True
    except Exception as e:
        print(f'write log error: {e}')
