from atom.api import Atom, Unicode, Int, Value
from PIL import Image
from matplotlib.figure import Figure

class MagicBox( Atom ):
    fps       = Int( 20 )
    videoPath = Unicode()
    status    = Unicode()
    gif       = Value()
    currentFrame = Figure()
    gifWidth     = Int( 800 )
    gifHeight    = Int( 500 )


    def load_gif( self ):
        loc      = 'C:\\Users\\Jianfeng\\Desktop\\a.gif'
        self.gif = Image.open( loc )
        self.currentFrame.figimage( self.gif.convert('RGB') )
        self.currentFrame.canvas.draw()

        # self.currentFrame = Figure( self.gif.convert( 'RGB' ) )