import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from UserInterface.Test import Ui_MainWindow

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.counter = 0

        self.ui.IncrementButton.clicked.connect(self.increment_counter)
        self.ui.DecrementButton.clicked.connect(self.decrement_counter)

    def increment_counter(self):
        self.counter += 1
        self.ui.label.setText(str(self.counter))

    def decrement_counter(self):
        self.counter -= 1
        self.ui.label.setText(str(self.counter))    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())