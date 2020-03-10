#!/usr/bin/env python3
import unittest
import get_picture as g


class Testeditor(unittest.TestCase):
    lines, ellipses, rectangles, polygons = g.read_file('test.svg')

    def test_read_file(self):
        self.assertIsNotNone(self.lines)
        self.assertIsNotNone(self.ellipses)
        self.assertIsNotNone(self.rectangles)
        self.assertIsNotNone(self.polygons)

    def test_read_file_lines(self):
        self.assertEqual(self.lines[0],
                         '<line stroke="#000000" x1="61" '
                         'x2="323" y1="376" y2="196" />')

    def test_read_file_ellipses(self):
        self.assertEqual(self.ellipses[0],
                         '<ellipse cx="356.0" cy="427.0" '
                         'fill="#FFFFFF" rx="33.0" ry="33.0"'
                         ' stroke="#000000" stroke-width="1" />')
        self.assertEqual(self.ellipses[1],
                         '<ellipse cx="585.0" cy="224.0" '
                         'fill="#FFFFFF" rx="133.0" ry="58.0"'
                         ' stroke="#000000" stroke-width="1" />')

    def test_read_file_rectangles(self):
        self.assertEqual(self.rectangles[0],
                         '<rect fill="#FFFFFF" height="66px" '
                         'stroke="#000000" stroke-width="1" '
                         'width="66px" x="562" y="395" />')
        self.assertEqual(self.rectangles[1],
                         '<rect fill="#FFFFFF" height="95px" '
                         'stroke="#000000" stroke-width="1" '
                         'width="446px" x="257" y="582" />')

    def test_read_file_polygons(self):
        self.assertEqual(self.polygons[0],
                         '<polygon fill="#FFFFFF" points="851,280 '
                         '965,362 921,497 780,497 736,362" '
                         'stroke="#000000" stroke-width="1" />')
        self.assertEqual(self.polygons[1],
                         '<polygon fill="#FFFFFF" points="110,140 '
                         '125,167 94,167" stroke="#000000" '
                         'stroke-width="1" />')

    def test_get_pencil(self):
        pencil = g.get_pencil(self.lines[0])
        self.assertEqual(pencil, '#000000')

    def test_get_fill(self):
        fill = g.get_fill(self.ellipses[0])
        self.assertEqual(fill, '#FFFFFF')

    def test_get_inf_line(self):
        points, pencil = g.get_inf_line(self.lines[0])
        self.assertEqual(points[0].x(), 61)
        self.assertEqual(points[0].y(), 376)
        self.assertEqual(points[1].x(), 323)
        self.assertEqual(points[1].y(), 196)
        self.assertEqual(pencil, '#000000')

    def test_get_inf_ellipse(self):
        points, width, height,\
         pencil, fill = g.get_inf_ellipse(self.ellipses[1])
        self.assertEqual(points[0].x(), 452)
        self.assertEqual(points[0].y(), 166)
        self.assertEqual(width, 266)
        self.assertEqual(height, 116)
        self.assertEqual(pencil, '#000000')
        self.assertEqual(fill, '#FFFFFF')

    def test_get_inf_circle(self):
        points, width, height,\
         pencil, fill = g.get_inf_ellipse(self.ellipses[0])
        self.assertEqual(points[0].x(), 323)
        self.assertEqual(points[0].y(), 394)
        self.assertEqual(width, 66)
        self.assertEqual(height, 66)
        self.assertEqual(pencil, '#000000')
        self.assertEqual(fill, '#FFFFFF')

    def test_get_inf_rectangle(self):
        points, width, height,\
         pencil, fill = g.get_inf_rectangle(self.rectangles[1])
        self.assertEqual(points[0].x(), 257)
        self.assertEqual(points[0].y(), 582)
        self.assertEqual(width, 446)
        self.assertEqual(height, 95)
        self.assertEqual(pencil, '#000000')
        self.assertEqual(fill, '#FFFFFF')

    def test_get_inf_square(self):
        points, width, height,\
         pencil, fill = g.get_inf_rectangle(self.rectangles[0])
        self.assertEqual(points[0].x(), 562)
        self.assertEqual(points[0].y(), 395)
        self.assertEqual(width, 66)
        self.assertEqual(height, 66)
        self.assertEqual(pencil, '#000000')
        self.assertEqual(fill, '#FFFFFF')

    def test_get_inf_triangle(self):
        polygon, pencil, fill = g.get_inf_polygon(self.polygons[1])
        self.assertEqual(polygon[0].x(), 110)
        self.assertEqual(polygon[0].y(), 140)
        self.assertEqual(polygon[1].x(), 125)
        self.assertEqual(polygon[1].y(), 167)
        self.assertEqual(polygon[2].x(), 94)
        self.assertEqual(polygon[2].y(), 167)
        self.assertEqual(pencil, '#000000')
        self.assertEqual(fill, '#FFFFFF')

    def test_get_inf_pentagon(self):
        polygon, pencil, fill = g.get_inf_polygon(self.polygons[0])
        self.assertEqual(polygon[0].x(), 851)
        self.assertEqual(polygon[0].y(), 280)
        self.assertEqual(polygon[1].x(), 965)
        self.assertEqual(polygon[1].y(), 362)
        self.assertEqual(polygon[2].x(), 921)
        self.assertEqual(polygon[2].y(), 497)
        self.assertEqual(polygon[3].x(), 780)
        self.assertEqual(polygon[3].y(), 497)
        self.assertEqual(polygon[4].x(), 736)
        self.assertEqual(polygon[4].y(), 362)
        self.assertEqual(pencil, '#000000')
        self.assertEqual(fill, '#FFFFFF')
