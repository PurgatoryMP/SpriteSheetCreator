"""This script contains all the QT Control Style settings"""
import pathlib

from image_generator import ImageGenerator


# TODO: Update all the stylesheets with the defined style settings.

def get_style():

    generator = ImageGenerator()
    transparent_checkered_background = generator.get_checker_pattern()
    print(transparent_checkered_background)

    style_settings = {
        "": "",
        "Transparent_Checkered_Background": transparent_checkered_background,
        "Main_Window_Background_Color": "#303030",
        "Dock_Widget_Background_color": "#3D3D3D",
        "Separator_Color": "#161616",
        "Selected_Color": "#4772B3",
        "Non_Selected_Color": "#434D4F",
        "Viewer_Background_color": "#262626",
        "Unfocused_Console_Background_Color": "#434D4F",
        "Focused_Console_Background_Color": "#495456",
        "Border_scale": "1",
        "Horizontal_Scrollbar_Color": "#bf7575",
        "Vertical_Scrollbar_Color": "#94bf75",
        "Large_Font_Size": "18",
        "Normal_Font_Size": "14",
        "Small_Font_Size": "10",
    }
    return style_settings


def main_window_style():
    # background-image: url({"G:/Models/Refrences/Dj9dRgDUUAAtBLc.jpg"});

    style_sheet = """
        QMainWindow {
            background-color: %(Main_Window_Background_Color)s;
            font-size: 18px;
            color: White;
            border: 1px solid Black;
            border-radius: 5px;
        }
        QMainWindow::separator {
            background-color: %(Separator_Color)s;
            border: 1px solid Black;
            border-radius: 3px;
        }
        QMainWindow::separator:hover  {
            background-color: %(Separator_Color)s;  
            border: 1px solid gold;
            border-radius: 3px;
        }
        
        QTabWidget::pane {
            border: 1px solid Gold;
            border-radius: 5px;
        }

        QTabBar::tab {
            background-color: %(Non_Selected_Color)s;
            color: White;
            padding: 5px;
            border: 1px solid Black;
            border-radius: 5px;
        }

        QTabBar::tab:selected {
            background-color: %(Selected_Color)s;
            color: Gold;
            border: 1px solid Gold;
            border-radius: 5px;
        }
        
        QDockWidget {
            background-color: %(Selected_Color)s;
            border-radius: 15px;
        }
        
        QDockWidget::title {
            alignment: AlignCenter;
            background-color: #484A4F;
            color: White;
            font-size: 14px;
            padding: 5px;
            border: 1px solid Black;
            border-radius: 5px;
        }
        
        QDockWidget::title:hover {
            background-color: #52545A;
            border: 1px solid LightGrey;
        }
        
        QDockWidget::float-button:hover {
            border: 1px solid LightBlue;
            border-radius: 10px;
        }
        
        QDockWidget::close-button:hover {
            border: 1px solid Red;
            border-radius: 10px;
        }
    }
    """ % get_style()

    return style_sheet

def table_widget_style():
    stylesheet = """
    QTableWidget {
        background-color: #484A4F;  /* Set the background color */
        alternate-background-color: Green;  /* Set the alternate row background color */
        selection-background-color: Blue;  /* Set the selection background color */
        selection-color: Gold;  /* Set the selection text color */
        selection-border: 1px solid Gold;
        color: white;
        border: 1px solid Black;
        border-radius: 10px;
    }

    QTableWidget::item {
        background-color: #6e6f70;
        border: 1px solid Black;
        border-radius: 10px;
        padding: 5px;
    }

    QHeaderView::section {
        background-color: #434D4F;  /* Set the header background color */
        color: White;  /* Set the header text color */
        padding: 5px;  /* Set the padding for header sections */
        border: 1px solid Black;
        border-radius: 5px;
    }

    QHeaderView::section:checked {
        background-color: #4772B3;  /* Set the background color when the section is checked */
        
    }

    QTableWidget QTableCornerButton::section {
        background-color: #4772B3;  /* Set the corner button background color */
        border: 1px solid Black;
        border-radius: 20px;
    }
    
    QHeaderView QTableCornerButton::checked {
        background-color: Red;  /* Set the background color when the section is checked */
        
    }

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
    return stylesheet

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
            background-color: #545454;
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
            background-color: %(Viewer_Background_color)s;
        }
        
        QGraphicsView:hover {
            background-color: #484A4F;
            border: 2px solid LightGrey;
            border-radius: 8px;
        }
    """ % get_style()
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

def explore_folder_btn_style():
    style_sheet = """
        QPushButton {
            background-color: #4772B3;
            color: White;
            border: 1px solid Black;
            font-size: 14px;
            border-radius: 8px;
            padding: 6;
        }

        QPushButton:hover {
            background-color: #5284d1;
            color: White;
        }

        QPushButton:pressed {
            background-color: #39619e;
            color: White;
        }
    """
    return style_sheet

def folder_path_label_style():
    style_sheet = """
            QLabel {
                background-color: #434D4F;
                color: White;
                font-size: 14px;
                border: 1px solid Black;
                border-radius: 8px;
                padding: 4px;

            }
        """
    return style_sheet

def console_style():
    style_sheet = """
        QTextEdit {
            background-color: %(Unfocused_Console_Background_Color)s; /* Background color */
            color: #White; /* Text color */
            font-family: Arial, sans-serif; /* Font family */
            font-size: 12px; /* Font size */
            border: 1px solid Black; /* Border style */
            padding: 4px; /* Padding */
        }
        
        QTextEdit:hover {
            background-color: #4F5B5D;
            border: 1px solid White;
        }
        
        QTextEdit:focus {
            background-color: %(Focused_Console_Background_Color)s; /* Background color */
            color: #White; /* Text color */
            border: 1px solid #50BBAE; /* Border style when focused */         
        }
    """ % get_style()
    return style_sheet

def status_bar_style():
    style_sheet = """
        QStatusBar {
            background-color: #545454;
            color: #000000;
            font-family: Arial;
            font-size: 12px;
            border: 1px solid Black;
            border-radius: 8px;
        }
        
        StatusBar:QLabel {
            color: White;
            font-size: 14px;
            border: 1px solid Black;
            border-radius: 8px;
        }   
        
        QSizeGrip {
            background-color: #434D4F;
            border: 1px solid Black;
            border-radius: 5px;
        }
        QSizeGrip:hover {
            background-color: lightgreen;
            border: 1px solid Black;
            border-radius: 5px;
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
