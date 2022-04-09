import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie

class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, size=1.0, on_top=False):
        super(Sticker, self).__init__()
        self.timer = QtCore.QTimer(self)
        self.img_path = img_path
        self.xy = xy
        self.from_xy = xy
        self.from_xy_diff = [0, 0]
        self.to_xy = xy
        self.to_xy_diff = [0, 0]
        self.speed = 60
        self.direction = [0, 0] # x: 0(left), 1(right), y: 0(up), 1(down)
        self.size = size
        self.on_top = on_top
        self.localPos = None

        self.setupUi()
        self.show()

    #mouse actions
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.to_xy_diff == [0, 0] and self.from_xy_diff == [0, 0]:
            pass
        else:
            self.walk_diff(self.from_xy_diff, self.to_xy_diff, self.speed, restart=True)

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        self.localPos = a0.localPos()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        self.timer.stop()
        self.xy = [(a0.globalX() - self.localPos.x()), (a0.globalY() - self.localPos.y())]
        self.move(*self.xy)

    
    def walk(self, from_xy, to_xy, speed=60):
        self.from_xy = from_xy
        self.to_xy = to_xy
        self.speed = speed

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.__walkHandler)
        self.timer.start(1000 / self.speed)

    def walk_diff(self, from_xy_diff, to_xy_diff, speed=60, restart=False):
        self.from_xy_diff = from_xy_diff
        self.to_xy_diff = to_xy_diff
        self.from_xy = [self.xy[0] + self.from_xy_diff[0], self.xy[1] + self.from_xy_diff[1]]
        self.to_xy = [self.xy[0] + self.to_xy_diff[0], self.xy[1] + self.to_xy_diff[1]]
        self.speed = speed
        if restart:
            self.timer.start()
        else:
            self.timer.timeout.connect(self.__walkHandler)
            self.timer.start(1000 / self.speed)

    def __walkHandler(self):
        if self.xy[0] >= self.to_xy[0]:
            self.direction[0] = 0
        elif self.xy[0] < self.from_xy[0]:
            self.direction[0] = 1

        if self.direction[0] == 0:
            self.xy[0] -= 1
        else:
            self.xy[0] += 1

        if self.xy[1] >= self.to_xy[1]:
            self.direction[1] = 0
        elif self.xy[1] < self.from_xy[1]:
            self.direction[1] = 1

        if self.direction[1] == 0:
            self.xy[1] -= 1
        else:
            self.xy[1] += 1

        self.move(*self.xy)

    def setupUi(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)

        #if on_top is true, an object will be displayed on top
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint if self.on_top else QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        label = QtWidgets.QLabel(centralWidget)
        movie = QMovie(self.img_path)
        label.setMovie(movie)
        movie.start()
        movie.stop()

        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)

        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()

        self.setGeometry(self.xy[0], self.xy[1], w, h)

    def mouseDoubleClickEvent(self, e):
        QtWidgets.qApp.quit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)


    s1 = Sticker('images/amongus/orange.gif', xy=[1790, 770], size=0.3, on_top=True)

    s2 = Sticker('images/amongus/mint.gif', xy=[0, 895], size=0.4, on_top=True)

    s2.walk_diff(from_xy_diff=[-50, 0], to_xy_diff=[200, 0], speed=120)

    s3 = Sticker('images/pokemon/pikachu1.gif', xy=[0, 910], size=0.8, on_top=True)
    s3.walk(from_xy=[0, 910], to_xy=[1600, 910], speed=400)

    s4 = Sticker('images/pokemon/snorlax1.gif', xy=[1780, 897], size=0.3, on_top=True)

    s5 = Sticker('images/misc/wave1.gif', xy=[-61, -23], size=0.7, on_top=False)
    

    sys.exit(app.exec_())