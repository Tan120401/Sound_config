import copy
import importlib
import os
import sys
from datetime import datetime

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import QMainWindow, QApplication, QHeaderView, QStyledItemDelegate, QTableWidgetItem, QProxyStyle, \
    QMessageBox

from Resource.data import data_testcase
from common_lib import init_log_file, write_result_report
from sound_config_ui import Ui_mainWindow

# from Resource.data import app_list_data

app_list_data = data_testcase

#Class css text center
class CenterAlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter

#Class css check box center
class CheckBoxStyle(QProxyStyle):
    def subElementRect(self, element, option, widget=None):
        r = super().subElementRect(element, option, widget)
        if element == self.SubElement.SE_ItemViewItemCheckIndicator:
            r.moveCenter(option.rect.center())
        return r

#Class threads
class Worker(QThread):
    finished = pyqtSignal() # Signal to indicate the thread is finished

    def __init__(self, target = None):
        super().__init__()
        self.target = target
        self._is_running = True

    def run(self):
        # while self._is_running:
        #     if self.target:
        #         self.target()
        # self.finished.emit()
        if self.target:
            self.target()
        self.finished.emit() # Emit the signal when the work is done

    def stop(self):
        self._is_running = False
        self.terminate()

class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.app_list_info = app_list_data #Danh sach tat ca app
        self.app_selected = []  #Danh sach da chon
        self.current_index = 0 #Chi muc hien tai
        self.threads = [] #Mang chua cach luong
        self.log_file_name = ''
        self.is_selected_all = False #Flag kiem tra select all hay chua
        self.flag_stared = False #Flag kiem tra da chay hay chua
        self.refreshed =  False #Flag kiem tra da refresh hay chua
        self.searched = False #Flag kiem tra da search chua
        self.status_checkboxes = False #Flag kiem tra da select all hay chua

        self.init_ui()

        #Event click button
        self.ui.tableResult.cellChanged.connect(self.onCellChanged)
        self.ui.startBtn.clicked.connect(self.on_clicked_start)
        self.ui.stopBtn.clicked.connect(self.on_clicked_stop)
        self.ui.selectallBtn.clicked.connect(self.uncheckAllCheckBoxes)
        self.ui.refreshBtn.clicked.connect(self.refresh_data)
        self.ui.searchBtn.clicked.connect(self.perform_search)
        self.ui.searchBar.returnPressed.connect(self.perform_search)
        self.ui.searchBar.returnPressed.connect(self.perform_search)
        self.ui.openlogBtn.clicked.connect(self.open_log_folder)

    # Function init ui
    def init_ui(self):
        try:
            global tablewidget
            # init table
            tablewidget = self.ui.tableResult
            tablewidget.setColumnCount(4)
            tablewidget.setHorizontalHeaderLabels(['No.', 'App Name', 'Result', 'Download Link'])

            # Format header
            header = tablewidget.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            tablewidget.setColumnWidth(0, 36)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
            tablewidget.setColumnWidth(1, 220)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
            tablewidget.setColumnWidth(2, 80)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

            # Don't show row index
            tablewidget.verticalHeader().setVisible(False)

            # CSS for header
            tablewidget.setStyleSheet("""
                               QHeaderView::section {
                                   background-color: #9ACBD0;
                                   color: black;
                                   padding: 4px;
                                   font-size: 12pt;
                                   border: 1px solid #E2E0C8;
                               }
                           """)
            center = CenterAlignDelegate()
            tablewidget.setItemDelegateForColumn(2, center)
            tablewidget.verticalHeader().setDefaultSectionSize(40)

            # init data table widget
            tablewidget.setRowCount(0)
            for index, app_info in enumerate(self.app_list_info):
                tablewidget.insertRow(index)

                #Draw check box
                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                if not self.is_selected_all:
                    checkbox_item.setCheckState(Qt.CheckState.Unchecked)
                else:
                    checkbox_item.setCheckState(Qt.CheckState.Checked)
                tablewidget.setItem(index, 0, checkbox_item)

                #Draw app name
                tablewidget.setItem(index, 1, QTableWidgetItem(app_info[0]))
        except Exception as e:
            print('error:', e)

    # Function init report file name
    def init_report_file(self):
        now = datetime.now()
        current_time = now.strftime('%m%d%Y_%H%M%S')
        global report_file_name
        report_file_name = f"{current_time}_UIT_REPORT.xlsx"
        self.testcase_name_report = []
        self.testcase_result_report = []

    # Click start btn
    def on_clicked_start(self):
        if len(self.app_selected) == 0:
            self.show_notification('Please select test case!')
            if self.flag_stared:
                pass
            else:
                self.app_list_info = app_list_data
        else:

            self.init_report_file()
            self.log_file_name = init_log_file()
            self.ui.refreshBtn.setEnabled(False)
            self.ui.selectallBtn.setEnabled(False)
            self.ui.searchBtn.setEnabled(False)
            self.app_list_info = copy.deepcopy(self.app_selected)
            self.flag_stared = True
            self.is_selected_all = True
            self.init_ui()
            self.run_next_testcase()

    # Click stop btn
    def on_clicked_stop(self):
        try:
            # Dừng tất cả các luồng (threads)
            for thread in self.threads:
                if thread.isRunning():
                    thread.stop()  # Gọi hàm stop() từ Worker class
                    thread.wait()  # Chờ thread dừng hoàn toàn
            # Reset trạng thái
            self.flag_stared = False
            self.ui.refreshBtn.setEnabled(True)
            self.ui.selectallBtn.setEnabled(True)
            self.ui.searchBtn.setEnabled(True)
            self.show_notification("Tất cả các tiến trình đã dừng.")
        except Exception as e:
            print("Error while stopping threads:", e)

    #Function run next test case
    def run_next_testcase(self):
        self.reload_row_data('Running', self.current_index, 2)  # reload status running
        try:
            if self.current_index < len(self.app_list_info):
                #init thread
                thread = Worker(target= self.start_handle_testcase)
                self.threads.append(thread)
                #thread done
                thread.finished.connect(self.on_thread_finished)
                #thread start
                thread.start()
                print(f'Started handle test case thread: {self.app_list_info[self.current_index]}')
        except Exception as e:
            print(f'Run next test case error: {e}')

    #Function start handle test case
    def start_handle_testcase(self):
        if self.current_index >= len(self.threads) or not self.threads[self.current_index]._is_running:
            return
        try:
            file_name = self.app_list_info[self.current_index][0] # Tên file để import hàm
            testcase = file_name.replace(" ", "_") # Chuyển dấu cách thành dấu _
            module = importlib.import_module(file_name)
            testcase_function = getattr(module, testcase)
        except Exception as e:
            print('error: ', e)

        # Truyền tham số filename exe và download link cho hàm thực hiện test case
        result = testcase_function(self.app_list_info[self.current_index][1], self.log_file_name)
        self.testcase_name_report.append(testcase)
        if result:
            self.reload_row_data('PASS', self.current_index, 2)
            self.testcase_result_report.append('Pass')
        else:
            self.testcase_result_report.append('Fail')
            self.reload_row_data('FAIL', self.current_index, 2)
        print(self.testcase_name_report, self.testcase_result_report)
        write_result_report(self.testcase_name_report, self.testcase_result_report, report_file_name)
    # Function finish handle test case
    def on_thread_finished(self):
        print(f'Thread for testcase {self.app_list_info[self.current_index]} finished')
        self.current_index += 1
        if self.current_index < len(self.app_list_info):
            self.run_next_testcase()
        else:
            self.current_index = 0
            self.is_selected_all = False
            self.show_notification('All test case run successfully')
            self.ui.refreshBtn.setEnabled(True)
            self.ui.selectallBtn.setEnabled(True)
            self.ui.searchBtn.setEnabled(True)

    # Change status checkbox
    def onCellChanged(self, row, col):
        if col == 0:
            if self.searched:
                select_temp = [] #Temp list to record selected app

                item = self.ui.tableResult.item(row, col)
                box_check = item.checkState() #Get checkbox status

                self.ui.tableResult.blockSignals(True)

                element_select = copy.deepcopy(self.app_list_info[row]) #Data selecting

                if box_check == Qt.CheckState.Checked:
                    select_temp.append(element_select)
                    detail = self.app_list_info[row][1]
                    detail_testcase = QTableWidgetItem(detail)
                    self.ui.tableResult.setItem(row, col + 3, detail_testcase)
                else:
                    if element_select in self.app_selected:
                        self.app_selected.remove(element_select)
                    if len(select_temp) > 0:
                        select_temp.remove(element_select)
                    self.ui.tableResult.setItem(row, col + 3, QTableWidgetItem(""))

                if len(select_temp) > 0:
                    for temp in select_temp:
                        self.app_selected.append(temp)

                self.ui.tableResult.blockSignals(False)
            else:
                item = self.ui.tableResult.item(row, col)
                box_check = item.checkState()

                self.ui.tableResult.blockSignals(True)

                element_select = copy.deepcopy(self.app_list_info[row])

                if box_check == Qt.CheckState.Checked:
                    self.app_selected.append(element_select)
                    detail = self.app_list_info[row][1]
                    detail_testcase = QTableWidgetItem(detail)
                    self.ui.tableResult.setItem(row, col + 3, detail_testcase)
                elif len(self.app_selected) > 0:
                    self.app_selected.remove(element_select)
                    self.ui.tableResult.setItem(row, col + 3, QTableWidgetItem(""))

                self.ui.tableResult.blockSignals(False)

            #Checkbox all?
            checkbox_status = self.areAllCheckBoxesChecked()
            if checkbox_status == True:
                self.ui.selectallBtn.setText('unselect All')
                self.status_checkboxes = True

            else:
                self.status_checkboxes = False
                self.ui.selectallBtn.setText('Select All')

    #Function check to checkbox all
    def areAllCheckBoxesChecked(self):
        rowCount = self.ui.tableResult.rowCount()
        colCount = self.ui.tableResult.columnCount()

        for row in range(rowCount):
            item = self.ui.tableResult.item(row, 0)
            if item and item.checkState() != Qt.CheckState.Checked:
                return False
        return True

    # Function check/uncheck all check box
    def uncheckAllCheckBoxes(self):
        self.status_checkboxes = not self.status_checkboxes
        self.ui.tableResult.blockSignals(True)
        rowCount = self.ui.tableResult.rowCount()
        colCount = self.ui.tableResult.columnCount()

        if self.status_checkboxes == False:
            self.app_selected = []
            self.ui.selectallBtn.setText('Select All')
            for row in range(rowCount):
                for col in range(colCount):
                    item = self.ui.tableResult.item(row, col)
                    if item and item.checkState() == Qt.CheckState.Checked:
                        item.setCheckState(Qt.CheckState.Unchecked)
        else:
            if self.flag_stared:
                self.app_selected = self.app_list_info
            else:
                self.app_selected = app_list_data
            self.ui.selectallBtn.setText('Unselect All')
            for row in range(rowCount):
                item = self.ui.tableResult.item(row, 0)
                if item and item.checkState() == Qt.CheckState.Unchecked:
                    item.setCheckState(Qt.CheckState.Checked)

        self.ui.tableResult.blockSignals(False)

    # Function clear table data
    def clear_table_data(self):
        for row in range(self.ui.tableResult.rowCount()):
            item = self.ui.tableResult.item(row, 2)
            if item:
                try:
                    self.ui.tableResult.blockSignals(True)
                    item.setText('')
                    self.ui.tableResult.blockSignals(False)
                except Exception as e:
                    print(f"Error setting text at row {row}: {e}")

    # Function reload row data
    def reload_row_data(self, result, row_index, col_index):
        item = QTableWidgetItem(f'{result}')
        if result.lower() == 'pass':
            item.setForeground(QBrush(QColor("#A1EEBD")))
        elif result.lower() == 'fail':
            item.setForeground(QBrush(QColor("red")))
        else:
            item.setForeground(QBrush(QColor("#B1F0F7")))
        self.ui.tableResult.blockSignals(True)
        tablewidget.setItem(row_index, col_index, item)
        self.ui.tableResult.blockSignals(False)

    # Function show notifications uninstall
    def show_notification(self, message):
        try:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Thông báo")
            msg.setText(message)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            # msg.buttonClicked.connect(self.msgbtn)
            msg.setStyleSheet("""
                        QMessageBox {
                            background-color: #f0f0f0;
                            font-size: 14px;
                            min-width: 500px;
                            min-height: 150px;
                        }
                        QMessageBox QLabel {
                            color: #2c3e50;
                        }
                        QMessageBox QPushButton {
                            background-color: #3498db;
                            color: #ffffff;
                            border-radius: 5px;
                            padding: 5px 10px;
                        }
                        QMessageBox QPushButton:hover {
                            background-color: #2980b9;
                        }
                    """)
            msg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
            msg.exec()
        except Exception as e:
            print('noti error: ', e)
            pass

    #Function refresh data
    def refresh_data(self):

        # init test case name and detail
        self.app_list_info = app_list_data

        self.app_selected = []  # all test case selected
        self.current_index = 0  # test case index
        self.threads = []

        self.refreshed = True
        self.is_selected_all = False
        self.flag_stared = False

        self.init_ui()  # init ui
        self.ui.tableResult.blockSignals(False)

    # Function search
    def perform_search(self):
        try:
            self.searched = False
            self.app_list_info = app_list_data
            search_text =  self.ui.searchBar.text()
            result = []
            if search_text == '':
                self.app_list_info = self.app_selected
            else:
                self.searched = True
                result = [item for item in self.app_list_info if search_text.lower() in item[0].lower()]
                self.app_list_info = result

            self.init_ui()  # init ui
            self.ui.tableResult.blockSignals(False)
            return result
        except Exception as e:
            print('error', e)
            pass

    # Function open log folder
    def open_log_folder(self):
        path_file = r'C:\UIT_Auto\settings'
        try:
            if hasattr(sys, 'frozen'):
                path_file = os.path.dirname(sys.executable)
            else:
                # Đường dẫn của thư mục chứa file script đang chạy
                path_file = os.path.dirname(os.path.abspath(__file__))

            os.startfile(path_file)
        except Exception as e:
            print(f'Open log file error: {e}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    checkbox_style = CheckBoxStyle(app.style())
    app.setStyle(checkbox_style)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
