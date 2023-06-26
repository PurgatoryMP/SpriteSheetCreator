"""This script contains all the QT Control Style settings"""
import pathlib

import image_generator

def main_window_style():
    # background-image: url({"G:/Models/Refrences/Dj9dRgDUUAAtBLc.jpg"});

    style_sheet = """
        QMainWindow {
            background-color: #303030;
            font-size: 18px;
            color: White;
            border: 1px solid Black;
            border-radius: 5px;
    }
    """

    return style_sheet

def dock_widget_style():
    style_sheet = """
        QWidget {
            alignment: AlignCenter;
            background-color: #3D3D3D;
            font-size: 18px;
            color: #E5E5E5;
            border: 1px solid Black;
            border-radius: 5px;
    }
    """
    return style_sheet

def menu_bar_style():
    style_sheet = """
        QMenuBar {
            qproperty-alignment: AlignCenter;
            background-color: #586875;
            font-size: 14px;
            color: White;
            border: 1px solid Black;
            border-radius: 5px;
        }

        QMenuBar::item:selected {
            background-color: #4a5157;
            color: White;
            border: 1px solid Black;
            border-radius: 5px;
        }

        QMenuBar::item:pressed {
            background-color: LightGreen;
            color: White;
            border: 1px solid Black;
        }

        QMenu {
            qproperty-alignment: AlignCenter;
            background-color: #545454;
            color: White;
            border: 1px solid Black;
            border-radius: 5px;
        }

        QMenu::item:selected {
            background-color: lightGrey;
            color: black;
            border: 1px solid Black;
            border-radius: 5px;
        }

        QMenu::item:pressed {
            background-color: LightGreen;
            color: black;
            border: 1px solid Black;
            border-radius: 5px;
        }
    """
    return style_sheet

def scroll_bar_style():
    style_sheet = """
    QScrollBar:vertical {
        background-color: #575859;
        width: 15px;
        margin: 0px;
    }
    
    QScrollBar:horizontal {
        background-color: #575859;
        height: 15px;
        margin: 0px;
    }

    QScrollBar::handle:vertical {
        border: 1px solid Black;
        background: #94bf75;
        min-height: 20px;
        border-radius: 5px;
    }

    QScrollBar::handle:horizontal {
        border: 1px solid Black;
        background: #bf7575;
        min-width: 20px;
        border-radius: 5px;
    }
    """
    return style_sheet

def graphics_scene_style():
    # checker_image = image_generator.create_checker_pattern(16, 16, 8)
    # f'background-image: url("{checker_image}"); border: 1px solid black;'

    style_sheet = """
        QGraphicsView {
        background-color: #333333;
        }
        
        QGraphicsView:hover {
            background-color: #484A4F;
            border: 2px solid LightGrey;
            border-radius: 8px;
        }
    """
    return style_sheet


def spinbox_style():
    # arrow_pixmap = image_generator.generate_arrow_image()
    # / *image: url({""" + arrow_pixmap + """}); * /

    style_sheet = """
        QSpinBox {
            qproperty-alignment: AlignCenter;
            background-color: #545454;
            color: White;
            font-size: 14px;
            font-weight: string;
            border: 1px solid Black;
            border-radius: 8px;
            padding: 4px;
            padding-right: 20px; /* Add space for the right arrow button */
        }
        
        QSpinBox::hover {
            background-color: #686868;
        }
    
        QSpinBox::up-button, QSpinBox::down-button {
            width: 15px;
            height: 15px;
            border: 1px solid Black;
            border-radius: 5px;
            background-color: DarkGrey;
        }
        
        QSpinBox::up-button:hover {
            background-color: LightGrey;
        }
        QSpinBox::down-button:hover {
            background-color: LightGrey;
        }
    
        QSpinBox::up-button {
            subcontrol-position: right; /* Position the up arrow button on the right side */
            right: 0;
            subcontrol-border: 1px solid Black;
            subcontrol-origin: border;
        }
    
        QSpinBox::down-button {
            subcontrol-position: left; /* Position the down arrow button on the left side */
            left: 0;
            subcontrol-border: 1px solid Black;
            subcontrol-origin: border;
        }
    """
    return style_sheet


def play_btn_style():
    style_sheet = """
        QPushButton {
            background-color: LightGreen;
            color: black;
            border: 1px solid Black;
            font-size: 14px;
            border-radius: 8px;  
            width: 25px;
            height: 20px;
            padding: 6;
        }

        QPushButton:hover {
            background-color: Green;
            color: black;
        }

        QPushButton:pressed {
            background-color: DarkGreen;
            color: black;
        }
    """
    return style_sheet


def stop_btn_style():
    style_sheet = """
        QPushButton {
            background-color: LightPink;
            color: black;
            border: 1px solid Black;
            font-size: 14px;
            border-radius: 8px;          
            width: 25px;
            height: 20px;
            padding: 6;
        }

        QPushButton:hover {
            background-color: Red;
            color: black;
        }

        QPushButton:pressed {
            background-color: DarkRed;
            color: black;
        }
    """
    return style_sheet

def console_style():
    style_sheet = """
        QTextEdit {
            background-color: #3D3D3D; /* Background color */
            color: #White; /* Text color */
            font-family: Arial, sans-serif; /* Font family */
            font-size: 12px; /* Font size */
            border: 1px solid #CCCCCC; /* Border style */
            padding: 4px; /* Padding */
        }
        
        QTextEdit:focus {
            border: 1px solid #0000FF; /* Border style when focused */
}
    """
    return style_sheet

def seperator_label_style():
    style_sheet = """
        QLabel {
            border: 0px solid Black;
            color: White;
            font-size: 18px;
            padding: 4px;
            width: 50px;
            height: 20px;
        }
    """
    return style_sheet


def bubble_label_style():
    style_sheet = """
        QLabel {
            background-color: #4772B3;
            color: White;
            font-size: 14px;
            border: 1px solid Black;
            border-radius: 8px;
            padding: 4px;
            
        }
    """
    return style_sheet
