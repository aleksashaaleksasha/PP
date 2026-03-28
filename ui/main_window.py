from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, \
    QTableWidgetItem, QMessageBox, QLineEdit, QCheckBox, QGroupBox, QFormLayout
from PyQt5.QtCore import Qt
from database.models import User
from database.db_connection import DatabaseConnection


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"Молочный комбинат - {user.username}")
        self.setMinimumSize(800, 500)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        top = QHBoxLayout()
        top.addWidget(QLabel(f"Пользователь: {user.username}"))
        top.addWidget(QLabel(f"Роль: {'Админ' if user.is_admin else 'Пользователь'}"))
        top.addStretch()
        logout = QPushButton("Выход")
        logout.clicked.connect(self.logout)
        top.addWidget(logout)
        layout.addLayout(top)

        if user.is_admin:
            self.create_admin_panel(layout)
        else:
            layout.addWidget(QLabel("Добро пожаловать!"))

        central.setLayout(layout)

    def create_admin_panel(self, layout):
        layout.addWidget(QLabel("Управление пользователями"))

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "Админ", "Заблокирован"])
        layout.addWidget(self.table)

        self.load_users()

        form = QGroupBox("Добавить/Изменить")
        f_layout = QFormLayout()
        self.user_id = QLineEdit()
        self.user_id.setReadOnly(True)
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.is_admin_cb = QCheckBox()
        f_layout.addRow("ID:", self.user_id)
        f_layout.addRow("Логин:", self.username)
        f_layout.addRow("Пароль:", self.password)
        f_layout.addRow("Админ:", self.is_admin_cb)
        form.setLayout(f_layout)
        layout.addWidget(form)

        btns = QHBoxLayout()
        add = QPushButton("Добавить")
        add.clicked.connect(self.add_user)
        update = QPushButton("Обновить")
        update.clicked.connect(self.update_user)
        unblock = QPushButton("Разблокировать")
        unblock.clicked.connect(self.unblock_user)
        delete = QPushButton("Удалить")
        delete.clicked.connect(self.delete_user)
        clear = QPushButton("Очистить")
        clear.clicked.connect(self.clear_form)
        refresh = QPushButton("Обновить")
        refresh.clicked.connect(self.load_users)
        btns.addWidget(add)
        btns.addWidget(update)
        btns.addWidget(unblock)
        btns.addWidget(delete)
        btns.addWidget(clear)
        btns.addStretch()
        btns.addWidget(refresh)
        layout.addLayout(btns)

        self.table.itemSelectionChanged.connect(self.on_select)

    def load_users(self):
        users = User.get_all_users()
        self.table.setRowCount(len(users))
        for i, u in enumerate(users):
            self.table.setItem(i, 0, QTableWidgetItem(str(u[0])))
            self.table.setItem(i, 1, QTableWidgetItem(u[1]))
            self.table.setItem(i, 2, QTableWidgetItem("Да" if u[2] else "Нет"))
            self.table.setItem(i, 3, QTableWidgetItem("Да" if u[3] else "Нет"))
        self.table.resizeColumnsToContents()

    def on_select(self):
        selected = self.table.selectedItems()
        if selected:
            row = selected[0].row()
            self.user_id.setText(self.table.item(row, 0).text())
            self.username.setText(self.table.item(row, 1).text())
            self.is_admin_cb.setChecked(self.table.item(row, 2).text() == "Да")
            self.password.clear()

    def add_user(self):
        if not self.username.text() or not self.password.text():
            QMessageBox.warning(self, "Ошибка", "Заполните логин и пароль!")
            return
        ok, msg = User.create_user(self.username.text(), self.password.text(), self.is_admin_cb.isChecked())
        QMessageBox.information(self, "Успех" if ok else "Ошибка", msg)
        if ok:
            self.clear_form()
            self.load_users()

    def update_user(self):
        if not self.user_id.text():
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя!")
            return
        pwd = self.password.text()
        if not pwd:
            cur = DatabaseConnection().get_cursor()
            cur.execute("SELECT password FROM users WHERE user_id=%s", (self.user_id.text(),))
            pwd = cur.fetchone()[0]
        ok, msg = User.update_user(int(self.user_id.text()), self.username.text(), pwd, self.is_admin_cb.isChecked())
        QMessageBox.information(self, "Успех" if ok else "Ошибка", msg)
        if ok:
            self.clear_form()
            self.load_users()

    def unblock_user(self):
        if not self.user_id.text():
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя!")
            return
        User.unblock_user(int(self.user_id.text()))
        QMessageBox.information(self, "Успех", "Пользователь разблокирован!")
        self.clear_form()
        self.load_users()

    def delete_user(self):
        if not self.user_id.text():
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя!")
            return
        if self.username.text() == self.user.username:
            QMessageBox.warning(self, "Ошибка", "Нельзя удалить себя!")
            return
        User.delete_user(int(self.user_id.text()))
        QMessageBox.information(self, "Успех", "Пользователь удален!")
        self.clear_form()
        self.load_users()

    def clear_form(self):
        self.user_id.clear()
        self.username.clear()
        self.password.clear()
        self.is_admin_cb.setChecked(False)

    def logout(self):
        self.close()
        from ui.login_window import LoginWindow
        self.login = LoginWindow()
        self.login.show()