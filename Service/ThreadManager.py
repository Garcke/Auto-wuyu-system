from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool

class WorkerSignals(QObject):
    update = pyqtSignal(str)
    error = pyqtSignal(str)
    finished = pyqtSignal()

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            self.signals.error.emit(str(e))
        else:
            self.signals.finished.emit()

class ThreadManager:
    def __init__(self):
        self.threadpool = QThreadPool()

    def start_worker(self, fn, *args, **kwargs):
        worker = Worker(fn, *args, **kwargs)
        self.threadpool.start(worker)
        return worker.signals