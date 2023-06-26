from PyQt5.QtWidgets import QMenuBar, QAction, QMenu

import style_sheet

def create_menu_bar():
    menubar = QMenuBar()

    file_menu = menubar.addMenu("File")

    new_action = QAction("New", menubar)
    open_action = QAction("Open", menubar)
    save_action = QAction("Save", menubar)
    save_as_action = QAction("Save As", menubar)
    close_action = QAction("Close", menubar)
    exit_action = QAction("Exit", menubar)
    about_action = QAction("About", menubar)

    file_menu.addAction(new_action)
    file_menu.addAction(open_action)
    file_menu.addAction(save_action)
    file_menu.addAction(save_as_action)
    file_menu.addAction(close_action)
    file_menu.addSeparator()
    file_menu.addAction(exit_action)
    file_menu.addSeparator()
    file_menu.addAction(about_action)

    file_menu.setStyleSheet(style_sheet.menu_bar_style())

    return menubar
