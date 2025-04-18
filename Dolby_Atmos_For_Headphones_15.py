from time import sleep

import pyautogui
from pywinauto import Application

from common_lib import click_object, click_object_by_index, write_log, scroll_center, connect_app, find_object, \
    open_app, click_object_ad

def Dolby_Atmos_For_Headphones_16(detail_testcase, log_file_name):
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
        product_tab = click_object_ad(dolby_window, title='PRODUCTS', auto_id='NavigationPanel_enableDolbyTabLabel', control_type='ListItem')
        headphone_button = click_object_ad(dolby_window, title='Select product: Dolby Atmos for Headphones',
                                           control_type='ListItem')
        dolby_for_speaker  = click_object_ad(dolby_window, title='Dolby Atmos for Headphones', control_type='Text')
        if dolby_for_speaker:
            pass_list.append('Dolby Atmos for Headphones')
        else:
            fail_list.append('Dolby Atmos for Headphones')

        setup_button = click_object_ad(dolby_window, title='Setup', control_type='Button')

        go_to_settings = click_object_ad(dolby_window, title='Go to settings', control_type='Button')

        sleep(5)
        setting_window = connect_app('Settings')

        choose_headphone = click_object_ad(setting_window, title='Headphones', control_type='Text')
        setting_window.close()

        if setup_button:
            sleep(2)
            ready = click_object_ad(dolby_window, title='Ready to use', control_type='Text')
            if ready:
                pass_list.append('Enable normally -> Ready to use')
            else:
                fail_list.append('Enable abnormally -> Ready to use')

        # Write log
        write_log('Dolby_Atmos_For_Headphones_15', pass_list, fail_list, log_file_name)
        if len(fail_list) > 0:
            return False
        elif len(pass_list) > 0:
            return True
    except Exception as e:
        print(f'write log error: {e}')
