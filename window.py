# Import necessary modules
import sys # use sys to accept command line arguments
import pathlib
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QFileDialog, QMessageBox
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QPixmap # used for displaying images

class MainWindow(QWidget):
    def __init__(self):
        """Constructor for Main Window Class"""
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Set up the application's GUI"""
        self.setMinimumSize(800, 100) # As an alternative to setGeometry method
        self.setWindowTitle("Compare Directories")
        self.setUpMainWindow()
        self.show() # Display the window on the screen

    def setUpMainWindow(self):
        """Create and arrange widgets in the main window"""
        input_label = QLabel("Input Folder")
        self.input_edit = QLineEdit()
        self.input_edit.setClearButtonEnabled(True)
        self.input_button = QPushButton("Search Dir.")
        self.input_button.clicked.connect(self.openInputDirDialog)

        output_label = QLabel("Output Folder")
        self.output_edit = QLineEdit()
        self.output_edit.setClearButtonEnabled(True)
        self.output_button = QPushButton("Search Dir.")
        self.output_button.clicked.connect(self.openOutputDirDialog)

        file_label = QLabel("File Name")
        self.file_edit = QLineEdit()
        self.file_edit.setClearButtonEnabled(True)
        txt_label = QLabel(".txt")

        self.start_button = QPushButton("START")
        self.start_button.clicked.connect(self.compareDirectories)

        self.main_grid = QGridLayout()
        self.main_grid.addWidget(input_label, 0, 0)
        self.main_grid.addWidget(self.input_edit, 0, 1, 1, 3)
        self.main_grid.addWidget(self.input_button, 0, 4)
        self.main_grid.addWidget(output_label, 1, 0)
        self.main_grid.addWidget(self.output_edit, 1, 1, 1, 3)
        self.main_grid.addWidget(self.output_button, 1, 4)
        self.main_grid.addWidget(file_label, 2, 0)
        self.main_grid.addWidget(self.file_edit, 2, 1, 1, 2)
        self.main_grid.addWidget(txt_label, 2, 3)
        self.main_grid.addWidget(self.start_button, 2, 4)
        self.setLayout(self.main_grid)

    def openInputDirDialog(self):
        """Open a dialog to select the input directory"""
        input_dir = QFileDialog.getExistingDirectory(self, "Select Input Directory")
        if input_dir:
            self.input_edit.setText(input_dir)

    def openOutputDirDialog(self):
        """Open a dialog to select the output directory"""
        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if output_dir:
            self.output_edit.setText(output_dir)

    def compareDirectories(self):
        """Compare directories and write results to a text file"""
        input_dir = pathlib.Path(self.input_edit.text())
        output_dir = pathlib.Path(self.output_edit.text())
        file_name = self.file_edit.text()

        if not input_dir.is_dir():
            QMessageBox.warning(self, "Invalid Input Directory", "The specified input directory does not exist.")
            return

        if not output_dir.is_dir():
            QMessageBox.warning(self, "Invalid Output Directory", "The specified output directory does not exist.")
            return

        if not file_name:
            QMessageBox.warning(self, "Invalid File Name", "The specified file name is empty.")
            return

        try:
            with open (output_dir / f'{file_name}.txt', 'w') as f:
                for item in input_dir.iterdir():
                    if item.is_file():
                        size = item.stat().st_size
                        last_modified = datetime.fromtimestamp(item.stat().st_mtime)
                    else:
                        size = sum(file.stat().st_size for file in item.glob('**/*') if file.is_file())
                        last_modified = max(
                            datetime.fromtimestamp(file.stat().st_mtime) for file in item.glob('**/*') if file.is_file())
                    relative_path = item.relative_to(input_dir)
                    f.write(f"{relative_path} - {size} bytes - Last Modified: {last_modified}\n")
            QMessageBox.information(self, "Success", "Directory comparison completed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


# Run the program
if __name__ == '__main__':
    app = QApplication(sys.argv) # Create QApplication object
    window = MainWindow() # Initiate the window
    sys.exit(app.exec()) # Used for starting the event loop (exec) and safely closing the program (sys.exit)