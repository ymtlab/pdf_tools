import math
import subprocess
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import red, white, black
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import landscape, portrait

class Stamp():
    def __init__(self, path=None, parent=None, item=None):
        self.path = path
        self.parent = parent
        self.item = item
        self.squares = []
        self.circle_stamps = []
        self.resolution = 300

    def add_circle_stamp(self, item):
        self.circle_stamps.append( CircleStamp(self, item) )

    def add_square(self, item):
        self.squares.append( Square(self, item) )

    def save(self, page_size, page_rot=0):
        # set canvas
        self.canvas = canvas.Canvas( str(self.path) )
        if page_rot == 90:
            page_size = (page_size[1], page_size[0])
        self.pagesize = page_size
        self.canvas.setPageSize(page_size)
        # set shapes to canvas
        [ circle_stamp.draw() for circle_stamp in self.circle_stamps ]
        [ square.draw() for square in self.squares ]
        # save
        self.canvas.save()
        self.canvas = canvas.Canvas(self.path)
    
    def to_pdf(self, pdf_path, output_folder):
        output = output_folder / pdf_path.name
        if output.exists():
            output.unlink()
        cmd = [ 'bin\\pdftk.exe', str(pdf_path), 'stamp', str(self.path), 'output', str(output) ]
        self.subprocess_popen(cmd)

    def subprocess_popen(self, cmd):
        print(cmd)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        proc = subprocess.Popen(
            cmd, 
            encoding='cp932', 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            startupinfo=startupinfo
        )
        stdout, stderr = proc.communicate(timeout=1000)
        return stdout, stderr
        
    def p(self, x):
        return round( float(x) / float(self.resolution) * 72.0, 2 )

class Square():
    def __init__(self, parent, item):
        self.parent = parent
        self.item = item
        self.colors = {'Black':black,'White':white,'Red':red}

    def preview(self, path):
        # set canvas
        self.parent = Stamp(path, None, None)
        c = [ self.p(i) for i in self.item.data('Page size').split(',') ]
        pagesize = ( c[2] - c[0] + 2, c[3] - c[1] + 2 )
        self.parent.canvas = canvas.Canvas( str(path) )
        self.parent.canvas.setPageSize(pagesize)

        # draw
        self.parent.canvas.setStrokeColor( self.colors[self.item.data('stroke')] )
        self.parent.canvas.setFillColor( self.colors[self.item.data('fill')] )
        self.parent.canvas.rect(1, 1, pagesize[0]-2, pagesize[1]-2, stroke=True, fill=True)

        # save
        self.parent.canvas.save()

    def draw(self):
        self.parent.canvas.setStrokeColor( self.colors[self.item.data('stroke')] )
        self.parent.canvas.setFillColor( self.colors[self.item.data('fill')] )

        c = [ self.p(i) for i in self.item.data('Page size').split(',') ]
        w = c[2] - c[0]
        h = c[3] - c[1]
        x = c[0]
        y = self.parent.pagesize[1] - c[1] - h

        self.parent.canvas.rect(x, y, w, h, stroke=True, fill=True)

    def p(self, x):
        resolution = 300
        return round(float(x)/float(resolution)*72.0, 2)

class CircleStamp():
    def __init__(self, parent, item):
        self.parent = parent
        self.item = item
        self.colors = {'Black':black,'White':white,'Red':red}

    def p(self, x):
        return round(float(x)/float(self.parent.resolution)*72.0, 2)

    def preview(self, path):
        # set canvas
        self.parent = Stamp(path, None, None)
        pagesize = ( self.item.data('size')[1] + 1, self.item.data('size')[1] + 1 )
        self.parent.canvas = canvas.Canvas( str(path) )
        self.parent.canvas.setPageSize(pagesize)

        # draw
        stampsize = self.item.data('size')
        stamp_coordinate = (pagesize[0]/2, pagesize[1]/2)
        self.parent.canvas.setStrokeColor( self.colors[self.item.data('stroke')] )
        rx, ry = stampsize[0]/2.0, stampsize[1]/2.0
        self.draw_circle(stamp_coordinate[0], stamp_coordinate[1], rx, ry)
        self.parent.canvas.setStrokeColor( self.colors[self.item.data('stroke')] )
        self.draw_upper_line(stamp_coordinate[0], stamp_coordinate[1], rx, ry)
        self.draw_lower_line(stamp_coordinate[0], stamp_coordinate[1], rx, ry)
        self.draw_string(stamp_coordinate[0], stamp_coordinate[1], ry)

        # save
        self.parent.canvas.save()

    def draw(self):
        size = self.item.data('size')
        stamp_coordinate = [ self.p(s) for s in self.item.data('Page size').split(',') ]
        stamp_coordinate[1] = self.parent.pagesize[1] - stamp_coordinate[1]

        self.parent.canvas.setStrokeColor( self.colors[self.item.data('stroke')] )
        rx, ry = size[0]/2.0, size[1]/2.0
        self.draw_circle(stamp_coordinate[0], stamp_coordinate[1], rx, ry)
        self.parent.canvas.setStrokeColor( self.colors[self.item.data('stroke')] )
        self.draw_upper_line(stamp_coordinate[0], stamp_coordinate[1], rx, ry)
        self.draw_lower_line(stamp_coordinate[0], stamp_coordinate[1], rx, ry)
        self.draw_string(stamp_coordinate[0], stamp_coordinate[1], ry)

    def draw_circle(self, xc, yc, rx, ry):
        self.parent.canvas.setStrokeColor( self.colors[self.item.data('stroke')] )
        self.parent.canvas.ellipse(xc-rx, yc-ry, xc+rx, yc+ry)

    def draw_upper_line(self, xc, yc, rx, ry):
        y = ry / 3.0
        t = math.asin(1.0/3.0)
        x = rx * math.cos(t)
        self.parent.canvas.line(xc + x, yc + y, xc - x, yc + y)

    def draw_lower_line(self, xc, yc, rx, ry):
        y = -1.0 * ry / 3.0
        t = math.asin(1.0/3.0)
        x = rx * math.cos(t)
        self.parent.canvas.line(xc + x, yc + y, xc - x, yc + y)

    def draw_string(self, xc, yc, ry):
        self.parent.canvas.setFillColor(self.colors[self.item.data('stroke')])
        fp, fs, s = self.item.data('font0'), self.item.data('font_size0'), self.item.data('text0')
        pdfmetrics.registerFont(TTFont(fp.stem, str(fp)))
        self.parent.canvas.setFont(fp.stem, fs)
        self.parent.canvas.drawCentredString(xc, yc-fs*0.6+10.0*ry/15.0, s)
        
        fp, fs, s = self.item.data('font1'), self.item.data('font_size1'), self.item.data('text1')
        pdfmetrics.registerFont(TTFont(fp.stem, str(fp)))
        self.parent.canvas.setFont(fp.stem, fs)
        self.parent.canvas.drawCentredString(xc, yc-fs*0.6+1.0, s)
        
        fp, fs, s = self.item.data('font2'), self.item.data('font_size2'), self.item.data('text2')
        pdfmetrics.registerFont(TTFont(fp.stem, str(fp)))
        self.parent.canvas.setFont(fp.stem, fs)
        self.parent.canvas.drawCentredString(xc, yc-fs*0.6-7.5*ry/15.0, s)

if __name__ == '__main__':
    '''
    def w():
        return 38.0

    def s():
        return 6.0

    def t():
        return 'aaa'

    cs = CircleStamp()
    cs.stamp_size = (w, w)
    cs.font = Path('C:/Windows/Fonts/msgothic.ttc')
    cs.font_sizes = [s, s, s]
    cs.texts = [t, t, t]

    cs.save('__test__.pdf', (40.0, 40.0), (20.0, 20.0))
    '''
