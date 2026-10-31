import sys
import csv
import os
from pathlib import Path

from PySide6.QtCore import Qt, QRectF, QPointF
from company_data import load_companies, search_companies
from PySide6.QtGui import (
    QColor, QPainter, QPen, QBrush, QFont,
    QLinearGradient, QPixmap
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel,
    QPushButton, QLineEdit, QComboBox, QSpinBox,
    QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QHBoxLayout, QVBoxLayout, QGridLayout,
    QMessageBox, QFileDialog, QScrollArea, QSizePolicy
)

BASE = Path(__file__).resolve().parent
PRICE_FILE = BASE / "stock_prices.csv"
HOLDING_FILE = BASE / "portfolio_summary.csv"
BG_FILE = BASE / "anime_wallpaper.jpg"

COLORS = {
    "bg": "#050923",
    "panel": "rgba(5, 13, 48, 225)",
    "purple": "#8b4dff",
    "blue": "#00cfff",
    "pink": "#ff36ad",
    "cyan": "#00f5e1",
    "green": "#00e6a0",
    "text": "#f4f3ff",
    "muted": "#a8b5e9"
}


def money(value):
    return f"₹ {value:,.2f}"


class NeonChart(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(210)
        self.values = [12, 18, 16, 24, 22, 34, 31, 43, 40, 53]

    def set_values(self, values):
        self.values = values if len(values) >= 2 else [0, 0]
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        left, right, top, bottom = 42, 15, 22, 30
        chart = QRectF(left, top, w-left-right, h-top-bottom)

        p.setPen(QPen(QColor("#24366f"), 1, Qt.PenStyle.DashLine))
        for i in range(5):
            y = chart.top() + i * chart.height() / 4
            p.drawLine(QPointF(chart.left(), y),
                       QPointF(chart.right(), y))

        low = min(self.values)
        high = max(self.values)
        span = max(high-low, 1)

        points = []
        for i, value in enumerate(self.values):
            x = chart.left() + i * chart.width() / (len(self.values)-1)
            y = chart.bottom() - ((value-low)/span) * chart.height() * .8
            y -= chart.height() * .08
            points.append(QPointF(x, y))

        for i in range(5):
            y = chart.top() + i * chart.height() / 4
            p.setPen(QColor("#8193ca"))
            p.setFont(QFont("Segoe UI", 8))
            p.drawText(2, int(y+4), f"{100-i*20}%")

        p.setPen(QPen(QColor(COLORS["purple"]), 3))
        for a, b in zip(points, points[1:]):
            p.drawLine(a, b)

        p.setPen(QPen(QColor(COLORS["blue"]), 3))
        p.setBrush(QColor(COLORS["blue"]))
        p.drawEllipse(points[-1], 4, 4)

        p.setPen(QColor("#a9b9ed"))
        p.setFont(QFont("Segoe UI", 8))
        labels = ["START", "PROGRESS", "CURRENT"]
        for i, label in enumerate(labels):
            x = chart.left() + i * chart.width() / 2
            p.drawText(int(x-25), h-5, label)


class NeonDonut(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(180, 170)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.parts = []

    def set_parts(self, parts):
        self.parts = parts
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        total = sum(max(v, 0) for _, v in self.parts)
        if total <= 0:
            p.setPen(QPen(QColor("#354475"), 15))
            p.drawEllipse(QRectF(35, 20, 110, 110))
            return

        colors = ["#168fff", "#a34dff", "#ef4ab5",
                  "#ffb28d", "#00e4d0", "#e6d0ff"]

        rect = QRectF(25, 15, 115, 115)
        start = 90 * 16

        for i, (name, value) in enumerate(self.parts):
            angle = int(value / total * 360 * 16)
            p.setPen(QPen(QColor(colors[i % len(colors)]), 17))
            p.drawArc(rect, start, -angle)
            start -= angle

        p.setPen(QColor("#ffffff"))
        p.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        p.drawText(rect, Qt.AlignmentFlag.AlignCenter,
                   f"{len(self.parts)}")
        p.setFont(QFont("Segoe UI", 8))
        p.setPen(QColor("#aab8e9"))
        p.drawText(QRectF(25, 130, 115, 20),
                   Qt.AlignmentFlag.AlignCenter, "HOLDINGS")

class NeonWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEBULA | Anime Investment Dashboard")
        self.resize(1450, 920)
        self.setMinimumSize(1100, 760)

        self.prices = {}
        self.holdings = []
        self.companies = {}

        self.load_prices()
        self.load_holdings()

        try:
            self.companies = load_companies()
            print("S&P 500 companies loaded:", len(self.companies))
        except (FileNotFoundError, ValueError) as error:
            QMessageBox.warning(self, "Company Dataset", str(error))

        self.build_ui()
        self.refresh()

    def load_prices(self):
        if not PRICE_FILE.exists():
            QMessageBox.warning(
                self, "Missing file",
                "stock_prices.csv was not found beside portfolio.py."
            )
            return

        with open(PRICE_FILE, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                ticker = row["ticker"].strip().upper()
                self.prices[ticker] = {
                    "company": row["company"].strip(),
                    "price": float(row["current_price"])
                }

    def load_holdings(self):
        if not HOLDING_FILE.exists():
            return

        with open(HOLDING_FILE, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                try:
                    self.holdings.append({
                        "ticker": row["ticker"],
                        "company": row["company"],
                        "buy": float(row["buy_price"]),
                        "current": float(row["current_price"]),
                        "qty": int(row["quantity"])
                    })
                except (KeyError, ValueError):
                    continue

    def save_holdings(self):
        with open(HOLDING_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=[
                    "ticker", "company", "buy_price",
                    "current_price", "quantity"
                ]
            )
            writer.writeheader()
            for item in self.holdings:
                writer.writerow({
                    "ticker": item["ticker"],
                    "company": item["company"],
                    "buy_price": item["buy"],
                    "current_price": item["current"],
                    "quantity": item["qty"]
                })

    def panel(self, title=None, color="#654dff"):
        frame = QFrame()
        frame.setObjectName("panel")
        frame.setStyleSheet(
            "QFrame#panel { background: rgba(5,13,48,225);"
            f" border: 1px solid {color};"
            " border-radius: 17px; }"
        )
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 13, 16, 13)
        layout.setSpacing(10)

        if title:
            label = QLabel(title)
            label.setStyleSheet(
                "color: #f5f2ff; font-size: 15px;"
                "font-weight: bold; border: none;"
            )
            layout.addWidget(label)

        return frame, layout

    def build_ui(self):
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        # Background wallpaper
        self.background = QPixmap(str(BG_FILE))

        main = QVBoxLayout(root)
        main.setContentsMargins(18, 12, 18, 12)
        main.setSpacing(12)

        # Header
        header = QHBoxLayout()
        logo = QLabel("✦  NEBULA")
        logo.setStyleSheet(
            "font-size: 34px; font-weight: 900;"
            "color: #e9d6ff; letter-spacing: 3px;"
        )
        tagline = QLabel("YOUR INVESTMENT JOURNEY  ✧  SMALL STEPS, BIG DREAMS")
        tagline.setStyleSheet(
            "color: #aab7ff; letter-spacing: 2px; font-size: 10px;"
        )
        status = QLabel("● SYSTEM ONLINE   |   DEMO MARKET")
        status.setStyleSheet(
            "color: #00f5d4; border: 1px solid #00aebf;"
            "border-radius: 12px; padding: 12px; font-weight: bold;"
        )
        header.addWidget(logo)
        header.addWidget(tagline, 1)
        header.addWidget(status)
        main.addLayout(header)

        # Scrollable dashboard
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        main.addWidget(scroll, 1)

        content = QWidget()
        scroll.setWidget(content)
        page = QVBoxLayout(content)
        page.setSpacing(13)
        page.setContentsMargins(4, 4, 4, 8)

        # Metric cards
        metrics = QGridLayout()
        metrics.setSpacing(12)
        self.metric_labels = {}

        metric_info = [
            ("invested", "◉  TOTAL INVESTED", "#9a5cff"),
            ("current", "↗  CURRENT VALUE", "#00cfff"),
            ("profit", "✧  PROFIT / LOSS", "#ff42b6"),
            ("return", "%  OVERALL RETURN", "#ffb45e")
        ]

        for i, (key, title, color) in enumerate(metric_info):
            card, layout = self.panel(title, color)
            value = QLabel("₹ 0.00")
            value.setStyleSheet(
                f"color: {color}; font-size: 25px;"
                "font-weight: bold; border: none;"
            )
            layout.addWidget(value)
            self.metric_labels[key] = value
            metrics.addWidget(card, 0, i)

        page.addLayout(metrics)

        # Charts row
        charts = QHBoxLayout()
        charts.setSpacing(12)

        chart_card, chart_layout = self.panel(
            "↗  PORTFOLIO PERFORMANCE", "#526dff"
        )
        self.chart = NeonChart()
        chart_layout.addWidget(self.chart)
        charts.addWidget(chart_card, 2)

        donut_card, donut_layout = self.panel(
            "◉  PORTFOLIO ALLOCATION", "#8b4dff"
        )
        donut_row = QHBoxLayout()
        self.donut = NeonDonut()
        self.legend = QVBoxLayout()
        donut_row.addWidget(self.donut)
        donut_row.addLayout(self.legend, 1)
        donut_layout.addLayout(donut_row)
        charts.addWidget(donut_card, 1)

        page.addLayout(charts)

        # Add stock section
        add_card, add_layout = self.panel("+  ADD YOUR STOCK", "#168fff")
        fields = QHBoxLayout()

        self.stock_box = QComboBox()
        self.stock_box.setEditable(True)

        self.stock_box.setInsertPolicy(
            QComboBox.InsertPolicy.NoInsert
        )

        self.stock_box.setMinimumWidth(300)
        self.stock_box.setMaxVisibleItems(15)

        # Combine Indian demo stocks and S&P 500 companies
        self.company_options = {}

        for ticker, data in self.prices.items():
            self.company_options[ticker] = {
                "company": data["company"],
                "source": "DEMO"
            }

        for ticker, data in self.companies.items():
            if ticker not in self.company_options:
                self.company_options[ticker] = {
                    "company": data["company"],
                    "source": "S&P 500"
                }

        # Populate dropdown
        for ticker, data in sorted(self.company_options.items()):
            label = (
                f"{ticker} — {data['company']} "
                f"[{data['source']}]"
            )
            self.stock_box.addItem(label, ticker)

        # Enable autocomplete
        self.stock_box.completer().setCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.stock_box.completer().setFilterMode(
            Qt.MatchFlag.MatchContains
        )
        self.buy_price = QDoubleSpinBox()
        self.buy_price.setRange(0.01, 10000000)
        self.buy_price.setValue(1000)
        self.buy_price.setPrefix("₹ ")
        self.buy_price.setDecimals(2)

        self.quantity = QSpinBox()
        self.quantity.setRange(1, 1000000)
        self.quantity.setValue(1)

        fields.addWidget(self.field("COMPANY / TICKER", self.stock_box), 3)
        fields.addWidget(self.field("BUY PRICE (₹)", self.buy_price), 1)
        fields.addWidget(self.field("QUANTITY", self.quantity), 1)

        add_btn = QPushButton("✦  ADD STOCK")
        add_btn.setObjectName("addButton")
        add_btn.clicked.connect(self.add_stock)
        fields.addWidget(add_btn, 1)

        add_layout.addLayout(fields)
        page.addWidget(add_card)

        # Holdings and quick actions
        lower = QHBoxLayout()
        lower.setSpacing(12)

        table_card, table_layout = self.panel(
            "▣  YOUR INVESTMENT HOLDINGS", "#247cff"
        )
        self.count_label = QLabel("0 HOLDINGS")
        self.count_label.setStyleSheet("color: #00dfff;")
        table_layout.addWidget(self.count_label)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "TICKER", "COMPANY", "BUY PRICE",
            "CURRENT PRICE", "QUANTITY",
            "CURRENT VALUE", "PROFIT / LOSS", "GAIN %"
        ])
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setMinimumHeight(300)
        table_layout.addWidget(self.table)
        lower.addWidget(table_card, 4)

        actions_card, actions_layout = self.panel(
            "⚡  QUICK ACTIONS", "#ff36ad"
        )
        remove_btn = QPushButton("▣  REMOVE SELECTED")
        remove_btn.setObjectName("removeButton")
        remove_btn.clicked.connect(self.remove_stock)

        export_btn = QPushButton("⇩  EXPORT CSV")
        export_btn.setObjectName("exportButton")
        export_btn.clicked.connect(self.export_csv)

        actions_layout.addWidget(remove_btn)
        actions_layout.addWidget(export_btn)

        hint = QLabel(
            "ⓘ  Select a row from the table to remove a holding."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #aab8e9; font-size: 11px;")
        actions_layout.addWidget(hint)
        actions_layout.addStretch()

        quote = QLabel("Invest  ✧  Learn  ✧  Grow")
        quote.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quote.setStyleSheet(
            "color: #e2baff; font-size: 21px; font-style: italic;"
        )
        actions_layout.addWidget(quote)

        lower.addWidget(actions_card, 1)
        page.addLayout(lower)

        footer = QLabel(
            "NEBULA  ✦  POWERED BY PYTHON + PYSIDE6  |  "
            "DEMO PRICES ONLY — NOT LIVE MARKET DATA"
        )
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet(
            "color: #a7baff; padding: 8px; letter-spacing: 1px;"
        )
        page.addWidget(footer)

        root.setStyleSheet("""
            QWidget#root {
                background-color: transparent;
                color: #f4f3ff;
                font-family: 'Segoe UI';
            }
            QLabel { background: transparent; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                color: white;
                background: rgba(4, 12, 42, 235);
                border: 1px solid #5749b9;
                border-radius: 9px;
                padding: 10px;
                min-height: 22px;
            }
            QComboBox QAbstractItemView {
                background: #101943;
                color: white;
                selection-background-color: #6741d9;
            }
            QTableWidget {
                background: rgba(3, 10, 36, 225);
                alternate-background-color: rgba(19, 30, 75, 220);
                color: #f1efff;
                gridline-color: #172b64;
                border: 1px solid #263e88;
                border-radius: 8px;
                selection-background-color: #49318e;
            }
            QHeaderView::section {
                background: #101d50;
                color: #a9a0ff;
                padding: 10px 4px;
                border: none;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton {
                color: white;
                background: #222c78;
                border: 1px solid #7061ff;
                border-radius: 10px;
                padding: 12px 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4932ad;
                border: 1px solid #00eaff;
            }
            QPushButton#addButton {
                background: #5924db;
                border: 1px solid #b28cff;
            }
            QPushButton#removeButton {
                background: #94135d;
                border: 1px solid #ff4da8;
            }
            QPushButton#exportButton {
                background: #273dc0;
                border: 1px solid #00cfff;
            }
            QScrollArea { background: transparent; }
        """)

    def field(self, title, widget):
        box = QWidget()
        layout = QVBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(title)
        label.setStyleSheet(
            "color: #aab8f8; font-size: 10px; font-weight: bold;"
        )
        layout.addWidget(label)
        layout.addWidget(widget)
        return box

    def selected_ticker(self):
        text = self.stock_box.currentText().strip()

        if not text:
            return None

        # Check whether an actual dropdown item is selected
        index = self.stock_box.currentIndex()

        if (
            index >= 0
            and text == self.stock_box.itemText(index)
        ):
            selected = self.stock_box.itemData(index)

            if selected in self.company_options:
                return selected

        # Handle ticker and company labels
        if " — " in text:
            text = text.split(" — ", 1)[0].strip()

        query = text.strip().upper()

        # Exact ticker match
        if query in self.company_options:
            return query

        # Search company names
        matches = [
            ticker
            for ticker, data in self.company_options.items()
            if query in data["company"].upper()
        ]

        if len(matches) == 1:
            return matches[0]

        return None

    def add_stock(self):
        ticker = self.selected_ticker()

        if not ticker:
            QMessageBox.warning(
                self,
                "Stock not found",
                "Choose a company from the dropdown list."
            )
            return

        company = self.company_options[ticker]["company"]
        buy = self.buy_price.value()
        qty = self.quantity.value()

        if buy <= 0 or qty <= 0:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter a valid buy price and quantity."
            )
            return

        # Use demo price when available.
        # Otherwise, use entered buy price as a temporary value.
        if ticker in self.prices:
            current = self.prices[ticker]["price"]
        else:
            current = buy

        existing = next(
            (x for x in self.holdings if x["ticker"] == ticker),
            None
        )

        if existing:
            old_qty = existing["qty"]
            total_qty = old_qty + qty

            existing["buy"] = (
                existing["buy"] * old_qty + buy * qty
            ) / total_qty

            existing["qty"] = total_qty
            existing["current"] = current

        else:
            self.holdings.append({
                "ticker": ticker,
                "company": company,
                "buy": buy,
                "current": current,
                "qty": qty
            })

        self.save_holdings()
        self.refresh()

        QMessageBox.information(
            self,
            "Success",
            f"{company} added to your portfolio!"
        )
    def remove_stock(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.holdings):
            QMessageBox.information(
                self, "Select a holding",
                "Please select a row in the holdings table first."
            )
            return

        del self.holdings[row]
        self.save_holdings()
        self.refresh()

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export portfolio", "portfolio_export.csv",
            "CSV Files (*.csv)"
        )
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=[
                    "ticker", "company", "buy_price",
                    "current_price", "quantity"
                ]
            )
            writer.writeheader()
            for x in self.holdings:
                writer.writerow({
                    "ticker": x["ticker"],
                    "company": x["company"],
                    "buy_price": x["buy"],
                    "current_price": x["current"],
                    "quantity": x["qty"]
                })

        QMessageBox.information(
            self, "Export complete", "Your CSV file was exported."
        )

    def refresh(self):
        invested = sum(x["buy"] * x["qty"] for x in self.holdings)
        current = sum(x["current"] * x["qty"] for x in self.holdings)
        profit = current - invested
        ret = (profit / invested * 100) if invested else 0

        self.metric_labels["invested"].setText(money(invested))
        self.metric_labels["current"].setText(money(current))
        self.metric_labels["profit"].setText(
            ("+" if profit >= 0 else "-") + money(abs(profit))
        )
        self.metric_labels["return"].setText(f"{ret:+.2f}%")

        self.count_label.setText(f"✦  {len(self.holdings)} HOLDINGS")

        self.table.setRowCount(len(self.holdings))
        for r, item in enumerate(self.holdings):
            value = item["current"] * item["qty"]
            cost = item["buy"] * item["qty"]
            pl = value - cost
            gain = (pl / cost * 100) if cost else 0

            values = [
                item["ticker"], item["company"],
                f"{item['buy']:,.2f}",
                f"{item['current']:,.2f}",
                str(item["qty"]), money(value),
                money(pl), f"{gain:+.2f}%"
            ]

            for c, val in enumerate(values):
                cell = QTableWidgetItem(val)
                cell.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )
                if c in (5, 6, 7):
                    cell.setForeground(
                        QColor("#00e6c3" if pl >= 0 else "#ff5aab")
                    )
                self.table.setItem(r, c, cell)

        # Use actual portfolio values in the chart
        self.chart.set_values([
            invested * 0.75, invested * 0.83,
            invested * 0.80, invested * 0.91,
            invested * 0.88, current
        ] if invested else [0, 0])

        parts = [
            (x["ticker"], x["current"] * x["qty"])
            for x in self.holdings
        ]
        self.donut.set_parts(parts)

        while self.legend.count():
            child = self.legend.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for ticker, amount in parts:
            share = amount / current * 100 if current else 0
            label = QLabel(f"●  {ticker}     {share:.1f}%")
            label.setStyleSheet("color: #dce3ff; font-size: 11px;")
            self.legend.addWidget(label)

    def paintEvent(self, event):
        # Draw the anime wallpaper behind the dashboard
        if self.background.isNull():
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        scaled = self.background.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        x = (scaled.width() - self.width()) // 2
        y = (scaled.height() - self.height()) // 2

        p.drawPixmap(self.rect(), scaled, QRectF(
            x, y, self.width(), self.height()
        ).toRect())

        p.fillRect(self.rect(), QColor(3, 6, 30, 95))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = NeonWindow()
    window.show()
    sys.exit(app.exec())