# charts.py - ฟังก์ชันสร้างกราฟ

import plotly.graph_objects as go
from config import COLORS, PROGRAM_COLORS, MAP_CONFIG
from data_utils import add_coordinate_offset

def create_map_figure(filtered_df):
    """สร้างแผนที่"""
    if len(filtered_df) == 0:
        return go.Figure().add_annotation(
            text="No universities match the selected criteria",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text_secondary'])
        )
    
    # เพิ่มการเลื่อนพิกัดสำหรับมหาวิทยาลัยที่ซ้อนทับกัน
    filtered_df = add_coordinate_offset(filtered_df)
    
    fig = go.Figure()
    
    # เพิ่มจุดสำหรับแต่ละประเภทโปรแกรม
    for prog_type in filtered_df['program_type'].unique():
        prog_data = filtered_df[filtered_df['program_type'] == prog_type]
        
        fig.add_trace(go.Scattermapbox(
            lat=prog_data['display_lat'],
            lon=prog_data['display_lon'],
            mode='markers',
            marker=dict(
                size=MAP_CONFIG['marker_size'],
                symbol='circle',
                color=PROGRAM_COLORS.get(prog_type, COLORS['secondary']),
                opacity=0.9,
                sizemode='diameter'
            ),
            text=prog_data['unique_id'],
            hovertemplate='<b>🏫 ' + prog_data['มหาวิทยาลัย'].astype(str) + '</b><br>' +
                         '📚 ' + prog_data['program_type'].astype(str) + '<br>' +
                         '🎓 ' + prog_data['หลักสูตร'].astype(str) + '<br>' +
                         '🏢 ' + prog_data['วิทยาเขต'].astype(str) + '<br>' +
                         '💰 Tuition: ฿' + prog_data['final_tuition_fee'].apply(lambda x: f"{x:,.0f}") + '<br>' +
                         '<extra></extra>',
            customdata=prog_data['final_tuition_fee'],
            name=prog_type
        ))
    
    fig.update_layout(
        mapbox=dict(
            style=MAP_CONFIG['style'],
            center=dict(lat=MAP_CONFIG['center_lat'], lon=MAP_CONFIG['center_lon']),
            zoom=MAP_CONFIG['zoom']
        ),
        height=450,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text_primary'], family="Inter"),
        legend=dict(
            title=dict(text='Program Types', font=dict(size=14, color=COLORS['text_primary'])),
            orientation='v',
            x=0.02,
            y=0.98,
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='rgba(255,255,255,0.5)',
            borderwidth=1,
            font=dict(size=12, color=COLORS['text_primary']),
            itemclick='toggleothers',
            itemdoubleclick='toggle'
        )
    )
    
    return fig

def create_regional_chart(filtered_df):
    """สร้างกราฟเปรียบเทียบภูมิภาค"""
    if len(filtered_df) == 0:
        return go.Figure().add_annotation(
            text="No data available",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text_secondary'])
        )
    
    # คำนวณสถิติภูมิภาค
    regional_stats = filtered_df.groupby('region').agg({
        'final_tuition_fee': ['mean', 'count'],
        'มหาวิทยาลัย': 'nunique'
    }).round(0)
    
    regional_stats.columns = ['avg_tuition', 'program_count', 'university_count']
    regional_stats = regional_stats.reset_index()
    
    fig = go.Figure()
    
    # กราฟแท่งสำหรับจำนวนโปรแกรม
    fig.add_trace(go.Bar(
        name='Programs',
        x=regional_stats['region'],
        y=regional_stats['program_count'],
        marker_color=COLORS['primary'],
        opacity=0.8,
        text=regional_stats['program_count'],
        textposition='auto',
        textfont=dict(color='white', size=12, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Programs: %{y}<extra></extra>'
    ))
    
    # กราฟเส้นสำหรับค่าเล่าเรียนเฉลี่ย
    fig.add_trace(go.Scatter(
        name='Avg. Tuition',
        x=regional_stats['region'],
        y=regional_stats['avg_tuition'],
        mode='lines+markers',
        line=dict(color=COLORS['warning'], width=3),
        marker=dict(size=8, color=COLORS['warning']),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Avg. Tuition: ฿%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Programs & Average Tuition by Region',
            font=dict(size=16, color=COLORS['text_primary'], family='Inter'),
            x=0.5
        ),
        xaxis=dict(title='Region', color=COLORS['text_secondary'], tickangle=45),
        yaxis=dict(title='Number of Programs', color=COLORS['text_secondary'], side='left'),
        yaxis2=dict(title='Average Tuition (฿)', color=COLORS['text_secondary'], overlaying='y', side='right'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=COLORS['text_primary']),
        margin=dict(l=50, r=50, t=80, b=100)
    )
    
    return fig

def create_program_distribution_chart(filtered_df):
    """สร้างกราฟแสดงการกระจายโปรแกรม"""
    if len(filtered_df) == 0:
        return go.Figure().add_annotation(
            text="No data available",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text_secondary'])
        )
    
    # คำนวณการกระจายโปรแกรม
    program_counts = filtered_df['program_type'].value_counts()
    colors_list = [PROGRAM_COLORS.get(prog, COLORS['secondary']) for prog in program_counts.index]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=program_counts.index,
            values=program_counts.values,
            hole=0.4,
            marker=dict(colors=colors_list, line=dict(color='white', width=2)),
            textinfo='label+percent+value',
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
            textfont=dict(size=12, family='Inter')
        )
    ])
    
    fig.update_layout(
        annotations=[
            dict(
                text=f"Total<br>{program_counts.sum()}<br>Programs",
                x=0.5, y=0.5,
                font_size=14,
                font_color=COLORS['text_primary'],
                font_family='Inter',
                showarrow=False
            )
        ],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=COLORS['text_primary']),
        margin=dict(l=20, r=20, t=80, b=20),
        showlegend=True,
        legend=dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.05
        )
    )
    
    return fig