import os
import sys

from GUI.MainWindow import MainWindow
from PySide6.QtWidgets import (
    QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))      # фон окна - белый
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))        # текст окна - черный
    
    palette.setColor(QPalette.Base, QColor(240, 240, 240))        # фон полей ввода - белый
    palette.setColor(QPalette.Text, QColor(0, 0, 0))              # текст в полях - черный
    
    palette.setColor(QPalette.Button, QColor(192, 192, 192))      # фон кнопок - светло-серый
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))        # текст кнопок - черный
    
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))     # выделение - синий
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))  # текст выделения - белый
    
    palette.setColor(palette.ColorRole.PlaceholderText, Qt.GlobalColor.gray)


    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220)) # подсказки
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))       # текст подсказок - черный
    app.setPalette(palette)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()