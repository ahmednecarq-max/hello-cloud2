from flask import Flask, render_template_string, request [cite: 33]
import os [cite: 33]
import psycopg2 [cite: 33]

app = Flask(__name__) [cite: 33]

# Veritabanı bağlantı adresi (Render'dan aldığın URL buraya gelecek) [cite: 33, 144]
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ahmed:L61zQ5loZnWdDT0fQT5aYmRhUwN57qoo@dpg-d8evvb19rddc73c51neg-a.oregon-postgres.render.com/hello_cloud3_db_ectf") [cite: 33, 144]

# Web sitesinin görünümünü belirleyen HTML tasarımı [cite: 33]
HTML = """
<!doctype html>
<html>
<head>
<title>Buluttan Selam!</title> [cite: 33]
<style>
body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; } [cite: 33]
h1 { color: #333; } [cite: 33]
form { margin: 20px auto; } [cite: 33]
input { padding: 10px; font-size: 16px; } [cite: 33]
button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; } [cite: 33]
ul { list-style: none; padding: 0; } [cite: 33]
li { background: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; } [cite: 33]
</style>
</head> [cite: 35]
<body>
<h1>Buluttan Selam!</h1> [cite: 48]
<p>Adını yaz, selamını bırak </p> [cite: 49]
<form method="POST"> [cite: 50]
<input type="text" name="isim" placeholder="Adını yaz" required> [cite: 51]
<button type="submit">Gönder</button> [cite: 52]
</form> [cite: 53]
<h3>Ziyaretçiler:</h3> [cite: 54]
<ul> [cite: 45]
{% for ad in isimler %} [cite: 55]
<li>{{ ad }}</li> [cite: 57]
{% endfor %} [cite: 59]
</ul> [cite: 61]
</body> [cite: 63]
</html> [cite: 65]
"""

# Veritabanına bağlanmayı sağlayan fonksiyon [cite: 69]
def connect_db(): [cite: 69]
    conn = psycopg2.connect(DATABASE_URL) [cite: 71]
    return conn [cite: 73, 74]

# Ana sayfa yüklendiğinde veya form gönderildiğinde çalışacak kısım [cite: 77]
@app.route("/", methods=["GET", "POST"]) [cite: 77]
def index(): [cite: 80]
    conn = connect_db() [cite: 81, 82]
    cur = conn.cursor() [cite: 94]
    
    # Eğer tablo yoksa otomatik oluştur [cite: 95]
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)") [cite: 95]
    
    # Eğer kullanıcı formdan isim gönderdiyse veritabanına kaydet [cite: 96]
    if request.method == "POST": [cite: 96]
        isim = request.form.get("isim") [cite: 97]
        if isim: [cite: 98]
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,)) [cite: 99]
            conn.commit() [cite: 99]
            
    # Son eklenen 10 ismi veritabanından çek ve listele [cite: 100]
    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10") [cite: 100]
    isimler = [row[0] for row in cur.fetchall()] [cite: 100]
    
    cur.close() [cite: 103]
    conn.close() [cite: 106]
    
    return render_template_string(HTML, isimler=isimler) [cite: 107]

if __name__ == "__main__": [cite: 110, 111, 113]
    app.run(host="0.0.0.0", port=5000) [cite: 114]
