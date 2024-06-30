from flask import Flask, render_template

app = Flask(__name__)

DEFAULT_VIDEO_URL = "https://www.yabo.gg/wp-content/uploads/2023/09/01.mp4"

@app.route('/')
def index():
    return render_template('index.html', video_url=DEFAULT_VIDEO_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
