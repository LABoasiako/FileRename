import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
import os
from shutil import copy2
import csv

button_styling = "*{color: #f6f6f6; font-family: 'Shanti'; font-size: 24px; margin: 1px 5px; padding: 5px;} " \
                 "*:hover{background:'#a7a6ba';}"


class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Rename")
        self.resize(700, 350)
        self.setStyleSheet("background: #322f3d; color: #f6f6f6;")


        ########  Create Widgets
        self.directory_files = QListWidget()
        self.directory_files.sortItems()
        self.directory_files.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.directory_files.itemSelectionChanged.connect(self.evt_directory_files_selection)

        self.files_to_edit = QListWidget()
        self.files_to_edit.sortItems()
        self.files_to_edit.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.files_to_edit.itemSelectionChanged.connect(self.evt_lbxLanguages_selection)


        self.directory_button = QPushButton("Select Directory", self)
        self.directory_button.setStyleSheet(button_styling)
        self.directory_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.directory_button.clicked.connect(self.evt_directory_clicked)

        self.add_button = QPushButton("Add Files", self)
        self.add_button.setStyleSheet(button_styling)
        self.add_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.add_button.clicked.connect(self.evt_add_clicked)

        self.remove_button = QPushButton("Remove Files", self)
        self.remove_button.setStyleSheet(button_styling)
        self.remove_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.remove_button.clicked.connect(self.evt_remove_clicked)

        self.rename_button = QPushButton("Rename Files", self)
        self.rename_button.setStyleSheet(button_styling)
        self.rename_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.rename_button.clicked.connect(self.evt_rename_clicked)

        self.d_label = QLabel("Directory Files", self)
        self.d_label.setStyleSheet("color: #f6f6f6; font-family: 'Arial'; font-size: 24px; padding: 5px 0px;")
        self.d_label.setAlignment(Qt.AlignCenter)

        self.edit_label = QLabel("Files To Modify", self)
        self.edit_label.setStyleSheet("color: #f6f6f6; font-family: 'Arial'; font-size: 24px; padding: 5px 0px;")
        self.edit_label.setAlignment(Qt.AlignCenter)

        self.setupLayout()

    def setupLayout(self):
        self.grid = QGridLayout()

        self.grid.addWidget(self.directory_button, 1, 1) # Row, Column, RowSpan, ColumnSpan
        self.grid.addWidget(self.add_button, 2, 1)
        self.grid.addWidget(self.remove_button, 3, 1)
        self.grid.addWidget(self.rename_button, 4, 1)
        self.grid.addWidget(self.directory_files, 1, 0, 5, 1)
        self.grid.addWidget(self.files_to_edit, 1, 2, 5, 1)
        self.grid.addWidget(self.d_label, 0, 0)
        self.grid.addWidget(self.edit_label, 0, 2)

        self.setLayout(self.grid)

    #######   Event Handlers
    def evt_add_clicked(self):
        lstItems = self.directory_files.selectedItems()
        for itm in lstItems:
            QLWI = self.directory_files.takeItem(self.directory_files.row(itm))
            self.files_to_edit.addItem(QLWI)
        self.files_to_edit.sortItems()
        self.repaint()
        self.files_to_edit.repaint()

    def evt_remove_clicked(self):
        lstItems = self.files_to_edit.selectedItems()
        for itm in lstItems:
            QLWI = self.files_to_edit.takeItem(self.files_to_edit.row(itm))
            self.directory_files.addItem(QLWI)
        self.directory_files.sortItems()
        self.repaint()
        self.directory_files.repaint()

    def evt_rename_clicked(self):
        if self.files_to_edit.count() > 0:
            self.Rename_list = []
            self.Rename_list.append(["Old Name", "New Name"])
            number = 1
            items = [self.files_to_edit.item(x).text() for x in range(self.files_to_edit.count())]
            for item in items:
                if number < 10:
                    self.Rename_list.append([item, f"00{number}.mp3"])
                    copy2(f'{self.directory}/{item}', f'{self.directory}/Rename/00{number}.mp3')
                    number += 1
                else:
                    self.Rename_list.append([item, f"00{number}.mp3"])
                    copy2(f'{self.directory}/{item}', f'{self.directory}/Rename/0{number}.mp3')
                    number += 1
            print(self.Rename_list)
            # print(self.directory)
            with open(f"{self.directory}/Rename/rename.csv", "w") as f:
                write = csv.writer(f)
                for row in self.Rename_list:
                    write.writerow(row)

            self.file_rename_popup()
        else:
            self.no_file_popup()


    def evt_directory_clicked(self):
        # Create Dictionary For Files
        self.directory_files.clear()
        self.files_to_edit.clear()
        files = []
        self.directory = QFileDialog.getExistingDirectory()
        dir_files = os.listdir(self.directory)
        # print(dir_files)
        for file in dir_files:
            files.append(file)
        self.directory_files.addItems(files)
        self.directory_files.sortItems()
        self.directory_files.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.directory_files.itemSelectionChanged.connect(self.evt_directory_files_selection)

    def evt_directory_files_selection(self):
        self.add_button.setDefault(True)
        self.repaint()

    # Popup messages
    def file_rename_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("File Renamed")
        msg.setText("Your Files have been renamed")
        msg.setIcon(QMessageBox.Information)

        x = msg.exec_()

    def no_file_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("No Files Selected")
        msg.setText("Your have not selected any files modify")
        msg.setIcon(QMessageBox.Critical)

        x = msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())



