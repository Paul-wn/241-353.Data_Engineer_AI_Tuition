import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Sample data based on your CSV structure
sample_data = {
    'university_name': [
        'จุฬาลงกรณ์มหาวิทยาลัย', 'มหาวิทยาลัยเกษตรศาสตร์', 'มหาวิทยาลัยธรรมศาสตร์',
        'มหาวิทยาลัยเชียงใหม่', 'มหาวิทยาลัยขอนแก่น', 'มหาวิทยาลยสงขลานครินทร์',
        'มหาวิทยาลัยมหิดล', 'มหาวิทยาลัยศิลปกรรมศาสตร์', 'มหาวิทยาลัยเทคโนโลยีพระจอมเกล้า',
        'มหาวิทยาลัยราชภัฏ'
    ],
    'faculty': [
        'วิศวกรรมศาสตร์', 'วิศวกรรมศาสตร์', 'วิศวกรรมศาสตร์', 'วิศวกรรมศาสตร์',
        'วิศวกรรมศาสตร์', 'วิศวกรรมศาสตร์', 'วิศวกรรมศาสตร์', 'วิศวกรรมศาสตร์',
        'วิศวกรรมศาสตร์', 'วิศวกรรมศาสตร์'
    ],
    'major_eng': [
        'Computer Engineering', 'Computer Engineering', 'Computer Engineering',
        'Computer Engineering', 'Computer Engineering', 'Computer Engineering',
        'Computer Engineering', 'Computer Engineering', 'Computer Engineering',
        'Computer Engineering'
    ],
    'region': [
        'กรุงเทพฯ', 'กรุงเทพฯ', 'กรุงเทพฯ', 'เชียงใหม่', 'ขอนแก่น', 'สงขลา',
        'กรุงเทพฯ', 'กรุงเทพฯ', 'กรุงเทพฯ', 'ราชบุรี'
    ],
    'tuition_fee': [
        232800, 156000, 184000, 400000, 200000, 156000,
        232800, 101200, 200000, 25000
    ],
    'latitude': [
        13.7367, 13.8462, 14.0697, 18.7883, 16.4419, 7.0087,
        13.7942, 13.7563, 13.7278, 13.5282
    ],
    'longitude': [
        100.5332, 100.5691, 100.6132, 98.9853, 102.8160, 100.4951,
        100.5325, 100.5018, 100.7647, 99.8191
    ]
}

df = pd.DataFrame(sample_data)

# Initialize Dash app
app = dash.Dash(__name__)

# Define pastel colors theme
colors = {
    'background': '#fef7ff',
    'primary': '#b794f6',
    'secondary': '#a9a9a9',
    'success': '#9ae6b4',
    'info': '#90cdf4',
    'warning': '#faf089',
    'danger': '#feb2b2',
    'pink': '#fbb6ce',
    'purple': '#d6bcfa',
    'blue': '#a8e6cf',
    'orange': '#ffd3a5'
}

# Create the layout
app.layout = html.Div([
    html.H1("Thailand University Dashboard", 
            style={'textAlign': 'center', 'marginBottom': '30px', 'color': colors['primary']}),
    
    html.Div([
        # Left section - Map and details
        html.Div([
            # Map section
            html.Div([
                html.H3("Thailand Map of Universities", 
                       style={'textAlign': 'center', 'marginBottom': '20px'}),
                dcc.Graph(
                    id='thailand-map',
                    style={'height': '400px'},
                    config={'displayModeBar': False}
                )
            ], style={
                'border': '3px solid ' + colors['primary'],
                'borderRadius': '20px',
                'padding': '20px',
                'marginBottom': '20px',
                'backgroundColor': 'white',
                'boxShadow': f'0 4px 15px rgba(183, 148, 246, 0.3)'
            }),
            
            # Details section
            html.Div([
                html.H4("University Details", style={'marginBottom': '15px'}),
                html.Div(id='university-details', children=[
                    html.P("Click on a pin to see details", style={'textAlign': 'center', 'color': colors['secondary']})
                ])
            ], style={
                'border': '2px solid ' + colors['pink'],
                'borderRadius': '20px',
                'padding': '20px',
                'backgroundColor': colors['blue'],
                'minHeight': '200px',
                'boxShadow': f'0 4px 10px rgba(183, 148, 246, 0.2)'
            })
        ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        # Right section - Statistics
        html.Div([
            html.H3("Descriptive Statistics", style={'textAlign': 'center', 'marginBottom': '20px'}),
            html.Div(id='statistics-content')
        ], style={
            'width': '33%', 
            'display': 'inline-block', 
            'verticalAlign': 'top',
            'marginLeft': '2%',
            'border': '3px solid ' + colors['purple'],
            'borderRadius': '20px',
            'padding': '20px',
            'backgroundColor': 'white',
            'minHeight': '600px',
            'boxShadow': f'0 4px 15px rgba(214, 188, 250, 0.3)'
        }),
        
    ], style={'margin': '20px'}),
    
    # Bottom section - Regional comparison
    html.Div([
        html.H3("Regional Comparison", style={'textAlign': 'center', 'marginBottom': '20px'}),
        html.P("Tuition fee differences by region (Most expensive, cheapest, and mean)", 
               style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        html.Div([
            dcc.Graph(id='regional-comparison', style={'height': '300px'})
        ])
    ], style={
        'margin': '20px',
        'border': '3px solid ' + colors['pink'],
        'borderRadius': '20px',
        'padding': '20px',
        'backgroundColor': 'white',
        'boxShadow': f'0 4px 15px rgba(251, 182, 206, 0.3)'
    })
    
], style={'backgroundColor': colors['background'], 'minHeight': '100vh', 'padding': '20px'})

# Callback for map
@app.callback(
    Output('thailand-map', 'figure'),
    Input('thailand-map', 'id')
)
def update_map(_):
    # Create a cropped map showing only Thailand using mapbox
    fig = go.Figure()
    
    # Add university markers
    fig.add_trace(go.Scattermapbox(
        lat=df['latitude'],
        lon=df['longitude'],
        mode='markers',
        marker=dict(
            size=18,
            color=colors['danger'],
            opacity=0.9,
            sizemode='diameter'
        ),
        text=df['university_name'],
        hovertemplate='<b>🏫 %{text}</b><br>' +
                     '📍 %{customdata[1]}<br>' +
                     '💰 Tuition: ฿%{customdata[0]:,.0f}<br>' +
                     '<extra></extra>',
        customdata=list(zip(df['tuition_fee'], df['region'])),
        name='Universities'
    ))
    
    # Configure mapbox to show only Thailand (cropped view)
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",  # Free map style
            center=dict(lat=13.0, lon=101.0),  # Center of Thailand
            zoom=5.8,  # Zoom level to fit Thailand perfectly
            # These bounds will crop the map to show only Thailand
            bounds=dict(
                west=97.3,   # Western boundary of Thailand
                east=105.6,  # Eastern boundary of Thailand  
                south=5.6,   # Southern boundary of Thailand
                north=20.4   # Northern boundary of Thailand
            )
        ),
        title={
            'text': "🇹🇭 Thailand Universities Map",
            'x': 0.5,
            'font': {'size': 20, 'color': colors['primary'], 'family': 'Arial Black'}
        },
        height=500,
        margin=dict(l=0, r=0, t=60, b=0),
        showlegend=False,
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary'])
    )
    
    return fig

# Callback for university details
@app.callback(
    Output('university-details', 'children'),
    Input('thailand-map', 'clickData')
)
def update_details(clickData):
    if clickData is None:
        return html.P("🖱️ Click on a university pin to see details", 
                     style={'textAlign': 'center', 'color': colors['secondary'], 'fontSize': '16px'})
    
    point_index = clickData['points'][0]['pointIndex']
    university_data = df.iloc[point_index]
    
    return html.Div([
        html.H5(f"🏛️ {university_data['university_name']}", style={'color': colors['primary'], 'fontSize': '18px'}),
        html.Hr(style={'border': f'1px solid {colors["pink"]}'}),
        html.Div([
            html.Div([
                html.P([html.Strong("🏫 Faculty: ", style={'color': colors['purple']}), university_data['faculty']], 
                       style={'marginBottom': '8px'}),
                html.P([html.Strong("📚 Major: ", style={'color': colors['purple']}), university_data['major_eng']], 
                       style={'marginBottom': '8px'}),
                html.P([html.Strong("🗺️ Region: ", style={'color': colors['purple']}), university_data['region']], 
                       style={'marginBottom': '8px'}),
                html.P([html.Strong("💰 Tuition Fee: ", style={'color': colors['purple']}), f"฿{university_data['tuition_fee']:,.0f}"], 
                       style={'marginBottom': '8px'})
            ], style={'backgroundColor': colors['blue'], 'padding': '15px', 'borderRadius': '15px', 'border': f'2px solid {colors["pink"]}'}),
        ]),
        html.Div([
            html.Div("🎓", style={'fontSize': '60px', 'textAlign': 'center'})
        ], style={'textAlign': 'center', 'marginTop': '20px', 'backgroundColor': colors['warning'], 'padding': '10px', 'borderRadius': '50%', 'width': '80px', 'height': '80px', 'margin': '20px auto', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
    ])

# Callback for statistics
@app.callback(
    Output('statistics-content', 'children'),
    Input('thailand-map', 'id')
)
def update_statistics(_):
    total_universities = len(df)
    avg_tuition = df['tuition_fee'].mean()
    max_tuition = df['tuition_fee'].max()
    min_tuition = df['tuition_fee'].min()
    most_expensive_uni = df[df['tuition_fee'] == max_tuition]['university_name'].iloc[0]
    cheapest_uni = df[df['tuition_fee'] == min_tuition]['university_name'].iloc[0]
    
    # Regional stats
    regional_stats = df.groupby('region')['tuition_fee'].agg(['mean', 'count']).round(0)
    
    return html.Div([
        # General Statistics
        html.Div([
            html.H5("📊 General Statistics", style={'color': colors['info'], 'marginBottom': '15px'}),
            html.Div([
                html.Div([
                    html.P("🏫", style={'fontSize': '24px', 'margin': '0'}),
                    html.P(f"{total_universities}", style={'fontWeight': 'bold', 'fontSize': '20px', 'margin': '0'}),
                    html.P("Universities", style={'fontSize': '12px', 'margin': '0'})
                ], style={'textAlign': 'center', 'backgroundColor': colors['pink'], 'padding': '15px', 'borderRadius': '15px', 'marginBottom': '10px'}),
                
                html.Div([
                    html.P("💰", style={'fontSize': '24px', 'margin': '0'}),
                    html.P(f"฿{avg_tuition:,.0f}", style={'fontWeight': 'bold', 'fontSize': '16px', 'margin': '0'}),
                    html.P("Average Tuition", style={'fontSize': '12px', 'margin': '0'})
                ], style={'textAlign': 'center', 'backgroundColor': colors['blue'], 'padding': '15px', 'borderRadius': '15px', 'marginBottom': '15px'})
            ])
        ]),
        
        # Most Expensive
        html.Div([
            html.H5("💎 Most Expensive", style={'color': colors['danger'], 'marginBottom': '10px'}),
            html.Div([
                html.P(most_expensive_uni, style={'fontSize': '13px', 'marginBottom': '5px', 'fontWeight': '500'}),
                html.P(f"฿{max_tuition:,.0f}", style={'fontWeight': 'bold', 'color': colors['danger'], 'fontSize': '18px', 'margin': '0'})
            ], style={'backgroundColor': colors['orange'], 'padding': '12px', 'borderRadius': '12px', 'marginBottom': '15px'})
        ]),
        
        # Cheapest
        html.Div([
            html.H5("💸 Most Affordable", style={'color': colors['success'], 'marginBottom': '10px'}),
            html.Div([
                html.P(cheapest_uni, style={'fontSize': '13px', 'marginBottom': '5px', 'fontWeight': '500'}),
                html.P(f"฿{min_tuition:,.0f}", style={'fontWeight': 'bold', 'color': colors['success'], 'fontSize': '18px', 'margin': '0'})
            ], style={'backgroundColor': colors['warning'], 'padding': '12px', 'borderRadius': '12px', 'marginBottom': '15px'})
        ]),
        
        # Regional breakdown
        html.Div([
            html.H5("🗺️ By Region", style={'color': colors['primary'], 'marginBottom': '10px'}),
            html.Div([
                html.Div([
                    html.P([html.Strong(f"📍 {region}: ", style={'color': colors['purple']}), 
                           f"฿{stats['mean']:,.0f}", html.Br(), 
                           html.Small(f"({stats['count']} universities)", style={'color': colors['secondary']})])
                ], style={'backgroundColor': colors['pink'], 'padding': '8px', 'borderRadius': '8px', 'marginBottom': '5px'})
                for region, stats in regional_stats.iterrows()
            ])
        ])
    ])

# Callback for regional comparison chart
@app.callback(
    Output('regional-comparison', 'figure'),
    Input('thailand-map', 'id')
)
def update_regional_comparison(_):
    regional_stats = df.groupby('region')['tuition_fee'].agg(['min', 'max', 'mean']).reset_index()
    
    fig = go.Figure()
    
    # Add bars for min, max, mean
    fig.add_trace(go.Bar(
        x=regional_stats['region'],
        y=regional_stats['min'],
        name='Cheapest',
        marker_color=colors['success'],
        marker_line_color=colors['primary'],
        marker_line_width=2
    ))
    
    fig.add_trace(go.Bar(
        x=regional_stats['region'],
        y=regional_stats['max'],
        name='Most Expensive',
        marker_color=colors['danger'],
        marker_line_color=colors['primary'],
        marker_line_width=2
    ))
    
    fig.add_trace(go.Bar(
        x=regional_stats['region'],
        y=regional_stats['mean'],
        name='Average',
        marker_color=colors['info'],
        marker_line_color=colors['primary'],
        marker_line_width=2
    ))
    
    fig.update_layout(
        title={
            'text': "🎨 Tuition Fee Comparison by Region",
            'x': 0.5,
            'font': {'size': 18, 'color': colors['primary']}
        },
        xaxis_title="📍 Region",
        yaxis_title="💰 Tuition Fee (฿)",
        barmode='group',
        height=300,
        margin=dict(l=50, r=50, t=80, b=50),
        paper_bgcolor=colors['background'],
        plot_bgcolor='white',
        font=dict(color=colors['primary']),
        legend=dict(
            bgcolor=colors['pink'],
            bordercolor=colors['primary'],
            borderwidth=2
        )
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)