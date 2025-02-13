import importlib
import os
import sys
from datetime import datetime
from logging import exception

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import QMainWindow, QApplication, QHeaderView, QStyledItemDelegate, QTableWidgetItem, QProxyStyle, \
    QMessageBox

from Resource.data import data_testcase
from common_lib import write_result_report, init_file_name
from sound_config import Ui_mainWindow
from Realtek_Audio_console_App_2 import Realtek_Audio_console_App_2

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
        if self.target:
            self.target()
        self.finished.emit() # Emit the signal when the work is done

    def stop(self):
        self._is_running = False

class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.testcase_name = [] #All test case
        self.testcase_detail = [] #Detail test case

        #init test case name and detail
        self.testcase_name = data_testcase['test case']
        self.testcase_detail = data_testcase['test case detail']

        #List of result report
        self.testcase_name_report = []
        self.testcase_result_report = []
        self.init_file_name = []

        self.testcase_selected = [] #all test case selected
        self.testcase_selected_detail = [] #all test case selected detail
        self.current_index = 0 #test case index
        self.threads = []

        #Flag to control selected
        self.is_selected = False

        self.init_ui() #init ui
        self.status_checkboxes = False #State control checkbox all

        #Event click button
        self.ui.tableResult.cellChanged.connect(self.onCellChanged)
        self.ui.startBtn.clicked.connect(self.on_clicked_start)
        self.ui.selectallBtn.clicked.connect(self.uncheckAllCheckBoxes)
        self.ui.openlogBtn.clicked.connect(self.open_log_folder)

    # Function init ui
    def init_ui(self):
        try:
            global tablewidget
            # init table
            tablewidget = self.ui.tableResult
            tablewidget.setColumnCount(4)
            tablewidget.setHorizontalHeaderLabels(['No.', 'Test case name', 'Result', 'Test case detail'])

            # Format header
            header = tablewidget.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            tablewidget.setColumnWidth(0, 36)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
            tablewidget.setColumnWidth(1, 180)
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
            tablewidget.setItemDelegateForColumn(1, center)
            tablewidget.setItemDelegateForColumn(2, center)

            # init data table widget
            tablewidget.setRowCount(0)
            dic_data = data_testcase
            # self.testcase_name = dic_data['test case']
            print('test case name init: ', self.testcase_name)
            # self.testcase_detail = dic_data['test case detail']
            for i, (name, detail) in enumerate(zip(self.testcase_name, self.testcase_detail)):
                tablewidget.insertRow(i)

                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                if not self.is_selected:
                    checkbox_item.setCheckState(Qt.CheckState.Unchecked)
                else:
                    checkbox_item.setCheckState(Qt.CheckState.Checked)
                tablewidget.setItem(i, 0, checkbox_item)

                tablewidget.setItem(i, 1, QTableWidgetItem(name))
                print('abc')
            # Merger col test case detail
            tablewidget.setSpan(0, 3, len(self.testcase_name), 1)
        except Exception as e:
            print(e)

    # Click start btn
    def on_clicked_start(self):
        # self.clear_table_data()
        if len(self.testcase_selected) == 0:
            self.show_notification('Please select test case!')
            self.testcase_name = data_testcase['test case']
            self.testcase_detail = data_testcase['test case detail']
        else:
            self.init_file_name = init_file_name()
            self.testcase_name = self.testcase_selected
            self.testcase_detail = self.testcase_selected_detail
            print('test case name when click start: ', self.testcase_name)
            self.is_selected = True
            self.init_ui()
            self.run_next_testcase()

    #Function run next test case
    def run_next_testcase(self):
        self.reload_row_data('Running', self.current_index, 2)  # reload status running
        try:
            if self.current_index < len(self.testcase_name):
                #init thread
                thread = Worker(target= self.start_handle_testcase)
                self.threads.append(thread)
                #thread done
                thread.finished.connect(self.on_thread_finished)
                #thread start
                thread.start()
                print(f'Started handle test case thread: {self.testcase_name[self.current_index]}')
        except Exception as e:
            print(f'Run next test case error: {e}')

    #Function start handle test case
    def start_handle_testcase(self):
        if self.current_index >= len(self.threads) or not self.threads[self.current_index]._is_running:
            return
        testcase = self.testcase_name[self.current_index]
        module_name = f'{testcase}'
        module = importlib.import_module(module_name)
        testcase_function = getattr(module, testcase)
        result = testcase_function(self.testcase_detail[self.current_index], self.init_file_name[0])
        print(f'result {testcase}: {result}')
        if result:
            self.reload_row_data('PASS', self.current_index, 2)
            self.testcase_result_report.append("PASS")
        else:
            self.reload_row_data('FAIL', self.current_index, 2)
            self.testcase_result_report.append("FAIL")
        self.testcase_name_report.append(testcase)

        #Write result to excel file
        write_result_report(self.testcase_name_report, self.testcase_result_report, self.init_file_name[1])

    # Function finish handle test case
    def on_thread_finished(self):
        print(f'Thread for testcase {self.testcase_name[self.current_index]} finished')
        self.current_index += 1
        if self.current_index < len(self.testcase_name):
            self.run_next_testcase()
        else:
            self.show_notification('Successfully test case!')
            # self.testcase_name = data_testcase['test case']
            self.is_selected = False
            self.testcase_name = self.testcase_selected
            self.testcase_detail = self.testcase_selected_detail

    # Change status check
    def onCellChanged(self, row, col):
        if col == 0 and not self.is_selected:
            item = self.ui.tableResult.item(row, col)
            box_check = item.checkState()
            self.ui.tableResult.blockSignals(True)

            if box_check == Qt.CheckState.Checked:
                print('Selected: ', self.testcase_selected)
                print('row selected: ', self.testcase_name)
                self.testcase_selected.append(self.testcase_name[row])
                self.testcase_selected_detail.append(self.testcase_detail[row])
                detail = '\n'.join(self.testcase_detail[row])
                detail_testcase = QTableWidgetItem(detail)
                self.ui.tableResult.setItem(0, col + 3, detail_testcase)
            else:
                self.testcase_name = self.testcase_name
                print('test case name truoc select: ', self.testcase_name)
                print('row unselected: ', self.testcase_name[row])
                self.testcase_selected.remove(self.testcase_name[row])
                self.testcase_selected_detail.remove(self.testcase_detail[row])
                self.ui.tableResult.setItem(0, col + 3, QTableWidgetItem(""))
                print('test case name sau select: ', self.testcase_name)
            self.ui.tableResult.blockSignals(False)

            checkbox_status = self.areAllCheckBoxesChecked()
            if checkbox_status == True:
                self.ui.selectallBtn.setText('unselect All')
                self.status_checkboxes = True

            else:
                self.status_checkboxes = False
                self.ui.selectallBtn.setText('Select All')

            print('selected test case: ', self.testcase_selected)

    # Function check status all check box
    def areAllCheckBoxesChecked(self):
        rowCount = self.ui.tableResult.rowCount()
        colCount = self.ui.tableResult.columnCount()

        for row in range(rowCount):
            item = self.ui.tableResult.item(row, 0)
            if item and item.checkState() != Qt.CheckState.Checked:
                return False
        return True

        #Function uncheck all check box

    #Function check/uncheck all check box
    def uncheckAllCheckBoxes(self):
        self.ui.tableResult.blockSignals(True)
        rowCount = self.ui.tableResult.rowCount()
        colCount = self.ui.tableResult.columnCount()

        if self.status_checkboxes == True:
            self.ui.selectallBtn.setText('Select All')

            for row in range(rowCount):
                for col in range(colCount):
                    item = self.ui.tableResult.item(row, col)
                    if item and item.checkState() == Qt.CheckState.Checked:
                        item.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.testcase_selected = data_testcase['test case']
            self.testcase_selected_detail = data_testcase['test case detail']
            self.ui.selectallBtn.setText('Unselect All')
            for row in range(rowCount):
                item = self.ui.tableResult.item(row, 0)
                if item and item.checkState() == Qt.CheckState.Unchecked:
                    item.setCheckState(Qt.CheckState.Checked)

        self.status_checkboxes = not self.status_checkboxes

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
                    print(f"Item at row {row}: {item.text()}")
                    print("Text cleared successfully.")
                except Exception as e:
                    print(f"Error setting text at row {row}: {e}")

    # Function reload row data
    def reload_row_data(self, result, row_index, col_index):
        item = QTableWidgetItem(f'{result}')
        if result.lower() == 'pass':
            item.setForeground(QBrush(QColor("green")))
        elif result.lower() == 'fail':
            item.setForeground(QBrush(QColor("red")))
        else:
            item.setForeground(QBrush(QColor("blue")))
        self.ui.tableResult.blockSignals(True)
        tablewidget.setItem(row_index, col_index, item)
        self.ui.tableResult.blockSignals(False)

    # Function show notifications uninstall
    def show_notification(self, message):
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
        msg.exec()

    # Function open log folder
    def open_log_folder(self):
        try:
            if hasattr(sys, 'frozen'):
                path_file = os.path.dirname(sys.executable)
            else:
                # Đường dẫn của thư mục chứa file script đang chạy
                path_file = os.path.dirname(os.path.abspath(__file__))
            os.startfile(path_file)
            print(path_file)
        except Exception as e:
            print(f'Open log file error: {e}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    checkbox_style = CheckBoxStyle(app.style())
    app.setStyle(checkbox_style)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
