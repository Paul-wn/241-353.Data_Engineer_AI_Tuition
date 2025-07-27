# data_utils.py - ฟังก์ชันจัดการข้อมูล

import pandas as pd
import numpy as np
from config import DATA_CONFIG

def load_and_clean_data():
    """โหลดและทำความสะอาดข้อมูล"""
    df = pd.read_csv(DATA_CONFIG['csv_file'])
    df_clean = df.copy()
    
    # ใช้คอลัมน์ค่าเล่าเรียนที่ปรับแล้ว
    df_clean['final_tuition_fee'] = df_clean[DATA_CONFIG['tuition_column']]
    
    # ลบแถวที่ไม่มีข้อมูลค่าเล่าเรียนหรือพิกัด
    df_clean = df_clean.dropna(subset=['final_tuition_fee', 'latitude', 'longitude'])
    
    # สร้าง unique ID
    df_clean['unique_id'] = df_clean.index.astype(str)
    
    # เพิ่มข้อมูลภูมิภาคและประเภทโปรแกรม
    df_clean['region'] = df_clean.apply(
        lambda row: get_region_from_coordinates(row['latitude'], row['longitude']), 
        axis=1
    )
    df_clean['program_type'] = df_clean['หลักสูตร'].apply(categorize_program)
    
    return df_clean

def get_region_from_coordinates(lat, lon):
    """แปลงพิกัดเป็นภูมิภาค"""
    if lat >= 17.0:
        return 'ภาคเหนือ'
    elif lat >= 14.0 and lon >= 101.5:
        return 'ภาคอีสาน'
    elif lat <= 11.0:
        return 'ภาคใต้'
    elif lat >= 13.5 and lat <= 14.5 and lon >= 100.2 and lon <= 101.2:
        return 'กรุงเทพฯและปริมณฑล'
    else:
        return 'ภาคกลาง'

def categorize_program(program_name):
    """จัดประเภทโปรแกรม"""
    program_name = str(program_name)
    
    if any(word in program_name for word in ['ปัญญาประดิษฐ์', 'Artificial Intelligence', 'AI']):
        return 'AI Engineering'
    elif any(word in program_name for word in ['ระบบอัจฉริยะ', 'Intelligence Systems']):
        return 'Intelligent Systems'
    elif any(word in program_name for word in ['ดิจิทัล', 'Digital']):
        return 'Digital Engineering'
    elif any(word in program_name for word in ['ไซเบอร์', 'Cyber']):
        return 'Cybersecurity'
    else:
        return 'Computer Engineering'

def filter_dataframe(df, program_type, region, tuition_range):
    """กรองข้อมูลตามเงื่อนไข"""
    filtered_df = df.copy()
    
    if program_type != 'all':
        filtered_df = filtered_df[filtered_df['program_type'] == program_type]
    
    if region != 'all':
        filtered_df = filtered_df[filtered_df['region'] == region]
    
    filtered_df = filtered_df[
        (filtered_df['final_tuition_fee'] >= tuition_range[0]) &
        (filtered_df['final_tuition_fee'] <= tuition_range[1])
    ]
    
    return filtered_df

def add_coordinate_offset(df):
    """เพิ่มการเลื่อนพิกัดเล็กน้อยสำหรับมหาวิทยาลัยที่อยู่ตำแหน่งเดียวกัน"""
    grouped = df.groupby(['latitude', 'longitude'])
    
    result_dfs = []
    for (lat, lon), group in grouped:
        if len(group) > 1:
            # เพิ่มการเลื่อนแบบสุ่มเล็กน้อย
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