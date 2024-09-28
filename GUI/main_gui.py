import sys
import os
import shutil
import zipfile
import rarfile
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QFileDialog, QTextEdit, QApplication
from PyQt5.QtCore import QTimer

import traceback
# Add the project root directory to Python's module search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import QRCodeProcessor
from Service.ThreadManager import ThreadManager

class MainWindow(QMainWindow):
    def __init__(self, username, token):
        super().__init__()
        self.username = username
        self.token = token
        self.setWindowTitle("自动五育评分系统 - 主界面")
        self.setFixedSize(800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 账号信息
        account_info = QLabel(f"账号: {self.username}")
        layout.addWidget(account_info)

        # 会员充值按钮
        recharge_button = QPushButton("会员充值")
        recharge_button.clicked.connect(self.open_recharge_page)
        layout.addWidget(recharge_button)

        # 上传压缩包功能
        upload_button = QPushButton("上传压缩包")
        upload_button.clicked.connect(self.upload_file)
        layout.addWidget(upload_button)

        # 自动填写按钮
        self.auto_fill_button = QPushButton("自动填写")
        self.auto_fill_button.clicked.connect(self.start_processing)
        self.auto_fill_button.setEnabled(False)
        layout.addWidget(self.auto_fill_button)

        # 状态标签
        self.status_label = QLabel("就绪")
        layout.addWidget(self.status_label)

        # 代码运行可视化区域
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.temp_dir = None
        self.thread_manager = ThreadManager()

    def open_recharge_page(self):
        QMessageBox.information(self, "充值", "正在跳转到充值页面...")

    def upload_file(self):
        rarfile.UNRAR_TOOL = r".\\unrar_win\\UnRAR.exe"  # 请确保这个路径是正确的

        file_path, _ = QFileDialog.getOpenFileName(self, "选择压缩包", "", "压缩文件 (*.rar *.zip)")
        if file_path:
            self.temp_dir = os.path.join("C:", "tmp", "qrcodes")
            os.makedirs(self.temp_dir, exist_ok=True)
            
            try:
                if file_path.lower().endswith('.rar'):
                    with rarfile.RarFile(file_path, 'r') as rar_ref:
                        rar_ref.extractall(self.temp_dir)
                elif file_path.lower().endswith('.zip'):
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(self.temp_dir)
                else:
                    raise ValueError("不支持的文件格式")
                
                extracted_folders = [f for f in os.listdir(self.temp_dir) if os.path.isdir(os.path.join(self.temp_dir, f))]
                if extracted_folders:
                    self.temp_dir = os.path.join(self.temp_dir, extracted_folders[0])
                
                extracted_files = os.listdir(self.temp_dir)
                self.log_area.append(f"解压后的文件列表: {extracted_files}")
                
                self.auto_fill_button.setEnabled(True)
                self.log_area.append(f"压缩包已上传并解压到 {self.temp_dir}")
            except (rarfile.BadRarFile, zipfile.BadZipFile, ValueError) as e:
                QMessageBox.warning(self, "错误", f"无法解压文件: {str(e)}")
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                self.temp_dir = None
            except Exception as e:
                QMessageBox.warning(self, "错误", f"发生未知错误: {str(e)}")
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                self.temp_dir = None

    def start_processing(self):
        if self.temp_dir:
            try:
                self.log_area.clear()
                processor = QRCodeProcessor(self.token, self.temp_dir)
                signals = self.thread_manager.start_worker(processor.process_qrcodes)
                
                signals.update.connect(self.update_status)
                signals.finished.connect(self.processing_finished)
                signals.error.connect(self.handle_processing_error)
                
                self.auto_fill_button.setEnabled(False)
                
                self.update_timer = QTimer(self)
                self.update_timer.timeout.connect(self.force_gui_update)
                self.update_timer.start(100)
            except Exception as e:
                error_msg = traceback.format_exc()
                self.log_area.append(f"Error starting processing: {str(e)}\n{error_msg}")
                QMessageBox.critical(self, "错误", f"启动处理时出错:\n{str(e)}")
                self.auto_fill_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "错误", "请先上传压缩包")

    def update_status(self, message):
        self.status_label.setText(message)
        self.log_area.append(message)
        self.log_area.verticalScrollBar().setValue(self.log_area.verticalScrollBar().maximum())

    def force_gui_update(self):
        QApplication.processEvents()

    def processing_finished(self):
        self.status_label.setText("处理完成")
        self.auto_fill_button.setEnabled(True)
        self.update_timer.stop()
        QMessageBox.information(self, "完成", "所有文件处理完成")

    def handle_processing_error(self, error_msg):
        self.log_area.append(error_msg)
        QMessageBox.critical(self, "处理错误", error_msg)
        self.auto_fill_button.setEnabled(True)
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow("test_user", "test_token") # 密码账号测试
    main_window.show()
    sys.exit(app.exec_())