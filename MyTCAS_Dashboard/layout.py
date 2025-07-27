# layout.py - ส่วนประกอบของหน้าเว็บ

from dash import dcc, html
from config import COLORS

def create_header():
    """สร้างส่วนหัวของหน้าเว็บ"""
    return html.Div([
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
    ], className="fade-in")

def create_filters(df_clean):
    """สร้างส่วนกรองข้อมูล"""
    return html.Div([
        html.Div([
            # Program filter
            html.Div([
                html.Label([
                    html.Span("🎓", style={'marginRight': '8px'}),
                    "Program Type"
                ], style={
                    'fontWeight': '600', 
                    'color': COLORS['text_primary'],
                    'fontSize': '14px',
                    'marginBottom': '8px',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='program-filter',
                    options=[{'label': '✨ All Programs', 'value': 'all'}] + 
                            [{'label': f'📚 {prog}', 'value': prog} for prog in df_clean['program_type'].unique()],
                    value='all',
                    style={'borderRadius': '12px', 'border': 'none', 'fontSize': '14px'},
                    className='modern-dropdown',
                    maxHeight=150,
                    optionHeight=30 
                )
            ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '3%'}),
            
            # Region filter
            html.Div([
                html.Label([
                    html.Span("🗺️", style={'marginRight': '8px'}),
                    "Region"
                ], style={
                    'fontWeight': '600', 
                    'color': COLORS['text_primary'],
                    'fontSize': '14px',
                    'marginBottom': '8px',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='region-filter',
                    options=[{'label': '🌍 All Regions', 'value': 'all'}] + 
                            [{'label': f'📍 {region}', 'value': region} for region in df_clean['region'].unique()],
                    value='all',
                    style={'borderRadius': '12px', 'border': 'none', 'fontSize': '14px'},
                    className='modern-dropdown',
                    maxHeight=150,
                    optionHeight=30 
                )
            ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '3%'}),
            
            # Tuition range slider
            html.Div([
                html.Label([
                    html.Span("💰", style={'marginRight': '8px'}),
                    "Tuition Range (฿)"
                ], style={
                    'fontWeight': '600', 
                    'color': COLORS['text_primary'],
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
                            'style': {'color': COLORS['text_secondary'], 'fontSize': '12px', 'fontWeight': '500'}
                        },
                        int(df_clean['final_tuition_fee'].max()): {
                            'label': f"฿{int(df_clean['final_tuition_fee'].max()/1000)}K",
                            'style': {'color': COLORS['text_secondary'], 'fontSize': '12px', 'fontWeight': '500'}
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
    ], className="fade-in")

def create_map_section():
    """สร้างส่วนแผนที่"""
    return html.Div([
        html.Div([
            html.H3([
                html.Span("🗺️", style={'marginRight': '12px'}),
                "Interactive Universities Map"
            ], style={
                'color': COLORS['text_primary'],
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
    ], style={'width': '58%', 'display': 'inline-block', 'verticalAlign': 'top'})

def create_details_section():
    """สร้างส่วนรายละเอียดมหาวิทยาลัย"""
    return html.Div([
        html.Div([
            html.H3([
                html.Span("🏛️", style={'marginRight': '12px'}),
                "University Details"
            ], style={
                'color': COLORS['text_primary'],
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
                               'color': COLORS['text_secondary'],
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

def create_statistics_section():
    """สร้างส่วนสถิติ"""
    return html.Div([
        html.Div([
            html.H3([
                html.Span("📊", style={'marginRight': '12px'}),
                "Quick Stats"
            ], style={
                'color': COLORS['text_primary'],
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
    ], style={'width': '35%', 'display': 'inline-block', 'verticalAlign': 'top'})

def create_charts_section():
    """สร้างส่วนกราฟ"""
    return html.Div([
        # Regional analysis
        html.Div([
            html.Div([
                html.H3([
                    html.Span("🌍", style={'marginRight': '12px'}),
                    "Regional Analysis"
                ], style={
                    'color': COLORS['text_primary'],
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
                    'color': COLORS['text_primary'],
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