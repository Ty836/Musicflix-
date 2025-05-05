from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

ADMIN_USER = "admin"
ADMIN_PASS = "your_password"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/lyrics')
def lyrics():
    return render_template('lyrics.html')

@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/wallpapers')
def wallpapers():
    return render_template('wallpapers.html')

@app.route('/anime')
def anime():
    return render_template('anime.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USER and request.form['password'] == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid credentials"
    return render_template('admin.html', error=error)

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    file = request.files.get('file')
    if not file or file.filename == '':
        return "No file selected", 400
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
