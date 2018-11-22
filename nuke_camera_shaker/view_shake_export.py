from PySide2 import QtWidgets, QtCore

from nuke_camera_shaker.constants import FILE_EXTENSION


class SpinLayout(QtWidgets.QHBoxLayout):

    def __init__(self, label_text):
        super(SpinLayout, self).__init__()
        self.build_widgets(label_text)

    def build_widgets(self, label_text):
        label = QtWidgets.QLabel(label_text)
        label.setFixedWidth(60)
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.addWidget(label)
        self.spin = QtWidgets.QSpinBox()
        self.spin.setFixedWidth(150)
        self.spin.setRange(0, 100000)
        self.spin.setValue(1001)
        self.addWidget(self.spin)


class HorizontalLine(QtWidgets.QFrame):
    def __init__(self):
        super(HorizontalLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class ViewExport(QtWidgets.QWidget):
    save_file = QtCore.Signal(str)
    export = QtCore.Signal(object)

    def __init__(self):
        super(ViewExport, self).__init__()
        self._build_widgets()
        self._build_layouts()
        self._set_window_properties()
        self._set_up_signals()

    def _set_window_properties(self):
        self.setMinimumSize(500, 150)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Export Camera Shake file.')

    def _build_widgets(self):
        self.file_path = QtWidgets.QLineEdit()
        self.file_path.setPlaceholderText('Shake file location...')

        self.file_dialog_button = QtWidgets.QPushButton()
        icon = self.file_dialog_button.style().standardIcon(QtWidgets.QStyle.SP_FileDialogStart)
        self.file_dialog_button.setIcon(icon)

        self.file_dialog = QtWidgets.QFileDialog()
        self.file_dialog.setDefaultSuffix(FILE_EXTENSION)

        self.radio_range = QtWidgets.QRadioButton("Bake and export specific range.")
        self.radio_range.setChecked(True)
        self.radio_range.setMinimumWidth(260)
        self.radio_keys = QtWidgets.QRadioButton("Export Existing keyframes.")

        self.first = SpinLayout('First:')
        self.last = SpinLayout('Last:')

        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.cancel_button.setFixedWidth(100)
        self.export_button = QtWidgets.QPushButton('Export')
        self.export_button.setFixedWidth(100)

    def _build_layouts(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        file_layout = QtWidgets.QHBoxLayout()
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(self.file_dialog_button)

        radio_layout = QtWidgets.QHBoxLayout()
        radio_layout.setAlignment(QtCore.Qt.AlignLeft)
        radio_layout.addWidget(self.radio_range)
        radio_layout.addWidget(self.radio_keys)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignRight)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.export_button)

        main_layout.addLayout(file_layout)
        main_layout.addLayout(radio_layout)
        main_layout.addLayout(self.first)
        main_layout.addLayout(self.last)
        main_layout.addLayout(button_layout)

    def _set_up_signals(self):
        self.file_dialog_button.clicked.connect(self.place_file)
        self.cancel_button.clicked.connect(self.close)
        self.export_button.clicked.connect(self.export_retime_file)
        self.radio_keys.toggled.connect(self.toggle_range)
        self.radio_range.toggled.connect(self.toggle_range)

    def toggle_range(self, state):
        self.first.spin.setEnabled(self.radio_range.isChecked())
        self.last.spin.setEnabled(self.radio_range.isChecked())

    def place_file(self):
        filter_ = '*.{}'.format(FILE_EXTENSION)
        retime_file, _ = self.file_dialog.getSaveFileName(parent=self,
                                                          caption='Export Camera shake file',
                                                          filter=filter_)

        if retime_file:
            self.save_file.emit(retime_file)

    def update_field(self, filepath):
        self.file_path.setText(filepath)

    def update_node_and_knobs(self, node_name, knobs):
        self.node_name_line.setText(node_name)
        self.node_name_line.setEnabled(False)
        self.knob.clear()
        self.knob.addItems(knobs)

    def export_retime_file(self):

        self.export.emit((self.file_path.text(),
                          self.node_name_line.text(),
                          self.knob.currentText(),
                          self.radio_range.isChecked(),
                          int(self.first.spin.text()),
                          int(self.last.spin.text())
                          ))

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Catch user key events.

        Args:
            event: (QtGui.event)

        """
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()