import ujson
import uos

class ConfigReader:

    CONFIG_PATH = 'config.json'

    def __init__( self ):
        self.m_oData = {}
        self.m_sWIFI_SSID = ''
        self.m_sWIFI_Password = ''
        self.m_sServer_IP = ''
        self.m_sServer_Port = ''

    def init( self ):
        if ConfigReader.CONFIG_PATH not in uos.listdir():
            return False

        with open( ConfigReader.CONFIG_PATH, 'r' ) as oFile:
            self.m_oData = ujson.load( oFile )

        try:
            self.m_sWIFI_SSID = self.m_oData["Wifi"]["SSID"]
            self.m_sWIFI_Password = self.m_oData["Wifi"]["Password"]
            self.m_sServer_IP = self.m_oData["Server"]["IP"]
            self.m_sServer_Port = self.m_oData["Server"]["Port"]
        except KeyError as oError:
            print(str(oError))
            raise oError
            return False

        return True


    def GetWifiConfig( self ):
        return ( self.m_sWIFI_SSID, self.m_sWIFI_Password )

    def GetServerConfig( self ):
        return ( self.m_sServer_IP, self.m_sServer_Port )
