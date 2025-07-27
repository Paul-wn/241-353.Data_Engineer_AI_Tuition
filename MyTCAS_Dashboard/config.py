# config.py - การตั้งค่าและสี

# สีธีมของแอป
COLORS = {
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

# สีสำหรับแต่ละประเภทโปรแกรม
PROGRAM_COLORS = {
    'Computer Engineering': COLORS['primary'],
    'AI Engineering': COLORS['danger'],
    'Digital Engineering': COLORS['info'],
    'Intelligent Systems': COLORS['warning'],
    'Cybersecurity': COLORS['success']
}

# การตั้งค่าแผนที่
MAP_CONFIG = {
    'center_lat': 13.5,
    'center_lon': 101.0,
    'zoom': 4.8,
    'style': 'carto-positron',
    'marker_size': 14
}

# การตั้งค่าไฟล์ข้อมูล
DATA_CONFIG = {
    'csv_file': 'data\data_via_location_noises.csv',
    'tuition_column': 'ค่าใช้จ่ายที่ปรับแล้ว'
}