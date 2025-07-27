import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Load the actual data from CSV
df = pd.read_csv('data/data_via_location_noises.csv')

# Clean and prepare the data
df_clean = df.copy()

# Use the already cleaned tuition fee column
df_clean['final_tuition_fee'] = df_clean['ค่าใช้จ่ายที่ปรับแล้ว']

# Remove rows with missing tuition fee or coordinates
df_clean = df_clean.dropna(subset=['final_tuition_fee', 'latitude', 'longitude'])

# Create a unique identifier for each program entry
df_clean['unique_id'] = df_clean.index.astype(str)

# Create region mapping based on coordinates (rough geographical regions)
def get_region_from_coordinates(lat, lon):
    if lat > 17:  # Northern Thailand
        return 'ภาคเหนือ'
    elif lat > 15 and lon > 103:  # Northeast Thailand
        return 'ภาคอีสาน'
    elif lat < 10:  # Southern Thailand
        return 'ภาคใต้'
    elif lat > 13 and lat <= 15:  # Central Thailand (excluding Bangkok metro)
        return 'ภาคกลาง'
    else:  # Bangkok and vicinity
        return 'กรุงเทพฯและปริมณฑล'

df_clean['region'] = df_clean.apply(lambda row: get_region_from_coordinates(row['latitude'], row['longitude']), axis=1)

# Create program type categorization
def categorize_program(program_name):
    if 'ปัญญาประดิษฐ์' in str(program_name) or 'Artificial Intelligence' in str(program_name) or 'AI' in str(program_name):
        return 'AI Engineering'
    elif 'ระบบอัจฉริยะ' in str(program_name) or 'Intelligence Systems' in str(program_name):
        return 'Intelligent Systems'
    elif 'ดิจิทัล' in str(program_name) or 'Digital' in str(program_name):
        return 'Digital Engineering'
    elif 'ไซเบอร์' in str(program_name) or 'Cyber' in str(program_name):
        return 'Cybersecurity'
    else:
        return 'Computer Engineering'

df_clean['program_type'] = df_clean['หลักสูตร'].apply(categorize_program)

# Initialize Dash app
app = dash.Dash(__name__)

# Define enhanced pastel colors theme
colors = {
    'background': '#fef7ff',
    'primary': '#b794f6',
    'secondary': '#a9a9a9',
    'success': '#48bb78',
    'info': '#4299e1',
    'warning': '#ed8936',
    'danger': '#e53e3e',
    'pink': '#ed64a6',
    'purple': '#9f7aea',
    'blue': '#a8e6cf',
    'orange': '#ffd3a5',
    'teal': '#38b2ac',
    'cyan': '#0bc5ea'
}

# Create the layout
app.layout = html.Div([
    html.H1("🇹🇭 Thailand Computer & AI Engineering Universities Dashboard", 
            style={'textAlign': 'center', 'marginTop': '5px', 'color': colors['primary'], 'fontFamily': 'Arial Black'}),
    
    html.Div([
        # Filter controls
        html.Div([
            html.Div([
                html.Label("🎓 Program Type:", style={'fontWeight': 'bold', 'color': colors['primary']}),
                dcc.Dropdown(
                    id='program-filter',
                    options=[{'label': 'All Programs', 'value': 'all'}] + 
                            [{'label': prog, 'value': prog} for prog in df_clean['program_type'].unique()],
                    value='all',
                    style={'marginTop': '5px'}
                )
            ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),
            
            html.Div([
                html.Label("🗺️ Region:", style={'fontWeight': 'bold', 'color': colors['primary']}),
                dcc.Dropdown(
                    id='region-filter',
                    options=[{'label': 'All Regions', 'value': 'all'}] + 
                            [{'label': region, 'value': region} for region in df_clean['region'].unique()],
                    value='all',
                    style={'marginTop': '5px'}
                )
            ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),
            
            html.Div([
                html.Label("💰 Tuition Range (฿):", style={'fontWeight': 'bold', 'color': colors['primary']}),
                dcc.RangeSlider(
                    id='tuition-slider',
                    min=df_clean['final_tuition_fee'].min(),
                    max=df_clean['final_tuition_fee'].max(),
                    value=[df_clean['final_tuition_fee'].min(), df_clean['final_tuition_fee'].max()],
                    marks={
                        int(df_clean['final_tuition_fee'].min()): f"฿{int(df_clean['final_tuition_fee'].min()/1000)}K",
                        int(df_clean['final_tuition_fee'].max()): f"฿{int(df_clean['final_tuition_fee'].max()/1000)}K"
                    },
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={'width': '35%', 'display': 'inline-block'})
        ], style={
            'backgroundColor': 'white',
            'padding': '20px',
            'marginBottom': '20px',
            'borderRadius': '15px',
            'border': f'2px solid {colors["primary"]}',
            'boxShadow': f'0 4px 15px rgba(183, 148, 246, 0.3)'
        })
    ], style={'margin': '20px'}),
    
    html.Div([
        # Left section - Map and details
        html.Div([
            # Map section
            html.Div([
                dcc.Graph(
                    id='thailand-map',
                    style={'height': '400px', 'width': '100%'},
                    config={
                        'scrollZoom': True,  # <<< ต้องใส่อันนี้ เพื่อให้ scroll mouse zoom ได้
                        'displayModeBar': True  # ถ้าต้องการให้มีปุ่ม zoom/pan บนแผนที่
                            }
                )
            ], style={
                'border': f'2px solid {colors["primary"]}',
                'borderRadius': '20px',
                'padding': '20px',
                'marginRight': '20px',
                'backgroundColor': 'white',
                'boxShadow': f'0 4px 15px rgba(183, 148, 246, 0.3)',
                'flex': '1'  # ให้กินพื้นที่เท่ากับฝั่งขวา
                }),
            
            # Details section
            html.Div([
                html.H4("🏛️ University Details", style={'marginBottom': '15px', 'color': colors['primary']}),
                html.Div(id='university-details', children=[
                    html.P("🖱️ Click on a university pin to see details", 
                        style={'textAlign': 'center', 'color': colors['secondary'], 'fontSize': '16px'})
                    ])
            ], style={
                'border': f'2px solid {colors["primary"]}',
                'borderRadius': '20px',
                'padding': '20px',
                'backgroundColor': 'white',
                'minHeight': '250px',
                'boxShadow': f'0 4px 10px rgba(183, 148, 246, 0.2)',
                'flex': '1'  # ให้กินพื้นที่เท่ากันกับ map
            })
        ], style={'display': 'flex', 'flexDirection': 'row', 'width': '100%', 'marginBottom': '20px'}),
        

    # Container หลัก จัดแนวนอน
    html.Div([
        # Statistics Dashboard (ซ้าย)
        html.Div([
            html.H3("📊 Statistics Dashboard", style={
                'textAlign': 'center',
                'marginBottom': '20px',
                'color': colors['primary']
            }),
            html.Div(id='statistics-content')
        ], style={
            'width': '37%',
            'border': f'3px solid {colors["purple"]}',
            'borderRadius': '20px',
            'padding': '20px',
            'backgroundColor': 'white',
            'minHeight': '750px',
            'boxShadow': f'0 4px 15px rgba(214, 188, 250, 0.3)',
            'display': 'inline-block',
            'verticalAlign': 'top'
        }),

        # Container สำหรับกราฟ 2 อันนี้ (ขวา)
        html.Div([
            # Regional comparison
            html.Div([
                html.H3("🗺️ Regional Analysis", style={
                    'textAlign': 'center',
                    'marginBottom': '20px',
                    'color': colors['primary']
                }),
                dcc.Graph(id='regional-comparison', style={'height': '350px'})
            ], style={
                'width': '100%',
                'border': f'3px solid {colors["pink"]}',
                'borderRadius': '20px',
                'padding': '20px',
                'backgroundColor': 'white',
                'boxShadow': f'0 4px 15px rgba(251, 182, 206, 0.3)',
                'marginBottom': '20px'
            }),

            # Program type distribution
            html.Div([
                html.H3("🎓 Program Distribution", style={
                    'textAlign': 'center',
                    'marginBottom': '20px',
                    'color': colors['primary']
                }),
                dcc.Graph(id='program-distribution', style={'height': '350px'})
            ], style={
                'width': '100%',
                'border': f'3px solid {colors["teal"]}',
                'borderRadius': '20px',
                'padding': '20px',
                'backgroundColor': 'white',
                'boxShadow': f'0 4px 15px rgba(56, 178, 172, 0.3)'
            }),
        ], style={
            'width': '60%',
            'display': 'inline-block',
            'marginLeft': '3%',
            'verticalAlign': 'top',
        }),
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'width': '100%',
        'justifyContent': 'space-between',
        'margin': '20px 0'
    }),
    ], style={
        'backgroundColor': colors['background'],
        'minHeight': '100vh',
        'padding': '20px'
    }),
])

# Helper function to filter dataframe
def filter_dataframe(program_type, region, tuition_range):
    filtered_df = df_clean.copy()
    
    if program_type != 'all':
        filtered_df = filtered_df[filtered_df['program_type'] == program_type]
    
    if region != 'all':
        filtered_df = filtered_df[filtered_df['region'] == region]
    
    filtered_df = filtered_df[
        (filtered_df['final_tuition_fee'] >= tuition_range[0]) &
        (filtered_df['final_tuition_fee'] <= tuition_range[1])
    ]
    
    return filtered_df

# Function to add slight offset to coordinates for overlapping universities
def add_coordinate_offset(df):
    """Add slight random offset to coordinates for universities at the same location"""
    grouped = df.groupby(['latitude', 'longitude'])
    
    result_dfs = []
    for (lat, lon), group in grouped:
        if len(group) > 1:
            # Add small random offsets for overlapping locations
            offsets = np.random.uniform(-0.01, 0.01, size=(len(group), 2))
            group = group.copy()
            group['display_lat'] = lat + offsets[:, 0]
            group['display_lon'] = lon + offsets[:, 1]
        else:
            group = group.copy()
            group['display_lat'] = group['latitude']
            group['display_lon'] = group['longitude']
        result_dfs.append(group)
    
    return pd.concat(result_dfs, ignore_index=True)

# Callback for map
@app.callback(
    Output('thailand-map', 'figure'),
    [Input('program-filter', 'value'),
     Input('region-filter', 'value'),
     Input('tuition-slider', 'value')]
)
def update_map(program_type, region, tuition_range):
    filtered_df = filter_dataframe(program_type, region, tuition_range)
    
    if len(filtered_df) == 0:
        return go.Figure().add_annotation(text="No universities match the selected criteria", x=0.5, y=0.5, showarrow=False)
    
    # Add coordinate offsets for overlapping universities
    filtered_df = add_coordinate_offset(filtered_df)
    
    # Create color mapping for program types
    program_colors = {
        'Computer Engineering': colors['primary'],
        'AI Engineering': colors['danger'],
        'Digital Engineering': colors['info'],
        'Intelligent Systems': colors['warning'],
        'Cybersecurity': colors['success']
    }
    
    fig = go.Figure()
    
    # Add markers for each program type
    for prog_type in filtered_df['program_type'].unique():
        prog_data = filtered_df[filtered_df['program_type'] == prog_type]
        
        fig.add_trace(go.Scattermapbox(
            lat=prog_data['display_lat'],
            lon=prog_data['display_lon'],
            mode='markers',
            marker=dict(
                size=12,
                symbol='circle',
                color=program_colors.get(prog_type, colors['secondary']),
                opacity=0.8,
                sizemode='diameter'
            ),
            text=prog_data['unique_id'],  # Use unique_id instead of university name
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
            style="open-street-map",
            center=dict(lat=13.5, lon=101.0),  # กลางประเทศไทยโดยประมาณ
            zoom=4.8  # ระดับการซูมที่ครอบคลุมประเทศไทย
        ),
        title={
            'text': f"🗺️ Universities Map",
            'x': 0.5,
            'font': {'size': 18, 'color': colors['primary'], 'family': 'Arial Black'}
        },
        height=500,
        margin=dict(l=0, r=0, t=60, b=0),
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary']),
        legend=dict(
            title='📚 Program Type',  # ชื่อหัวข้อ legend
            orientation='v',          # แนวตั้ง (ใช้ 'h' หากต้องการแนวนอน)
            x=0.01,                   # ตำแหน่งซ้าย-ขวา (0 = ซ้ายสุด, 1 = ขวาสุด)
            y=0.99,                   # ตำแหน่งบน-ล่าง (0 = ล่างสุด, 1 = บนสุด)
            bgcolor='rgba(255,255,255,0.8)',  # พื้นหลังโปร่งใสเล็กน้อย
            bordercolor=colors['primary'],
            borderwidth=0.5,
            font=dict(
                size=10,
                color=colors['primary']
            ),
            itemclick='toggleothers',   # คลิกเลือกเฉพาะตัวเดียว
            itemdoubleclick='toggle'    # ดับเบิลคลิกเพื่อแสดง/ซ่อน
        )
)
    
    
    return fig

# Callback for university details
@app.callback(
    Output('university-details', 'children'),
    [Input('thailand-map', 'clickData'),
     Input('program-filter', 'value'),
     Input('region-filter', 'value'),
     Input('tuition-slider', 'value')]
)
def update_details(clickData, program_type, region, tuition_range):
    if clickData is None:
        return html.P("🖱️ Click on a university pin to see details", 
                     style={'textAlign': 'center', 'color': colors['secondary'], 'fontSize': '16px'})
    
    filtered_df = filter_dataframe(program_type, region, tuition_range)
    filtered_df = add_coordinate_offset(filtered_df)
    
    # Find the clicked program using unique_id
    clicked_unique_id = clickData['points'][0]['text']
    try:
        university_data = filtered_df[filtered_df['unique_id'] == clicked_unique_id].iloc[0]
    except IndexError:
        return html.P("Program details not found", 
                     style={'textAlign': 'center', 'color': colors['secondary'], 'fontSize': '16px'})
    
    # Get all programs from the same university for additional context
    same_university_programs = filtered_df[
        filtered_df['มหาวิทยาลัย'] == university_data['มหาวิทยาลัย']
    ]
    
    return html.Div([
        # University header with logo
        html.Div([
            html.Div([
                html.Img(
                    src=university_data['img'],
                    style={
                        'width': '80px', 
                        'height': '80px', 
                        'objectFit': 'contain',
                        'borderRadius': '10px',
                        'border': f'2px solid {colors["primary"]}',
                        'backgroundColor': 'white',
                        'padding': '5px'
                    }
                )
            ], style={'width': '90px', 'display': 'inline-block', 'verticalAlign': 'top'}),
            
            html.Div([
                html.H5(f"🏛️ {university_data['มหาวิทยาลัย']}", 
                        style={'color': colors['primary'], 'fontSize': '16px', 'marginBottom': '5px', 'marginTop': '0px'}),
                html.P([html.Strong("🏢 Campus: ", style={'color': colors['info']}), 
                       university_data['วิทยาเขต']], 
                       style={'marginBottom': '5px', 'fontSize': '14px'}),
                html.P([html.Strong("🗺️ Region: ", style={'color': colors['info']}), 
                       university_data['region']], 
                       style={'marginBottom': '0px', 'fontSize': '14px'})
            ], style={'width': 'calc(100% - 100px)', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': '10px'})
        ], style={'marginBottom': '15px'}),
        
        html.Hr(style={'border': f'1px solid {colors["pink"]}', 'margin': '10px 0'}),
        
        # Selected Program Details (highlighted)
        html.Div([
            html.H6("🎯 Selected Program", style={'color': colors['danger'], 'marginBottom': '10px'}),
            html.Div([
                html.P([html.Strong("📚 Program: ", style={'color': colors['purple']}), 
                       university_data['หลักสูตร']], 
                       style={'marginBottom': '8px', 'fontSize': '14px'}),
                html.P([html.Strong("🌐 English Name: ", style={'color': colors['purple']}), 
                       str(university_data['หลักสูตรEng']) if pd.notna(university_data['หลักสูตรEng']) else 'N/A'], 
                       style={'marginBottom': '8px', 'fontSize': '14px'}),
                html.P([html.Strong("💰 Tuition Fee: ", style={'color': colors['danger']}), 
                       f"฿{university_data['final_tuition_fee']:,.0f}"], 
                       style={'marginBottom': '8px', 'fontSize': '16px', 'fontWeight': 'bold'}),
                html.P([html.Strong("🎓 Faculty: ", style={'color': colors['purple']}), 
                       university_data['คณะ']], 
                       style={'marginBottom': '8px', 'fontSize': '14px'}),
                html.P([html.Strong("📖 Program Type: ", style={'color': colors['purple']}), 
                       university_data['program_type']], 
                       style={'marginBottom': '8px', 'fontSize': '14px'})
            ], style={
                'backgroundColor': colors['orange'], 
                'padding': '15px', 
                'borderRadius': '15px', 
                'border': f'3px solid {colors["danger"]}'
            })
        ], style={'marginBottom': '15px'}),
        
        # Other programs from the same university (if any)
        html.Div([
            html.H6(f"🏫 Other Programs at {university_data['มหาวิทยาลัย'][:20]}{'...' if len(university_data['มหาวิทยาลัย']) > 20 else ''}", 
                   style={'color': colors['info'], 'marginBottom': '10px'}),
            html.Div([
                html.Div([
                    html.P([
                        html.Strong(f"📚 {prog['หลักสูตร'][:30]}{'...' if len(str(prog['หลักสูตร'])) > 30 else ''}", 
                                  style={'color': colors['primary'], 'fontSize': '13px'}),
                        html.Br(),
                        html.Strong(f"💰 ฿{prog['final_tuition_fee']:,.0f}", 
                                  style={'color': colors['success'], 'fontSize': '14px'}),
                        f" | {prog['program_type']}"
                    ])
                ], style={
                    'backgroundColor': colors['blue'], 
                    'padding': '8px', 
                    'borderRadius': '8px', 
                    'marginBottom': '5px',
                    'border': f'1px solid {colors["primary"]}' if prog['unique_id'] != university_data['unique_id'] else f'2px solid {colors["danger"]}'
                })
                for _, prog in same_university_programs.iterrows()
            ])
        ]) if len(same_university_programs) > 1 else html.Div()
    ])

# Callback for statistics
@app.callback(
    Output('statistics-content', 'children'),
    [Input('program-filter', 'value'),
     Input('region-filter', 'value'),
     Input('tuition-slider', 'value')]
)
def update_statistics(program_type, region, tuition_range):
    filtered_df = filter_dataframe(program_type, region, tuition_range)
    
    if len(filtered_df) == 0:
        return html.P("No programs match the selected criteria", 
                     style={'textAlign': 'center', 'color': colors['secondary']})
    
    total_programs = len(filtered_df)
    total_universities = filtered_df['มหาวิทยาลัย'].nunique()
    avg_tuition = filtered_df['final_tuition_fee'].mean()
    max_tuition = filtered_df['final_tuition_fee'].max()
    min_tuition = filtered_df['final_tuition_fee'].min()
    most_expensive_program = filtered_df[filtered_df['final_tuition_fee'] == max_tuition].iloc[0]
    cheapest_program = filtered_df[filtered_df['final_tuition_fee'] == min_tuition].iloc[0]
    
    # Program type distribution
    program_stats = filtered_df['program_type'].value_counts()
    
    return html.Div([
        # General Statistics
        html.Div([
            html.H5("📊 General Statistics", style={'color': colors['info'], 'marginBottom': '15px'}),
            html.Div([
                html.Div([
                    html.P("🏫", style={'fontSize': '20px', 'margin': '0'}),
                    html.P(f"{total_universities}", style={'fontWeight': 'bold', 'fontSize': '18px', 'margin': '0'}),
                    html.P("Universities", style={'fontSize': '11px', 'margin': '0'})
                ], style={'textAlign': 'center', 'backgroundColor': colors['pink'], 'padding': '12px', 'borderRadius': '12px', 'marginBottom': '8px'}),
                
                html.Div([
                    html.P("📚", style={'fontSize': '20px', 'margin': '0'}),
                    html.P(f"{total_programs}", style={'fontWeight': 'bold', 'fontSize': '18px', 'margin': '0'}),
                    html.P("Programs", style={'fontSize': '11px', 'margin': '0'})
                ], style={'textAlign': 'center', 'backgroundColor': colors['teal'], 'padding': '12px', 'borderRadius': '12px', 'marginBottom': '8px'}),
                
                html.Div([
                    html.P("💰", style={'fontSize': '20px', 'margin': '0'}),
                    html.P(f"฿{avg_tuition:,.0f}", style={'fontWeight': 'bold', 'fontSize': '14px', 'margin': '0'}),
                    html.P("Average Tuition", style={'fontSize': '11px', 'margin': '0'})
                ], style={'textAlign': 'center', 'backgroundColor': colors['blue'], 'padding': '12px', 'borderRadius': '12px', 'marginBottom': '15px'})
            ])
        ]),
        
        # Most Expensive
        html.Div([
            html.H5("💎 Most Expensive", style={'color': colors['danger'], 'marginBottom': '10px'}),
            html.Div([
                html.P(f"{most_expensive_program['มหาวิทยาลัย'][:25]}{'...' if len(most_expensive_program['มหาวิทยาลัย']) > 25 else ''}", 
                      style={'fontSize': '12px', 'marginBottom': '3px', 'fontWeight': '500'}),
                html.P(f"{most_expensive_program['หลักสูตร'][:30]}{'...' if len(str(most_expensive_program['หลักสูตร'])) > 30 else ''}", 
                      style={'fontSize': '11px', 'marginBottom': '5px', 'color': colors['purple']}),
                html.P(f"฿{max_tuition:,.0f}", style={'fontWeight': 'bold', 'color': colors['danger'], 'fontSize': '16px', 'margin': '0'})
            ], style={'backgroundColor': colors['orange'], 'padding': '10px', 'borderRadius': '10px', 'marginBottom': '15px'})
        ]),
        
        # Cheapest
        html.Div([
            html.H5("💸 Most Affordable", style={'color': colors['success'], 'marginBottom': '10px'}),
            html.Div([
                html.P(f"{cheapest_program['มหาวิทยาลัย'][:25]}{'...' if len(cheapest_program['มหาวิทยาลัย']) > 25 else ''}", 
                      style={'fontSize': '12px', 'marginBottom': '3px', 'fontWeight': '500'}),
                html.P(f"{cheapest_program['หลักสูตร'][:30]}{'...' if len(str(cheapest_program['หลักสูตร'])) > 30 else ''}", 
                      style={'fontSize': '11px', 'marginBottom': '5px', 'color': colors['purple']}),
                html.P(f"฿{min_tuition:,.0f}", style={'fontWeight': 'bold', 'color': colors['success'], 'fontSize': '16px', 'margin': '0'})
            ], style={'backgroundColor': colors['warning'], 'padding': '10px', 'borderRadius': '10px', 'marginBottom': '15px'})
        ]),
        
        # Program type breakdown
        html.Div([
            html.H5("🎓 Program Types", style={'color': colors['primary'], 'marginBottom': '10px'}),
            html.Div([
                html.Div([
                    html.P([html.Strong(f"📚 {prog_type}: ", style={'color': colors['purple']}), 
                           f"{count} programs"])
                ], style={'backgroundColor': colors['pink'], 'padding': '6px', 'borderRadius': '6px', 'marginBottom': '4px', 'fontSize': '13px'})
                for prog_type, count in program_stats.items()
            ])
        ])
    ])

# Callback for regional comparison chart
@app.callback(
    Output('regional-comparison', 'figure'),
    [Input('program-filter', 'value'),
     Input('region-filter', 'value'),
     Input('tuition-slider', 'value')]
)
def update_regional_comparison(program_type, region, tuition_range):
    filtered_df = filter_dataframe(program_type, region, tuition_range)
    
    if len(filtered_df) == 0:
        return go.Figure().add_annotation(text="No data available", x=0.5, y=0.5, showarrow=False)
    
    regional_stats = filtered_df.groupby('region')['final_tuition_fee'].agg(['min', 'max', 'mean', 'count']).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=regional_stats['region'],
        y=regional_stats['min'],
        name='Cheapest',
        marker_color=colors['success'],
        text=regional_stats['min'].apply(lambda x: f"฿{x:,.0f}"),
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        x=regional_stats['region'],
        y=regional_stats['max'],
        name='Most Expensive',
        marker_color=colors['danger'],
        text=regional_stats['max'].apply(lambda x: f"฿{x:,.0f}"),
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        x=regional_stats['region'],
        y=regional_stats['mean'],
        name='Average',
        marker_color=colors['info'],
        text=regional_stats['mean'].apply(lambda x: f"฿{x:,.0f}"),
        textposition='auto'
    ))
    
    fig.update_layout(
        title="💰 Tuition Fee Analysis by Region",
        xaxis_title="Region",
        yaxis_title="Tuition Fee (฿)",
        barmode='group',
        height=350,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color=colors['primary'])
    )
    
    return fig

# Callback for program distribution chart
@app.callback(
    Output('program-distribution', 'figure'),
    [Input('program-filter', 'value'),
     Input('region-filter', 'value'),
     Input('tuition-slider', 'value')]
)
def update_program_distribution(program_type, region, tuition_range):
    filtered_df = filter_dataframe(program_type, region, tuition_range)
    
    if len(filtered_df) == 0:
        return go.Figure().add_annotation(text="No data available", x=0.5, y=0.5, showarrow=False)
    
    program_counts = filtered_df['program_type'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=program_counts.index,
        values=program_counts.values,
        hole=0.4,
        marker_colors=[colors['primary'], colors['danger'], colors['info'], colors['warning'], colors['success']]
    )])
    
    fig.update_layout(
        title="📊 Distribution of Program Types",
        height=350,
        paper_bgcolor='white',
        font=dict(color=colors['primary'])
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)