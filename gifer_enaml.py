import enaml
from   enaml.qt.qt_application import QtApplication

from magicbox import MagicBox


def main():
    with enaml.imports():
        from magicbox_ui import MagicBoxView

    box = MagicBox()
    app = QtApplication()

    view = MagicBoxView( box=box )
    view.show()

    app.start()


if __name__ == '__main__':
    main()