import network
import utime

class WifiController:

    def __init__( self ):
        pass

    def init( self ):
        self.m_oConnection = network.WLAN( network.STA_IF )
        self.m_oConnection.active(True)
        return self.m_oConnection.active()

    def ConnectToWifi( self, sSSID, sPassword, nTimeout = 10000 ):
        self.m_oConnection.connect( sSSID, sPassword )

        nStartTime = utime.ticks_ms()
        bIsConnected = False
        while True:
            bIsConnected = self.m_oConnection.isconnected()
            if bIsConnected is True:
                break
            # has the timeout elapsed?
            if utime.ticks_ms() - nStartTime > abs(nTimeout - 10):
                break
            else:
                utime.sleep_ms(10)

        return bIsConnected

    def IsConnected( self ):
        return self.m_oConnection.isconnected()
