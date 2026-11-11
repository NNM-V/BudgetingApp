from PySide6.QtGraphs import (
    QGraphsTheme,
    QPieSeries,
    QPieSlice,
)
from PySide6.QtCore import Qt
from PySide6.QtQuickWidgets import QQuickWidget


class PieChart(QQuickWidget):

    def __init__(self):
        super().__init__()
        # Theme
        self.theme = QGraphsTheme()
        self.theme.setTheme(QGraphsTheme.Theme.MixSeries)
        self.theme.setLabelBorderVisible(True)
        self.theme.setLabelBackgroundVisible(True)
        self.theme.setBackgroundColor(Qt.lightGray)
        # Size
        self.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.resize(1000, 720)
        # Pie series
        self.series = QPieSeries()
        self.series.setLabelsPosition(QPieSlice.LabelPosition.Outside)
        # Initial properties
        self.setInitialProperties({
            "theme": self.theme,
            "seriesList": [self.series],
        })
        # GraphsView must be loaded last
        self.loadFromModule('QtGraphs', 'GraphsView')

    def append_data(self, category_dict: dict):
        # Convert dictionary data into list
        key_list = list(category_dict.keys())
        val_list = list(category_dict.values())
        # Set list data to Label and pie slice
        self.series.setSliceLabels(key_list)
        self.series.setSliceData(val_list)
        self.series.setLabelsVisible(True)
