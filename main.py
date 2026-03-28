import sys
from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Молочный комбинат")

    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
