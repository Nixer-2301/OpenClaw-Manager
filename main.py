import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream, QTimer
from ui.main_window import MainWindow
from ui.splash_screen import SplashScreen
from core.settings_manager import SettingsManager
from config import APP_NAME, APP_VERSION


def load_stylesheet(app, theme='dark'):
    style_path = Path(__file__).parent / 'resources' / 'styles' / f'{theme}.qss'
    if style_path.exists():
        file = QFile(str(style_path))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            app.setStyleSheet(stream.readAll())
            file.close()
    else:
        app.setStyleSheet('')


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)

    settings_manager = SettingsManager()
    theme = settings_manager.get('interface', 'theme', 'dark')
    load_stylesheet(app, theme)

    splash = SplashScreen()
    splash.show()

    window = MainWindow()

    QTimer.singleShot(1500, lambda: (splash.close(), window.show()))

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
