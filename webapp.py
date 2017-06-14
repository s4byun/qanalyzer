from flask import Flask, render_template
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
@app.route("/index")
def index():
    title = {"text": 'Query Analyzer'}
    return render_template('index.html', title=title)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8080, passthrough_errors=True)

    #1, 2
