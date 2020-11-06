import sys

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from random import randrange

LEVELS = [(8, 10), (16, 40), (20, 70)]  # новичок, любитель, профессионал (длина поля, кол-во мин)


class Timer(QMainWindow):
    timeout = QtCore.pyqtSignal()

    def __init__(self, lcd=None, sit=False):
        super(Timer, self).__init__()
        self.timeViewer = lcd

        self.time = 0
        self.timeInterval = 1000

        self.timerUp = QtCore.QTimer()
        self.timerUp.setInterval(self.timeInterval)
        self.timerUp.timeout.connect(self.updateUptime)

        self.timerUp.start()

        # self.pushButton_5.clicked.connect(self.timerUp.stop)  # НОВАЯ ИГРА ИЛИ ПРОИГРЫШ

    def setUnit(self):
        self.timeInterval = 1000
        self.timerUp.setInterval(self.timeInterval)
        self.timerDown.setInterval(self.timeInterval)

    def updateUptime(self):
        self.time += 1
        self.settimer(self.time)

    def settimer(self, int):
        self.time = int
        self.timeViewer.display(self.time)

    def reset(self):
        self.time = 0
        self.settimer(self.time)


class Saper(Timer, QMainWindow):
    def __init__(self):
        super(Saper, self).__init__()
        uic.loadUi('saper.ui', self)

        self.buttons = []  # список всех кнопок на игровом поле

        self.reset_pole.clicked.connect(self.new_game)
        self.level_1.clicked.connect(self.game_size)
        self.level_2.clicked.connect(self.game_size)
        self.level_3.clicked.connect(self.game_size)

    def game_size(self):  # Определение размера поля, количества мин
        if self.sender().text() == 'Новичок':
            self.len_pole, self.kolvo_mines = LEVELS[0]
        elif self.sender().text() == 'Любитель':
            self.len_pole, self.kolvo_mines = LEVELS[1]
        elif self.sender().text() == 'Профессионал':
            self.len_pole, self.kolvo_mines = LEVELS[2]
        self.new_game()

    def new_game(self):  # сброс всех полей, новая игра
        # self.gridLayout.
        for row in self.buttons:
            for elem in row:
                self.gridLayout.removeWidget(elem)
                elem.setParent(None)
        self.buttons = []
        for x in range(self.len_pole):
            self.buttons.append([])
            for y in range(self.len_pole):
                btn_pole = QPushButton(self)
                btn_pole.clicked.connect(self.mine_or_no)
                self.buttons[x] = self.buttons[x] + [btn_pole]
                self.gridLayout.addWidget(btn_pole, x, y)
        self.lcdNumber.display(self.kolvo_mines)  # выводим количество мин на поле
        self.mines_spread()  # разбрасываем мины на поле
        self.timer_()  # начинаем отсчет времени игры

    def timer_(self):  # Начало отсчета время игры
        timer = Timer(self.timeViewer, True)

    def mines_spread(self):  # разбрасываем мины на поле
        self.cells = [['0' for j in range(self.len_pole)] for i in range(self.len_pole)]  # создаем список всех ячеек,
        # 0 - пустая клетка, 1 - мина
        for _ in range(self.kolvo_mines):
            row, col = randrange(self.len_pole), randrange(self.len_pole)
            while self.cells[row][col] != '0':
                row, col = randrange(self.len_pole), randrange(self.len_pole)
            self.cells[row][col] = '1'

    def mine_or_no(self):  # проверка мина или нет
        for row_ in range(len(self.buttons)):
            for i in range(len(self.buttons)):
                if self.buttons[row_][i] == self.sender():
                    row, col = row_, i
                    break
        if self.cells[row][col] == '1':
            self.the_end_game(row, col)
        else:
            self.count_mines(row, col)

    def count_mines(self, r, c):  # Подсчет сколько мин вокруг клетки
        pass

    def the_end_game(self, r, c): # Проигрыш
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Saper()
    ex.show()
    sys.exit(app.exec())
