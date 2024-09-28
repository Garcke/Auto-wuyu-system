import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox
from PyQt5.QtGui import QPixmap, QImage,QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QEvent
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Service.AutoLogin import get_captcha_img, post_login
import requests
from io import BytesIO
from GUI.main_gui import MainWindow





class PasswordInputWithToggle(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(340, 40)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)
        
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("密码")
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setStyleSheet("""
            border: none;
            background: transparent;
            padding: 0 10px;
        """)
        
        self.show_password_check = QCheckBox()
        self.show_password_check.setFixedSize(30, 38)
        self.show_password_check.setStyleSheet("""
            QCheckBox {
                border: none;
                background: transparent;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                subcontrol-position: center;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #ccc;
                background: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                background: #4CAF50;
            }
        """)
        self.show_password_check.stateChanged.connect(self.toggle_password_visibility)
        
        layout.addWidget(self.password_entry, 1)
        layout.addWidget(self.show_password_check, 0)
        
        self.setMouseTracking(True)
        self.password_entry.installEventFilter(self)
        self.show_password_check.installEventFilter(self)
    
    def toggle_password_visibility(self, state):
        self.password_entry.setEchoMode(QLineEdit.Normal if state == Qt.Checked else QLineEdit.Password)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor("#ccc"))
        pen.setWidth(1)
        painter.setPen(pen)
        
        painter.setBrush(Qt.white)
        painter.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 5, 5)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseMove:
            self.update()
        return super().eventFilter(obj, event)

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自动五育评分系统")
        self.setFixedSize(800, 600)

        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置背景图片
        response = requests.get("http://27.37.67.47/static/img/login-background.6e364730.jpg")
        background_image = Image.open(BytesIO(response.content))
        background_image = background_image.convert("RGBA")
        data = background_image.tobytes("raw", "RGBA")
        qimage = QImage(data, background_image.width, background_image.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)
        
        background_label = QLabel(self)
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)

        content_widget = QWidget()
        content_widget.setFixedSize(450, 350)
        content_widget.setStyleSheet("""
            background-color: rgba(255, 255, 255, 220);
            border-radius: 10px;
            padding: 30px;
        """)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("✅自动五育评分✅")
        title_label.setStyleSheet("""
            font-size: 32px;
            color: #333;
            background-color: transparent;
            font-weight: bold;
            padding: 5px;
            border-radius: 5px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label)

        self.username_entry = self.create_input("账号")
        content_layout.addWidget(self.username_entry, alignment=Qt.AlignCenter)

        self.password_container = self.create_password_input()
        content_layout.addWidget(self.password_container, alignment=Qt.AlignCenter)

        self.login_button = QPushButton("登录")
        self.login_button.setStyleSheet("""
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
        """)
        self.login_button.clicked.connect(self.login)
        self.login_button.setFixedSize(340, 40)
        content_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        main_layout.addWidget(content_widget)

    def create_input(self, placeholder_text):
        entry = QLineEdit()
        entry.setPlaceholderText(placeholder_text)
        entry.setFixedSize(340, 40)
        entry.setStyleSheet("""
            font-size: 16px;
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 5px 10px;
        """)
        return entry

    def create_password_input(self):
        password_input = PasswordInputWithToggle()
        self.password_entry = password_input.password_entry
        return password_input

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        if not username or not password:
            QMessageBox.critical(self, "错误", "请输入账号和密码")
            return

        uuid, cap_code = get_captcha_img()
        token = post_login(username, password, uuid, cap_code)

        if token:
            QMessageBox.information(self, "成功", "登录成功")
            self.open_main_window(username, token)
        else:
            QMessageBox.critical(self, "错误", "登录失败：密码或者账号错误")

    def open_main_window(self, username, token):
        self.main_window = MainWindow(username, token)
        self.main_window.show()
        self.close()

def main():
    app = QApplication(sys.argv)
    login_app = LoginApp()
    login_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()