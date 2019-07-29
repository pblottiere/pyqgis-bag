# -*- coding: utf-8 -*-

from PyQt5.QtQuick import QQuickView

__author__ = "Paul Blottiere"
__date__ = "July 2019"
__copyright__ = "Copyright (C) 2019 Paul Blottiere"

QML = b"""
import QtCharts 2.0
import QtQuick 2.0

ChartView {
  title: pie.title
  antialiasing: true
  legend.visible: false

  PieSeries {
    id: pieChartId

    onClicked: {
      for ( var i = 0; i < count; i++ ) {
          at(i).exploded = false
      }
      slice.exploded = true
      pie.select(slice.label)
    }
  }

  Component.onCompleted: {
    addSlices()
  }

  function sortValues(obj)
  {
    var array=[]

    for(var key in obj) {
      if(obj.hasOwnProperty(key)) {
        array.push([key, obj[key]])
      }
    }

    array.sort(function(a, b) {
      return b[1]-a[1]
    });

    var dict = {}
    for ( const index in array ) {
        const item = array[index]
        dict[item[0]] = item[1]
    }

    return dict
  }

  function addSlices() {
    pieChartId.clear()
    const slices = sortValues(pie.slices)

    for (var name in slices) {
      var slice = pieChartId.append(name, slices[name])
      slice.color = pie.labelColor(name)
    }
  }

  Connections {
    target: pie
    onUpdated: {
      addSlices()
    }
  }
}
      """


class ChartPie(QObject):

    updated = QtCore.pyqtSignal()

    def __init__(self, layer):
        super().__init__()
        self._layer = layer
        self._slices = {}
        self.initSlices()

        self._layer.styleChanged.connect(self.update)

    def initSlices(self):
        slices = {}
        total_count = self._layer.featureCount()

        renderer = self._layer.renderer()
        for item in renderer.legendSymbolItems():
            if not renderer.legendSymbolItemChecked(item.ruleKey()):
                continue

            count = self._layer.featureCount(item.ruleKey())
            slices[item.label()] = count * 100 / total_count

        self._slices = slices

    @QtCore.pyqtSlot(str, result="QColor")
    def labelColor(self, label):
        renderer = self._layer.renderer()

        for item in renderer.legendSymbolItems():
            if item.label() != label:
                continue

            return item.symbol().color()

        return QColor()

    @QtCore.pyqtProperty(str)
    def title(self):
        return self._layer.name()

    @QtCore.pyqtProperty("QVariantMap")
    def slices(self):
        return self._slices

    def update(self):
        self.initSlices()
        self.updated.emit()

    @QtCore.pyqtSlot(str)
    def select(self, label):
        renderer = self._layer.renderer()

        for item in renderer.legendSymbolItems():
            if item.label() != label:
                continue

            rule = renderer.rootRule().findRuleByKey(item.ruleKey())
            expr = rule.filterExpression()

            features = []
            for f in self._layer.getFeatures(expr):
                features.append(f.id())

            self._layer.selectByIds(features)


layer = iface.activeLayer()

if layer and layer.renderer().type() == "RuleRenderer":
    qml = QTemporaryFile()
    qml.open()
    qml.write(QML)
    qml.close()

    pie = ChartPie(layer)

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.rootContext().setContextProperty("pie", pie)
    view.setSource(QUrl.fromLocalFile(qml.fileName()))

    container = QWidget.createWindowContainer(view)
    widget = QDockWidget()
    widget.setMinimumHeight(300)
    widget.setWidget(container)

    iface.addDockWidget(Qt.LeftDockWidgetArea, widget)
else:
    print("Invalid layer")
