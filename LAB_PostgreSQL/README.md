# 📝 PSU Note Application

**Student ID:** 6510110427  
**Name:** Warakorn Nupud  
**Lab:** PostgreSQL Database with Flask

---

## 📋 สรุปฟังก์ชันที่เพิ่มเติม

### � ฟังก์ชันจัดการบันทึก (Notes)
- **แก้ไขบันทึก** - แก้ไขหัวข้อ เนื้อหา และแท็ก
- **ลบบันทึก** - ลบบันทึกพร้อมยืนยัน

### 🏷️ ฟังก์ชันจัดการแท็ก (Tags)  
- **แก้ไขชื่อแท็ก** - เปลี่ยนชื่อแท็กพร้อมปุ่ม Reset
- **ลบแท็ก** - ลบแท็กออกจากทุกบันทึก

### �️ การแก้ไขปัญหา
- **แก้ Template Error** - เปลี่ยน `{% block content %}` เป็น `{% block body %}`
- **แก้ AttributeError** - เปลี่ยนจาก `populate_obj()` เป็น manual assignment
- **แก้ Foreign Key Error** - เอาแท็กออกจากบันทึกก่อนลบ

### 🎨 ปรับปรุง UI/UX
- **ปุ่ม Reset** - ล้างข้อมูลในฟอร์มแก้ไขแท็ก
- **การยืนยัน** - ป๊อปอัพยืนยันก่อนลบ
- **ปุ่ม Edit/Delete** - เพิ่มในหน้าแสดงบันทึก

## 🚀 วิธีรัน

```bash
# รัน PostgreSQL
docker-compose up -d

# รันแอป
python noteapp.py
```

**URL:** http://localhost:5000
