from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 限制上传文件大小为100MB

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

DEFAULT_VIDEO_URL = "https://www.yabo.gg/wp-content/uploads/2023/09/01.mp4"

@app.route('/')
def index():
    local_video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'video.mp4')
    if os.path.exists(local_video_path):
        video_url = url_for('uploaded_file', filename='video.mp4')
    else:
        video_url = DEFAULT_VIDEO_URL
    return render_template('index.html', video_url=video_url)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'video.mp4')
        file.save(file_path)
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
