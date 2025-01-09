import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog, QMessageBox, QColorDialog,
    QFontDialog, QToolBar, QStatusBar, QTabWidget, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout
)
from PyQt6.QtGui import QIcon, QFont, QTextCharFormat, QAction


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Инициализация интерфейса
        self.init_ui()

    def init_ui(self):
        # Настройка основного окна
        self.setWindowTitle('Text Editor')
        self.setGeometry(100, 100, 1000, 800)

        # Создание меню
        self.create_menus()

        # Создание панели инструментов и строки состояния
        self.create_toolbar()
        self.create_status_bar()

        # Показ главного окна
        self.show()

    def create_menus(self):
        # Главное меню
        menubar = self.menuBar()

        # Меню "Файл"
        file_menu = menubar.addMenu('Файл')
        new_action = QAction(QIcon('icons/new.png'), 'Новый', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)

        open_action = QAction(QIcon('icons/open.png'), 'Открыть...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)

        save_action = QAction(QIcon('icons/save.png'), 'Сохранить', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)

        save_as_action = QAction(QIcon('icons/save_as.png'), 'Сохранить как...', self)
        save_as_action.triggered.connect(self.save_file_as)

        print_action = QAction(QIcon('icons/print.png'), 'Печать...', self)
        print_action.setShortcut('Ctrl+P')
        print_action.triggered.connect(self.print_file)

        exit_action = QAction(QIcon('icons/exit.png'), 'Выход', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(print_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Меню "Правка"
        edit_menu = menubar.addMenu('Правка')
        undo_action = QAction(QIcon('icons/undo.png'), 'Отменить', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(lambda: self.current_editor().undo())

        redo_action = QAction(QIcon('icons/redo.png'), 'Повторить', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(lambda: self.current_editor().redo())

        cut_action = QAction(QIcon('icons/cut.png'), 'Вырезать', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.triggered.connect(lambda: self.current_editor().cut())

        copy_action = QAction(QIcon('icons/copy.png'), 'Копировать', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(lambda: self.current_editor().copy())

        paste_action = QAction(QIcon('icons/paste.png'), 'Вставить', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(lambda: self.current_editor().paste())

        select_all_action = QAction('Выделить всё', self)
        select_all_action.setShortcut('Ctrl+A')
        select_all_action.triggered.connect(lambda: self.current_editor().selectAll())

        find_action = QAction('Найти и заменить', self)
        find_action.setShortcut('Ctrl+F')
        find_action.triggered.connect(self.find_and_replace)

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(select_all_action)
        edit_menu.addAction(find_action)

        # Меню "Формат"
        format_menu = menubar
        # Меню "Формат"
        format_menu = menubar.addMenu('Формат')

        bold_action = QAction(QIcon('icons/bold.png'), 'Жирный', self, checkable=True)
        bold_action.setShortcut('Ctrl+B')
        bold_action.triggered.connect(self.toggle_bold)

        italic_action = QAction(QIcon('icons/italic.png'), 'Курсив', self, checkable=True)
        italic_action.setShortcut('Ctrl+I')
        italic_action.triggered.connect(self.toggle_italic)

        underline_action = QAction(QIcon('icons/underline.png'), 'Подчеркнуть', self, checkable=True)
        underline_action.setShortcut('Ctrl+U')
        underline_action.triggered.connect(self.toggle_underline)

        text_color_action = QAction(QIcon('icons/text_color.png'), 'Цвет текста...', self)
        text_color_action.triggered.connect(self.change_text_color)

        bg_color_action = QAction(QIcon('icons/bg_color.png'), 'Цвет фона...', self)
        bg_color_action.triggered.connect(self.change_background_color)

        font_action = QAction(QIcon('icons/font.png'), 'Выбрать шрифт...', self)
        font_action.triggered.connect(self.choose_font)

        format_menu.addAction(bold_action)
        format_menu.addAction(italic_action)
        format_menu.addAction(underline_action)
        format_menu.addSeparator()
        format_menu.addAction(text_color_action)
        format_menu.addAction(bg_color_action)
        format_menu.addAction(font_action)

        # Меню "Справка"
        help_menu = menubar.addMenu('Справка')

        about_action = QAction('О проекте', self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        # Создаем панель инструментов с основными кнопками
        toolbar = QToolBar("Инструменты")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Кнопки на панели инструментов
        toolbar.addAction(QIcon('icons/new.png'), "Новый", self.new_file)
        toolbar.addAction(QIcon('icons/open.png'), "Открыть", self.open_file)
        toolbar.addAction(QIcon('icons/save.png'), "Сохранить", self.save_file)
        toolbar.addSeparator()
        toolbar.addAction(QIcon('icons/undo.png'), "Отменить", lambda: self.current_editor().undo())
        toolbar.addAction(QIcon('icons/redo.png'), "Повторить", lambda: self.current_editor().redo())
        toolbar.addSeparator()
        toolbar.addAction(QIcon('icons/cut.png'), "Вырезать", lambda: self.current_editor().cut())
        toolbar.addAction(QIcon('icons/copy.png'), "Копировать", lambda: self.current_editor().copy())
        toolbar.addAction(QIcon('icons/paste.png'), "Вставить", lambda: self.current_editor().paste())

    def create_status_bar(self):
        # Создаем строку состояния
        self.status = QStatusBar()
        self.setStatusBar(self.status)

    def new_file(self):
        editor = QTextEdit()
        editor.textChanged.connect(self.update_status)
        index = self.tabs.addTab(editor, "Новый документ")
        self.tabs.setCurrentIndex(index)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    editor = QTextEdit()
                    editor.setText(f.read())
                    editor.textChanged.connect(self.update_status)
                    index = self.tabs.addTab(editor, filename)
                    self.tabs.setCurrentIndex(index)
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл:\n{e}")

    def save_file(self):
        editor = self.current_editor()
        if editor:
            current_index = self.tabs.currentIndex()
            filename = self.tabs.tabText(current_index)
            if filename == "Новый документ":
                self.save_file_as()
            else:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(editor.toPlainText())
                    self.status.showMessage("Файл успешно сохранен", 2000)
                except Exception as e:
                    QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")

    def save_file_as(self):
        editor = self.current_editor()
        if editor:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Сохранить файл как", "", "Текстовые файлы (*.txt);;Все файлы (*)"
            )
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(editor.toPlainText())
                    current_index = self.tabs.currentIndex()
                    self.tabs.setTabText(current_index, filename)
                    self.status.showMessage("Файл успешно сохранен", 2000)
                except Exception as e:
                    QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")

    def print_file(self):
        QMessageBox.information(self, "Печать", "Функция печати еще не реализована")

    def toggle_bold(self):
        editor = self.current_editor()
        if editor:
            cursor = editor.textCursor()
            fmt = cursor.charFormat()
            fmt.setFontWeight(QFont.Weight.Bold if not fmt.fontWeight() == QFont.Weight.Bold else QFont.Weight.Normal)
            cursor.mergeCharFormat(fmt)

    def toggle_italic(self):
        editor = self.current_editor()
        if editor:
            cursor = editor.textCursor()
            fmt = cursor.charFormat()
            fmt.setFontItalic(not fmt.fontItalic())
            cursor.mergeCharFormat(fmt)

    def toggle_underline(self):
        editor = self.current_editor()
        if editor:
            cursor = editor.textCursor()
            fmt = cursor.charFormat()
            fmt.setFontUnderline(not fmt.fontUnderline())
            cursor.mergeCharFormat(fmt)

    def change_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.current_editor().textCursor().mergeCharFormat(fmt)

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setBackground(color)
            self.current_editor().textCursor().mergeCharFormat(fmt)

    def choose_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            fmt = QTextCharFormat()
            fmt.setFont(font)
            self.current_editor().textCursor().mergeCharFormat(fmt)

    def find_and_replace(self):
        self.find_replace_dialog = QWidget()  # сохраняем в качестве атрибута
        self.find_replace_dialog.setWindowTitle("Найти и заменить")
        layout = QGridLayout()

        find_label = QLabel("Найти:")
        self.find_input = QLineEdit()
        replace_label = QLabel("Заменить на:")
        self.replace_input = QLineEdit()

        find_button = QPushButton("Найти")
        replace_button = QPushButton("Заменить")
        find_button.clicked.connect(self.find_text)
        replace_button.clicked.connect(self.replace_text)

        layout.addWidget(find_label, 0, 0)
        layout.addWidget(self.find_input, 0, 1)
        layout.addWidget(replace_label, 1, 0)
        layout.addWidget(self.replace_input, 1, 1)
        layout.addWidget(find_button, 2, 0)
        layout.addWidget(replace_button, 2, 1)

        self.find_replace_dialog.setLayout(layout)  # Используем атрибут для хранения диалога
        self.find_replace_dialog.show()

    def find_text(self):
        editor = self.current_editor()
        if editor:
            cursor = editor.textCursor()
            pattern = self.find_input.text()
            if not editor.find(pattern):
                QMessageBox.information(self, "Результат", "Текст не найден")

    def replace_text(self):
        editor = self.current_editor()
        if editor:
            cursor = editor.textCursor()
            if cursor.hasSelection():
                cursor.insertText(self.replace_input.text())

    def close_tab(self, index):
        if self.tabs.count() > 1:
            editor = self.tabs.widget(index)
            if editor.document().isModified():
                choice = QMessageBox.question(self, "Сохранить изменения?",
                                              "Документ был изменен. Сохранить?",
                                              QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if choice == QMessageBox.StandardButton.Yes:
                    self.save_file()
            self.tabs.removeTab(index)

    def current_editor(self):
        editor = self.tabs.currentWidget()
        if isinstance(editor, QTextEdit):  # Проверяем, что текущий виджет - это QTextEdit
            return editor
        else:
            QMessageBox.warning(self, "Ошибка", "Нет открытого документа для работы")
            return None

    def update_status(self):
        self.status.showMessage("Изменения внесены", 2000)

    def about(self):
        QMessageBox.information(self, "О проекте", "Текстовый редактор\nВерсия 1.0\nРазработано командой XYZ",
                                QMessageBox.StandardButton.Ok)


def main():
    app = QApplication(sys.argv)
    editor = TextEditor()
    sys.exit(app.exec())


main()
