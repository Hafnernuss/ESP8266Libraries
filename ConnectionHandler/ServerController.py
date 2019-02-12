import urequests

class ServerController:

    def __init__( self ):
        pass

    def init( self ):
        try:
            oRequest = urequests.get( "http://10.0.0.20:5000" )
        except OSError as oException:
            return False

        if oRequest.text == "Hello, World!":
            return True
        else:
            return False
