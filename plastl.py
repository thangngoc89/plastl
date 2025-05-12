import os
import sys
from multiprocessing import Pool, cpu_count, freeze_support

import trimesh
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


class SimpleUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plastl Mesh Converter")
        self.setWindowIcon(QIcon(resource_path("assets/plastl.ico")))  # Windows/Linux
        self.resize(600, 550)
        self.setAcceptDrops(True)

        self.input_files = []
        self.output_folder = ""
        self.output_format = "PLY"

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Input Files (Drag & Drop or Select):"))
        self.file_list = QListWidget()
        self.file_list.setFixedHeight(120)
        layout.addWidget(self.file_list)

        select_button = QPushButton("Select Files")
        select_button.clicked.connect(self.select_files)
        layout.addWidget(select_button)

        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Output Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PLY", "STL"])
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)

        out_layout = QHBoxLayout()
        out_button = QPushButton("Select Output Folder")
        out_button.clicked.connect(self.select_output_folder)
        self.out_folder_label = QLabel("(No folder selected)")
        out_layout.addWidget(out_button)
        out_layout.addWidget(self.out_folder_label)
        layout.addLayout(out_layout)

        self.run_button = QPushButton("Run")
        self.run_button.setObjectName("Run")
        self.run_button.clicked.connect(self.run)
        layout.addWidget(self.run_button)

        open_button = QPushButton("Open Output Folder")
        open_button.clicked.connect(self.open_output_folder)
        layout.addWidget(open_button)

        layout.addWidget(QLabel("Log:"))
        self.log_box = QListWidget()
        self.log_box.setFixedHeight(150)
        layout.addWidget(self.log_box)

        self.setLayout(layout)
        # Create a menu bar
        menu_bar = QMenuBar(self)

        # Create Help menu
        help_menu = menu_bar.addMenu("Help")

        # About action
        about_action = QAction("About Plastl", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        # Add menu bar to the layout (must insert at the top)
        layout.setMenuBar(menu_bar)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path):
                self.input_files.append(path)
                self.file_list.addItem(path)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Files", "", "Mesh Files (*.stl *.ply *.obj);;All Files (*)"
        )
        if files:
            self.input_files.extend(files)
            for f in files:
                self.file_list.addItem(f)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.out_folder_label.setText(folder)

    def open_output_folder(self):
        if os.path.isdir(self.output_folder):
            if sys.platform.startswith("linux"):
                os.system(f'xdg-open "{self.output_folder}"')
            elif sys.platform == "darwin":
                os.system(f'open "{self.output_folder}"')
            else:
                os.system(f'start "" "{self.output_folder}"')

    def show_about_dialog(self):
        QMessageBox.information(
            self,
            "About Plastl",
            "<b>Plastl Mesh Converter</b><br><br>"
            "A simple batch tool for converting 3D mesh files between STL and PLY formats.<br>"
            "Supports drag-and-drop and multiprocessing for fast processing.<br><br>"
            "Developed using PyQt5 and Trimesh.<br>"
            "Version: 1.0.5<br>"
            "© 2025 Khoa Nguyen<br><br>"
            '<a href="https://github.com/thangngoc89/plastl" style="color:#2980b9;">'
            "GitHub Repository</a>",
        )

    @staticmethod
    def convert_file(input_path: str, output_path: str) -> tuple:
        try:
            original_size = os.path.getsize(input_path)

            mesh = trimesh.load(input_path, force="mesh", process=True)
            mesh.export(output_path)

            converted_size = os.path.getsize(output_path)
            percent_saved = (
                (original_size - converted_size) / original_size * 100
                if original_size > 0
                else 0
            )

            return (input_path, True, "", percent_saved)
        except Exception as e:
            return (input_path, False, str(e), 0.0)

    def run(self):
        if not self.input_files:
            QMessageBox.warning(
                self, "Missing Input", "Please select or drop input mesh files."
            )
            return

        if not self.output_folder:
            QMessageBox.warning(
                self, "Missing Output Folder", "Please select an output folder."
            )
            return

        self.output_format = self.format_combo.currentText().lower()
        allowed_exts = [".stl", ".ply", ".obj"]
        valid_files = [
            f
            for f in self.input_files
            if os.path.splitext(f)[-1].lower() in allowed_exts
        ]
        if not valid_files:
            QMessageBox.warning(
                self, "Invalid Files", "Only .stl, .ply, or .obj files are allowed."
            )
            return

        # Prepare task list
        tasks = []
        for f in valid_files:
            name = os.path.splitext(os.path.basename(f))[0]
            out_path = os.path.join(self.output_folder, f"{name}.{self.output_format}")
            tasks.append((f, out_path))

        # Disable UI and clear logs
        self.run_button.setEnabled(False)
        self.log_box.clear()

        # Multiprocessing
        with Pool(processes=min(cpu_count(), len(tasks))) as pool:
            results = pool.starmap(self.convert_file, tasks)

        # Re-enable run button
        self.run_button.setEnabled(True)

        # Log output
        success_count = 0
        for f, ok, msg, percent_saved in results:
            name = os.path.basename(f)
            if ok:
                if self.output_format == "ply":
                    log_msg = f"✅ {name} → .ply | Saved {percent_saved:.1f}%"
                else:
                    log_msg = f"✅ {name} converted successfully."
                self.log_box.addItem(log_msg)
                success_count += 1
            else:
                self.log_box.addItem(f"❌ {name} failed: {msg}")

        if success_count == len(tasks):
            QMessageBox.information(
                self, "Success", f"All {success_count} files converted."
            )
        elif success_count == 0:
            QMessageBox.critical(self, "Failure", f"All files failed to convert.")
        else:
            QMessageBox.warning(
                self,
                "Partial Success",
                f"{success_count} of {len(tasks)} files converted.",
            )


def main():
    app = QApplication(sys.argv)
    win = SimpleUI()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    freeze_support()
    main()
