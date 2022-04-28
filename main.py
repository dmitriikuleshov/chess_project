from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, pyqtSlot, Qt
import sys
from chess import *


class ChooseWidget(QWidget):
    def __init__(self, main_widget, row, col, color):
        super().__init__()
        uic.loadUi('widget.ui', self)
        self.main_widget = main_widget
        self.row, self.col = row, col
        self.color = color

        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinMaxButtonsHint
                            | Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Выбор фигуры')
        self.icon_size = QSize(60, 60)

        self.make_choose_signal()

        self.btn_show_Queen.setIcon(self.main_widget.WQ_icon if self.color == WHITE else self.main_widget.BQ_icon)
        self.btn_show_Queen.setIconSize(self.icon_size)

        self.btn_show_Bishop.setIcon(self.main_widget.WB_icon if self.color == WHITE else self.main_widget.BB_icon)
        self.btn_show_Bishop.setIconSize(self.icon_size)

        self.btn_show_Knight.setIcon(self.main_widget.WN_icon if self.color == WHITE else self.main_widget.BN_icon)
        self.btn_show_Knight.setIconSize(self.icon_size)

        self.btn_show_Rook.setIcon(self.main_widget.WR_icon if self.color == WHITE else self.main_widget.BR_icon)
        self.btn_show_Rook.setIconSize(self.icon_size)

    @pyqtSlot()
    def make_choose_signal(self):
        self.btn_Queen.clicked.connect(self.set_figure)
        self.btn_Bishop.clicked.connect(self.set_figure)
        self.btn_Knight.clicked.connect(self.set_figure)
        self.btn_Rook.clicked.connect(self.set_figure)

    def set_figure(self):
        button = self.sender()
        if button is self.btn_Queen:
            self.main_widget.board.field[self.row][self.col] = Queen(self.color)
        elif button is self.btn_Bishop:
            self.main_widget.board.field[self.row][self.col] = Bishop(self.color)
        elif button is self.btn_Knight:
            self.main_widget.board.field[self.row][self.col] = Knight(self.color)
        elif button is self.btn_Rook:
            rook = Rook(self.color)
            rook.castling_passed = True
            self.main_widget.board.field[self.row][self.col] = rook
        self.main_widget.setEnabled(True)
        self.main_widget.draw_figures()
        self.close()


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('chess.ui', self)
        self.setWindowTitle('Шахматы')
        self.icon_size = QSize(81, 81)
        self.setWindowIcon(QIcon('icons/chess.ico'))
        self.btn_00.setIconSize(self.icon_size)
        self.board = Board()
        self.WP_icon = QIcon('icons/WP.ico')
        self.WR_icon = QIcon('icons/WR.ico')
        self.WK_icon = QIcon('icons/WK.ico')
        self.WB_icon = QIcon('icons/WB.ico')
        self.WN_icon = QIcon('icons/WN.ico')
        self.WQ_icon = QIcon('icons/WQ.ico')

        self.BP_icon = QIcon('icons/BP.ico')
        self.BR_icon = QIcon('icons/BR.ico')
        self.BK_icon = QIcon('icons/BK.ico')
        self.BB_icon = QIcon('icons/BB.ico')
        self.BN_icon = QIcon('icons/BN.ico')
        self.BQ_icon = QIcon('icons/BQ.ico')
        self.white_classes_icons = {"<class 'chess.King'>": self.WK_icon, "<class 'chess.Queen'>": self.WQ_icon,
                                    "<class 'chess.Bishop'>": self.WB_icon, "<class 'chess.Pawn'>": self.WP_icon,
                                    "<class 'chess.Knight'>": self.WN_icon, "<class 'chess.Rook'>": self.WR_icon}
        self.black_classes_icons = {"<class 'chess.King'>": self.BK_icon, "<class 'chess.Queen'>": self.BQ_icon,
                                    "<class 'chess.Bishop'>": self.BB_icon, "<class 'chess.Pawn'>": self.BP_icon,
                                    "<class 'chess.Knight'>": self.BN_icon, "<class 'chess.Rook'>": self.BR_icon}
        self.button_position = {self.btn_00: (0, 0), self.btn_01: (0, 1), self.btn_02: (0, 2), self.btn_03: (0, 3),
                                self.btn_04: (0, 4), self.btn_05: (0, 5), self.btn_06: (0, 6), self.btn_07: (0, 7),

                                self.btn_10: (1, 0), self.btn_11: (1, 1), self.btn_12: (1, 2), self.btn_13: (1, 3),
                                self.btn_14: (1, 4), self.btn_15: (1, 5), self.btn_16: (1, 6), self.btn_17: (1, 7),

                                self.btn_20: (2, 0), self.btn_21: (2, 1), self.btn_22: (2, 2), self.btn_23: (2, 3),
                                self.btn_24: (2, 4), self.btn_25: (2, 5), self.btn_26: (2, 6), self.btn_27: (2, 7),

                                self.btn_30: (3, 0), self.btn_31: (3, 1), self.btn_32: (3, 2), self.btn_33: (3, 3),
                                self.btn_34: (3, 4), self.btn_35: (3, 5), self.btn_36: (3, 6), self.btn_37: (3, 7),

                                self.btn_40: (4, 0), self.btn_41: (4, 1), self.btn_42: (4, 2), self.btn_43: (4, 3),
                                self.btn_44: (4, 4), self.btn_45: (4, 5), self.btn_46: (4, 6), self.btn_47: (4, 7),

                                self.btn_50: (5, 0), self.btn_51: (5, 1), self.btn_52: (5, 2), self.btn_53: (5, 3),
                                self.btn_54: (5, 4), self.btn_55: (5, 5), self.btn_56: (5, 6), self.btn_57: (5, 7),

                                self.btn_60: (6, 0), self.btn_61: (6, 1), self.btn_62: (6, 2), self.btn_63: (6, 3),
                                self.btn_64: (6, 4), self.btn_65: (6, 5), self.btn_66: (6, 6), self.btn_67: (6, 7),

                                self.btn_70: (7, 0), self.btn_71: (7, 1), self.btn_72: (7, 2), self.btn_73: (7, 3),
                                self.btn_74: (7, 4), self.btn_75: (7, 5), self.btn_76: (7, 6), self.btn_77: (7, 7)
                                }

        self.position_button = {}
        for elem in self.button_position:
            self.position_button[self.button_position[elem]] = elem
        self.draw_figures()

        self.chosen_figure = None
        for elem in self.button_position:
            elem.clicked.connect(self.move_figure)
            elem.clicked.connect(self.choose_figure)
            elem.clicked.connect(self.pawn_moved)

        self.widget = None

    def draw_figures(self):
        for i in range(8):
            for j in range(8):
                if not (self.board.field[i][j] is None):
                    figure = self.board.field[i][j]
                    if figure.get_color() == WHITE:
                        self.position_button[(i, j)].setIcon(self.white_classes_icons[str(type(figure))])
                    elif figure.get_color() == BLACK:
                        self.position_button[(i, j)].setIcon(self.black_classes_icons[str(type(figure))])
                    self.position_button[(i, j)].setIconSize(self.icon_size)
                else:
                    self.position_button[(i, j)].setIcon(QIcon(None))

    def choose_figure(self):
        self.chosen_figure = self.sender()

    def move_figure(self):
        if not (self.chosen_figure is None):
            button = self.sender()
            row = self.button_position[self.chosen_figure][0]
            col = self.button_position[self.chosen_figure][1]
            row1 = self.button_position[button][0]
            col1 = self.button_position[button][1]
            if self.board.move_piece(row, col, row1, col1):
                print(self.main_label.text())
                if self.main_label.text() == 'ХОД БЕЛЫХ':
                    self.main_label.setText('ХОД ЧЁРНЫХ')
                else:
                    self.main_label.setText('ХОД БЕЛЫХ')
                self.draw_figures()

    def pawn_moved(self):
        for i in range(8):
            if isinstance(self.board.field[7][i], Pawn):
                self.widget = ChooseWidget(self, row=7, col=i, color=WHITE)
                self.setEnabled(False)
                self.widget.show()
            elif isinstance(self.board.field[0][i], Pawn):
                self.widget = ChooseWidget(self, row=0, col=i, color=BLACK)
                self.setEnabled(False)
                self.widget.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWidget()
    MainWindow.show()
    sys.exit(app.exec_())
