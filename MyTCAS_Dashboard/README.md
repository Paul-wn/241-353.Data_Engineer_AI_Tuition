# VIBE CODING 
🇹🇭 Thailand Computer & AI Engineering Universities Dashboard

Dashboard สำหรับค้นหาและเปรียบเทียบหลักสูตรวิศวกรรมคอมพิวเตอร์และปัญญาประดิษฐ์ในประเทศไทย

## 📁 โครงสร้างไฟล์

```
project/
├── main.py              # ไฟล์หลักของแอป
├── config.py            # การตั้งค่าและสี
├── data_utils.py        # ฟังก์ชันจัดการข้อมูล
├── layout.py            # ส่วนประกอบของหน้าเว็บ
├── charts.py            # ฟังก์ชันสร้างกราฟ
├── callbacks.py         # ฟังก์ชัน Callback สำหรับ Dash
├── requirements.txt     # Dependencies
├── assets/
│   └── custom.css       # CSS สำหรับการจัดแต่ง
└── data/
    └── data_via_location_noises.csv  # ข้อมูลมหาวิทยาลัย
```

## 🚀 การติดตั้งและใช้งาน

### 1. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 2. เตรียมข้อมูล

ให้แน่ใจว่าไฟล์ `data/data_via_location_noises.csv` มีอยู่และมีคอลัมน์ที่จำเป็น:

* `มหาวิทยาลัย` - ชื่อมหาวิทยาลัย
* `หลักสูตร` - ชื่อหลักสูตร
* `วิทยาเขต` - ชื่อวิทยาเขต
* `ค่าใช้จ่ายที่ปรับแล้ว` - ค่าเล่าเรียน
* `latitude`, `longitude` - พิกัดมหาวิทยาลัย

### 3. รันแอป

```bash
python main.py
```

แอปจะรันที่ `http://127.0.0.1:8050` หรือ `http://localhost:8050`

## 📊 ฟีเจอร์หลัก

### 🗺️ แผนที่แบบ Interactive

* แสดงตำแหน่งมหาวิทยาลัยบนแผนที่ประเทศไทย
* คลิกเพื่อดูรายละเอียดแต่ละมหาวิทยาลัย
* สีแยกตามประเภทโปรแกรม

### 🔍 ระบบกรองข้อมูล

* กรองตามประเภทโปรแกรม
* กรองตามภูมิภาค
* กรองตามช่วงค่าเล่าเรียน

### 📈 กราฟวิเคราะห์

* การเปรียบเทียบภูมิภาค
* การกระจายประเภทโปรแกรม
* สถิติด่วนและข้อมูลเชิงลึก

## 🎨 การปรับแต่ง

### เปลี่ยนสีธีม

แก้ไขไฟล์ `config.py` ส่วน `COLORS`:

```python
COLORS = {
    'primary': '#6366f1',    # สีหลัก
    'secondary': '#64748b',  # สีรอง
    # ... สีอื่นๆ
}
```

### เพิ่มประเภทโปรแกรมใหม่

แก้ไขฟังก์ชัน `categorize_program()` ในไฟล์ `data_utils.py`:

```python
def categorize_program(program_name):
    if 'คำสำคัญใหม่' in str(program_name):
        return 'ประเภทใหม่'
    # ... เงื่อนไขอื่นๆ
```

### เปลี่ยนการตั้งค่าแผนที่

แก้ไขไฟล์ `config.py` ส่วน `MAP_CONFIG`:

```python
MAP_CONFIG = {
    'center_lat': 13.5,    # จุดกึ่งกลางแผนที่
    'center_lon': 101.0,   # จุดกึ่งกลางแผนที่
    'zoom': 4.8,           # ระดับการซูม
    'style': 'carto-positron'  # สไตล์แผนที่
}
```

## 🛠️ การพัฒนาต่อ

### เพิ่มฟีเจอร์ใหม่

1. เพิ่มฟังก์ชันใน `charts.py` สำหรับกราหใหม่
2. เพิ่ม component ใน `layout.py`
3. เพิ่ม callback ใน `callbacks.py`

### เปลี่ยนแหล่งข้อมูล

แก้ไขไฟล์ `config.py` ส่วน `DATA_CONFIG`:

```python
DATA_CONFIG = {
    'csv_file': 'path/to/new/data.csv',
    'tuition_column': 'ชื
```
