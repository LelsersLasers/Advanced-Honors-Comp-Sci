import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

app = QApplication(sys.argv)

options = QFileDialog.Options()
options |= QFileDialog.ReadOnly  # Allow read-only access

file_dialog = QFileDialog()
file_dialog.setNameFilter("Image Files (*.png *.jpeg *.jpg);;All Files (*)")
file_dialog.setOptions(options)
file_dialog.setFileMode(QFileDialog.ExistingFile)  # Allow selection of a single existing file

if file_dialog.exec_():
    selected_file = file_dialog.selectedFiles()[0]
else:
    print("No files selected.")