import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QSlider, QPushButton, QLineEdit,
                            QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QIntValidator
import numpy as np
from rgb_to_cmyk import rgb_to_cmyk, cmyk_to_rgb

class ColorPreviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QColor(255, 255, 255)
        self.setMinimumSize(200, 200)
    
    def setColor(self, color):
        self.color = color
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.color)

class ColorConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('RGB-CMYK カラーコンバーター (Japan Color 2001 Coated)')
        self.setGeometry(100, 100, 1000, 600)
        
        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # 左側（RGB）
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        self.rgb_preview = ColorPreviewWidget()
        left_layout.addWidget(QLabel('RGB プレビュー'))
        left_layout.addWidget(self.rgb_preview)
        
        # RGBスライダーとテキストボックス
        rgb_grid = QGridLayout()
        
        # R
        rgb_grid.addWidget(QLabel('R:'), 0, 0)
        self.r_slider = QSlider(Qt.Orientation.Horizontal)
        self.r_slider.setMaximum(255)
        self.r_edit = QLineEdit()
        self.r_edit.setValidator(QIntValidator(0, 255))
        rgb_grid.addWidget(self.r_slider, 0, 1)
        rgb_grid.addWidget(self.r_edit, 0, 2)
        
        # G
        rgb_grid.addWidget(QLabel('G:'), 1, 0)
        self.g_slider = QSlider(Qt.Orientation.Horizontal)
        self.g_slider.setMaximum(255)
        self.g_edit = QLineEdit()
        self.g_edit.setValidator(QIntValidator(0, 255))
        rgb_grid.addWidget(self.g_slider, 1, 1)
        rgb_grid.addWidget(self.g_edit, 1, 2)
        
        # B
        rgb_grid.addWidget(QLabel('B:'), 2, 0)
        self.b_slider = QSlider(Qt.Orientation.Horizontal)
        self.b_slider.setMaximum(255)
        self.b_edit = QLineEdit()
        self.b_edit.setValidator(QIntValidator(0, 255))
        rgb_grid.addWidget(self.b_slider, 2, 1)
        rgb_grid.addWidget(self.b_edit, 2, 2)
        
        left_layout.addLayout(rgb_grid)
        layout.addWidget(left_widget)
        
        # 右側（CMYK）
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        self.cmyk_preview = ColorPreviewWidget()
        right_layout.addWidget(QLabel('CMYK プレビュー'))
        right_layout.addWidget(self.cmyk_preview)
        
        # CMYKスライダー
        cmyk_grid = QGridLayout()
        
        # C
        cmyk_grid.addWidget(QLabel('C:'), 0, 0)
        self.c_slider = QSlider(Qt.Orientation.Horizontal)
        self.c_slider.setMaximum(100)
        self.c_label = QLabel('0%')
        cmyk_grid.addWidget(self.c_slider, 0, 1)
        cmyk_grid.addWidget(self.c_label, 0, 2)
        
        # M
        cmyk_grid.addWidget(QLabel('M:'), 1, 0)
        self.m_slider = QSlider(Qt.Orientation.Horizontal)
        self.m_slider.setMaximum(100)
        self.m_label = QLabel('0%')
        cmyk_grid.addWidget(self.m_slider, 1, 1)
        cmyk_grid.addWidget(self.m_label, 1, 2)
        
        # Y
        cmyk_grid.addWidget(QLabel('Y:'), 2, 0)
        self.y_slider = QSlider(Qt.Orientation.Horizontal)
        self.y_slider.setMaximum(100)
        self.y_label = QLabel('0%')
        cmyk_grid.addWidget(self.y_slider, 2, 1)
        cmyk_grid.addWidget(self.y_label, 2, 2)
        
        # K
        cmyk_grid.addWidget(QLabel('K:'), 3, 0)
        self.k_slider = QSlider(Qt.Orientation.Horizontal)
        self.k_slider.setMaximum(100)
        self.k_label = QLabel('0%')
        cmyk_grid.addWidget(self.k_slider, 3, 1)
        cmyk_grid.addWidget(self.k_label, 3, 2)
        
        right_layout.addLayout(cmyk_grid)
        
        # 最適化ボタン
        optimize_btn = QPushButton('CMYKを最適化')
        optimize_btn.clicked.connect(self.optimize_cmyk_values)
        right_layout.addWidget(optimize_btn)
        
        layout.addWidget(right_widget)
        
        # シグナル接続
        self.r_slider.valueChanged.connect(self.update_rgb_edit_from_slider)
        self.g_slider.valueChanged.connect(self.update_rgb_edit_from_slider)
        self.b_slider.valueChanged.connect(self.update_rgb_edit_from_slider)
        
        self.r_edit.textChanged.connect(self.update_rgb_slider_from_edit)
        self.g_edit.textChanged.connect(self.update_rgb_slider_from_edit)
        self.b_edit.textChanged.connect(self.update_rgb_slider_from_edit)
        
        self.c_slider.valueChanged.connect(self.update_cmyk_labels)
        self.m_slider.valueChanged.connect(self.update_cmyk_labels)
        self.y_slider.valueChanged.connect(self.update_cmyk_labels)
        self.k_slider.valueChanged.connect(self.update_cmyk_labels)
        
        # 初期値設定
        self.r_edit.setText('0')
        self.g_edit.setText('0')
        self.b_edit.setText('0')
        self.update_from_rgb()
    
    def update_rgb_edit_from_slider(self):
        sender = self.sender()
        if sender == self.r_slider:
            self.r_edit.setText(str(sender.value()))
        elif sender == self.g_slider:
            self.g_edit.setText(str(sender.value()))
        elif sender == self.b_slider:
            self.b_edit.setText(str(sender.value()))
        self.update_from_rgb()
    
    def update_rgb_slider_from_edit(self):
        sender = self.sender()
        try:
            value = int(sender.text() or '0')
            if sender == self.r_edit:
                self.r_slider.setValue(value)
            elif sender == self.g_edit:
                self.g_slider.setValue(value)
            elif sender == self.b_edit:
                self.b_slider.setValue(value)
            self.update_from_rgb()
        except ValueError:
            pass
    
    def update_cmyk_labels(self):
        self.c_label.setText(f"{self.c_slider.value()}%")
        self.m_label.setText(f"{self.m_slider.value()}%")
        self.y_label.setText(f"{self.y_slider.value()}%")
        self.k_label.setText(f"{self.k_slider.value()}%")
        self.update_from_cmyk()
    
    def update_from_rgb(self):
        r = self.r_slider.value()
        g = self.g_slider.value()
        b = self.b_slider.value()
        
        # RGBプレビューを更新
        self.rgb_preview.setColor(QColor(r, g, b))
        
        # CMYKを計算して更新（ただし最適化ボタンを押すまでは変更しない）
        if not hasattr(self, '_updating_cmyk'):
            self._updating_cmyk = True
            c, m, y, k = rgb_to_cmyk(r, g, b)
            
            self.c_slider.setValue(int(c))
            self.m_slider.setValue(int(m))
            self.y_slider.setValue(int(y))
            self.k_slider.setValue(int(k))
            
            # CMYKプレビューを更新
            r_cmyk, g_cmyk, b_cmyk = cmyk_to_rgb(c, m, y, k)
            self.cmyk_preview.setColor(QColor(r_cmyk, g_cmyk, b_cmyk))
            self._updating_cmyk = False
    
    def update_from_cmyk(self):
        if hasattr(self, '_updating_cmyk') and self._updating_cmyk:
            return
        
        c = self.c_slider.value()
        m = self.m_slider.value()
        y = self.y_slider.value()
        k = self.k_slider.value()
        
        # CMYKからRGBに変換
        r, g, b = cmyk_to_rgb(c, m, y, k)
        
        # CMYKプレビューを更新
        self.cmyk_preview.setColor(QColor(r, g, b))
    
    def optimize_cmyk_values(self):
        r = self.r_slider.value()
        g = self.g_slider.value()
        b = self.b_slider.value()
        
        c, m, y, k = rgb_to_cmyk(r, g, b)
        
        self._updating_cmyk = True
        self.c_slider.setValue(int(c))
        self.m_slider.setValue(int(m))
        self.y_slider.setValue(int(y))
        self.k_slider.setValue(int(k))
        self._updating_cmyk = False
        
        self.update_from_cmyk()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ColorConverter()
    ex.show()
    sys.exit(app.exec())
