from flask import Flask, render_template
import teradata
from datetime import datetime, timezone
import time

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
@app.route("/index")
def index():


    udaExec = teradata.UdaExec(appName="adjfkl", version="1.0")
    con = udaExec.connect(method="odbc",system="italy",username="tqpe_uda_solutions_admin",password="tqpe_uda_solutions_admin")

    rows = con.execute(
        ("select * from TQST_TEST_PROFILE_DB.hack_runtime order by sql_name asc, run_num;"))
    timestamp = []
    for row in rows:
        timestamp.append([time.mktime(row["StartTime"].timetuple()) * 1000,float(row["run_duration"])])
        #timestamp.append([row["StartTime"].timetuple()),float(row["run_duration"])])
    #print(timestamp)



    series = [
        {
            "name": 'Sample Query 1 - Success',
            "color": 'rgba(71, 206, 244, 0.5)',
            "data": timestamp,#[

        }#,
        #{
            #"name": "Sample Query 2 - Fail",
            #"color": 'rgba(255, 0, 0, 0.5)',
            #"data": [
             #   [2, 2]
                # [Date.UTC(2017, 06, 13, 09, 12, 32), 20.2],
                # [Date.UTC(2017, 06, 14, 07, 05, 02), 25.2],
                # [Date.UTC(2017, 06, 15, 17, 05, 02), 31.2]
            #]
        #}
    ]
    return render_template('index.html', series=series)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8081, passthrough_errors=True)

    #1, 2
