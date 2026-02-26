splash_window_style = """
#container {
    background-color: rgba(255, 255, 255, 180);
    border-radius: 8px;
}
QLabel {
    color: #303030;
    font-size: 14px;
}
"""
url_label_style = """
QPushButton {
    background: transparent;
    border: none;
    color: #303030;
    text-decoration: underline;
    font-size: 12px;
    outline: none;
}

QPushButton:focus {
    outline: none;
}
"""
check_box_style = """
    QCheckBox {
        color: #303030;   
        font-size: 12px;
    }
"""

slider_style = """
QSlider::groove:horizontal {
    height: 6px;
    background: #f0f0f0;
    margin: 2px 0;
    border-radius: 3px;
    border: 1px solid #888;
}

QSlider::sub-page:horizontal {    
    background: #303030;         
    border-radius: 3px;
    border: 1px solid #888;
}

QSlider::add-page:horizontal {    
    background: #f8f8f8;
    border-radius: 3px;
    border: 1px solid #888;
}

QSlider::handle:horizontal {
    background-color: #666;
    border: 2px solid #444;
    width: 18px;
    height: 18px;
    margin: -6px 0;   
    border-radius: 3px;
}
"""

push_btn_style = """
QPushButton {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 10px 20px;
    font-size: 14px;
    min-height: 18px;
    outline: none;
}

QPushButton:focus {
    outline: none;
}

QPushButton:hover {
    background-color: #3a3a3a;
    border: 1px solid #666;
}

QPushButton:pressed {
    background-color: #1e1e1e;
    padding: 11px 20px 9px 20px; 
}

QPushButton:disabled {
    background-color: #222;
    color: #555;
    border: 1px solid #333;
}
"""


text_label_style_piano_map_black = """
QLabel {
    color: #f8f8f8;
    background-color: #303030;           
    font-size: 12px;
    min-width: 100px; 
    min-height: 30px;
    max-height: 30px; 
    border-radius: 4px;
    border: 2px solid #555555;
}
"""

text_label_style_piano_map_black_press = """
QLabel {
    color: #f8f8f8;
    background-color: #505050;           
    font-size: 12px;
    min-width: 100px; 
    min-height: 30px;
    max-height: 30px; 
    border-radius: 4px;
    border: 2px solid #555555;
}
"""

text_label_style_piano_map_black_sp = """
QLabel {
    color: #f8f8f8;
    background-color: #303030;           
    font-size: 12px;
    min-width: 100px; 
    min-height: 30px;
    max-height: 30px; 
    border-radius: 4px;
    border: 2px solid #555555;
    margin-left: 100px
}
"""

text_label_style_piano_map_black_sp_press = """
QLabel {
    color: #f8f8f8;
    background-color: #505050;           
    font-size: 12px;
    min-width: 100px; 
    min-height: 30px;
    max-height: 30px; 
    border-radius: 4px;
    border: 2px solid #555555;
    margin-left: 100px
}
"""

text_label_style_piano_map_white = """
QLabel {
    color: #303030;
    background-color: #f8f8f8;               
    font-size: 12px;
    min-width: 100px; 
    min-height: 30px; 
    max-height: 30px; 
    border-radius: 4px;
    border: 2px solid #aaaaaa;
}
"""

text_label_style_piano_map_white_press = """
QLabel {
    color: #303030;
    background-color: #e8e8e8;               
    font-size: 12px;
    min-width: 100px; 
    min-height: 30px; 
    max-height: 30px; 
    border-radius: 4px;
    border: 2px solid #aaaaaa;
}
"""

text_label_style = """
QLabel {
    color: #303030;                  
    font-size: 14px;              
}
"""

text_label_style_mini = """
QLabel {
    color: #303030;                  
    font-size: 12px;              
}
"""

text_label_style_desc = """
QLabel {
    color: #808080;                  
    font-size: 12px;              
}
"""

text_browser_style = """
QTextBrowser {
    background-color: #f8f8f8; 
    color: #303030;                          
    font-size: 12px;
    border: 2px solid #aaaaaa;
    border-radius: 4px;                     
    padding: 4px;
}
QScrollBar:vertical {
    width: 6px;
    background: transparent;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
        background: transparent;
        border: none;
    }
QScrollBar::handle:vertical {
    background: rgba(180,180,180,0.4);
    border-radius: 3px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(180,180,180,0.8);
    border-radius: 3px;
}
"""
