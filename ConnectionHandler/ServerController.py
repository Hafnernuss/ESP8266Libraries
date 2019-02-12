import urequests

class ServerController:

    def __init__( self ):
        pass

    def init( self, sIP, sPort ):
        try:
            oRequest = urequests.get( sIP + ":" + sPort )
        except OSError as oException:
            return False

        if oRequest.text == "Hello, World!":
            return True
        else:
            return False
