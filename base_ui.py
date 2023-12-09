import sys
import torch
import cv2
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide6.QtGui import QPixmap, QImage
from main_window_ui import Ui_MainWindow
from PySide6.QtCore import QTimer

def convert2QImage(img):
    height, width, channel = img.shape
    return QImage(img.data, width, height, channel * width, QImage.Format_RGB888)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.model = torch.hub.load("./", "custom", path="runs/train/exp3/weights/best.pt", source="local")
        self.timer = QTimer()
        self.timer.setInterval(30)
        self.video = None
        self.bind_slots()

    def image_pred(self, file_path):
        results = self.model(file_path)
        image = results.render()[0]
        self.count_people(results)
        return convert2QImage(image)

    def open_image(self):
        self.timer.stop()
        file_path = QFileDialog.getOpenFileName(self, dir="./datasets/images/train", filter="*.jpg;*.png;*.jpeg")
        if file_path[0]:
            file_path = file_path[0]
            qimage = self.image_pred(file_path)
            self.input.setPixmap(QPixmap(file_path))
            self.output.setPixmap(QPixmap.fromImage(qimage))

    def video_pred(self, ):
        ret, frame = self.video.read()
        if not ret:
            self.timer.stop()
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.input.setPixmap(QPixmap.fromImage(convert2QImage(frame)))
            results = self.model(frame)
            image = results.render()[0]
            self.output.setPixmap(QPixmap.fromImage(convert2QImage(image)))
            self.count_people(results)
        

    def open_video(self):
        file_path = QFileDialog.getOpenFileName(self, dir="./datasets", filter="*.mp4")
        if file_path[0]:
            file_path = file_path[0]
            self.video = cv2.VideoCapture(file_path)
            self.timer.start()

    def count_people(self, results):
        # 假设results包含检测到的对象信息
        # 在这个例子中，我们简单地统计所有检测到的人
        people_count = sum(1 for obj in results.xyxy[0] if obj[-1] == 0)  # 0表示人类的类别标签

        # 在这里你可以使用people_count进行进一步的处理，比如显示在UI上
        print(f"人数统计: {people_count}")

     # 绑定将按钮与函数绑定           
    def bind_slots(self):
        self.detec_timage.clicked.connect(self.open_image)
        self.detect_video.clicked.connect(self.open_video)
        self.timer.timeout.connect(self.video_pred)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()