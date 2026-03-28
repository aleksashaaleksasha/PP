from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.models import User
from widgets.captcha import Captcha
import os


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Авторизация")
        self.setFixedSize(450, 450)

        layout = QVBoxLayout()

        form = QGroupBox("Вход")
        f_layout = QVBoxLayout()
        self.login = QLineEdit()
        self.login.setPlaceholderText("Логин")
        self.passw = QLineEdit()
        self.passw.setPlaceholderText("Пароль")
        self.passw.setEchoMode(QLineEdit.Password)
        f_layout.addWidget(self.login)
        f_layout.addWidget(self.passw)
        form.setLayout(f_layout)
        layout.addWidget(form)

        captcha_group = QGroupBox("Соберите фрагменты")
        captcha_layout = QVBoxLayout()
        images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "widgets", "captcha")
        self.captcha = Captcha(images_dir, 100)
        captcha_layout.addWidget(self.captcha)
        captcha_group.setLayout(captcha_layout)
        layout.addWidget(captcha_group)

        btn = QPushButton("Войти")
        btn.clicked.connect(self.handle_login)
        layout.addWidget(btn)

        self.setLayout(layout)

    def handle_login(self):
        login = self.login.text().strip()
        password = self.passw.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        if not self.captcha.is_solved():
            QMessageBox.warning(self, "Ошибка", "Соберите пазл правильно!")
            return

        user, status = User.authenticate(login, password)

        if status == "blocked":
            QMessageBox.critical(self, "Доступ заблокирован", "Вы заблокированы. Обратитесь к администратору.")
            return

        if status == "success":
            QMessageBox.information(self, "Успех", "Вы успешно авторизовались!")
            self.open_main(user)
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль.")

    def open_main(self, user):
        from ui.main_window import MainWindow
        self.main = MainWindow(user)
        self.main.show()
        self.close()