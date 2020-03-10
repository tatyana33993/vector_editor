#!/usr/bin/env python3
import math
from PyQt5.QtGui import QPolygonF
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen, QColor
import svgwrite
import get_picture


class Scene(QGraphicsScene):
    colors = {'black': '#000000',
              'white': '#FFFFFF',
              'dark grey': '##A9A9A9',
              'light grey': '#D3D3D3',
              'dark red': '#8B0000',
              'brown': '#A52A2A',
              'red': '#FF0000',
              'pink': '#FFC0CB',
              'orange': '#FFA500',
              'gold': '#FFD700',
              'yellow': '#FFFF00',
              'light yellow': '#FFFFE0',
              'green': '#008000',
              'forest green': '#ADFF2F',
              'turquoise': '#40E0D0',
              'light turquoise': '#AFEEEE',
              'blue': '#0000FF',
              'cornflower': '#6495ED',
              'purple': '#800080',
              'plum': '#DDA0DD'
              }
    tool = ''
    pencil = colors['black']
    fill = colors['white']
    pattern = ''
    count_clicked = 0
    clicked = []
    figure_size = 0

    def __init__(self):
        super().__init__()
        self.setSceneRect(3, 63, 995, 695)
        self.svg_document = svgwrite.Drawing(filename="picture.svg",
                                             size=("995px", "695px"))

    def draw(self):
        if self.tool == 'line' and self.count_clicked == 2:
            self.draw_line(self.clicked, self.pencil)
        if self.tool == 'circle' and self.count_clicked == 1:
            self.draw_ellipse(self.clicked, self.figure_size,
                              self.figure_size, self.pencil, self.fill)
        if self.tool == 'ellipse' and self.count_clicked == 2:
            width = self.clicked[1].x() - self.clicked[0].x()
            height = self.clicked[1].y() - self.clicked[0].y()
            self.draw_ellipse(self.clicked, width,
                              height, self.pencil, self.fill)
        if self.tool == 'square' and self.count_clicked == 1:
            self.draw_rectangle(self.clicked, self.figure_size,
                                self.figure_size, self.pencil, self.fill)
        if self.tool == 'rectangle' and self.count_clicked == 2:
            width = self.clicked[1].x() - self.clicked[0].x()
            height = self.clicked[1].y() - self.clicked[0].y()
            self.draw_rectangle(self.clicked, width,
                                height, self.pencil, self.fill)
        if self.tool == 'triangle' and self.count_clicked == 1:
            point = self.clicked[0]
            polygon = self.createPoly(3, self.figure_size,
                                      270, point)
            self.draw_polygon(polygon, self.pencil, self.fill)
        if self.tool == 'pentagon' and self.count_clicked == 1:
            point = self.clicked[0]
            polygon = self.createPoly(5, self.figure_size,
                                      270, point)
            self.draw_polygon(polygon, self.pencil, self.fill)

    def upload_picture(self, filename):
        lines, ellipses,\
         rectangles, polygons = get_picture.read_file(filename)
        if len(lines) != 0:
            for line in lines:
                points, pencil = get_picture.get_inf_line(line)
                self.draw_line(points, pencil)
        if len(ellipses) != 0:
            for ellipse in ellipses:
                points, width, height,\
                 pencil, fill = get_picture.get_inf_ellipse(ellipse)
                self.draw_ellipse(points, width, height, pencil, fill)
        if len(rectangles) != 0:
            for rectangle in rectangles:
                points, width, height,\
                 pencil, fill = get_picture.get_inf_rectangle(rectangle)
                self.draw_rectangle(points, width, height, pencil, fill)
        if len(polygons) != 0:
            for polygon in polygons:
                polygon, pencil, fill = get_picture.get_inf_polygon(polygon)
                self.draw_polygon(polygon, pencil, fill)

    def get_start_pattern(self, lines, ellipses, rectangles, polygons):
        minx = 1000
        miny = 700
        if len(lines) != 0:
            for line in lines:
                points, pencil = get_picture.get_inf_line(line)
                minx, miny = self.get_minx_miny(minx, miny, points)
        if len(ellipses) != 0:
            for ellipse in ellipses:
                points, width, height, \
                 pencil, fill = get_picture.get_inf_ellipse(ellipse)
                minx, miny = self.get_minx_miny(minx, miny, points)
        if len(rectangles) != 0:
            for rectangle in rectangles:
                points, width, height, \
                 pencil, fill = get_picture.get_inf_rectangle(rectangle)
                minx, miny = self.get_minx_miny(minx, miny, points)
        if len(polygons) != 0:
            for polygon in polygons:
                polygon, pencil, fill = get_picture.get_inf_polygon(polygon)
                minx, miny = self.get_minx_miny(minx, miny, polygon)
        x = self.clicked[0].x() - minx
        y = self.clicked[0].y() - miny
        return (x, y)

    def get_minx_miny(self, minx, miny, points):
        for point in points:
            point = QPoint(point.x() * self.figure_size / 180,
                           point.y() * self.figure_size / 180)
            if point.x() < minx:
                minx = point.x()
            if point.y() < miny:
                miny = point.y()
        return (minx, miny)

    def draw_pattern(self):
        path = './patterns/' + self.pattern
        lines, ellipses, rectangles, polygons = get_picture.read_file(path)
        x, y = self.get_start_pattern(lines, ellipses, rectangles, polygons)
        if len(lines) != 0:
            for line in lines:
                points, pencil = get_picture.get_inf_line(line)
                new_points = self.get_new_points(points, [], x, y)
                self.draw_line(new_points, pencil)
        if len(ellipses) != 0:
            for ellipse in ellipses:
                points, width, height,\
                 pencil, fill = get_picture.get_inf_ellipse(ellipse)
                new_points = self.get_new_points(points, [], x, y)
                width = width * self.figure_size / 180
                height = height * self.figure_size / 180
                self.draw_ellipse(new_points, width, height, pencil, fill)
        if len(rectangles) != 0:
            for rectangle in rectangles:
                points, width, height,\
                 pencil, fill = get_picture.get_inf_rectangle(rectangle)
                new_points = self.get_new_points(points, [], x, y)
                width = width * self.figure_size / 180
                height = height * self.figure_size / 180
                self.draw_rectangle(new_points, width, height, pencil, fill)
        if len(polygons) != 0:
            for polygon in polygons:
                polygon, pencil, fill = get_picture.get_inf_polygon(polygon)
                newpolygon = self.get_new_points(polygon, QPolygonF(), x, y)
                self.draw_polygon(newpolygon, pencil, fill)

    def get_new_points(self, points, new_points, x, y):
        for point in points:
            new_point = QPoint((point.x() * self.figure_size / 180) + x,
                               (point.y() * self.figure_size / 180) + y)
            new_points.append(new_point)
        return new_points

    def createPoly(self, n, r, s, pos):
        polygon = QPolygonF()
        w = 360 / n  # angle per step
        for i in range(n):  # add the points of polygon
            t = w * i + s
            x = r * math.cos(math.radians(t))
            y = r * math.sin(math.radians(t))
            polygon.append(QPoint(pos.x() + x, pos.y() + y))
        return polygon

    def draw_line(self, points, pencil):
        pen = QPen()
        pen.setBrush(QColor(pencil))
        point1 = points[0]
        point2 = points[1]
        self.addLine(point1.x(), point1.y(),
                     point2.x(), point2.y(), pen)
        self.svg_document.add(
            self.svg_document.line(start=(point1.x(),
                                          point1.y()),
                                   end=(point2.x(),
                                        point2.y()),
                                   stroke=pencil))
        self.resert_clicks()

    def draw_ellipse(self, points, width, height, pencil, fill):
        pen = QPen()
        pen.setBrush(QColor(pencil))
        point = points[0]
        self.addEllipse(point.x(), point.y(),
                        width, height, pen) \
            .setBrush(QColor(fill))
        self.svg_document.add(
            self.svg_document.ellipse(center=(point.x()
                                              + width / 2,
                                              point.y()
                                              + height / 2),
                                      r=(width / 2,
                                         height / 2),
                                      stroke_width="1",
                                      stroke=pencil,
                                      fill=fill))
        self.resert_clicks()

    def draw_rectangle(self, points, width, height, pencil, fill):
        pen = QPen()
        pen.setBrush(QColor(pencil))
        point = points[0]
        (self.addRect(point.x(), point.y(),
                      width, height, pen)) \
            .setBrush(QColor(fill))
        self.svg_document.add(
            self.svg_document.rect(insert=(point.x(),
                                           point.y()),
                                   size=("{}px".format(width),
                                         "{}px".format(height)),
                                   stroke_width="1",
                                   stroke=pencil,
                                   fill=fill))
        self.resert_clicks()

    def draw_polygon(self, polygon, pencil, fill):
        pen = QPen()
        pen.setBrush(QColor(pencil))
        self.addPolygon(polygon, pen) \
            .setBrush(QColor(fill))
        newpolygon = []
        for e in polygon:
            newpolygon.append((int(e.x()), int(e.y())))
        self.svg_document.add(
            self.svg_document.polygon(newpolygon,
                                      stroke_width="1",
                                      stroke=pencil,
                                      fill=fill))
        self.resert_clicks()

    def resert_clicks(self):
        self.count_clicked = 0
        self.clicked = []
