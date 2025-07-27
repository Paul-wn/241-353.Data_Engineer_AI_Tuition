# app.py - ไฟล์หลักของแอป

import dash
from dash import html
from config import COLORS
from data_utils import load_and_clean_data
from layout import (
    create_header, 
    create_filters, 
    create_map_section, 
    create_details_section,
    create_statistics_section, 
    create_charts_section
)
from callbacks import register_callbacks

# โหลดข้อมูล
df_clean = load_and_clean_data()

# สร้างแอป Dash
app = dash.Dash(__name__, external_stylesheets=['assets/custom.css'])

# กำหนด Layout หลัก
app.layout = html.Div([
    # Container หลักพร้อมพื้นหลัง gradient
    html.Div([
        # ส่วนหัว
        create_header(),
        
        # ส่วนกรองข้อมูล
        create_filters(df_clean),
        
        # เนื้อหาหลัก
        html.Div([
            # แถวแผนที่และรายละเอียด
            html.Div([
                create_map_section(),
                create_details_section()
            ], style={'marginBottom': '32px'}),
            
            # แถววิเคราะห์ข้อมูล
            html.Div([
                create_statistics_section(),
                create_charts_section()
            ])
        ], className="fade-in")
    ], style={
        'background': COLORS['background'],
        'minHeight': '100vh',
        'padding': '40px 20px',
        'fontFamily': "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
    })
], style={'margin': '0', 'padding': '0'})

# ลงทะเบียน callbacks
register_callbacks(app, df_clean)

# รันแอป
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8050)