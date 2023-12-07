"""This script contains all the QT Control Style settings"""
# import pathlib

# from image_generator import ImageGenerator


# TODO: Update all the stylesheets with the defined style settings.
# TODO: Find out why I can't use an image I generated as a background post run.

def get_style():

    # generator = ImageGenerator()
    # transparent_checkered_background = str(generator.get_checker_pattern()).replace("\\", "/")
    # print(transparent_checkered_background)

    style_settings = {

        "Main_Window_Background_Color": "#303030",
        "Dock_Widget_Background_color": "#3D3D3D",
        "Dock_Title_Background_Color": "#484A4F",
        "ProgressBar_Background_Color": "#303030",
        "ProgressBar_Loading_Color": "#42f572",
        "Border_Radius": "5px",
        "Separator_Color": "#161616",
        "Selected_Color": "#4772B3",
        "Pressed_Color": "#47b369",
        "PlayBtn_Color": "DarkGreen",
        "PlayBtn_Color_Hover": "Green",
        "PlayBtn_Color_Pressed": "lightGreen",
        "StopBtn_Color": "DarkRed",
        "StopBtn_Color_Hover": "Red",
        "StopBtn_Color_Pressed": "Pink",
        "Non_Selected_Color": "#434D4F",
        "Viewer_Background_color": "#262626",
        "Unfocused_Console_Background_Color": "#434D4F",
        "Hover_Console_Background_Color": "#4F5B5D",
        "Focused_Console_Background_Color": "#495456",
        "Border_size_color": "1px solid Black",
        "Border_hover_size_color": "1px solid gold",
        "Horizontal_Scrollbar_Color": "#bf7575",
        "Vertical_Scrollbar_Color": "#94bf75",
        "Font_Family": "Arial, sans-serif",
        "Font_Size": "14px",
        "Font_Color": "#e8e8e8",
        "Hover_Font_Color": "#fcfcfa",
        "Selected_Font_Color": "#FFD700",
        "padding_size": "4px",
    }
    return style_settings


def main_window_style():
    style_sheet = """
        QMainWindow {
            background-color: %(Main_Window_Background_Color)s;
            font-size: %(Font_Size)s;
            color: %(Font_Color)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
        }
        QMainWindow::separator {
            background-color: %(Separator_Color)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
        }
        QMainWindow::separator:hover  {
            background-color: %(Separator_Color)s;  
            border: %(Border_hover_size_color)s;
            border-radius: %(Border_Radius)s;
        }        
        QTabWidget::pane {
            border: 1px solid Gold;
            border-radius: %(Border_Radius)s;
        }
        QTabBar::tab {
            background-color: %(Non_Selected_Color)s;
            color: %(Font_Color)s;
            padding: %(padding_size)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
        }
        QTabBar::tab:selected {
            background-color: %(Selected_Color)s;
            color: %(Selected_Font_Color)s;
            border: %(Border_hover_size_color)s;
            border-radius: %(Border_Radius)s;
        }        
        QDockWidget {
            background-color: %(Selected_Color)s;
            border-radius: %(Border_Radius)s;
        }        
        QDockWidget::title {
            alignment: AlignCenter;
            background-color: %(Dock_Title_Background_Color)s;
            color: %(Font_Color)s;
            font-size: %(Font_Size)s;
            padding: %(padding_size)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
        }        
        QDockWidget::title:hover {
            background-color: #52545A;
            border: 1px solid LightGrey;
        }        
        QDockWidget::float-button:hover {
            border: 1px solid LightBlue;
            border-radius: %(Border_Radius)s;
        }        
        QDockWidget::close-button:hover {
            border: 1px solid Red;
            border-radius: %(Border_Radius)s;
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
        border: %(Border_size_color)s;
        border-radius: %(Border_Radius)s;
    }
    QTableWidget::item {
        background-color: #6e6f70;
        border: %(Border_size_color)s;
        border-radius: %(Border_Radius)s;
        padding: %(padding_size)s;
    }
    QHeaderView::section {
        background-color: #434D4F;  /* Set the header background color */
        color: %(Font_Color)s;
        padding: %(padding_size)s;
        border: %(Border_size_color)s;
        border-radius: %(Border_Radius)s;
    }
    QHeaderView::section:checked {
        background-color: #4772B3;  /* Set the background color when the section is checked */
        
    }
    QTableWidget QTableCornerButton::section {
        background-color: #4772B3;  /* Set the corner button background color */
        border: %(Border_size_color)s;
        border-radius: %(Border_Radius)s;
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
        border: %(Border_size_color)s;
        background: #94bf75;
        min-height: 20px;
        border-radius: %(Border_Radius)s;
    }
    QScrollBar::handle:horizontal {
        border: %(Border_size_color)s;
        background: #bf7575;
        min-width: 20px;
        border-radius: %(Border_Radius)s;
    }
    """ % get_style()
    return stylesheet

def dock_widget_style():
    style_sheet = """
        QWidget {
            alignment: AlignCenter;
            background-color: %(Dock_Widget_Background_color)s;
            font-size: %(Font_Size)s;
            color: %(Font_Color)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
    }
    """ % get_style()
    return style_sheet

def menu_bar_style():
    style_sheet = """
        QMenuBar {
            qproperty-alignment: AlignCenter;
            background-color: #545454;
            font-size: %(Font_Size)s;
            color: %(Font_Color)s;
            padding: %(padding_size)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
        }
        QMenuBar::item:selected {
            background-color: %(Selected_Color)s;
            color: %(Selected_Font_Color)s;
            border: %(Border_hover_size_color)s;
            border-radius: %(Border_Radius)s;
        }
        QMenuBar::item:pressed {
            background-color: %(Pressed_Color)s;
            color: %(Font_Color)s;
            border: %(Border_size_color)s;
        }
        QMenu {
            qproperty-alignment: AlignCenter;
            background-color: #545454;
            color: %(Font_Color)s;
            padding: %(padding_size)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
        }
        QMenu::item:selected {
            background-color: %(Selected_Color)s;
            color: %(Font_Color)s;
            border: %(Border_hover_size_color)s;
            border-radius: %(Border_Radius)s;
        }
        QMenu::item:pressed {
            background-color: %(Pressed_Color)s;
            color: %(Selected_Font_Color)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
        }
    """ % get_style()
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
        border: %(Border_size_color)s;
        background: #94bf75;
        min-height: 20px;
        border-radius: %(Border_Radius)s;
    }
    QScrollBar::handle:horizontal {
        border: %(Border_size_color)s;
        background: #bf7575;
        min-width: 20px;
        border-radius: %(Border_Radius)s;
    }
    """ % get_style()
    return style_sheet

def progress_bar_style():
    style_sheet = """
    QProgressBar {
        background-color: %(ProgressBar_Background_Color)s;
        text-visible: false;
        width: 50px;
        }
    QProgressBar::chunk {
        background-color: %(ProgressBar_Loading_Color)s;
    }    
    """ % get_style()
    return style_sheet

def graphics_View_style():
    # checker_image = image_generator.create_checker_pattern(16, 16, 8)
    # f'background-image: url("{checker_image}"); border: 1px solid black;'

    style_sheet = """
        QGraphicsView {
            background-color: %(Main_Window_Background_Color)s;
        }        
        QGraphicsView:hover {
            background-color: #484A4F;
            border: 2px solid LightGrey;
            border-radius: %(Border_Radius)s;
        }
    """ % get_style()
    return style_sheet

def checkbox_style():
    style_sheet = """
        QCheckBox {
            border: none;
            font-size: %(Font_Size)s;
            color: %(Font_Color)s;
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
            color: %(Font_Color)s;
            font-size: %(Font_Size)s;
            font-weight: string;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
            padding: %(padding_size)s;
            padding-right: 20px; /* Add space for the right arrow button */
        }        
        QSpinBox::hover {
            background-color: #686868;
        }    
        QSpinBox::up-button, QSpinBox::down-button {
            width: 15px;
            height: 15px;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
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
            subcontrol-border: %(Border_size_color)s;
            subcontrol-origin: border;
        }    
        QSpinBox::down-button {
            subcontrol-position: left; /* Position the down arrow button on the left side */
            left: 0;
            subcontrol-border: %(Border_size_color)s;
            subcontrol-origin: border;
        }
    """ % get_style()
    return style_sheet


def spinbox_style_disabled():
    # arrow_pixmap = image_generator.generate_arrow_image()
    # / *image: url({""" + arrow_pixmap + """}); * /

    style_sheet = """
        QSpinBox {
            qproperty-alignment: AlignCenter;
            background-color: #545454;
            color: %(Font_Color)s;
            font-size: %(Font_Size)s;
            font-weight: string;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
            padding: %(padding_size)s;
            padding-right: 20px; /* Add space for the right arrow button */
        }
        QSpinBox::hover {
            background-color: #686868;
        }
        QSpinBox::up-button, QSpinBox::down-button {
            width: 15px;
            height: 15px;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
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
            subcontrol-border: %(Border_size_color)s;
            subcontrol-origin: border;
        }
        QSpinBox::down-button {
            subcontrol-position: left; /* Position the down arrow button on the left side */
            left: 0;
            subcontrol-border: %(Border_size_color)s;
            subcontrol-origin: border;
        }
    """ % get_style()
    return style_sheet

def play_btn_style():
    style_sheet = """
        QPushButton {
            background-color: %(PlayBtn_Color)s;
            color: %(Font_Color)s;
            border: %(Border_size_color)s;
            font-size: %(Font_Size)s;
            border-radius: %(Border_Radius)s;
            width: 25px;
            height: 20px;
            padding: %(padding_size)s;
        }
        QPushButton:hover {
            background-color: %(PlayBtn_Color_Hover)s;
            color: %(Hover_Font_Color)s;
        }
        QPushButton:pressed {
            background-color: %(PlayBtn_Color_Pressed)s;
            color: %(Selected_Font_Color)s;
        }
    """ % get_style()
    return style_sheet


def stop_btn_style():
    style_sheet = """
        QPushButton {
            background-color: %(StopBtn_Color)s;
            color: %(Font_Color)s;
            border: %(Border_size_color)s;
            font-size: %(Font_Size)s;
            border-radius: %(Border_Radius)s;      
            width: 25px;
            height: 20px;
            padding: %(padding_size)s;
        }
        QPushButton:hover {
            background-color: %(StopBtn_Color_Hover)s;
            color: %(Hover_Font_Color)s;
        }
        QPushButton:pressed {
            background-color: %(StopBtn_Color_Pressed)s;
            color: %(Selected_Font_Color)s;
        }
    """ % get_style()
    return style_sheet

def explore_folder_btn_style():
    style_sheet = """
        QPushButton {
            background-color: #4772B3;
            color: %(Font_Color)s;
            border: %(Border_size_color)s;
            font-size: %(Font_Size)s;
            border-radius: %(Border_Radius)s;
            padding: %(padding_size)s;
        }
        QPushButton:hover {
            background-color: #5284d1;
            color: %(Hover_Font_Color)s;
        }
        QPushButton:pressed {
            background-color: %(Pressed_Color)s;
            color: %(Selected_Font_Color)s;
        }
    """ % get_style()
    return style_sheet

def image_grid_image_style():
    style_sheet = """
        QLabel:hover {
            background-color: #6b7c80;
            border: %(Border_hover_size_color)s;
            border-radius: %(Border_Radius)s;
        }
        """ % get_style()
    return style_sheet

def image_grid_label_style():
    style_sheet = """
        QLabel {
            background-color: #434D4F;
            color: %(Font_Color)s;
            font-size: %(Font_Size)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
            padding: %(padding_size)s;
        }
        QLabel:hover {
            background-color: #6b7c80;
            border: %(Border_hover_size_color)s;
            border-radius: %(Border_Radius)s;
        }
        """ % get_style()
    return style_sheet

def folder_path_label_style():
    style_sheet = """
        QLabel {
            cursor: DragCopyCursor;
            background-color: #434D4F;
            color: %(Font_Color)s;
            font-size: %(Font_Size)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
            padding: %(padding_size)s;
        }
        QLabel:hover {
            background-color: #4F5B5D;
            border: %(Border_hover_size_color)s;
            border-radius: %(Border_Radius)s;
        }
        """ % get_style()
    return style_sheet

def console_style():
    style_sheet = """
        QTextEdit {
            background-color: %(Unfocused_Console_Background_Color)s; /* Background color */
            color: %(Font_Color)s;
            font-family: %(Font_Family)s;
            font-size: %(Font_Size)s;
            border: %(Border_size_color)s;
            padding: %(padding_size)s;
        }
        
        QTextEdit:hover {
            background-color: %(Hover_Console_Background_Color)s;
            border: %(Border_hover_size_color)s;
        }
        
        QTextEdit:focus {
            background-color: %(Focused_Console_Background_Color)s; /* Background color */
            color: %(Font_Color)s;
            border: 1px solid #50BBAE; /* Border style when focused */         
        }
    """ % get_style()
    return style_sheet

def status_bar_style():
    style_sheet = """
        QStatusBar {
            background-color: #545454;
            color: %(Font_Color)s;
            font-family: %(Font_Family)s;
            font-size: %(Font_Size)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
        }
        
        StatusBar:QLabel {
            color: %(Font_Color)s;
            font-size: %(Font_Size)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
        }   
        
        QSizeGrip {
            background-color: #434D4F;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
        }
        QSizeGrip:hover {
            background-color: lightgreen;
            border: %(Border_hover_size_color)s;
            border-radius: %(Border_Radius)s;
        }        
    """ % get_style()
    return style_sheet

def seperator_label_style():
    style_sheet = """
        QLabel {
            border: 0px solid Black;
            color: %(Font_Color)s;
            font-size: %(Font_Size)s;
            padding: %(padding_size)s;
            width: 50px;
            height: 20px;
        }
    """ % get_style()
    return style_sheet


def bubble_label_style():
    style_sheet = """
        QLabel {
            background-color: #4772B3;
            color: %(Font_Color)s;
            font-size: %(Font_Size)s;
            border: %(Border_size_color)s;
            border-radius: %(Border_Radius)s;
            padding: %(padding_size)s;       
        }
    """ % get_style()
    return style_sheet
