from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <form action="/redirect" method="post">
            <label for="url">Enter URL:</label>
            <input type="text" id="url" name="url" required>
            <input type="submit" value="Go">
        </form>
    '''

@app.route('/redirect', methods=['POST'])
def redirect_to_url():
    url = request.form['url']
    if not url.startswith('http'):
        url = 'http://' + url
    return redirect(f"/proxy/?url={url}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
