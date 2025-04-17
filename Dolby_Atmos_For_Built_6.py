from time import sleep

import pyautogui
from pywinauto import Application

from common_lib import click_object, click_object_by_index, write_log, scroll_center, connect_app, find_object, \
    open_app, click_object_ad

def Dolby_Atmos_For_Built_6(detail_testcase, log_file_name):
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
        setting_tab = click_object_ad(dolby_window, title='SETTINGS', auto_id='NavigationPanel_settingsTabLabel', control_type='ListItem')
        more_settings  = click_object_ad(dolby_window, title='More Settings', control_type='Text')
        if more_settings:
            pass_list.append('More Settings')
        else:
            fail_list.append('More Settings')

        enable_effect = click_object_ad(dolby_window, title='Dolby Atmos effects for speakers and headphones', control_type='Text')
        effect_button = click_object_ad(dolby_window, title='Dolby Atmos effects for speakers and headphones', control_type='Button')
        if enable_effect:
            pass_list.append('Dolby Atmos effects for speakers and headphones')
        else:
            fail_list.append('Dolby Atmos effects for speakers and headphones')

        if effect_button:
            pass_list.append('Dolby Atmos effects for speakers and headphones button')
        else:
            fail_list.append('Dolby Atmos effects for speakers and headphones button')

        dolby_window.close()
        # Write log
        write_log('Dolby_Atmos_For_Built', pass_list, fail_list, log_file_name)
        if len(fail_list) > 0:
            return False
        elif len(pass_list) > 0:
            return True
    except Exception as e:
        print(f'write log error: {e}')
