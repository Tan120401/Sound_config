from time import sleep

import pyautogui
from pywinauto import Application

from common_lib import click_object, click_object_by_index, write_log, scroll_center, connect_app, find_object, \
    open_app, click_object_ad

def check_internet_page(dolby_window, button, page, pass_list, fail_list):
    dolby_access_support = click_object_ad(dolby_window, title=button, control_type='Button')
    if dolby_access_support:
        sleep(8)
        if button == 'Rate Dolby Access':
            dolby_window = connect_app('Dolby Access')
            rate_window =  click_object(dolby_window, "Submit", "SubmitButton", "Button")
            if rate_window[0]:
                pass_list.append(button)
                click_object(dolby_window, "Close", "CloseButton", "Button")
            else:
                fail_list.append(button)
        elif button == 'Introduction':
            intro_window = click_object_ad(dolby_window, title="Skip introduction", control_type="Button")
            if intro_window:
                pass_list.append(button)
            else:
                fail_list.append(button)
        else:
            internet_page = connect_app(page)

            if internet_page:
                pass_list.append(button)
                internet_page.close()
            else:
                fail_list.append(button)
    else:
        fail_list.append(button)

def Execute_Dolby_Access_3(detail_testcase, log_file_name):
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

        info_button = click_object(dolby_window, 'More information about Dolby Access, Dolby Atmos, and frequently asked questions', 'NavigationPanel_infoButton', 'Button')
        if info_button[0]:
            pass_list.append(detail_testcase[0])
        else:
            fail_list.append(detail_testcase[0])
        check_internet_page(dolby_window, 'Dolby Access Support', 'Home - Profile 1 - Microsoft​ Edge', pass_list, fail_list)
        check_internet_page(dolby_window, 'Feedback', 'Dolby Access Support - Dolby - Profile 1 - Microsoft​ Edge', pass_list, fail_list)
        check_internet_page(dolby_window, 'Rate Dolby Access', '', pass_list, fail_list)
        check_internet_page(dolby_window, 'What is Dolby Atmos?', 'Elevate Your Game with Dolby & Dolby Access - Dolby - Profile 1 - Microsoft​ Edge', pass_list, fail_list)
        check_internet_page(dolby_window, 'Privacy policy', 'Dolby Privacy Policy - Dolby - Profile 1 - Microsoft​ Edge', pass_list, fail_list)
        check_internet_page(dolby_window, 'License', 'Dolby End User License Agreement - Dolby - Profile 1 - Microsoft​ Edge', pass_list, fail_list)
        check_internet_page(dolby_window, 'Introduction', 'Home - Profile 1 - Microsoft​ Edge', pass_list, fail_list)

        dolby_window.close()
        # Write log
        write_log('Execute_Dolby_Access_3', pass_list, fail_list, log_file_name)
        if len(fail_list) > 0:
            return False
        elif len(pass_list) > 0:
            return True
    except Exception as e:
        print(f'write log error: {e}')
