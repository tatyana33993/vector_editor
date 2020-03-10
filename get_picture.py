#!/usr/bin/env python3
import re
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygonF


def read_file(filename):
    file = open(filename, 'r',  encoding='utf-8')
    lines = []
    ellipses = []
    rectangles = []
    polygons = []
    for line in file:
        if line.find('<line') != -1:
            arr = re.findall(r'(<line.*?/>)', line)
            for e in arr:
                lines.append(e)
        if line.find('<ellipse') != -1:
            arr = re.findall(r'(<ellipse.*?/>)', line)
            for e in arr:
                ellipses.append(e)
        if line.find('<rect') != -1:
            arr = re.findall(r'(<rect.*?/>)', line)
            for e in arr:
                rectangles.append(e)
        if line.find('<polygon') != -1:
            arr = re.findall(r'(<polygon.*?/>)', line)
            for e in arr:
                polygons.append(e)
    file.close()
    return (lines, ellipses, rectangles, polygons)


def get_pencil(line):
    stroke = re.findall(r'(stroke=".*?")', line)[0]
    pencil = stroke[stroke.find('"') + 1: stroke.rfind('"')]
    return pencil


def get_fill(line):
    fill = re.findall(r'(fill=".*?")', line)[0]
    fill = fill[fill.find('"') + 1: fill.rfind('"')]
    return fill


def get_inf_line(line):
    pencil = get_pencil(line)
    points = []
    x1 = re.findall(r'(x1=".*?")', line)[0]
    x1 = int(x1[x1.find('"') + 1: x1.rfind('"')])
    x2 = re.findall(r'(x2=".*?")', line)[0]
    x2 = int(x2[x2.find('"') + 1: x2.rfind('"')])
    y1 = re.findall(r'(y1=".*?")', line)[0]
    y1 = int(y1[y1.find('"') + 1: y1.rfind('"')])
    y2 = re.findall(r'(y2=".*?")', line)[0]
    y2 = int(y2[y2.find('"') + 1: y2.rfind('"')])
    point1 = QPoint(x1, y1)
    point2 = QPoint(x2, y2)
    points.append(point1)
    points.append(point2)
    return (points, pencil)


def get_inf_ellipse(line):
    pencil = get_pencil(line)
    fill = get_fill(line)
    points = []
    rx = re.findall(r'(rx=".*?")', line)[0]
    rx = int(rx[rx.find('"') + 1: rx.rfind('.')])
    ry = re.findall(r'(ry=".*?")', line)[0]
    ry = int(ry[ry.find('"') + 1: ry.rfind('.')])
    width = rx * 2
    height = ry * 2
    cx = re.findall(r'(cx=".*?")', line)[0]
    cx = int(cx[cx.find('"') + 1: cx.rfind('.')])
    cy = re.findall(r'(cy=".*?")', line)[0]
    cy = int(cy[cy.find('"') + 1: cy.rfind('.')])
    point = QPoint(cx - rx, cy - ry)
    points.append(point)
    return (points, width, height, pencil, fill)


def get_inf_rectangle(line):
    pencil = get_pencil(line)
    fill = get_fill(line)
    points = []
    width = re.findall(r'(width="\d*px")', line)[0]
    width = int(width[width.find('"') + 1:width.find('p')])
    height = re.findall(r'(height="\d*px")', line)[0]
    height = int(height[height.find('"') + 1:height.find('p')])
    x = re.findall(r'(x="\d*")', line)[0]
    x = int(x[x.find('"') + 1: x.rfind('"')])
    y = re.findall(r'(y="\d*")', line)[0]
    y = int(y[y.find('"') + 1: y.rfind('"')])
    point = QPoint(x, y)
    points.append(point)
    return (points, width, height, pencil, fill)


def get_inf_polygon(line):
    pencil = get_pencil(line)
    fill = get_fill(line)
    polygon = QPolygonF()
    arr_points = re.findall(r'(points=".*?")', line)[0]
    arr_points = arr_points[arr_points.find('"') + 1:arr_points.rfind('"')]
    points = arr_points.split(' ')
    for e in points:
        x, y = e.split(',')
        polygon.append(QPoint(int(x), int(y)))
    return (polygon, pencil, fill)
