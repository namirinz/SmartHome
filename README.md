# SmartHome
This smart home project has built for OCOP 2019 at Triamudomsuksa Pattanakarn School.

# Equipemnt
1) Raspberry Pi 3B+
2) Raspberry Pi camera v2
3) Servo motor
4) DHT 22
5) Micro Switch
6) RGB LED

# Feature
1) Face Recognition | ระบบรู้จำใบหน้า
2) Raspi x Line Notify | การใช้ line notify เพื่อแจ้งเตือนและส่งข้อมูลแก่เจ้าของ
3) Control Panel feat NETPIE.io | สำหรับควบคุมอุปรณ์ต่างๆผ่านเว็บไซต์และสมาร์ทโฟน

# ขั้นตอน
 ## การเพิ่มข้อมูลใบหน้าลงในฐานข้อมูล
 1) รันคำสั่ง python build_face_dataset.py --cascade haarcascade_frontalface_default.xml --output dataset/"ชื่อใบหน้า"
   เพื่อเก็บข้อมูลใบหน้าลงในฐานข้อมูล (ยิ่งเยอะการประมวลผลยิ่งแม่นยำ)
 2) รันคำสั่ง python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog
   เพื่อ encode โดยจะนำข้อมูลจากฐานข้อมูลแปลงเป็นไฟล์ที่สามารถประมวลผลได้ 
 ## ระบบ main
 1) เมื่อ micro switch ถูกกด ระบบจะทำการถ่ายรูปใบหน้าแล้วส่งไลน์ไปยังเจ้าของ (Admin)
 2) ระบบ face recognition จะทำงานยื่นใบหน้าให้มีกรอบสี่เหลี่ยมหน้าในจอ
 3) หากประมวลผลแล้วพบว่าใบหน้าตรงกับฐานข้อมูล ระบบจะส่งไลน์ไปยังเจ้าของว่า "ชื่อที่อยู่ในฐานข้อมูล" ได้ทำการสแกนหน้า พร้อมทั้งปลดล๊อคประตู
 4) หากประมวลผลแล้วพบว่าใบหน้าไม่ตรงกับฐานข้อมูล ระบบจะส่งไลน์ไปยังเจ้าของว่า "มีผู้บุกรุก" ได้ทำการสแกนหน้า ส่วนประตูก็จะไม่ปลดล็อค
 
