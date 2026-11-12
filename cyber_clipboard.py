import sys
import sqlite3
import os
import ctypes
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, 
                             QLineEdit, QLabel, QListWidgetItem)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# --- FORÇA O WINDOWS A RECONHECER O APP SEPARADO DO PYTHON ---
try:
    myappid = 'nexus.clipboard.manager.v3'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

class DatabaseManager:
    def __init__(self, db_name="nexus_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tabs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tab_name TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def get_tabs(self):
        self.cursor.execute("SELECT name FROM tabs")
        return [row[0] for row in self.cursor.fetchall()]

    def add_tab(self, name):
        try:
            self.cursor.execute("INSERT INTO tabs (name) VALUES (?)", (name,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

    def remove_tab(self, name):
        self.cursor.execute("DELETE FROM tabs WHERE name = ?", (name,))
        self.cursor.execute("DELETE FROM texts WHERE tab_name = ?", (name,))
        self.conn.commit()

    def get_texts(self, tab_name):
        self.cursor.execute("SELECT id, content FROM texts WHERE tab_name = ? ORDER BY id DESC", (tab_name,))
        return self.cursor.fetchall()

    def add_text(self, tab_name, content):
        self.cursor.execute("INSERT INTO texts (tab_name, content) VALUES (?, ?)", (tab_name, content))
        self.conn.commit()
        return self.cursor.lastrowid

    def remove_text(self, text_id):
        self.cursor.execute("DELETE FROM texts WHERE id = ?", (text_id,))
        self.conn.commit()

class CyberClipboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEXUS // CLIPBOARD_MANAGER_v3.0")
        self.resize(600, 700)
        
        # --- CARREGAMENTO DO ÍCONE ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "icone.png") 
        
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Aviso: Ícone não encontrado em {icon_path}")

        self.db = DatabaseManager()

        self.setStyleSheet("""
            QMainWindow { background-color: #09090b; }
            QTabWidget::pane { border: 1px solid #ff007f; background-color: #09090b; top: -1px; }
            QTabBar::tab {
                background: #111; color: #00ffcc; border: 1px solid #ff007f;
                padding: 8px 15px; font-family: 'Consolas'; font-weight: bold;
            }
            QTabBar::tab:selected { background: #ff007f; color: #ffffff; }
            QListWidget { background-color: #000000; border: none; outline: none; }
            QListWidget::item { border-bottom: 1px solid #222; }
            QListWidget::item:hover { background-color: #151515; }
            QLineEdit {
                background-color: #111; color: #fff; border: 1px solid #00ffcc;
                padding: 8px; font-family: 'Consolas'; font-size: 13px;
            }
            QPushButton {
                background-color: transparent; color: #00ffcc; border: 1px solid #00ffcc;
                padding: 8px 15px; font-family: 'Consolas'; font-weight: bold;
            }
            QPushButton:hover { background-color: #00ffcc; color: #000; }
            QPushButton#deleteBtn {
                background-color: transparent; color: #ff0044; border: 1px solid #ff0044;
                padding: 2px; font-size: 12px;
            }
            QPushButton#deleteBtn:hover { background-color: #ff0044; color: #fff; }
            QPushButton#btnAba { color: #ff007f; border-color: #ff007f; }
            QPushButton#btnAba:hover { background-color: #ff007f; color: #fff; }
        """)

        self.clipboard = QApplication.clipboard()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 1. BARRA SUPERIOR
        self.top_layout = QHBoxLayout()
        self.new_tab_input = QLineEdit()
        self.new_tab_input.setPlaceholderText(">> NOME DO NOVO ASSUNTO...")
        self.new_tab_input.returnPressed.connect(self.create_new_tab) 
        
        self.add_tab_btn = QPushButton("[ CRIAR ABA ]")
        self.add_tab_btn.setObjectName("btnAba")
        self.add_tab_btn.clicked.connect(self.create_new_tab)
        
        self.top_layout.addWidget(self.new_tab_input)
        self.top_layout.addWidget(self.add_tab_btn)
        self.layout.addLayout(self.top_layout)

        # 2. SISTEMA DE ABAS
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.delete_tab)
        self.layout.addWidget(self.tabs)

        # 3. BARRA INFERIOR
        self.bottom_layout = QHBoxLayout()
        self.new_text_input = QLineEdit()
        self.new_text_input.setPlaceholderText(">> INSERIR NOVO TEXTO NA ABA ATUAL...")
        self.new_text_input.returnPressed.connect(self.add_text_to_current_tab)
        
        self.add_text_btn = QPushButton("[ ADD TEXTO ]")
        self.add_text_btn.clicked.connect(self.add_text_to_current_tab)
        
        self.bottom_layout.addWidget(self.new_text_input)
        self.bottom_layout.addWidget(self.add_text_btn)
        self.layout.addLayout(self.bottom_layout)

        self.load_data_from_db()

    # --- BANCO DE DADOS E CARREGAMENTO ---
    def load_data_from_db(self):
        saved_tabs = self.db.get_tabs()
        if not saved_tabs:
            self.db.add_tab("GERAL")
            saved_tabs = ["GERAL"]

        for tab_name in saved_tabs:
            self.create_tab_ui(tab_name)
            texts = self.db.get_texts(tab_name)
            for text_id, content in texts: 
                self.add_item_to_ui(tab_name, text_id, content, insert_at_top=False)

    # --- GERENCIAMENTO DE ABAS ---
    def create_new_tab(self):
        tab_name = self.new_tab_input.text().strip().upper()
        if tab_name:
            self.db.add_tab(tab_name)
            self.create_tab_ui(tab_name)
            self.new_tab_input.clear()

    def create_tab_ui(self, tab_name):
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == tab_name:
                self.tabs.setCurrentIndex(i)
                return

        tab = QWidget()
        tab.setObjectName(tab_name)
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        
        list_widget = QListWidget()
        list_widget.itemClicked.connect(self.copy_to_clipboard)
        layout.addWidget(list_widget)
        
        self.tabs.addTab(tab, tab_name)
        self.tabs.setCurrentWidget(tab)

    def delete_tab(self, index):
        tab_name = self.tabs.tabText(index)
        self.db.remove_tab(tab_name)
        self.tabs.removeTab(index)

    # --- GERENCIAMENTO DE TEXTOS ---
    def add_text_to_current_tab(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            tab_name = self.tabs.tabText(self.tabs.currentIndex())
            new_text = self.new_text_input.text().strip()
            if new_text:
                text_id = self.db.add_text(tab_name, new_text)
                self.add_item_to_ui(tab_name, text_id, new_text, insert_at_top=True)
                self.new_text_input.clear()

    def add_item_to_ui(self, tab_name, text_id, content, insert_at_top=False):
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == tab_name:
                tab = self.tabs.widget(i)
                list_widget = tab.findChild(QListWidget)
                
                item = QListWidgetItem()
                item.setData(Qt.ItemDataRole.UserRole, content)
                item.setData(Qt.ItemDataRole.UserRole + 1, text_id)
                
                row_widget = QWidget()
                row_layout = QHBoxLayout(row_widget)
                row_layout.setContentsMargins(10, 10, 10, 10)
                
                label = QLabel(content)
                label.setStyleSheet("color: #00ffcc; font-family: 'Consolas'; font-size: 14px;")
                label.setWordWrap(True)
                label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents) 
                
                del_btn = QPushButton("X")
                del_btn.setObjectName("deleteBtn")
                del_btn.setFixedSize(24, 24)
                del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                del_btn.clicked.connect(lambda checked, lw=list_widget, itm=item: self.delete_item(lw, itm))
                
                row_layout.addWidget(label)
                row_layout.addWidget(del_btn)
                
                item.setSizeHint(row_widget.sizeHint())
                
                if insert_at_top:
                    list_widget.insertItem(0, item)
                else:
                    list_widget.addItem(item)
                    
                list_widget.setItemWidget(item, row_widget)
                break

    def delete_item(self, list_widget, item):
        text_id = item.data(Qt.ItemDataRole.UserRole + 1)
        self.db.remove_text(text_id)
        row = list_widget.row(item)
        list_widget.takeItem(row)

    def copy_to_clipboard(self, item):
        text = item.data(Qt.ItemDataRole.UserRole)
        self.clipboard.setText(text)
        self.setWindowTitle(f"NEXUS // COPIADO: {text[:25]}...")

if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    window = CyberClipboard()
    window.show()
    sys.exit(app.exec())