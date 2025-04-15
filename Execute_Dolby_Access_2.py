from time import sleep

import pyautogui
from pywinauto import Application

from common_lib import click_object, click_object_by_index, write_log, scroll_center


def Execute_Dolby_Access_2(detail_testcase, log_file_name):
    try:
        # The List contains the pass fail objects
        pass_list = []
        fail_list = []

        # Search app
        pyautogui.hotkey('win', 's')

        pyautogui.hotkey('ctrl', 'a')

        pyautogui.write('Dolby Access', interval=0.05)
        sleep(1)

        # Connect to search window
        app = Application(backend='uia').connect(title_re='Search')
        target_window = app.window(title_re='Search')

        is_app_settings = click_object(target_window, "App settings", "pp_Settings", "ListItem")
        sleep(2)

        # Connect to settings window
        app1 = Application(backend='uia').connect(title_re='Settings')
        setting_window = app1.window(title_re='Settings')
        scroll_center(setting_window, 'Defaults', 'SettingsGroupControlTemplate_DisplayName', 'Text')
        print(setting_window.print_control_identifiers())

    except Exception as e:
        print(f'write log error: {e}')