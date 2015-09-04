# TestPySide.py
import sys

from PySide.QtCore import *
from PySide.QtGui import *

# Define Form
class Form(QDialog):
    def __init__(self,parent=None):
        super(Form,self).__init__(parent)
        self.setWindowTitle('Test Form') 

# Main function
if __name__=='__main__':

    # Create Qt App
    app=QApplication(sys.argv)

    # Create window
    NewForm=Form()
    NewForm.show()

    # exit
    sys.exit(app.exec_())
