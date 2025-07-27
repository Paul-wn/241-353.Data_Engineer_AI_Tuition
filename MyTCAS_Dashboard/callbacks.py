# callbacks.py - ฟังก์ชัน Callback สำหรับ Dash

from dash import Input, Output, callback, html
from data_utils import filter_dataframe, add_coordinate_offset
from charts import create_map_figure, create_regional_chart, create_program_distribution_chart
from config import COLORS

def register_callbacks(app, df_clean):
    """ลงทะเบียน callback ทั้งหมด"""
    
    @app.callback(
        Output('thailand-map', 'figure'),
        [Input('program-filter', 'value'),
         Input('region-filter', 'value'),
         Input('tuition-slider', 'value')]
    )
    def update_map(program_type, region, tuition_range):
        filtered_df = filter_dataframe(df_clean, program_type, region, tuition_range)
        return create_map_figure(filtered_df)

    @app.callback(
        Output('university-details', 'children'),
        [Input('thailand-map', 'clickData'),
         Input('program-filter', 'value'),
         Input('region-filter', 'value'),
         Input('tuition-slider', 'value')]
    )
    def update_details(clickData, program_type, region, tuition_range):
        if clickData is None:
            return create_default_details()
        
        filtered_df = filter_dataframe(df_clean, program_type, region, tuition_range)
        filtered_df = add_coordinate_offset(filtered_df)
        
        # หาข้อมูลที่ถูกคลิก
        clicked_unique_id = clickData['points'][0]['text']
        try:
            university_data = filtered_df[filtered_df['unique_id'] == clicked_unique_id].iloc[0]
        except IndexError:
            return html.P("Program details not found", 
                         style={'textAlign': 'center', 'color': COLORS['text_secondary'], 'fontSize': '16px'})
        
        return create_university_details(university_data, filtered_df)

    @app.callback(
        Output('statistics-content', 'children'),
        [Input('program-filter', 'value'),
         Input('region-filter', 'value'),
         Input('tuition-slider', 'value')]
    )
    def update_statistics(program_type, region, tuition_range):
        filtered_df = filter_dataframe(df_clean, program_type, region, tuition_range)
        
        if len(filtered_df) == 0:
            return html.Div([
                html.P("🔍 No data available for selected filters", 
                       style={'textAlign': 'center', 'color': COLORS['text_secondary']})
            ])
        
        return create_statistics_content(filtered_df)

    @app.callback(
        Output('regional-comparison', 'figure'),
        [Input('program-filter', 'value'),
         Input('region-filter', 'value'),
         Input('tuition-slider', 'value')]
    )
    def update_regional_chart(program_type, region, tuition_range):
        filtered_df = filter_dataframe(df_clean, program_type, region, tuition_range)
        return create_regional_chart(filtered_df)

    @app.callback(
        Output('program-distribution', 'figure'),
        [Input('program-filter', 'value'),
         Input('region-filter', 'value'),
         Input('tuition-slider', 'value')]
    )
    def update_program_chart(program_type, region, tuition_range):
        filtered_df = filter_dataframe(df_clean, program_type, region, tuition_range)
        return create_program_distribution_chart(filtered_df)

def create_default_details():
    """สร้างรายละเอียดเริ่มต้น"""
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
                   'color': COLORS['text_secondary'],
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

def create_university_details(university_data, filtered_df):
    """สร้างรายละเอียดมหาวิทยาลัย"""
    # หาโปรแกรมอื่นๆ ในมหาวิทยาลัยเดียวกัน
    same_university_programs = filtered_df[
        filtered_df['มหาวิทยาลัย'] == university_data['มหาวิทยาลัย']
    ]
    
    return html.Div([
        # หัวข้อมหาวิทยาลัย
        html.Div([
            html.Div([
                html.Img(
                    src=university_data.get('img', '/assets/default-university.png'),
                    style={
                        'width': '80px', 
                        'height': '80px', 
                        'objectFit': 'contain',
                        'borderRadius': '16px',
                        'border': f'3px solid {COLORS["primary"]}',
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
                'color': COLORS['text_primary'],
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
                'color': COLORS['text_secondary'],
                'fontSize': '14px',
                'fontWeight': '500',
                'marginBottom': '16px'
            }),
            
            # ป้ายประเภทโปรแกรม
            html.Div([
                html.Span(university_data['program_type'], style={
                    'fontSize': '12px',
                    'fontWeight': '600',
                    'color': 'white',
                    'backgroundColor': COLORS['primary'],
                    'padding': '6px 12px',
                    'borderRadius': '16px',
                    'display': 'inline-block'
                })
            ], style={'textAlign': 'center', 'marginBottom': '16px'})
        ]),
        
        # รายละเอียดโปรแกรม
        html.Div([
            html.H5([
                html.Span("🎓 ", style={'marginRight': '8px'}),
                "Program Details"
            ], style={
                'color': COLORS['text_primary'],
                'fontSize': '16px',
                'fontWeight': '600',
                'marginBottom': '12px'
            }),
            
            html.P(university_data['หลักสูตร'], style={
                'color': COLORS['text_secondary'],
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
        
        # ข้อมูลค่าเล่าเรียน
        html.Div([
            html.H5([
                html.Span("💰 ", style={'marginRight': '8px'}),
                "Tuition Fee"
            ], style={
                'color': COLORS['text_primary'],
                'fontSize': '16px',
                'fontWeight': '600',
                'marginBottom': '12px'
            }),
            
            html.Div([
                html.Span("฿", style={
                    'fontSize': '18px',
                    'color': COLORS['warning'],
                    'fontWeight': '600'
                }),
                html.Span(f"{university_data['final_tuition_fee']:,.0f}", style={
                    'fontSize': '24px',
                    'fontWeight': '700',
                    'color': COLORS['text_primary'],
                    'marginLeft': '4px'
                })
            ], style={
                'textAlign': 'center',
                'padding': '16px',
                'backgroundColor': 'rgba(245, 158, 11, 0.1)',
                'borderRadius': '16px',
                'border': '2px solid rgba(245, 158, 11, 0.3)',
                'marginBottom': '16px'
            })
        ]),
        
        # โปรแกรมอื่นๆ ในมหาวิทยาลัยเดียวกัน
        html.Div([
            html.H5([
                html.Span("📚 ", style={'marginRight': '8px'}),
                f"Other Programs ({len(same_university_programs)} total)"
            ], style={
                'color': COLORS['text_primary'],
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
                        'backgroundColor': COLORS['info'],
                        'padding': '4px 8px',
                        'borderRadius': '12px',
                        'margin': '2px',
                        'display': 'inline-block'
                    })
                    for prog_type in same_university_programs['program_type'].unique()
                ])
            ]) if len(same_university_programs) > 1 else None
        ]),
        
        # สถิติด่วน
        html.Div([
            html.Div([
                html.Div([
                    html.Span("🌍", style={'fontSize': '16px', 'marginBottom': '4px'}),
                    html.Br(),
                    html.Span("Region", style={
                        'fontSize': '12px',
                        'color': COLORS['text_secondary'],
                        'fontWeight': '500'
                    }),
                    html.Br(),
                    html.Span(university_data['region'], style={
                        'fontSize': '14px',
                        'fontWeight': '600',
                        'color': COLORS['text_primary']
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
                        'color': COLORS['text_secondary'],
                        'fontWeight': '500'
                    }),
                    html.Br(),
                    html.Span(f"#{university_data.name + 1}", style={
                        'fontSize': '14px',
                        'fontWeight': '600',
                        'color': COLORS['text_primary']
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

def create_statistics_content(filtered_df):
    """สร้างเนื้อหาสถิติ"""
    # คำนวณสถิติ
    total_programs = len(filtered_df)
    total_universities = filtered_df['มหาวิทยาลัย'].nunique()
    avg_tuition = filtered_df['final_tuition_fee'].mean()
    min_tuition = filtered_df['final_tuition_fee'].min()
    max_tuition = filtered_df['final_tuition_fee'].max()
    regions_count = filtered_df['region'].nunique()
    
    return html.Div([
        # เมตริกหลัก
        html.Div([
            create_stat_card("🎓", total_programs, "Programs"),
            create_stat_card("🏛️", total_universities, "Universities"),
            create_stat_card("💰", f"฿{avg_tuition:,.0f}", "Avg. Tuition", font_size='24px'),
            create_stat_card("🌍", regions_count, "Regions")
        ]),
        
        # ข้อมูลเชิงลึกค่าเล่าเรียน
        html.Div([
            html.H5([
                html.Span("📊 ", style={'marginRight': '8px'}),
                "Tuition Insights"
            ], style={
                'color': COLORS['text_primary'],
                'fontSize': '16px',
                'fontWeight': '700',
                'marginBottom': '16px',
                'textAlign': 'center'
            }),
            
            create_insight_card("🔻 Lowest:", f"฿{min_tuition:,.0f}", COLORS['success']),
            create_insight_card("🔺 Highest:", f"฿{max_tuition:,.0f}", COLORS['danger'])
        ]),
        
        # มหาวิทยาลัยชั้นนำ
        html.Div([
            html.H5([
                html.Span("🏆 ", style={'marginRight': '8px'}),
                "Top Universities"
            ], style={
                'color': COLORS['text_primary'],
                'fontSize': '16px',
                'fontWeight': '700',
                'marginBottom': '16px',
                'textAlign': 'center'
            }),
            
            html.Div([
                create_university_rank_item(idx, uni, count)
                for idx, (uni, count) in enumerate(
                    filtered_df['มหาวิทยาลัย'].value_counts().head(3).items()
                )
            ])
        ])
    ])

def create_stat_card(emoji, value, label, font_size='32px'):
    """สร้างการ์ดสถิติ"""
    return html.Div([
        html.Div([
            html.Span(emoji, style={'fontSize': '24px', 'marginBottom': '8px'}),
            html.Br(),
            html.Span(f"{value}", style={
                'fontSize': font_size, 
                'display': 'block', 
                'marginBottom': '4px',
                'fontWeight': '700',
                'color': COLORS['text_primary']
            }),
            html.Span(label, style={
                'fontSize': '14px',
                'color': COLORS['text_secondary'],
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
        })
    ])

def create_insight_card(label, value, color):
    """สร้างการ์ดข้อมูลเชิงลึก"""
    return html.Div([
        html.Span(label, style={
            'fontSize': '14px',
            'fontWeight': '600',
            'color': color
        }),
        html.Span(value, style={
            'fontSize': '14px',
            'fontWeight': '700',
            'color': COLORS['text_primary']
        })
    ], style={
        'padding': '12px',
        'backgroundColor': f'rgba({color.replace("#", "").replace("rgb(", "").replace(")", "")}, 0.1)',
        'borderRadius': '12px',
        'marginBottom': '8px',
        'border': f'1px solid rgba({color.replace("#", "").replace("rgb(", "").replace(")", "")}, 0.2)'
    })

def create_university_rank_item(idx, uni, count):
    """สร้างรายการอันดับมหาวิทยาลัย"""
    return html.Div([
        html.Span(f"#{idx + 1}", style={
            'fontSize': '12px',
            'fontWeight': '700',
            'color': COLORS['primary'],
            'marginRight': '8px'
        }),
        html.Span(uni, style={
            'fontSize': '12px',
            'fontWeight': '600',
            'color': COLORS['text_primary']
        }),
        html.Br(),
        html.Span(f"{count} programs", style={
            'fontSize': '11px',
            'color': COLORS['text_secondary'],
            'fontWeight': '500'
        })
    ], style={
        'padding': '8px 12px',
        'backgroundColor': 'rgba(255,255,255,0.6)',
        'borderRadius': '8px',
        'marginBottom': '8px',
        'border': '1px solid rgba(255,255,255,0.3)'
    })