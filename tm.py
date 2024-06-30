from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/music'
app.config['CHAT_LOG'] = 'chat.log'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 限制上传文件大小为100MB

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

DEFAULT_VIDEO_URL = "https://www.yabo.gg/wp-content/uploads/2023/09/01.mp4"

@app.route('/')
def index():
    music_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith(('.mp3', '.m4a'))]
    return render_template('index.html', video_url=DEFAULT_VIDEO_URL, music_files=music_files)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    music_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith(('.mp3', '.m4a'))]
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        file = request.files.get('file')
        file_url = None

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_url = url_for('uploaded_file', filename=f'music/{filename}')

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if file_url:
            chat_entry = f'{timestamp} - {username}: {message} <img src="{file_url}">\n'
        else:
            chat_entry = f'{timestamp} - {username}: {message}\n'

        with open(app.config['CHAT_LOG'], 'a') as f:
            f.write(chat_entry)

        return redirect(url_for('chat'))

    chat_history = []
    if os.path.exists(app.config['CHAT_LOG']):
        with open(app.config['CHAT_LOG'], 'r') as f:
            chat_history = f.readlines()

    return render_template('chat.html', chat_history=chat_history, music_files=music_files)

@app.route('/uploads/music/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload_music', methods=['GET', 'POST'])
def upload_music():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and (file.filename.endswith('.mp3') or file.filename.endswith('.m4a')):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for('upload_music'))

    return render_template('upload_music.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
