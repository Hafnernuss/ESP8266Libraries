# MicroPython Driver TFT display HAL
import time
from .LowLevel import Driver

COLOR_BLACK   = const(0x0000)
COLOR_BLUE    = const(0x001F)
COLOR_RED     = const(0xF800)
COLOR_GREEN   = const(0x07E0)
COLOR_CYAN    = const(0x07FF)
COLOR_MAGENTA = const(0xF81F)
COLOR_YELLOW  = const(0xFFE0)
COLOR_WHITE   = const(0xFFFF)

COLOR_CRIMSON = const(0xB861)

ORIENTATION_PORTRAIT = 0
ORIENTATION_LANDSCAPE = 1
ORIENTATION_PORTRAIT2 = 2
ORIENTATION_LANDSCAPE2 = 3

class TFT(Driver):

    def __init__( self, width, height, nSPI, dc, cs, rst, bl = None , orientation = 0 ):
        self.width = width
        self.height = height

        # Driver init
        super().__init__( width, height, nSPI, dc, cs, rst, bl , orientation )

    def Clear(self, color=COLOR_WHITE):
        """
        Clear the display filling it with color.
        """
        self.Rect(0, 0, self.width, self.height, color)

    def invert(self, state=None):
        """
        Get/set display color inversion.
        """
        if state is None:
            return self.inverted
        self.write_cmd(CMD_INVON if state else CMD_INVOFF)
        self.inverted = state

    def rgbcolor(self, r, g, b):
        """
        Pack 24-bit RGB into 16-bit value.
        """
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

    def pixel(self, x, y, color):
        """
        Draw a single pixel on the display with given color.
        """
        self._set_window(x, y, x + 1, y + 1)
        self.write_pixels(1, bytearray([color >> 8, color]))

    def Rect(self, x, y, w, h, color):
        """
        Draw a rectangle with specified coordinates/size and fill with color.
        """
        # check the coordinates and trim if necessary
        if x >= self.width or y >= self.height:
            return
        if x + w - 1 >= self.width:
            w = self.width - x
        if y + h - 1 >= self.height:
            h = self.height - y

        self._set_window(x, y, x + w - 1, y + h - 1)
        self.write_pixels((w*h), bytearray([color >> 8, color]))

    def Line(self, x0, y0, x1, y1, color):
        # line is vertical
        if x0 == x1:
            # use the smallest y
            start, end = (x1, y1) if y1 < y0 else (x0, y0)
            self.VLine(start, end, abs(y1 - y0) + 1, color)

        # line is horizontal
        elif y0 == y1:
            # use the smallest x
            start, end = (x1, y1) if x1 < x0 else (x0, y0)
            self.HLine(start, end, abs(x1 - x0) + 1, color)

        else:
            # Bresenham's algorithm
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            inx = 1 if x1 - x0 > 0 else -1
            iny = 1 if y1 - y0 > 0 else -1

            # steep line
            if dx >= dy:
                dy <<= 1
                e = dy - dx
                dx <<= 1
                while x0 != x1:
                    # draw pixels
                    self.pixel(x0, y0, color)
                    if e >= 0:
                        y0 += iny
                        e -= dx
                    e += dy
                    x0 += inx

            # not steep line
            else:
                dx <<= 1
                e = dx - dy
                dy <<= 1
                while y0 != y1:
                    # draw pixels
                    self.pixel(x0, y0, color)
                    if e >= 0:
                        x0 += inx
                        e -= dy
                    e += dx
                    y0 += iny

    def HLine(self, x, y, w, color):
        if x >= self.width or y >= self.height:
            return
        if x + w - 1 >= self.width:
            w = self.width - x

        self._set_window(x, y, x + w - 1, y)
        self.write_pixels(x+w-1, bytearray([color >> 8, color]))

    def VLine(self, x, y, h, color):
        if x >= self.width or y >= self.height:
            return
        if y + h -1 >= self.height:
            h = self.height - y

        self._set_window(x, y, x, y + h - 1)
        self.write_pixels(y+h-1, bytearray([color >> 8, color]))



    def _DrawQuarterCircle(self, x, y, radius, color, lQuarters = None, bFill = False, oFillColor = None ):
        curX = radius - 1
        curY = 0
        dx = 1
        dy = 1
        err = dx - ( radius * 2 )

        while curX >= curY:

            if bFill:
                if oFillColor is None:
                    oFillColor = oColor

                self.Line( x - curY, y - curX,  x + curY, y - curX, oFillColor )
                self.Line( x - curX, y - curY,  x + curX, y - curY, oFillColor )

                self.Line( x - curX, y + curY,   x + curX, y + curY, oFillColor )
                self.Line( x - curY, y + curX,   x + curY, y + curX, oFillColor )

            if lQuarters is None or "LR" in lQuarters :
                self.pixel( x + curX, y + curY, color ) # LR QR
                self.pixel( x + curY, y + curX, color ) # LR QR

            if lQuarters is None or "LL" in lQuarters:
                self.pixel( x - curY, y + curX, color ) # LL QR
                self.pixel( x - curX, y + curY, color ) # LL QR

            if lQuarters is None or "UL" in lQuarters:
                self.pixel( x - curX, y - curY, color )  # UL QR
                self.pixel( x - curY, y - curX, color )  # UL QR

            if lQuarters is None or "UR" in lQuarters:
                self.pixel( x + curY, y - curX, color ) # UR QR
                self.pixel( x + curX, y - curY, color ) # QR


            if err <= 0:
                curY += 1
                err += dy
                dy += 2

            if err > 0:
                curX -= 1
                dx += 2
                err += dx - ( radius * 2 )

    def Circle( self, nCenterX, nCenterY, nRadius, oColor ):
        self._DrawQuarterCircle( nCenterX, nCenterY, nRadius, oColor )

    def DrawCircleSegment( self, nCenterX, nCenterY, nRadius, oColor, lSegments ):
            self._DrawQuarterCircle( nCenterX, nCenterY, nRadius, oColor, lSegments )

    def CircleFilled( self,  nCenterX, nCenterY, nRadius, oColor, oFillColor = None ):
        self._DrawQuarterCircle( nCenterX, nCenterY, nRadius, oColor, None, True, oFillColor )


    def Text(self, x, y, string, font, color, size=1):
        """
        Draw text at a given position using the user font.
        Font can be scaled with the size parameter.
        """
        if font is None:
            return

        width = size * font['width'] + 1

        px = x
        for c in string:
            self.char(px, y, c, font, color, size, size)
            px += width

            # wrap the text to the next line if it reaches the end
            if px + width > self.width:
                y += font['height'] * size + 1
                px = x

    def char(self, x, y, char, font, color, sizex=1, sizey=1):
        """
        Draw a character at a given position using the user font.

        Font is a data dictionary, can be scaled with sizex and sizey.
        """
        if font is None:
            return

        startchar = font['start']
        endchar = font['end']
        ci = ord(char)

        if startchar <= ci <= endchar:
            width = font['width']
            height = font['height']
            ci = (ci - startchar) * width

            ch = font['data'][ci:ci + width]

            # no font scaling
            px = x
            if sizex <= 1 and sizey <= 1:
                for c in ch:
                    py = y
                    for _ in range(height):
                        if c & 0x01:
                            self.pixel(px, py, color)
                        py += 1
                        c >>= 1
                    px += 1

            # scale to given sizes
            else:
                for c in ch:
                    py = y
                    for _ in range(height):
                        if c & 0x01:
                            self.Rect(px, py, sizex, sizey, color)
                        py += sizey
                        c >>= 1
                    px += sizex
        else:
            # character not found in this font
            return

    def reset(self):
        """
        Hard reset the display.
        """
        self.dc.value(0)
        self.rst.value(1)
        time.sleep_ms(500)
        self.rst.value(0)
        time.sleep_ms(500)
        self.rst.value(1)
        time.sleep_ms(500)
