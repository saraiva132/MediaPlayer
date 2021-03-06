__author__ = 'saraiva'

__author__ = 'saraiva'

''' This file is part of MediaPlayer

    MediaPlayer is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from PyQt4 import QtGui, uic
import sys


class Help(QtGui.QDialog):
    def __init__(self, parent = None):
        super(Help, self).__init__(parent = parent)

        # Load the UI
        uic.loadUi("share/ui/Help.ui", self)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Help()
    window.show()
    app.exec_()