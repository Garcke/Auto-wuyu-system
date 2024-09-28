import sys
from PyQt5.QtWidgets import QApplication
from GUI.login_gui import LoginApp

def main():
    app = QApplication(sys.argv)
    login_window = LoginApp()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()