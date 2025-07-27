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
    # Northern Thailand (ภาคเหนือ)
    if lat >= 17.0:
        return 'ภาคเหนือ'
    
    # Northeast Thailand (ภาคอีสาน)
    elif lat >= 14.0 and lon >= 101.5:
        return 'ภาคอีสาน'
    
    # Southern Thailand (ภาคใต้)
    elif lat <= 11.0:
        return 'ภาคใต้'
    
    # Bangkok Metropolitan Area (กรุงเทพฯและปริมณฑล)
    elif lat >= 13.5 and lat <= 14.5 and lon >= 100.2 and lon <= 101.2:
        return 'กรุงเทพฯและปริมณฑล'
    
    # Central Thailand (ภาคกลาง) - รวมตะวันตก, ตะวันออก, กลาง
    else:
        return 'ภาคกลาง'

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
app = dash.Dash(__name__, external_stylesheets=['assets/custom.css'])

# Enhanced modern color palette with gradients
colors = {
    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'surface': 'rgba(255, 255, 255, 0.95)',
    'surface_dark': 'rgba(255, 255, 255, 0.08)',
    'primary': '#6366f1',
    'primary_light': '#818cf8',
    'secondary': '#64748b',
    'accent': '#f59e0b',
    'success': '#10b981',
    'danger': '#ef4444',
    'warning': '#f59e0b',
    'info': '#3b82f6',
    'pink': '#ec4899',
    'purple': '#8b5cf6',
    'teal': '#14b8a6',
    'orange': '#f97316',
    'cyan': '#06b6d4',
    'emerald': '#059669',
    'rose': '#f43f5e',
    'text_primary': '#1f2937',
    'text_secondary': '#6b7280',
    'text_light': '#9ca3af'
}

# Create the layout with enhanced styling
app.layout = html.Div([

    # Main container with gradient background
    html.Div([
        # Header section with enhanced styling
        html.Div([
            html.H1([
                html.Span("🇹🇭", className="cute-emoji", style={'marginRight': '12px'}),
                html.Span("Thailand Computer & AI Engineering"),
                html.Br(),
                html.Span("Universities Dashboard", 
                         style={'fontSize': '28px', 'fontWeight': '600'})
            ], style={
                'textAlign': 'center',
                'margin': '0 0 32px 0',
                'fontSize': '36px',
                'fontWeight': '800',
                'letterSpacing': '-0.02em',
                'lineHeight': '1.2'
            }),
            
            html.P([
                "Discover the perfect Computer Science & AI Engineering program for your future ",
                html.Span("✨", className="cute-emoji")
            ], style={
                'textAlign': 'center',
                'color': 'rgba(255, 255, 255, 0.9)',
                'fontSize': '18px',
                'fontWeight': '400',
                'marginBottom': '40px',
                'maxWidth': '600px',
                'margin': '0 auto 40px auto'
            })
        ], className="fade-in"),
        
        # Enhanced filter controls
        html.Div([
            html.Div([
                # Program filter
                html.Div([
                    html.Label([
                        html.Span("🎓", style={'marginRight': '8px'}),
                        "Program Type"
                    ], style={
                        'fontWeight': '600', 
                        'color': colors['text_primary'],
                        'fontSize': '14px',
                        'marginBottom': '8px',
                        'display': 'block'
                    }),
                    dcc.Dropdown(
                        id='program-filter',
                        options=[{'label': '✨ All Programs', 'value': 'all'}] + 
                                [{'label': f'📚 {prog}', 'value': prog} for prog in df_clean['program_type'].unique()],
                        value='all',
                        style={
                            'borderRadius': '12px',
                            'border': 'none',
                            'fontSize': '14px',
                        },
                        className='modern-dropdown',maxHeight=150 , optionHeight=30 
                    )
                ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '3%'}),
                
                # Region filter
                html.Div([
                    html.Label([
                        html.Span("🗺️", style={'marginRight': '8px'}),
                        "Region"
                    ], style={
                        'fontWeight': '600', 
                        'color': colors['text_primary'],
                        'fontSize': '14px',
                        'marginBottom': '8px',
                        'display': 'block'
                    }),
                    dcc.Dropdown(
                        id='region-filter',
                        options=[{'label': '🌍 All Regions', 'value': 'all'}] + 
                                [{'label': f'📍 {region}', 'value': region} for region in df_clean['region'].unique()],
                        value='all',
                        style={
                            'borderRadius': '12px',
                            'border': 'none',
                            'fontSize': '14px'
                        },className='modern-dropdown',maxHeight=150 , optionHeight=30 
                    )
                ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '3%'}),
                
                # Tuition range slider
                html.Div([
                    html.Label([
                        html.Span("💰", style={'marginRight': '8px'}),
                        "Tuition Range (฿)"
                    ], style={
                        'fontWeight': '600', 
                        'color': colors['text_primary'],
                        'fontSize': '14px',
                        'marginBottom': '16px',
                        'display': 'block'
                    }),
                    dcc.RangeSlider(
                        id='tuition-slider',
                        min=df_clean['final_tuition_fee'].min(),
                        max=df_clean['final_tuition_fee'].max(),
                        value=[df_clean['final_tuition_fee'].min(), df_clean['final_tuition_fee'].max()],
                        marks={
                            int(df_clean['final_tuition_fee'].min()): {
                                'label': f"฿{int(df_clean['final_tuition_fee'].min()/1000)}K",
                                'style': {'color': colors['text_secondary'], 'fontSize': '12px', 'fontWeight': '500'}
                            },
                            int(df_clean['final_tuition_fee'].max()): {
                                'label': f"฿{int(df_clean['final_tuition_fee'].max()/1000)}K",
                                'style': {'color': colors['text_secondary'], 'fontSize': '12px', 'fontWeight': '500'}
                            }
                        },
                        tooltip={"placement": "bottom", "always_visible": True},
                        className='modern-slider'
                    )
                ], style={'width': '34%', 'display': 'inline-block'})
            ], style={
                'padding': '32px',
                'marginBottom': '32px',
                'borderRadius': '24px',
                'background': 'rgba(255, 255, 255, 0.15)',
                'backdropFilter': 'blur(20px)',
                'border': '1px solid rgba(255, 255, 255, 0.2)',
                'boxShadow': '0 8px 32px rgba(31, 38, 135, 0.2)',
                'overflow': 'visible',
                'position': 'relative',
                'zIndex': '1000'
            })
        ], className="fade-in"),
        
        # Main content area
        html.Div([
            # Map and details row
            html.Div([
                # Interactive map
                html.Div([
                    html.Div([
                        html.H3([
                            html.Span("🗺️", style={'marginRight': '12px'}),
                            "Interactive Universities Map"
                        ], style={
                            'color': colors['text_primary'],
                            'fontSize': '20px',
                            'fontWeight': '700',
                            'marginBottom': '20px',
                            'textAlign': 'center'
                        }),
                        dcc.Graph(
                            id='thailand-map',
                            style={'height': '450px', 'borderRadius': '16px'},
                            config={
                                'scrollZoom': True,
                                'displayModeBar': True,
                                'displaylogo': False,
                                'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                            }
                        )
                    ], style={
                        'background': 'rgba(255, 255, 255, 0.25)',
                        'backdropFilter': 'blur(10px)',
                        'borderRadius': '20px',
                        'border': '1px solid rgba(255, 255, 255, 0.3)',
                        'boxShadow': '0 8px 32px rgba(31, 38, 135, 0.37)',
                        'padding': '24px',
                        'transition': 'all 0.3s ease'
                    })
                ], style={'width': '58%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                
                # University details
                html.Div([
                    html.Div([
                        html.H3([
                            html.Span("🏛️", style={'marginRight': '12px'}),
                            "University Details"
                        ], style={
                            'color': colors['text_primary'],
                            'fontSize': '20px',
                            'fontWeight': '700',
                            'marginBottom': '20px',
                            'textAlign': 'center'
                        }),
                        html.Div(id='university-details', children=[
                            html.Div([
                                html.Div("🖱️", style={
                                    'fontSize': '48px',
                                    'textAlign': 'center',
                                    'marginBottom': '16px',
                                    'opacity': '0.6'
                                }),
                                html.P("Click on any university pin to explore detailed information", 
                                       style={
                                           'textAlign': 'center',
                                           'color': colors['text_secondary'],
                                           'fontSize': '16px',
                                           'fontWeight': '500',
                                           'lineHeight': '1.5'
                                       })
                            ], style={
                                'display': 'flex',
                                'flexDirection': 'column',
                                'justifyContent': 'center',
                                'alignItems': 'center',
                                'height': '300px'
                            })
                        ])
                    ], style={
                        'background': 'rgba(255, 255, 255, 0.25)',
                        'backdropFilter': 'blur(10px)',
                        'borderRadius': '20px',
                        'border': '1px solid rgba(255, 255, 255, 0.3)',
                        'boxShadow': '0 8px 32px rgba(31, 38, 135, 0.37)',
                        'padding': '24px',
                        'minHeight': '500px',
                        'transition': 'all 0.3s ease'
                    })
                ], style={'width': '40%', 'display': 'inline-block', 'marginLeft': '2%', 'verticalAlign': 'top'})
            ], style={'marginBottom': '32px'}),
            
            # Analytics row
            html.Div([
                # Statistics dashboard
                html.Div([
                    html.Div([
                        html.H3([
                            html.Span("📊", style={'marginRight': '12px'}),
                            "Quick Stats"
                        ], style={
                            'color': colors['text_primary'],
                            'fontSize': '20px',
                            'fontWeight': '700',
                            'marginBottom': '24px',
                            'textAlign': 'center'
                        }),
                        html.Div(id='statistics-content')
                    ], style={
                        'background': 'rgba(255, 255, 255, 0.25)',
                        'backdropFilter': 'blur(10px)',
                        'borderRadius': '20px',
                        'border': '1px solid rgba(255, 255, 255, 0.3)',
                        'boxShadow': '0 8px 32px rgba(31, 38, 135, 0.37)',
                        'padding': '24px',
                        'minHeight': '750px',
                        'transition': 'all 0.3s ease'
                    })
                ], style={'width': '35%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                
                # Charts section
                html.Div([
                    # Regional analysis
                    html.Div([
                        html.Div([
                            html.H3([
                                html.Span("🌍", style={'marginRight': '12px'}),
                                "Regional Analysis"
                            ], style={
                                'color': colors['text_primary'],
                                'fontSize': '20px',
                                'fontWeight': '700',
                                'marginBottom': '20px',
                                'textAlign': 'center'
                            }),
                            dcc.Graph(id='regional-comparison', style={'height': '350px'})
                        ], style={
                            'background': 'rgba(255, 255, 255, 0.25)',
                            'backdropFilter': 'blur(10px)',
                            'borderRadius': '20px',
                            'border': '1px solid rgba(255, 255, 255, 0.3)',
                            'boxShadow': '0 8px 32px rgba(31, 38, 135, 0.37)',
                            'padding': '24px',
                            'marginBottom': '20px',
                            'transition': 'all 0.3s ease'
                        })
                    ]),
                    
                    # Program distribution
                    html.Div([
                        html.Div([
                            html.H3([
                                html.Span("📚", style={'marginRight': '12px'}),
                                "Program Distribution"
                            ], style={
                                'color': colors['text_primary'],
                                'fontSize': '20px',
                                'fontWeight': '700',
                                'marginBottom': '20px',
                                'textAlign': 'center'
                            }),
                            dcc.Graph(id='program-distribution', style={'height': '350px'})
                        ], style={
                            'background': 'rgba(255, 255, 255, 0.25)',
                            'backdropFilter': 'blur(10px)',
                            'borderRadius': '20px',
                            'border': '1px solid rgba(255, 255, 255, 0.3)',
                            'boxShadow': '0 8px 32px rgba(31, 38, 135, 0.37)',
                            'padding': '24px',
                            'transition': 'all 0.3s ease'
                        })
                    ])
                ], style={'width': '63%', 'display': 'inline-block', 'marginLeft': '2%', 'verticalAlign': 'top'})
            ])
        ], className="fade-in")
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'minHeight': '100vh',
        'padding': '40px 20px',
        'fontFamily': "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
    })
], style={'margin': '0', 'padding': '0'})

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

# Enhanced callback for map with modern styling
@app.callback(
    Output('thailand-map', 'figure'),
    [Input('program-filter', 'value'),
     Input('region-filter', 'value'),
     Input('tuition-slider', 'value')]
)
def update_map(program_type, region, tuition_range):
    filtered_df = filter_dataframe(program_type, region, tuition_range)
    
    if len(filtered_df) == 0:
        return go.Figure().add_annotation(
            text="No universities match the selected criteria",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=colors['text_secondary'])
        )
    
    # Add coordinate offsets for overlapping universities
    filtered_df = add_coordinate_offset(filtered_df)
    
    # Enhanced color mapping for program types
    program_colors = {
        'Computer Engineering': colors['primary'],
        'AI Engineering': colors['danger'],
        'Digital Engineering': colors['info'],
        'Intelligent Systems': colors['warning'],
        'Cybersecurity': colors['success']
    }
    
    fig = go.Figure()
    
    # Add markers for each program type with enhanced styling
    for prog_type in filtered_df['program_type'].unique():
        prog_data = filtered_df[filtered_df['program_type'] == prog_type]
        
        fig.add_trace(go.Scattermapbox(
            lat=prog_data['display_lat'],
            lon=prog_data['display_lon'],
            mode='markers',
            marker=dict(
                size=14,
                symbol='circle',
                color=program_colors.get(prog_type, colors['secondary']),
                opacity=0.9,
                sizemode='diameter',
                # line=dict(width=2, color='white')
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
            style="carto-positron",
            center=dict(lat=13.5, lon=101.0),
            zoom=4.8
        ),
        height=450,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text_primary'], family="Inter"),
        legend=dict(
            title=dict(text='Program Types', font=dict(size=14, color=colors['text_primary'])),
            orientation='v',
            x=0.02,
            y=0.98,
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='rgba(255,255,255,0.5)',
            borderwidth=1,
            font=dict(size=12, color=colors['text_primary']),
            itemclick='toggleothers',
            itemdoubleclick='toggle'
        )
    )
    
    return fig

# Enhanced callback for university details with complete cute styling
@app.callback(
    Output('university-details', 'children'),
    [Input('thailand-map', 'clickData'),
     Input('program-filter', 'value'),
     Input('region-filter', 'value'),
     Input('tuition-slider', 'value')]
)
def update_details(clickData, program_type, region, tuition_range):
    if clickData is None:
        return html.Div([
            html.Div("🖱️", style={
                'fontSize': '48px',
                'textAlign': 'center',
                'marginBottom': '16px',
                'opacity': '0.6'
            }),
            html.P("Click on any university pin to explore detailed information", 
                   style={
                       'textAlign': 'center',
                       'color': colors['text_secondary'],
                       'fontSize': '16px',
                       'fontWeight': '500',
                       'lineHeight': '1.5'
                   }),
            html.Div([
                html.Span("✨", style={'fontSize': '20px', 'margin': '0 8px'}),
                html.Span("🎓", style={'fontSize': '20px', 'margin': '0 8px'}),
                html.Span("🌟", style={'fontSize': '20px', 'margin': '0 8px'}),
            ], style={'textAlign': 'center', 'marginTop': '16px', 'opacity': '0.7'})
        ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center',
            'alignItems': 'center',
            'height': '300px'
        })
    
    filtered_df = filter_dataframe(program_type, region, tuition_range)
    filtered_df = add_coordinate_offset(filtered_df)
    
    # Find the clicked program using unique_id
    clicked_unique_id = clickData['points'][0]['text']
    try:
        university_data = filtered_df[filtered_df['unique_id'] == clicked_unique_id].iloc[0]
    except IndexError:
        return html.P("Program details not found", 
                     style={'textAlign': 'center', 'color': colors['text_secondary'], 'fontSize': '16px'})
    
    # Get all programs from the same university for additional context
    same_university_programs = filtered_df[
        filtered_df['มหาวิทยาลัย'] == university_data['มหาวิทยาลัย']
    ]
    
    return html.Div([
        # University header with enhanced styling
        html.Div([
            html.Div([
                html.Img(
                    src=university_data.get('img', '/assets/default-university.png'),
                    style={
                        'width': '80px', 
                        'height': '80px', 
                        'objectFit': 'contain',
                        'borderRadius': '16px',
                        'border': f'3px solid {colors["primary"]}',
                        'backgroundColor': 'white',
                        'padding': '8px',
                        'boxShadow': '0 4px 16px rgba(99, 102, 241, 0.3)'
                    }
                )
            ], style={'textAlign': 'center', 'marginBottom': '16px'}),
            
            html.H4([
                html.Span("🏛️ ", style={'marginRight': '8px'}),
                university_data['มหาวิทยาลัย']
            ], style={
                'textAlign': 'center',
                'color': colors['text_primary'],
                'fontSize': '18px',
                'fontWeight': '700',
                'marginBottom': '8px',
                'lineHeight': '1.3'
            }),
            
            html.P([
                html.Span("📍 ", style={'marginRight': '4px'}),
                university_data['วิทยาเขต']
            ], style={
                'textAlign': 'center',
                'color': colors['text_secondary'],
                'fontSize': '14px',
                'fontWeight': '500',
                'marginBottom': '16px'
            }),
            
            # Program type badge
            html.Div([
                html.Span(university_data['program_type'], className="university-badge")
            ], style={'textAlign': 'center', 'marginBottom': '16px'})
        ]),
        
        # Program details section
        html.Div([
            html.H5([
                html.Span("🎓 ", style={'marginRight': '8px'}),
                "Program Details"
            ], style={
                'color': colors['text_primary'],
                'fontSize': '16px',
                'fontWeight': '600',
                'marginBottom': '12px'
            }),
            
            html.P(university_data['หลักสูตร'], style={
                'color': colors['text_secondary'],
                'fontSize': '14px',
                'fontWeight': '500',
                'lineHeight': '1.4',
                'marginBottom': '16px',
                'padding': '12px',
                'backgroundColor': 'rgba(255,255,255,0.3)',
                'borderRadius': '12px',
                'border': '1px solid rgba(255,255,255,0.2)'
            })
        ]),
        
        # Tuition information with enhanced styling
        html.Div([
            html.H5([
                html.Span("💰 ", style={'marginRight': '8px'}),
                "Tuition Fee"
            ], style={
                'color': colors['text_primary'],
                'fontSize': '16px',
                'fontWeight': '600',
                'marginBottom': '12px'
            }),
            
            html.Div([
                html.Span("฿", style={
                    'fontSize': '18px',
                    'color': colors['warning'],
                    'fontWeight': '600'
                }),
                html.Span(f"{university_data['final_tuition_fee']:,.0f}", 
                          className="tuition-highlight",
                          style={'marginLeft': '4px'})
            ], style={
                'textAlign': 'center',
                'padding': '16px',
                'backgroundColor': 'rgba(245, 158, 11, 0.1)',
                'borderRadius': '16px',
                'border': '2px solid rgba(245, 158, 11, 0.3)',
                'marginBottom': '16px'
            })
        ]),
        
        # Additional programs at same university
        html.Div([
            html.H5([
                html.Span("📚 ", style={'marginRight': '8px'}),
                f"Other Programs ({len(same_university_programs)} total)"
            ], style={
                'color': colors['text_primary'],
                'fontSize': '16px',
                'fontWeight': '600',
                'marginBottom': '12px'
            }) if len(same_university_programs) > 1 else None,
            
            html.Div([
                html.Div([
                    html.Span(prog_type, style={
                        'fontSize': '12px',
                        'fontWeight': '600',
                        'color': 'white',
                        'backgroundColor': colors['info'],
                        'padding': '4px 8px',
                        'borderRadius': '12px',
                        'margin': '2px',
                        'display': 'inline-block'
                    })
                    for prog_type in same_university_programs['program_type'].unique()
                ])
            ]) if len(same_university_programs) > 1 else None
        ]),
        
        # Quick stats for this university
        html.Div([
            html.Div([
                html.Div([
                    html.Span("🌍", style={'fontSize': '16px', 'marginBottom': '4px'}),
                    html.Br(),
                    html.Span("Region", style={
                        'fontSize': '12px',
                        'color': colors['text_secondary'],
                        'fontWeight': '500'
                    }),
                    html.Br(),
                    html.Span(university_data['region'], style={
                        'fontSize': '14px',
                        'fontWeight': '600',
                        'color': colors['text_primary']
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '12px',
                    'backgroundColor': 'rgba(255,255,255,0.2)',
                    'borderRadius': '12px',
                    'flex': '1',
                    'margin': '0 4px'
                }),
                
                html.Div([
                    html.Span("📊", style={'fontSize': '16px', 'marginBottom': '4px'}),
                    html.Br(),
                    html.Span("Rank", style={
                        'fontSize': '12px',
                        'color': colors['text_secondary'],
                        'fontWeight': '500'
                    }),
                    html.Br(),
                    html.Span(f"#{university_data.name + 1}", style={
                        'fontSize': '14px',
                        'fontWeight': '600',
                        'color': colors['text_primary']
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '12px',
                    'backgroundColor': 'rgba(255,255,255,0.2)',
                    'borderRadius': '12px',
                    'flex': '1',
                    'margin': '0 4px'
                })
            ], style={
                'display': 'flex',
                'marginTop': '16px'
            })
        ])
    ], style={'overflowY': 'auto', 'maxHeight': '400px'})

# Enhanced callback for statistics with cute metrics
@app.callback(
    Output('statistics-content', 'children'),
    [Input('program-filter', 'value'),
     Input('region-filter', 'value'),
     Input('tuition-slider', 'value')]
)
def update_statistics(program_type, region, tuition_range):
    filtered_df = filter_dataframe(program_type, region, tuition_range)
    
    if len(filtered_df) == 0:
        return html.Div([
            html.P("🔍 No data available for selected filters", 
                   style={'textAlign': 'center', 'color': colors['text_secondary']})
        ])
    
    # Calculate statistics
    total_programs = len(filtered_df)
    total_universities = filtered_df['มหาวิทยาลัย'].nunique()
    avg_tuition = filtered_df['final_tuition_fee'].mean()
    min_tuition = filtered_df['final_tuition_fee'].min()
    max_tuition = filtered_df['final_tuition_fee'].max()
    regions_count = filtered_df['region'].nunique()
    
    return html.Div([
        # Main metrics
        html.Div([
            # Total Programs
            html.Div([
                html.Div([
                    html.Span("🎓", style={'fontSize': '24px', 'marginBottom': '8px'}),
                    html.Br(),
                    html.Span(f"{total_programs}", className="metric-number", 
                              style={'fontSize': '32px', 'display': 'block', 'marginBottom': '4px'}),
                    html.Span("Programs", style={
                        'fontSize': '14px',
                        'color': colors['text_secondary'],
                        'fontWeight': '600'
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '20px',
                    'backgroundColor': 'rgba(255,255,255,0.9)',
                    'borderRadius': '16px',
                    'boxShadow': '0 4px 20px rgba(0,0,0,0.1)',
                    'transition': 'all 0.3s ease',
                    'cursor': 'pointer',
                    'marginBottom': '16px'
                }, className="stat-card")
            ]),
            
            # Total Universities
            html.Div([
                html.Div([
                    html.Span("🏛️", style={'fontSize': '24px', 'marginBottom': '8px'}),
                    html.Br(),
                    html.Span(f"{total_universities}", className="metric-number",
                              style={'fontSize': '32px', 'display': 'block', 'marginBottom': '4px'}),
                    html.Span("Universities", style={
                        'fontSize': '14px',
                        'color': colors['text_secondary'],
                        'fontWeight': '600'
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '20px',
                    'backgroundColor': 'rgba(255,255,255,0.9)',
                    'borderRadius': '16px',
                    'boxShadow': '0 4px 20px rgba(0,0,0,0.1)',
                    'transition': 'all 0.3s ease',
                    'cursor': 'pointer',
                    'marginBottom': '16px'
                }, className="stat-card")
            ]),
            
            # Average Tuition
            html.Div([
                html.Div([
                    html.Span("💰", style={'fontSize': '24px', 'marginBottom': '8px'}),
                    html.Br(),
                    html.Span(f"฿{avg_tuition:,.0f}", className="metric-number",
                              style={'fontSize': '24px', 'display': 'block', 'marginBottom': '4px'}),
                    html.Span("Avg. Tuition", style={
                        'fontSize': '14px',
                        'color': colors['text_secondary'],
                        'fontWeight': '600'
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '20px',
                    'backgroundColor': 'rgba(255,255,255,0.9)',
                    'borderRadius': '16px',
                    'boxShadow': '0 4px 20px rgba(0,0,0,0.1)',
                    'transition': 'all 0.3s ease',
                    'cursor': 'pointer',
                    'marginBottom': '16px'
                }, className="stat-card")
            ]),
            
            # Regions Count
            html.Div([
                html.Div([
                    html.Span("🌍", style={'fontSize': '24px', 'marginBottom': '8px'}),
                    html.Br(),
                    html.Span(f"{regions_count}", className="metric-number",
                              style={'fontSize': '32px', 'display': 'block', 'marginBottom': '4px'}),
                    html.Span("Regions", style={
                        'fontSize': '14px',
                        'color': colors['text_secondary'],
                        'fontWeight': '600'
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '20px',
                    'backgroundColor': 'rgba(255,255,255,0.9)',
                    'borderRadius': '16px',
                    'boxShadow': '0 4px 20px rgba(0,0,0,0.1)',
                    'transition': 'all 0.3s ease',
                    'cursor': 'pointer',
                    'marginBottom': '16px'
                }, className="stat-card")
            ])
        ]),
        
        # Tuition range insights
        html.Div([
            html.H5([
                html.Span("📊 ", style={'marginRight': '8px'}),
                "Tuition Insights"
            ], style={
                'color': colors['text_primary'],
                'fontSize': '16px',
                'fontWeight': '700',
                'marginBottom': '16px',
                'textAlign': 'center'
            }),
            
            # Min tuition
            html.Div([
                html.Span("🔻 Lowest: ", style={
                    'fontSize': '14px',
                    'fontWeight': '600',
                    'color': colors['success']
                }),
                html.Span(f"฿{min_tuition:,.0f}", style={
                    'fontSize': '14px',
                    'fontWeight': '700',
                    'color': colors['text_primary']
                })
            ], style={
                'padding': '12px',
                'backgroundColor': 'rgba(16, 185, 129, 0.1)',
                'borderRadius': '12px',
                'marginBottom': '8px',
                'border': '1px solid rgba(16, 185, 129, 0.2)'
            }),
            
            # Max tuition
            html.Div([
                html.Span("🔺 Highest: ", style={
                    'fontSize': '14px',
                    'fontWeight': '600',
                    'color': colors['danger']
                }),
                html.Span(f"฿{max_tuition:,.0f}", style={
                    'fontSize': '14px',
                    'fontWeight': '700',
                    'color': colors['text_primary']
                })
            ], style={
                'padding': '12px',
                'backgroundColor': 'rgba(239, 68, 68, 0.1)',
                'borderRadius': '12px',
                'marginBottom': '16px',
                'border': '1px solid rgba(239, 68, 68, 0.2)'
            })
        ]),
        
        # Top universities by program count
        html.Div([
            html.H5([
                html.Span("🏆 ", style={'marginRight': '8px'}),
                "Top Universities"
            ], style={
                'color': colors['text_primary'],
                'fontSize': '16px',
                'fontWeight': '700',
                'marginBottom': '16px',
                'textAlign': 'center'
            }),
            
            html.Div([
                html.Div([
                    html.Span(f"#{idx + 1}", style={
                        'fontSize': '12px',
                        'fontWeight': '700',
                        'color': colors['primary'],
                        'marginRight': '8px'
                    }),
                    html.Span(uni, style={
                        'fontSize': '12px',
                        'fontWeight': '600',
                        'color': colors['text_primary']
                    }),
                    html.Br(),
                    html.Span(f"{count} programs", style={
                        'fontSize': '11px',
                        'color': colors['text_secondary'],
                        'fontWeight': '500'
                    })
                ], style={
                    'padding': '8px 12px',
                    'backgroundColor': 'rgba(255,255,255,0.6)',
                    'borderRadius': '8px',
                    'marginBottom': '8px',
                    'border': '1px solid rgba(255,255,255,0.3)'
                })
                for idx, (uni, count) in enumerate(
                    filtered_df['มหาวิทยาลัย'].value_counts().head(3).items()
                )
            ])
        ])
    ])

# Enhanced callback for regional comparison chart
@app.callback(
    Output('regional-comparison', 'figure'),
    [Input('program-filter', 'value'),
     Input('region-filter', 'value'),
     Input('tuition-slider', 'value')]
)
def update_regional_chart(program_type, region, tuition_range):
    filtered_df = filter_dataframe(program_type, region, tuition_range)
    
    if len(filtered_df) == 0:
        return go.Figure().add_annotation(
            text="No data available",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=colors['text_secondary'])
        )
    
    # Calculate regional statistics
    regional_stats = filtered_df.groupby('region').agg({
        'final_tuition_fee': ['mean', 'count'],
        'มหาวิทยาลัย': 'nunique'
    }).round(0)
    
    regional_stats.columns = ['avg_tuition', 'program_count', 'university_count']
    regional_stats = regional_stats.reset_index()
    
    # Create dual-axis chart
    fig = go.Figure()
    
    # Bar chart for program count
    fig.add_trace(go.Bar(
        name='Programs',
        x=regional_stats['region'],
        y=regional_stats['program_count'],
        marker_color=colors['primary'],
        opacity=0.8,
        text=regional_stats['program_count'],
        textposition='auto',
        textfont=dict(color='white', size=12, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Programs: %{y}<extra></extra>'
    ))
    
    # Line chart for average tuition
    fig.add_trace(go.Scatter(
        name='Avg. Tuition',
        x=regional_stats['region'],
        y=regional_stats['avg_tuition'],
        mode='lines+markers',
        line=dict(color=colors['warning'], width=3),
        marker=dict(size=8, color=colors['warning']),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Avg. Tuition: ฿%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Programs & Average Tuition by Region',
            font=dict(size=16, color=colors['text_primary'], family='Inter'),
            x=0.5
        ),
        xaxis=dict(
            title='Region',
            color=colors['text_secondary'],
            tickangle=45
        ),
        yaxis=dict(
            title='Number of Programs',
            color=colors['text_secondary'],
            side='left'
        ),
        yaxis2=dict(
            title='Average Tuition (฿)',
            color=colors['text_secondary'],
            overlaying='y',
            side='right'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=colors['text_primary']),
        margin=dict(l=50, r=50, t=80, b=100)
    )
    
    return fig

# Enhanced callback for program distribution chart
@app.callback(
    Output('program-distribution', 'figure'),
    [Input('program-filter', 'value'),
     Input('region-filter', 'value'),
     Input('tuition-slider', 'value')]
)
def update_program_chart(program_type, region, tuition_range):
    filtered_df = filter_dataframe(program_type, region, tuition_range)
    
    if len(filtered_df) == 0:
        return go.Figure().add_annotation(
            text="No data available",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=colors['text_secondary'])
        )
    
    # Calculate program distribution
    program_counts = filtered_df['program_type'].value_counts()
    
    # Color mapping for programs
    program_colors_map = {
        'Computer Engineering': colors['primary'],
        'AI Engineering': colors['danger'],
        'Digital Engineering': colors['info'],
        'Intelligent Systems': colors['warning'],
        'Cybersecurity': colors['success']
    }
    
    colors_list = [program_colors_map.get(prog, colors['secondary']) for prog in program_counts.index]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=program_counts.index,
            values=program_counts.values,
            hole=0.4,
            marker=dict(
                colors=colors_list,
                line=dict(color='white', width=2)
            ),
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
                font_color=colors['text_primary'],
                font_family='Inter',
                showarrow=False
            )
        ],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=colors['text_primary']),
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

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)