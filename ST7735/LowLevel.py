# MicroPython Driver TFT display driver
import time
from machine import SPI, Pin

class Driver(object):

    # command definitions
    CMD_NOP     = const(0x00) # No Operation
    CMD_SWRESET = const(0x01) # Software reset
    CMD_RDDID   = const(0x04) # Read Display ID
    CMD_RDDST   = const(0x09) # Read Display Status

    CMD_SLPIN   = const(0x10) # Sleep in & booster off
    CMD_SLPOUT  = const(0x11) # Sleep out & booster on
    CMD_PTLON   = const(0x12) # Partial mode on
    CMD_NORON   = const(0x13) # Partial off (Normal)

    CMD_INVOFF  = const(0x20) # Display inversion off
    CMD_INVON   = const(0x21) # Display inversion on
    CMD_DISPOFF = const(0x28) # Display off
    CMD_DISPON  = const(0x29) # Display on
    CMD_CASET   = const(0x2A) # Column address set
    CMD_RASET   = const(0x2B) # Row address set
    CMD_RAMWR   = const(0x2C) # Memory write
    CMD_RAMRD   = const(0x2E) # Memory read

    CMD_PTLAR   = const(0x30) # Partial start/end address set
    CMD_COLMOD  = const(0x3A) # Interface pixel format
    CMD_MADCTL  = const(0x36) # Memory data access control

    CMD_RDID1   = const(0xDA) # Read ID1
    CMD_RDID2   = const(0xDB) # Read ID2
    CMD_RDID3   = const(0xDC) # Read ID3
    CMD_RDID4   = const(0xDD) # Read ID4

    # panel function commands
    CMD_FRMCTR1 = const(0xB1) # In normal mode (Full colors)
    CMD_FRMCTR2 = const(0xB2) # In Idle mode (8-colors)
    CMD_FRMCTR3 = const(0xB3) # In partial mode + Full colors
    CMD_INVCTR  = const(0xB4) # Display inversion control

    CMD_PWCTR1  = const(0xC0) # Power control settings
    CMD_PWCTR2  = const(0xC1) # Power control settings
    CMD_PWCTR3  = const(0xC2) # In normal mode (Full colors)
    CMD_PWCTR4  = const(0xC3) # In Idle mode (8-colors)
    CMD_PWCTR5  = const(0xC4) # In partial mode + Full colors
    CMD_VMCTR1  = const(0xC5) # VCOM control

    CMD_GMCTRP1 = const(0xE0)
    CMD_GMCTRN1 = const(0xE1)

    #00 = upper left printing right
    #60 = 90 right rotation
    #C0 = 180 right rotation
    #A0 = 270 right rotation
    ORIENTATIONS = [0x00, 0x60, 0xC0, 0xA0]


    def __init__(self, width, height, spi, dc, cs, rst, bl = None , orientation = 0 ):

        """
        SPI      - SPI Bus (CLK/MOSI/MISO)
        DC       - RS/DC data/command flag
        CS       - Chip Select, enable communication
        RST/RES  - Reset
        BL/Lite  - Backlight control
        """

        # self.tab        = tab
        self.power_on     = True
        self.inverted     = False
        self.backlight_on = True
        self.orientation = Driver.ORIENTATIONS[ orientation ]

        # self.tab = tab
        self.spi = SPI(1, baudrate=8000000, polarity=1, phase=0)
        self.dc  = Pin(dc, Pin.OUT)
        self.cs  = Pin(cs, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        self.bl  = bl

        # default margins, set yours in HAL init
        self.margin_row = 0
        self.margin_col = 0

        # hard reset first
        self.reset()

        self.write_cmd(Driver.CMD_SWRESET)
        time.sleep_ms(150)
        self.write_cmd(Driver.CMD_SLPOUT)
        time.sleep_ms(255)

        # TODO: optimize data streams and delays
        self.write_cmd(Driver.CMD_FRMCTR1)
        self.write_data(bytearray([0x01, 0x2C, 0x2D]))
        self.write_cmd(Driver.CMD_FRMCTR2)
        self.write_data(bytearray([0x01, 0x2C, 0x2D, 0x01, 0x2C, 0x2D]))
        time.sleep_ms(10)

        self.write_cmd(Driver.CMD_INVCTR)
        self.write_data(bytearray([0x07]))

        self.write_cmd(Driver.CMD_PWCTR1)
        self.write_data(bytearray([0xA2, 0x02, 0x84]))
        self.write_cmd(Driver.CMD_PWCTR2)
        self.write_data(bytearray([0xC5]))
        self.write_cmd(Driver.CMD_PWCTR3)
        self.write_data(bytearray([0x8A, 0x00]))
        self.write_cmd(Driver.CMD_PWCTR4)
        self.write_data(bytearray([0x8A, 0x2A]))
        self.write_cmd(Driver.CMD_PWCTR5)
        self.write_data(bytearray([0x8A, 0xEE]))

        self.write_cmd(Driver.CMD_VMCTR1)
        self.write_data(bytearray([0x0E]))

        self.write_cmd(Driver.CMD_INVOFF)
        self.write_cmd(Driver.CMD_MADCTL)
        # self._writedata(tft._TFTRotations[self.rotate] | rgb)
        self.write_data( bytearray( [self.orientation] ) ) # RGB

        self.write_cmd(Driver.CMD_COLMOD)
        self.write_data(bytearray([0x05]))

        self.write_cmd(Driver.CMD_CASET)
        self.write_data(bytearray([0x00, 0x01, 0x00, 127]))

        self.write_cmd(Driver.CMD_RASET)
        self.write_data(bytearray([0x00, 0x01, 0x00, 119]))

        self.write_cmd(Driver.CMD_GMCTRP1)
        self.write_data(bytearray([0x02, 0x1c, 0x07, 0x12, 0x37, 0x32,
            0x29, 0x2d, 0x29, 0x25, 0x2b, 0x39, 0x00, 0x01, 0x03, 0x10]))

        self.write_cmd(Driver.CMD_GMCTRN1)
        self.write_data(bytearray([0x03, 0x1d, 0x07, 0x06, 0x2e, 0x2c,
            0x29, 0x2d, 0x2e, 0x2e, 0x37, 0x3f, 0x00, 0x00, 0x02, 0x10]))

        self.write_cmd(Driver.CMD_NORON)
        time.sleep_ms(10)

        self.write_cmd(Driver.CMD_DISPON)
        time.sleep_ms(100)


    def power(self, state=None):
        """
        Get/set display power.
        """
        if state is None:
            return self.power_on
        self.write_cmd(CMD_DISPON if state else CMD_DISPOFF)
        self.power_on = state

    def backlight(self, state=None):
        """
        Get or set the backlight status if the pin is available.
        """
        if self.bl is None:
            return None
        else:
            if state is None:
                return self.backlight_on
            self.bl.value(1 if state else 0)
            self.backlight_on = state

    def write_pixels(self, count, color):
        """
        Write pixels to the display.

        count - total number of pixels
        color - 16-bit RGB value
        """
        self.dc.value(1)
        self.cs.value(0)
        for _ in range(count):
            self.spi.write(color)
        self.cs.value(1)

    def write_cmd(self, cmd):
        """
        Display command write implementation using SPI.
        """
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)

    def write_data(self, data):
        """
        Display data write implementation using SPI.
        """
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(data)
        self.cs.value(1)

    def _set_window(self, x0, y0, x1, y1):
        """
        Set window frame boundaries.

        Any pixels written to the display will start from this area.
        """
        # set row XSTART/XEND
        self.write_cmd(CMD_RASET)
        self.write_data(bytearray(
            [0x00, y0 + self.margin_row, 0x00, y1 + self.margin_row])
        )

        # set column XSTART/XEND
        self.write_cmd(CMD_CASET)
        self.write_data(bytearray(
            [0x00, x0 + self.margin_col, 0x00, x1 + self.margin_col])
        )

        # write addresses to RAM
        self.write_cmd(CMD_RAMWR)
