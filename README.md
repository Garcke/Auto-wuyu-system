# 开发文档

## 项目名称
自动五育评分系统

## 项目简介
该项目是一个基于PyQt5的桌面应用程序，旨在提供一个用户友好的界面，用于处理和分析二维码数据。用户可以上传压缩包，系统会自动解压并处理其中的二维码文件。每个二维码都存取每个评论系统的url，通过机器扫码获取每个url的cookie和验证，
从而实现自动填写学生评价

## 技术栈
- Python 3.x
- PyQt5
- rarfile
- zipfile

## 文件结构
```
/项目根目录
│
├── GUI/
│   └── login_gui.py # 登录界面代码
│   └── main_gui.py  # 主界面代码
│
├── main.py          # QRCodeProcessor类的实现
├── Service/
│   └── ThreadManager.py  # 线程管理类
│   └── QRCodeHandler.py  # 二维码处理类
│   └── AutoLogin.py  # 自动登录类
│   └── EvaluationSubmitter
└── unrar_win/
    └── UnRAR.exe   # 解压RAR文件的工具
```

## 主要功能
1. **用户登录**: 用户可以输入用户名和令牌进行登录。
2. **上传压缩包**: 用户可以上传包含二维码的压缩文件（支持RAR和ZIP格式）。
3. **自动填写**: 系统会自动处理解压后的二维码文件，并将结果显示在界面上。
4. **状态更新**: 实时更新处理状态和日志信息。

## 主要类和方法

### MainWindow类
- **`__init__(self, username, token)`**: 初始化主窗口，设置界面元素。
- **`open_recharge_page(self)`**: 打开充值页面的提示。
- **`upload_file(self)`**: 处理文件上传和解压缩。
- **`start_processing(self)`**: 启动二维码处理。
- **`update_status(self, message)`**: 更新状态标签和日志区域。
- **`force_gui_update(self)`**: 强制更新GUI以保持响应。
- **`processing_finished(self)`**: 处理完成后的操作。
- **`handle_processing_error(self, error_msg)`**: 处理错误信息并更新界面。

### QRCodeProcessor类
- 负责处理二维码的逻辑，连接信号以更新状态和处理结果。

### ThreadManager类
- 管理线程的启动和停止，确保处理过程不会阻塞主界面。

## 使用说明
1. 运行`main_gui.py`文件以启动应用程序。
2. 输入用户名和令牌进行登录。
3. 点击“上传压缩包”按钮选择包含二维码的压缩文件。
4. 点击“自动填写”按钮开始处理二维码。
5. 处理完成后，系统会显示处理结果和状态信息。

## 注意事项
- 请确保`unrar_win/UnRAR.exe`路径正确，以便能够解压RAR文件。
- 确保安装了所需的Python库（如PyQt5、rarfile等）。

## 贡献
欢迎任何形式的贡献，包括报告bug、提出功能请求或提交代码。

## 许可证
本项目采用MIT许可证，详细信息请参见LICENSE文件。

---

您可以根据项目的具体需求和功能进一步扩展和修改此文档。
