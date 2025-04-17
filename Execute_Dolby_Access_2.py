from time import sleep

import pyautogui
from pywinauto import Application

from common_lib import click_object, click_object_by_index, write_log, scroll_center, connect_app, find_object, open_app


def Execute_Dolby_Access_2(detail_testcase, log_file_name):
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

        skip_button = click_object(dolby_window, 'Skip introduction', 'IntroFlowPage_skipButton', 'Button')

        if skip_button[0]:
            pass_list.append(detail_testcase[0])
            pass_list.append(detail_testcase[1])
            pass_list.append('Skip introduction normally')
        else:
            pass_list.append(detail_testcase[0])
            pass_list.append(detail_testcase[1])
            fail_list.append("Can't skip introduction")

        dolby_window.close()

        dolby_window = open_app('Dolby Access')

        home_focus = dolby_window.child_window(title='HOME', auto_id='NavigationPanel_homeTabLabel', control_type='ListItem')

        if home_focus.exists():
            if home_focus.is_selected():
                pass_list.append('Home page is focusing')
            else:
                fail_list.append('Home page is not focusing')
        dolby_window.close()
        # Write log
        write_log('Execute_Dolby_Access_2', pass_list, fail_list, log_file_name)
        if len(fail_list) > 0:
            return False
        elif len(pass_list) > 0:
            return True
    except Exception as e:
        print(f'write log error: {e}')

