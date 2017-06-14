from flask import Flask, render_template
import time
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
@app.route("/index")
def index():
    series = [
        {
            "name": 'Sample Query 1 - Success',
            "color": 'rgba(71, 206, 244, 0.5)',
            "data": [
                ["2017,06,13,00,05,02", 10.0]
                # [Date.UTC(2017, 06, 13, 00, 05, 02), 10.0],
                # [Date.UTC(2017, 06, 13, 01, 10, 02), 8.1],
                # [Date.UTC(2017, 06, 13, 02, 00, 39), 9.5],
                # [Date.UTC(2017, 06, 13, 03, 23, 42), 10.2],
                # [Date.UTC(2017, 06, 13, 03, 30, 27), 8.2],
                # [Date.UTC(2017, 06, 14, 00, 17, 12), 5.2],
                # [Date.UTC(2017, 06, 14, 02, 52, 33), 6.9],
                # [Date.UTC(2017, 06, 14, 05, 39, 51), 3.0],
                # [Date.UTC(2017, 06, 15, 16, 25, 20), 4.2]
            ]
        },
        {
            "name": "Sample Query 2 - Fail",
            "color": 'rgba(255, 0, 0, 0.5)',
            "data": [
                # [Date.UTC(2017, 06, 13, 09, 12, 32), 20.2],
                # [Date.UTC(2017, 06, 14, 07, 05, 02), 25.2],
                # [Date.UTC(2017, 06, 15, 17, 05, 02), 31.2]
            ]
        }
    ]
    return render_template('index.html', series=series)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8081, passthrough_errors=True)

    #1, 2
