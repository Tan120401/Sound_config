import codecs
import os
import time
from datetime import datetime
from time import sleep
import subprocess

import pandas as pd
import pyautogui
from AppOpener import open
from pywinauto import Application, Desktop

# Function to write logs
def write_log(testcase_name,pass_list, fail_list, log_file_name):
    # Open log file and write
    try:
        log_folder = 'Sound_Config_Result'
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        # Full path for the log file
        log_file_path = os.path.join(log_folder, log_file_name)
        with codecs.open(f"{log_file_path}", "a", "utf-8") as file:
            file.write(f"*{testcase_name.upper()}\n")
            file.write("-List of pass: \n")
            file.write("\n".join(pass_list))
            file.write("\n")
            if len(fail_list) > 0:
                file.write("-List of fail: \n")
                file.write("\n".join(fail_list))
                file.write("\n")
            file.write("-------------------------------------------------------------------------\n")
    except Exception as e:
        print(f'Write log error: {e}')

# Function init log file
def init_log_file():
    # change_global_log_file()
    now = datetime.now()
    current_time = now.strftime('%m%d%Y_%H%M%S')
    print(current_time)
    global log_file_name
    log_file_name = f"{current_time}_SOUND_CONFIG.txt"
    return log_file_name

    # # check setting log exists
    # if os.path.exists(log_file_name):
    #     try:
    #         # delete file
    #         os.remove(log_file_name)
    #         print(f"Deleted existing log file: {log_file_name}")
    #         return log_file_name
    #     except Exception as e:
    #         print(f"Error deleting log file: {e}")
    # try:
    #     # Khởi tạo lại file log
    #     with codecs.open(log_file_name, "w", "utf-8") as file:
    #         file.write("")  # Tạo file rỗng
    #     print(f"Initialized new log file: {log_file_name}")
    #     return log_file_name
    # except Exception as e:
    #     print(f"Error initializing log file: {e}")

# Move to object and scroll
def scroll_center(target_window, title, auto_id, control_type):
    try:
        scroll_bar = target_window.child_window(title=title, auto_id=auto_id, control_type=control_type)
        scroll_bar_rec = scroll_bar.rectangle()
        pyautogui.moveTo(scroll_bar_rec.left + 20, scroll_bar_rec.top - 20)
        sleep(1)
        pyautogui.scroll(-800)
        sleep(1)
        return scroll_bar
    except Exception as e:
        print(f'Scroll error: {e}')

# Function close app
def close_app(app_name):
    try:
        app = Application(backend='uia').connect(title_re=app_name)
        target_window = app.window(title_re=app_name)
        target_window.close()
    except Exception as e:
        print(f'close app error: {e}')

# Function open app return target windows
def open_app(app_name):
    try:
        open(app_name, match_closest=False)
        sleep(3)
        app = Application(backend='uia').connect(title_re=app_name)
        target_window = app.window(title_re=app_name)
        return target_window
    except Exception as e:
        print(f'open app error: {e}')

# Print all windows
def print_all_windows():
    desktop = Desktop(backend='uia')
    all_windows = desktop.windows()
    for win in all_windows:
        print(win.window_text())

# Function open app return target windows
def connect_app(app_name):
    try:
        app = Application(backend='uia').connect(title_re=f'.*{app_name}.*')
        target_window = app.window(title_re=f'.*{app_name}.*')
        target_window.set_focus()
        return target_window
    except Exception as e:
        print(f'connect app error: {e}')
        return False

def wait_until(timeout, interval, condition):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition():
            return True
        time.sleep(interval)
    raise TimeoutError("Time out error")

# Function click object exist
def click_object(window, title, auto_id, control_type):
    object_select = window.child_window(title=title, auto_id=auto_id, control_type=control_type)
    try:
        wait_until(5, 1, lambda: object_select.exists())
        object_select.click_input()
        result = [True, title, object_select]
    except TimeoutError as e:
        print(f'Click error: {e}')
        result = [False, title, None]
    sleep(1)
    return result

# Function click object by index
def click_object_by_index(window, title, control_type, index):
    try:
        object_selects = window.descendants(title=title, control_type=control_type)
        object_select = object_selects[index]
        wait_until(5, 1, lambda: object_select.is_visible())
        object_select.click_input()
        result = [True, title, object_select]
    except Exception as e:
        print(f"Error clicking object: {e}")
        return (False, title, None)
    sleep(1)
    return result

# Function find object
def find_object(window, title, auto_id, control_type):
    object_find = window.child_window(title=title, auto_id=auto_id, control_type=control_type)
    try:
        wait_until(5, 0.5, lambda: object_find.exists())
        result = [True, title, object_find]
    except Exception as e:
        print(f'Find Object error: {e}')
        result = [False, title, None]
    return result

# Function click object by coordinates
def click_object_by_coordinates(left, top, right, bottom):
    # Define BoundingRectangle
    bounding_rectangle = {'l': left, 't': top, 'r': right, 'b': bottom}

    # Calculate the central coordinates
    center_x = (bounding_rectangle['l'] + bounding_rectangle['r']) // 2
    center_y = (bounding_rectangle['t'] + bounding_rectangle['b']) // 2

    # Move to the central coordinates and click
    pyautogui.moveTo(center_x, center_y)
    pyautogui.click()

# Function to find open windows
def find_open_window(app):
    # List all window
    try:
        all_window_active = Desktop(backend='uia').windows()
        is_app = False
        for win in all_window_active:
            if win.window_text() == app:
               is_app = True
               sleep(2)
               win.close()
        return is_app
    except Exception as e:
        print(f'Find app is open error: {e}')

# Function connected Wi-Fi
def get_connected_wifi():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
        result = result.decode("utf-8", errors="ignore")
        for line in result.split('\n'):
            if "SSID" in line:
                ssid = line.split(":")[1].strip()
                return ssid
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function click element in group
def click_object_within_group(group, name, auto_id, control_type):
    # get all element
    child_elements = group.descendants(control_type=control_type)
    # find elements
    for element in child_elements:
        if element.window_text() == name and element.automation_id() == auto_id:
            return element.click_input()
    return False

# Function init report file name
def init_file_name():
    now = datetime.now()
    current_time = now.strftime('%m%d%Y_%H%M%S')
    report_file_name = f"{current_time}_SOUND_CONFIG_REPORT.xlsx"
    log_file_name = f"{current_time}_SOUND_CONFIG_REPORT.txt"
    return [log_file_name, report_file_name]

#Function write result to excel file
def write_result_report(testcase_name, result, report_file_name):
    log_folder = 'Sound_Config_Result'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Full path for the log file
    log_file_path = os.path.join(log_folder, report_file_name)
    data_report = {
        'Test Case': testcase_name,
        'Result': result
    }
    df = pd.DataFrame(data_report)

    df.to_excel(log_file_path, sheet_name='Sound Config', index=False, engine='openpyxl')

    # Read back the file to verify
    dfread = pd.read_excel(log_file_path, sheet_name='Sound Config')

# Example usage

def click_object_ad(window, title=None, auto_id=None, control_type=None, index=0, click_able = True):
    try:
        # Nếu có auto_id, sử dụng child_window để tìm trực tiếp
        if auto_id is not None:
            child_params = {'auto_id': auto_id}
            if title is not None:
                child_params['title'] = title
            if control_type is not None:
                child_params['control_type'] = control_type

            try:
                object_select = window.child_window(**child_params)
            except Exception as e:
                print(f"Không tìm thấy phần tử bằng child_window: {e}")
                return False
        else:
            # Nếu không có auto_id, sử dụng descendants như trước
            params = {k: v for k, v in {'title': title, 'control_type': control_type}.items() if v is not None}
            if not params:
                raise ValueError("At least one of title, auto_id, or control_type must be provided.")

            object_selects = window.descendants(**params)

            # Kiểm tra nếu không tìm thấy phần tử nào
            if not object_selects:
                print("Không tìm thấy phần tử nào phù hợp", title)
                return False

            # Kiểm tra index có hợp lệ không
            if index >= len(object_selects):
                print(f"Index {index} vượt quá số lượng phần tử tìm thấy ({len(object_selects)})")
                return False

            # Lấy phần tử theo index
            object_select = object_selects[index]

        # Đợi cho đến khi phần tử có thể tương tác được
        if not wait_until(3, 0.5, lambda: object_select.is_visible() and object_select.is_enabled()):
            print("Phần tử không hiển thị hoặc không thể tương tác được")
            return False

        # Click vào phần tử
        if click_able:
            object_select.click_input()

        result = True
    except Exception as e:
        print(f'Click {title} error: {e}')
        result = False

    return result