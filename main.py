import os
import time
from PyQt5.QtCore import QObject, pyqtSignal
from Service.QRCodeHandler import decode_qrcode, extract_params
from Service.EvaluationSubmitter import submit_evaluation
import traceback
import requests

class QRCodeProcessor(QObject):
    update_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, token, temp_dir):
        super().__init__()
        self.token = token
        self.temp_dir = temp_dir

    def process_qrcodes(self):
        try:
            self.update_signal.emit("开始处理二维码...")

            jpg_files = [f for f in os.listdir(self.temp_dir) if f.lower().endswith('.jpg')]
            total_files = len(jpg_files)
            
            self.update_signal.emit(f"找到 {total_files} 个 JPG 文件")

            for index, filename in enumerate(jpg_files, 1):
                file_path = os.path.join(self.temp_dir, filename)
                self.update_signal.emit(f"处理文件 {index}/{total_files}: {filename}")

                url = decode_qrcode(file_path)
                if url is None:
                    self.update_signal.emit(f"无法解码二维码: {filename}")
                    continue

                transcript_id, hash_value = extract_params(url)
                if transcript_id and hash_value:
                    result = submit_evaluation(transcript_id, hash_value, self.token)
                    self.update_signal.emit(f"评估数据已提交: {filename}. 结果: {result}")
                else:
                    self.update_signal.emit(f"无法提取参数: {filename}")

                if index < total_files:
                    self.update_signal.emit("等待2秒...")
                    time.sleep(2)

            self.update_signal.emit("所有文件处理完成")
        except Exception as e:
            error_msg = traceback.format_exc()
            self.error_signal.emit(f"处理过程中出错: {str(e)}\n{error_msg}")
        finally:
            self.update_signal.emit("处理完成，正在清理临时文件...")
            self.finished_signal.emit()

# 在 MainWindow 类中添加以下方法：

def start_processing(self):
    self.processing_thread = QRCodeProcessor(self.token, self.temp_dir)
    self.processing_thread.update_signal.connect(self.update_status)
    self.processing_thread.finished_signal.connect(self.processing_finished)
    self.processing_thread.start()

def update_status(self, message):
    # 更新GUI上的状态信息
    self.status_label.setText(message)

def processing_finished(self):
    # 处理完成后的操作
    self.status_label.setText("处理完成")
    # 可以在这里添加其他完成后的操作，比如启用某些按钮等

# 在点击"自动填写"按钮时调用 start_processing 方法