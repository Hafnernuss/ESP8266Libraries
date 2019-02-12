from Libraries.ST7735 import Display
from Libraries.ST7735 import Fonts
import math

class TFTStatusLogger():


    def __init__( self, oTFT ):
        self.m_oTFT = oTFT
        self.m_oYPos = 0

    def init( self ):
        self.m_oTFT.Clear( Display.COLOR_BLACK )

    def LogTaskStart( self, sText ):
        self.m_oTFT.Text( 0, self.m_oYPos, sText, Fonts.terminalfont, Display.COLOR_WHITE, 1 )


    def LogTaskResult( self, bResult):
        if bResult:
            self.m_oTFT.Text( 90, self.m_oYPos, "[OK]", Fonts.terminalfont, Display.COLOR_GREEN, 1 )
        else:
            oTFT.Text( 90, self.m_oYPos, "[NOK]", Fonts.terminalfont, Display.COLOR_RED, 1 )

        self.m_oYPos += 10
