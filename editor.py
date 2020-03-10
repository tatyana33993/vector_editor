#!/usr/bin/env python3
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication,\
    QGraphicsView, QDockWidget, QWidget, QVBoxLayout, QPushButton,\
    QSlider, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from functools import partial
import drawing_scene


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scene = drawing_scene.Scene()
        self.pencils = QDockWidget('Pencils')
        self.fills = QDockWidget('Fills')
        self.patterns = QDockWidget('Patterns')
        self.initUI()

    def initUI(self):
        pattern = QAction(QIcon('./icons/pattern.png'), 'Pattern', self)
        pattern.triggered.connect(partial(self.add_patterns))

        pencil = QAction(QIcon('./icons/pencil.png'), 'Pencil', self)
        pencil.triggered.connect(partial(self.add_pencils))

        fill = QAction(QIcon('./icons/fill.png'), 'Fill', self)
        fill.triggered.connect(partial(self.add_fills))

        eraser = QAction(QIcon('./icons/eraser.png'), 'Eraser', self)
        eraser.triggered.connect(partial(self.scene.clear))

        line = QAction(QIcon('./icons/line.png'), 'Line', self)
        line.triggered.connect(partial(self.remake_tool, 'line'))

        circle = QAction(QIcon('./icons/circle.png'), 'Circle', self)
        circle.triggered.connect(partial(self.remake_tool, 'circle'))

        ellipse = QAction(QIcon('./icons/ellipse.png'), 'Ellipse', self)
        ellipse.triggered.connect(partial(self.remake_tool, 'ellipse'))

        square = QAction(QIcon('./icons/square.png'), 'Square', self)
        square.triggered.connect(partial(self.remake_tool, 'square'))

        rectangle = QAction(QIcon('./icons/rectangle.png'), 'Rectangle', self)
        rectangle.triggered.connect(partial(self.remake_tool, 'rectangle'))

        triangle = QAction(QIcon('./icons/triangle.png'), 'Triangle', self)
        triangle.triggered.connect(partial(self.remake_tool, 'triangle'))

        pentagon = QAction(QIcon('./icons/pentagon.png'), 'Pentagon', self)
        pentagon.triggered.connect(partial(self.remake_tool, 'pentagon'))

        self.toolbar = self.addToolBar('Pencil')
        self.toolbar.addAction(pencil)
        self.toolbar = self.addToolBar('Fill')
        self.toolbar.addAction(fill)
        self.toolbar = self.addToolBar('Line')
        self.toolbar.addAction(line)
        self.toolbar = self.addToolBar('Circle')
        self.toolbar.addAction(circle)
        self.toolbar = self.addToolBar('Ellipse')
        self.toolbar.addAction(ellipse)
        self.toolbar = self.addToolBar('Square')
        self.toolbar.addAction(square)
        self.toolbar = self.addToolBar('Rectangle')
        self.toolbar.addAction(rectangle)
        self.toolbar = self.addToolBar('Triangle')
        self.toolbar.addAction(triangle)
        self.toolbar = self.addToolBar('Pentagon')
        self.toolbar.addAction(pentagon)
        self.toolbar = self.addToolBar('Eraser')
        self.toolbar.addAction(eraser)
        self.toolbar = self.addToolBar('Pattern')
        self.toolbar.addAction(pattern)

        self.setGeometry(200, 200, 1000, 700)
        self.setWindowTitle('Vector editor')
        self.setWindowIcon(QIcon('./icons/editor.png'))

        openFile = QAction(QIcon('./icons/file.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.show_dialog_open)

        saveFile = QAction(QIcon('./icons/save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(partial(self.show_dialog_save, '/paint'))

        createPattern = QAction(QIcon('./icons/pattern.png'),
                                'Create pattern', self)
        createPattern.setStatusTip('Create new pattern')
        createPattern.triggered.connect(partial
                                        (self.show_dialog_create_pattern,
                                         './patterns/pattern'))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu = menubar.addMenu('&Save')
        fileMenu.addAction(saveFile)
        fileMenu = menubar.addMenu('&Create pattern')
        fileMenu.addAction(createPattern)

        view = QGraphicsView()
        view.setScene(self.scene)
        view.setFixedWidth(1000)
        view.setFixedHeight(700)
        view.show()
        self.setCentralWidget(view)
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(600, 25, 360, 30)
        sld.valueChanged.connect(self.remake_size)
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.scene.count_clicked += 1
            self.scene.clicked.append(event.pos())
            if self.scene.tool == 'pattern':
                self.scene.draw_pattern()
            else:
                self.scene.draw()

    def remake_tool(self, tool):
        self.scene.tool = tool

    def add_pencils(self):
        self.addDockWidget(Qt.RightDockWidgetArea, self.pencils)
        dockedWidget = QWidget(self)
        dockedWidget.setFixedHeight(600)
        dockedWidget.setFixedWidth(100)
        self.pencils.setWidget(dockedWidget)
        dockedWidget.setLayout(QVBoxLayout())
        for k in self.scene.colors.keys():
            col = QPushButton(k)
            col.clicked.connect(partial(self.remake_pencil, k))
            dockedWidget.layout().addWidget(col)

    def add_fills(self):
        self.addDockWidget(Qt.RightDockWidgetArea, self.fills)
        dockedWidget = QWidget(self)
        dockedWidget.setFixedHeight(600)
        dockedWidget.setFixedWidth(100)
        self.fills.setWidget(dockedWidget)
        dockedWidget.setLayout(QVBoxLayout())
        for k in self.scene.colors.keys():
            col = QPushButton(k)
            col.clicked.connect(partial(self.remake_fill, k))
            dockedWidget.layout().addWidget(col)

    def remake_pencil(self, pencil):
        self.scene.pencil = self.scene.colors[pencil]

    def remake_fill(self, fill):
        self.scene.fill = self.scene.colors[fill]

    def remake_size(self, value):
        self.scene.figure_size = value * 3

    def show_dialog_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            '/paint', filter='*.svg')
        filename, _ = fname

        self.scene.upload_picture(filename)

    def show_dialog_save(self, path):
        fname = QFileDialog.getSaveFileName(self, 'Save file', path,
                                            filter='*.svg')
        filename, _ = fname
        self.scene.svg_document.save()
        put = open('picture.svg', 'r')
        output = open(filename, 'w')
        for line in put:
            output.write(line)
        put.close()
        output.close()

    def show_dialog_create_pattern(self, path):
        self.show_dialog_save(path)

    def add_patterns(self):
        self.remake_tool('pattern')
        patterrnsnames = os.listdir('./patterns')
        self.addDockWidget(Qt.RightDockWidgetArea, self.patterns)
        dockedWidget = QWidget(self)
        dockedWidget.setFixedHeight(600)
        dockedWidget.setFixedWidth(100)
        self.patterns.setWidget(dockedWidget)
        dockedWidget.setLayout(QVBoxLayout())
        for e in patterrnsnames:
            if e.find('.svg') != -1:
                name = QPushButton(e.replace('.svg', ''))
                name.clicked.connect(partial(self.remake_pattern, e))
                dockedWidget.layout().addWidget(name)

    def remake_pattern(self, name):
        self.scene.pattern = name


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
