import os
import shutil
import sys

from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QFrame,
    QTextEdit, QProgressBar
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


# FILE EXTENSION MAPPING
FILE_CATEGORIES = {
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".xlsx": "Documents",
    ".pptx": "Documents",

    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".webp": "Images",

    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".mov": "Videos",

    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",

    ".py": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".c": "Code",
    ".html": "Code",
    ".css": "Code",
    ".js": "Code"
}


class FileOrganizer(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NEON FILE ORGANIZER")
        self.setMinimumSize(850, 650)

        self.selected_folder = None

        self.counts = {
            "Documents": 0,
            "Images": 0,
            "Videos": 0,
            "Archives": 0,
            "Code": 0
        }

        self.init_ui()

    def init_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        # HEADER
        header = QLabel("NEON FILE ORGANIZER")
        header.setFont(QFont("Segoe UI", 23, QFont.Bold))
        header.setObjectName("header")

        subtitle = QLabel(
            "SMART DESKTOP AUTOMATION  |  FILE MANAGEMENT"
        )
        subtitle.setObjectName("subtitle")

        main_layout.addWidget(header)
        main_layout.addWidget(subtitle)

        # FOLDER SELECTION
        folder_card = QFrame()
        folder_card.setObjectName("panel")

        folder_layout = QVBoxLayout(folder_card)

        folder_title = QLabel("SELECT DIRECTORY")
        folder_title.setObjectName("section")

        self.path_label = QLabel("No folder selected")
        self.path_label.setWordWrap(True)
        self.path_label.setObjectName("path")

        select_btn = QPushButton("  SELECT FOLDER")
        select_btn.clicked.connect(self.select_folder)

        folder_layout.addWidget(folder_title)
        folder_layout.addWidget(self.path_label)
        folder_layout.addWidget(select_btn)

        main_layout.addWidget(folder_card)

        # CATEGORY CARDS
        category_title = QLabel("FILE CATEGORIES")
        category_title.setObjectName("section")

        main_layout.addWidget(category_title)

        category_layout = QHBoxLayout()

        self.category_labels = {}

        for name in self.counts:

            card = QFrame()
            card.setObjectName("category")

            card_layout = QVBoxLayout(card)

            title = QLabel(name.upper())
            title.setAlignment(Qt.AlignCenter)

            number = QLabel("0")
            number.setObjectName("number")
            number.setAlignment(Qt.AlignCenter)

            self.category_labels[name] = number

            card_layout.addWidget(title)
            card_layout.addWidget(number)

            category_layout.addWidget(card)

        main_layout.addLayout(category_layout)

        # ORGANIZE BUTTON
        self.organize_btn = QPushButton("  ORGANIZE FILES")
        self.organize_btn.setObjectName("organize")
        self.organize_btn.setEnabled(False)
        self.organize_btn.clicked.connect(self.organize_files)

        main_layout.addWidget(self.organize_btn)

        # PROGRESS
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setFormat("%p% completed")

        main_layout.addWidget(self.progress)

        # ACTIVITY LOG
        log_title = QLabel("LIVE ACTIVITY LOG")
        log_title.setObjectName("section")

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText(
            "Your file organization activity will appear here..."
        )

        main_layout.addWidget(log_title)
        main_layout.addWidget(self.log)

        # SUMMARY
        self.summary = QLabel(
            "READY  |  Select a folder to begin."
        )
        self.summary.setObjectName("summary")

        main_layout.addWidget(self.summary)

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #10111c;
                color: #eeeeff;
                font-family: Segoe UI;
            }

            #header {
                color: #a78bfa;
                font-size: 25px;
                font-weight: bold;
            }

            #subtitle {
                color: #8585a5;
                font-size: 11px;
            }

            #section {
                color: #c4b5fd;
                font-size: 14px;
                font-weight: bold;
            }

            #panel, #category {
                background-color: #1b1c2c;
                border: 1px solid #34344d;
                border-radius: 12px;
                padding: 8px;
            }

            #path {
                color: #c4c4d8;
                padding: 8px;
            }

            QPushButton {
                background-color: #3730a3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #6d5ce8;
            }

            QPushButton:disabled {
                background-color: #39394b;
                color: #888899;
            }

            #organize {
                background-color: #7c3aed;
                font-size: 15px;
                padding: 15px;
            }

            #organize:hover {
                background-color: #9333ea;
            }

            #number {
                color: #a78bfa;
                font-size: 27px;
                font-weight: bold;
            }

            QTextEdit {
                background-color: #171827;
                border: 1px solid #34344d;
                border-radius: 8px;
                padding: 10px;
                color: #a5f3fc;
            }

            QProgressBar {
                background-color: #27283b;
                border: none;
                border-radius: 6px;
                height: 17px;
                text-align: center;
                color: white;
            }

            QProgressBar::chunk {
                background-color: #8b5cf6;
                border-radius: 6px;
            }

            #summary {
                color: #86efac;
                font-weight: bold;
                padding: 8px;
            }
        """)

    def add_log(self, message):
        self.log.append(message)

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder"
        )

        if folder:
            self.selected_folder = Path(folder)
            self.path_label.setText(folder)
            self.organize_btn.setEnabled(True)

            self.add_log("Folder selected successfully.")
            self.summary.setText("READY | Folder selected.")

    def get_unique_path(self, destination):

        if not destination.exists():
            return destination

        folder = destination.parent
        name = destination.stem
        extension = destination.suffix

        counter = 1

        while True:

            new_path = folder / f"{name}_{counter}{extension}"

            if not new_path.exists():
                return new_path

            counter += 1

    def organize_files(self):

        folder = self.selected_folder
        if folder is None:
            return

        self.organize_btn.setEnabled(False)
        self.log.clear()

        moved = 0
        skipped = 0
        errors = 0

        for key in self.counts:
            self.counts[key] = 0
            self.category_labels[key].setText("0")

        try:
            with os.scandir(folder) as directory:
                entries = list(directory)
        except OSError as error:
            self.add_log(f"ERROR: Cannot scan folder: {error}")
            self.summary.setText("FAILED | Could not scan the selected folder.")
            self.organize_btn.setEnabled(True)
            return

        files = []
        for entry in entries:
            try:
                if entry.is_file(follow_symlinks=False):
                    files.append(entry)
            except OSError as error:
                errors += 1
                self.add_log(f"ERROR: Could not inspect {entry.name}: {error}")

        total = len(files)

        if total == 0:
            self.add_log("No files found in this folder.")
            self.progress.setValue(100)
            self.summary.setText(
                f"COMPLETED | Moved: 0 | Skipped: 0 | Errors: {errors}"
            )
            self.add_log("\n========== FINAL SUMMARY ==========")
            self.add_log("Total files scanned: 0")
            self.add_log("Successfully moved: 0")
            self.add_log("Skipped: 0")
            self.add_log(f"Errors: {errors}")
            self.organize_btn.setEnabled(True)
            return

        self.progress.setValue(0)

        for index, entry in enumerate(files, start=1):

            source = Path(entry.path)
            extension = source.suffix.lower()

            category = FILE_CATEGORIES.get(extension)

            if category is None:
                skipped += 1
                self.add_log(f"SKIPPED: {source.name}")
            else:
                try:
                    destination_folder = folder / category
                    destination_folder.mkdir(parents=True, exist_ok=True)

                    destination = self.get_unique_path(
                        destination_folder / source.name
                    )

                    shutil.move(str(source), str(destination))

                    moved += 1
                    self.counts[category] += 1
                    self.category_labels[category].setText(
                        str(self.counts[category])
                    )
                    self.add_log(f"SUCCESS: {source.name} -> {category}")

                except FileExistsError:
                    errors += 1
                    self.add_log(f"COLLISION: {source.name}")

                except PermissionError:
                    errors += 1
                    self.add_log(f"PERMISSION DENIED: {source.name}")

                except OSError as error:
                    errors += 1
                    self.add_log(f"ERROR: {source.name} - {error}")

            self.progress.setValue(
                int(index / total * 100)
            )

            QApplication.processEvents()

        self.summary.setText(
            f"COMPLETED | Moved: {moved} | "
            f"Skipped: {skipped} | Errors: {errors}"
        )

        self.add_log("\n========== FINAL SUMMARY ==========")
        self.add_log(f"Total files scanned: {total}")
        self.add_log(f"Successfully moved: {moved}")
        self.add_log(f"Skipped: {skipped}")
        self.add_log(f"Errors: {errors}")

        self.organize_btn.setEnabled(True)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = FileOrganizer()
    window.show()

    sys.exit(app.exec())