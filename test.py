from common_lib import print_all_windows, connect_app

print_all_windows()
dolby_window =  connect_app('Dolby Access')
# print(dolby_window.print_control_identifiers())

submit = dolby_window.child_window(title="Submit", auto_id="SubmitButton", control_type="Button")
submit.click_input()