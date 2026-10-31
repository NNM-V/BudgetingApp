
from PyQt6.QtWidgets import *

class MyProxyStyle(QProxyStyle):
    def styleHint(self, hint, option = None, widget = None, returnData = None):
        if hint == QStyle.StyleHint.SH_ComboBox_Popup:
            return 0
        return super().styleHint(hint, option, widget, returnData)

