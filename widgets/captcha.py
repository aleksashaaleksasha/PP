from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QTransform
import random
import os


class Captcha(QWidget):
    def __init__(self, images_dir, piece_size=100):
        super().__init__()
        self.images_dir = images_dir
        self.piece_size = piece_size
        self.pieces = []
        self.rotations = [random.choice([0, 90, 180, 270]) for _ in range(4)]
        self.buttons = []
        self.init_ui()

    def load_pieces(self):
        pieces = []
        for i in range(1, 5):
            path = os.path.join(self.images_dir, f"{i}.png")
            if not os.path.exists(path):
                path = os.path.join(self.images_dir, f"{i}.jpg")
            if os.path.exists(path):
                pix = QPixmap(path).scaled(self.piece_size, self.piece_size, Qt.IgnoreAspectRatio,
                                           Qt.SmoothTransformation)
                pieces.append(pix)
        return pieces if len(pieces) == 4 else None

    def rotate(self, pix, angle):
        t = QTransform()
        t.rotate(angle)
        return pix.transformed(t, Qt.SmoothTransformation)

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        pieces = self.load_pieces()
        if not pieces:
            return

        self.pieces = pieces

        total_size = self.piece_size * 2
        self.setFixedSize(total_size, total_size)

        for i, rot in enumerate(self.rotations):
            btn = QPushButton()
            btn.setFixedSize(self.piece_size, self.piece_size)
            btn.setIcon(QIcon(self.rotate(pieces[i], rot)))
            btn.setIconSize(QSize(self.piece_size, self.piece_size))
            btn.clicked.connect(lambda _, idx=i: self.rotate_piece(idx))
            btn.setStyleSheet("padding: 0px; margin: 0px;")
            layout.addWidget(btn, i // 2, i % 2)
            self.buttons.append(btn)

        self.setLayout(layout)

    def rotate_piece(self, idx):
        self.rotations[idx] = (self.rotations[idx] + 90) % 360
        self.buttons[idx].setIcon(QIcon(self.rotate(self.pieces[idx], self.rotations[idx])))

    def is_solved(self):
        return all(r == 0 for r in self.rotations)