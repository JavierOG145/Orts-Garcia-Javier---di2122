from PySide6.QtWidgets import (
    QLabel, QFileDialog, QDialogButtonBox, QVBoxLayout
)


class fileDialog(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GUARDAR")

        q_btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(q_btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("En que archivo quieres guardar el historial?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)