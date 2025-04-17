from time import sleep

import pyautogui
from pywinauto import Application

from common_lib import click_object, write_log, find_object, click_object_by_index


def Realtek_Audio_console_App_5(detail_testcase, log_file_name):
    try:
        detail_testcase = detail_testcase.split('/')
        # The List contains the pass fail objects
        pass_list = []
        fail_list = []

        #Connect to Realtek Audio Console app
        app1 = Application(backend='uia').connect(title_re='Realtek Audio Console')
        realtek_window = app1.window(title_re='Realtek Audio Console')
        sleep(1)
        print(realtek_window.print_control_identifiers())
        is_main = click_object(realtek_window, 'Main', 'main', 'ListItem')
        if is_main[0]:
            is_main_active = is_main[2].is_active()
            if is_main_active:
                pass_list.append('Main tab is active')
            else:
                fail_list.append('Main tab not active')

        is_play_back = click_object_by_index(realtek_window, 'Playback Devices', 'Text', 1)
        is_speaker = click_object(realtek_window, 'Speakers', '', 'Text')
        is_recording = click_object_by_index(realtek_window, 'Recording Devices', 'Text', 1)
        is_microphone = click_object(realtek_window, 'Microphone Array', '', 'Text')

        obj_check = [is_main, is_play_back, is_speaker, is_recording, is_microphone]
        for obj in obj_check:
            if obj[0]:
                pass_list.append(obj[2].window_text())
            else:
                fail_list.append(obj[1])

        #Write log
        write_log('Realtek_Audio_console_App_5', pass_list, fail_list, log_file_name)
        if len(fail_list) > 0:
            return False
        elif len(pass_list) > 0:
            return True
    except Exception as e:
        print(f'write log error: {e}')

