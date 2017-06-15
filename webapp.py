from flask import Flask, render_template
import teradata
import time
import json
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

json_path = os.path.realpath(os.path.join("static", "js"))


def get_dbsc(con):
    sql_dbsc_id = "select distinct run_id from TQST_TEST_PROFILE_DB.hack_runtime"
    with con.cursor() as cursor:
        cursor.execute(sql_dbsc_id)
        res_id = cursor.fetchall()
        all_data = {}
        for run_id in res_id:
            dbsc_data = {}
            sql_dbsc_data = """select GroupName, FieldNum, FieldName, FieldValue from TQST_TEST_PROFILE_DB.hack_dbscontrol
                               where run_id = {} and GroupName <> '2'""".format(run_id[0])
            cursor.execute(sql_dbsc_data)
            res_data = cursor.fetchall()
            if not res_data:
                raise ValueError("There is no data")
            for r in res_data:
                k = "{0}  {1}[{2}]".format(r[0].strip(), r[2].strip(), r[1])
                dbsc_data[k] = r[3].split("(")[0].strip()
            all_data[int(run_id[0])] = dbsc_data
    return all_data


def get_query_data(con):
    rows = con.execute(
        ("select * from TQST_TEST_PROFILE_DB.hack_runtime order by sql_name asc, run_num;"))
    data = {}
    for row in rows:
        sql_name = row['sql_name']
        run_num = row['run_num']
        run_id = int(row['run_id'])
        run_duration = float(row['run_duration'])
        StartTime = time.mktime(row['startTime'].timetuple()) * 1000
        label = row['label']
        try:
            unique_query_data = data[sql_name]
            unique_query_data[run_num] = {
                'run_id': run_id,
                'run_duration': run_duration,
                'StartTime': StartTime,
                'label': label
            }
        except KeyError:
            data[sql_name] = {
                run_num: {
                    'run_id': run_id,
                    'run_duration': run_duration,
                    'StartTime': StartTime,
                    'label': label
                }
            }

    series = []
    for k_sql_name, sql_name_dict in data.items():
        points = []
        for k_run_num, run_num_dict in sql_name_dict.items():
            points.append([run_num_dict['StartTime'], run_num_dict['run_duration']])

        series.append({
            "name": k_sql_name,
            "color": "rgba(71, 206, 244, 0.5)",
            "data": points,
            "visible": "false"
        })
    return series


@app.route("/")
@app.route("/index")
def index():
    udaExec = teradata.UdaExec(appName="adjfkl", version="1.0")
    con = udaExec.connect(method="odbc", system="italy",
                          username="tqpe_uda_solutions_admin", password="tqpe_uda_solutions_admin")
    dbsc_data = get_dbsc(con)
    series = get_query_data(con)

    dbsc_output_path = os.path.join(json_path, "dbsc_data.json")
    with open(dbsc_output_path, 'w') as fp:
        json.dump(dbsc_data, fp)

    return render_template('index.html', series=series)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8081, passthrough_errors=True)
