import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ElementProperties(QDialog):
    def __init__(self, item):
        super().__init__()
        self.item = item
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Element Properties")
        layout = QVBoxLayout()

        if isinstance(self.item, LogicGate):
            self.label_edit = QLineEdit(self.item.label)
            self.input_count_spin = QSpinBox()
            self.input_count_spin.setMinimum(1)
            self.input_count_spin.setMaximum(8)
            self.input_count_spin.setValue(self.item.input_count)

            layout.addWidget(QLabel("Label:"))
            layout.addWidget(self.label_edit)
            layout.addWidget(QLabel("Input Count:"))
            layout.addWidget(self.input_count_spin)

        elif isinstance(self.item, InputPin) or isinstance(self.item, OutputPin):
            self.label_edit = QLineEdit(self.item.label)
            self.color_button = QPushButton("Select Color")
            self.color_button.clicked.connect(self.choose_color)

            layout.addWidget(QLabel("Label:"))
            layout.addWidget(self.label_edit)
            layout.addWidget(QLabel("Color:"))
            layout.addWidget(self.color_button)

            if hasattr(self.item, 'color'):
                self.color_button.setStyleSheet("background-color: {}".format(self.item.color.name()))

            if isinstance(self.item, InputPin):
                self.initial_state_checkbox = QCheckBox("Initial State")
                self.initial_state_checkbox.setChecked(self.item.value())
                layout.addWidget(self.initial_state_checkbox)

        elif isinstance(self.item, Wire):
            self.label_edit = QLineEdit(self.item.label)
            self.color_button = QPushButton("Select Color")
            self.color_button.clicked.connect(self.choose_color)

            layout.addWidget(QLabel("Label:"))
            layout.addWidget(self.label_edit)
            layout.addWidget(QLabel("Color:"))
            layout.addWidget(self.color_button)

            if hasattr(self.item, 'color'):
                self.color_button.setStyleSheet("background-color: {}".format(self.item.color.name()))

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def accept(self):
        if isinstance(self.item, LogicGate):
            self.item.label = self.label_edit.text()
            self.item.input_count = self.input_count_spin.value()
        elif isinstance(self.item, InputPin) or isinstance(self.item, OutputPin):
            self.item.label = self.label_edit.text()
            if hasattr(self.item, 'color'):
                self.item.color = QColor(self.color_button.styleSheet().split(": ")[1])
            if isinstance(self.item, InputPin):
                if hasattr(self.item, 'initial_state_checkbox'):
                    self.item._state = self.initial_state_checkbox.isChecked()
        elif isinstance(self.item, Wire):
            self.item.label = self.label_edit.text()
            if hasattr(self.item, 'color'):
                self.item.color = QColor(self.color_button.styleSheet().split(": ")[1])

        super().accept()

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            sender = self.sender()
            sender.setStyleSheet("background-color: {}".format(color.name()))

class InputPin(QGraphicsItem):
    size = 30

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rect = QRectF(-self.size / 2, -self.size / 2, self.size, self.size)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setAcceptHoverEvents(True)
        self.output = QPointF(5, -5)
        self._state = False
        self.label = "Input Pin"
        self.color = QColor("gray")

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(self.boundingRect())

        if self._state:
            painter.setBrush(QBrush(QColor("green")))
        else:
            painter.setBrush(QBrush(QColor("red")))
        painter.drawEllipse(self.boundingRect().adjusted(5, 5, -5, -5))

        painter.setPen(QPen(QColor("black")))
        painter.drawText(self.boundingRect().adjusted(0, 5, 0, 0),
                         Qt.AlignHCenter, "{}".format(1 if self._state else 0))

        painter.drawRect(int(self.output.x()), int(self.output.y()), 10, 10)

    def mouseReleaseEvent(self, event):
        self.scene().clearSelection()
        self.setZValue(1)
        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setZValue(2)
            self._state = not self._state
            self.update()
            self.scene().update()
        print("INPUT pin clicked - {}".format("ON" if self._state else "OFF"))

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for sel_item in self.scene().selectedItems():
                sel_item.update()

    def value(self):
        return self._state

    def contextMenuEvent(self, event):
        menu = QMenu()
        properties_action = QAction("Properties", self)
        properties_action.triggered.connect(self.show_properties)
        menu.addAction(properties_action)
        menu.exec_(event.screenPos())

    def show_properties(self):
        dialog = ElementProperties(self)
        dialog.exec_()

class OutputPin(QGraphicsItem):
    size = 30

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rect = QRectF(-self.size / 2, -self.size / 2, self.size, self.size)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setAcceptHoverEvents(True)
        self.input = QPointF(-15, -5)
        self._state = False
        self.label = "Output Pin"
        self.color = QColor("gray")

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.color))
        painter.drawRect(self.boundingRect())

        if self._state:
            painter.setBrush(QBrush(QColor("green")))
        else:
            painter.setBrush(QBrush(QColor("red")))
        painter.drawRect(self.boundingRect().adjusted(5, 5, -5, -5))

        painter.setPen(QPen(QColor("black")))
        painter.drawText(self.boundingRect().adjusted(0, 5, 0, 0),
                         Qt.AlignHCenter, "{}".format(1 if self._state else 0))

        painter.drawRect(int(self.input.x()), int(self.input.y()), 10, 10)

    def mousePressEvent(self, event):
        self.setZValue(2)
        print("OUTPUT pin clicked - {}".format("ON" if self._state else "OFF"))

    def mouseReleaseEvent(self, event):
        self.scene().clearSelection()
        self.setZValue(1)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for sel_item in self.scene().selectedItems():
                sel_item.update()

    def value(self):
        return self._state

    def setValue(self, state):
        self._state = state
        self.update()
        self.scene().update()

    def contextMenuEvent(self, event):
        menu = QMenu()
        properties_action = QAction("Properties", self)
        properties_action.triggered.connect(self.show_properties)
        menu.addAction(properties_action)
        menu.exec_(event.screenPos())

    def show_properties(self):
        dialog = ElementProperties(self)
        dialog.exec_()

class LogicGate(QGraphicsItem):
    def __init__(self, label, input_count=2):
        super().__init__()
        self.label = label
        self.input_count = input_count
        self.input_nodes = [QPointF(-20, i * 20 - 10) for i in range(input_count)]
        self.output_node = QPointF(40, 10)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.values = [0] * input_count

    def boundingRect(self):
        return QRectF(-30, -30, 60, 60)

    def paint(self, painter, option, widget):
        painter.drawRect(-20, -20, 40, 40)
        painter.drawText(-10, 0, self.label)
        painter.setBrush(Qt.black)
        for node in self.input_nodes:
            painter.drawEllipse(node, 3, 3)
        painter.drawEllipse(self.output_node, 3, 3)

    def set_input_value(self, index, value):
        self.values[index] = value
        self.update()

    def get_output_value(self):
        if self.label == "AND":
            if all(self.values):
                return 1
            else:
                return 0
        elif self.label == "OR":
            if any(self.values):
                return 1
            else:
                return 0
        elif self.label == "NOT":
            if self.values[0] == 0:
                return 1
            else:
                return 0
        elif self.label == "NAND":
            if all(self.values):
                return 0
            else:
                return 1
        elif self.label == "NOR":
            if all(not value for value in self.values):
                return 1
            else:
                return 0
        elif self.label == "XOR":
            if sum(self.values) % 2 == 1:
                return 1
            else:
                return 0
        elif self.label == "XNOR":
            if sum(self.values) % 2 == 0:
                return 1
            else:
                return 0
        return 0

    def update_outputs(self):
        output_value = self.get_output_value()
        for wire in self.scene().items():
            if isinstance(wire, Wire) and wire.start_item == self:
                if isinstance(wire.end_item, OutputPin):
                    wire.end_item.setValue(output_value)
                elif isinstance(wire.end_item, LogicGate):
                    for index, node in enumerate(wire.end_item.input_nodes):
                        if wire.end_item.mapFromScene(wire.start_item.scenePos()) == node:
                            wire.end_item.set_input_value(index, output_value)
                            wire.end_item.update_outputs()
                            break
    def contextMenuEvent(self, event):
        menu = QMenu()
        properties_action = QAction("Properties", self)
        properties_action.triggered.connect(self.show_properties)
        menu.addAction(properties_action)
        menu.exec_(event.screenPos())

    def show_properties(self):
        dialog = ElementProperties(self)
        dialog.exec_()

class Wire(QGraphicsLineItem):
    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.update_position()
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setPen(QPen(Qt.black, 2))
        self.label = "Wire"
        self.color = QColor("black")

    def update_position(self):
        self.setLine(QLineF(self.start_item.scenePos(), self.end_item.scenePos()))

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(self.color, 2))
        painter.drawLine(self.line())

    def contextMenuEvent(self, event):
        menu = QMenu()
        properties_action = QAction("Properties", self)
        properties_action.triggered.connect(self.show_properties)
        menu.addAction(properties_action)
        menu.exec_(event.screenPos())

    def show_properties(self):
        dialog = ElementProperties(self)
        dialog.exec_()

class LogicSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Basit Mantık Devreleri')

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.toolbar = self.addToolBar('Toolbar')


        self.add_gate_action = QAction('Kapı Ekle', self)
        self.add_gate_action.triggered.connect(self.add_gate)
        self.toolbar.addAction(self.add_gate_action)

        self.add_input_action = QAction('Giriş Kutusu Ekle', self)
        self.add_input_action.triggered.connect(self.add_input)
        self.toolbar.addAction(self.add_input_action)

        self.add_output_action = QAction("Çıkış Kutusu Ekle", self)
        self.add_output_action.triggered.connect(self.add_output)
        self.toolbar.addAction(self.add_output_action)

        self.add_wire_action = QAction('Bağlantı Hattı Ekle', self)
        self.add_wire_action.triggered.connect(self.add_wire)
        self.toolbar.addAction(self.add_wire_action)

        self.simulate_action = QAction('Simülasyonu Başlat', self)
        self.simulate_action.triggered.connect(self.simulate)
        self.toolbar.addAction(self.simulate_action)

        self.stop_action = QAction('Durdur', self)
        self.stop_action.triggered.connect(self.stop_simulation)
        self.toolbar.addAction(self.stop_action)

        self.reset_action = QAction('Sıfırla', self)
        self.reset_action.triggered.connect(self.reset_simulation)
        self.toolbar.addAction(self.reset_action)

        self.gates = []
        self.inputs = []
        self.outputs = []
        self.wires = []
        self.selected_items = []


    def stop_simulation(self):

        print("Simülasyon Durduruldu.")

    def reset_simulation(self):

        self.scene.clear()
        self.gates = []
        self.inputs = []
        self.outputs = []
        self.wires = []
        print("Simülasyon Sıfırlandı.")

    def add_gate(self):
        gate, ok = QInputDialog.getItem(self, "KAPI SEÇ", "Gate Type:", ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"], 0, False)
        if ok:
            logic_gate = LogicGate(gate, 2 if gate not in ["NOT"] else 1)
            self.scene.addItem(logic_gate)
            self.gates.append(logic_gate)

    def add_input(self):
        input_item = InputPin()
        self.scene.addItem(input_item)
        self.inputs.append(input_item)

    def add_output(self):
        output_item = OutputPin()
        self.scene.addItem(output_item)
        self.outputs.append(output_item)

    def add_wire(self):
        start_item = self.get_selected_item("Birinci Kapı")
        if start_item:
            end_item = self.get_selected_item("İkinci kapı")
            if end_item:
                wire = Wire(start_item, end_item)
                self.scene.addItem(wire)
                self.wires.append(wire)

    def get_selected_item(self, message):
        self.statusBar().showMessage(message)
        self.selected_item = None
        self.view.viewport().installEventFilter(self)
        while not self.selected_item:
            QApplication.processEvents(QEventLoop.AllEvents, 100)
        self.view.viewport().removeEventFilter(self)
        self.statusBar().clearMessage()
        return self.selected_item

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            item = self.scene.itemAt(self.view.mapToScene(event.pos()), QTransform())
            if item and isinstance(item, QGraphicsItem):
                self.selected_item = item
                return True
        return False

    def simulate(self):
        for gate in self.gates:
            gate.update_outputs()

        for output in self.outputs:
            output.update()

def main():
    app = QApplication(sys.argv)
    sim = LogicSimulator()
    sim.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()