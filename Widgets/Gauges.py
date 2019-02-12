from ESP8266Libraries.ST7735 import Display
from ESP8266Libraries.ST7735 import Fonts
import math

class Thermometer():

    Y_BEGIN = 5
    Y_END = 155
    X_MIDPOINT = 110
    DECORATOR_CIRCLE_RADIUS = 10

    BEGIN_TEMP = 15
    END_TEMP = 25

    SCALE_MARK_MAJOR_WIDTH = 5
    SCALE_MARK_MINOR_WIDTH = 2

    def __init__( self, tft ):
        self.tft = tft
        self.nCurrentTemperature = Thermometer.END_TEMP

    def init( self ):

        nCircleMidPointY = Thermometer.Y_END - Thermometer.DECORATOR_CIRCLE_RADIUS
        self.nScaleWidth = int( ( Thermometer.DECORATOR_CIRCLE_RADIUS / 2 ) - 2 ) * 2

        self.tft.CircleFilled( Thermometer.X_MIDPOINT, nCircleMidPointY, Thermometer.DECORATOR_CIRCLE_RADIUS, Display.COLOR_BLACK, Display.COLOR_CRIMSON )
        self.tft.Circle(Thermometer.X_MIDPOINT, nCircleMidPointY, Thermometer.DECORATOR_CIRCLE_RADIUS, Display.COLOR_BLACK )
        self.tft.Rect( int(Thermometer.X_MIDPOINT - self.nScaleWidth / 2), nCircleMidPointY - Thermometer.DECORATOR_CIRCLE_RADIUS, self.nScaleWidth, Thermometer.DECORATOR_CIRCLE_RADIUS, Display.COLOR_CRIMSON )

        #Draw Top Decorator

        self.nScaleStartY = Thermometer.Y_BEGIN + int( self.nScaleWidth / 2 )
        self.nScaleStartX = Thermometer.X_MIDPOINT - int( self.nScaleWidth / 2 )
        self.nScaleEndX = Thermometer.X_MIDPOINT + int( self.nScaleWidth / 2 )
        self.nScaleEndY = nCircleMidPointY - Thermometer.DECORATOR_CIRCLE_RADIUS

        self.nScaleHeight = self.nScaleEndY - self.nScaleStartY

        self.tft.DrawCircleSegment( Thermometer.X_MIDPOINT, Thermometer.Y_BEGIN + int( self.nScaleWidth / 2 ), int( self.nScaleWidth / 2 ), Display.COLOR_BLACK, ["UL", "UR"] )

        # Left Scale Line, twice for double line thickness
        self.tft.VLine( self.nScaleStartX, self.nScaleStartY, self.nScaleHeight, Display.COLOR_BLACK )
        # Right Scale Line, twice for double line thickness
        self.tft.VLine( self.nScaleEndX, self.nScaleStartY, self.nScaleHeight, Display.COLOR_BLACK )

        nDeltaDegrees = int( Thermometer.END_TEMP - Thermometer.BEGIN_TEMP ) + 1
        self.nPixelsPerDegree = int( self.nScaleHeight / (nDeltaDegrees - 1 ) )

        for nPos in range( nDeltaDegrees ):
            # Mainscale
            self.tft.HLine( self.nScaleStartX - Thermometer.SCALE_MARK_MAJOR_WIDTH, self.nScaleStartY + self.nPixelsPerDegree * nPos, Thermometer.SCALE_MARK_MAJOR_WIDTH, Display.COLOR_BLACK ) # Mainscale
            # Scaletext
            self.tft.Text( self.nScaleStartX - 20, self.nScaleStartY - 3 + self.nPixelsPerDegree * nPos, str( Thermometer.END_TEMP - nPos), Fonts.terminalfont, 1 )
            # Helperscale
            if nPos > 0:
                self.tft.HLine( self.nScaleStartX - Thermometer.SCALE_MARK_MINOR_WIDTH,
                                self.nScaleStartY - int( self.nPixelsPerDegree / 2 ) + self.nPixelsPerDegree * nPos, Thermometer.SCALE_MARK_MINOR_WIDTH, Display.COLOR_BLACK ) # Mainscale
            if nPos == nDeltaDegrees - 1:
                self.nScaleEndY  = self.nScaleStartY + self.nPixelsPerDegree * nPos

        self.nScaleHeight = self.nScaleEndY - self.nScaleStartY

    def SetTemperature( self, nTemp ):
        if nTemp == self.nCurrentTemperature:
            return



        #if nTemp > self.nCurrentTemperature:
        fMinorScaleAmount = divmod( nTemp, 1)
        nFillHeight = int( self.nPixelsPerDegree * ( int( fMinorScaleAmount[0] ) - Thermometer.BEGIN_TEMP ) ) + round( self.nPixelsPerDegree * fMinorScaleAmount[1] )
        print( nTemp )
        print( fMinorScaleAmount )

        # Clear Scale
        self.tft.Rect( self.nScaleStartX + 1, self.nScaleStartY, self.nScaleWidth - 1, self.nScaleHeight, Display.COLOR_WHITE )

        # Clear temp reading
        #self.tft.Rect( self.nScaleStartX + 1 + self.nScaleWidth, self.nScaleStartY, self.nScaleWidth - 1, self.nScaleHeight, Display.COLOR_WHITE )

        #redraw scale according to temp
        self.tft.Rect( self.nScaleStartX + 1, self.nScaleStartY + ( self.nScaleHeight - nFillHeight), self.nScaleWidth - 1, nFillHeight + + self.nPixelsPerDegree, Display.COLOR_CRIMSON )

        # render hline and text
        #self.tft.HLine( self.nScaleStartX + 1 + self.nScaleWidth, self.nScaleStartY + ( self.nScaleHeight - nFillHeight), Thermometer.SCALE_MARK_MINOR_WIDTH, Display.COLOR_BLACK )

        #self.tft.Text( self.nScaleStartX + 1 + self.nScaleWidth + Thermometer.SCALE_MARK_MINOR_WIDTH, self.nScaleStartY + ( self.nScaleHeight - nFillHeight) - 3, str( nTemp ), Fonts.terminalfont, 1 )
        self.tft.Rect( 10, 10, 30, 30,  Display.COLOR_WHITE )
        self.tft.Text( 10, 10, str( nTemp ), Fonts.terminalfont, 2 )
