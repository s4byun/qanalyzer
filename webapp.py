from flask import Flask, render_template, request, jsonify
import teradata
import time
import os
import json
import random

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


class JSONDelta:
    def __init__(self, json1, json2):
        self.value_delimiter = "::"
        self.key_delimiter = "/"
        self.dict_delimiter = "d"
        self.list_delimiter = "l"
        self.json1 = json1
        self.json2 = json2

    def diff(self):
        l1 = self.flatten("", self.json1)
        l2 = self.flatten("", self.json2)
        return self.diffdict(l1, l2)

    def flatten(self, accpath, obj):
        flattened_list = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                newpath = accpath + self.key_delimiter + str(k)
                flattened_list += self.flatten(newpath, v)
        elif isinstance(obj, list):
            newpath = accpath + self.key_delimiter
            for x in obj:
                if isinstance(x, list):
                    flattened_list += self.flatten(newpath + 'l', x)
                else:
                    flattened_list += self.flatten(newpath, x)
        else:
            return [accpath + self.value_delimiter + str(obj)]
        return flattened_list

    def diffdict(self, l1, l2):
        sl1 = sorted(l1)
        sl2 = sorted(l2)
        added_list = [x for x in sl1 if x not in sl2]
        rmved_list = [x for x in sl2 if x not in sl1]
        return {'add': added_list, 'rm': rmved_list}


@app.route('/tasm', methods=['POST'])
def tasm():
    file1 = str(request.form['tasm_file1'])
    file2 = str(request.form['tasm_file2'])
    return jsonify(get_tasm_diff(file1, file2))


@app.route('/dbsc', methods=['POST'])
def dbsc():
    run_id1 = request.form['run_id1']
    run_id2 = request.form['run_id2']
    return jsonify(get_dbsc_diff(run_id1, run_id2))


@app.route('/feature', methods=['POST'])
def feature():
    run_id1 = request.form['run_id1']
    run_id2 = request.form['run_id2']
    return jsonify(get_feature_usage_diff(run_id1, run_id2))


def get_tasm_diff(file1, file2):
    time.sleep(3)
    with open(file1) as of, open(file2) as nf:
        json1 = json.load(of)
        json2 = json.load(nf)
    return JSONDelta(json1, json2).diff()


def get_feature_usage_diff(run_id1, run_id2):
    feature_data = {'add': [], 'rm': []}
    udaExec = teradata.UdaExec(appName="qanalyzer", version="1.0")
    with udaExec.connect(method="odbc",
                         system="italy",
                         username="tqpe_uda_solutions_admin",
                         password="tqpe_uda_solutions_admin") as con:
        sql_query = \
            """
            select (select trim(feature_name) from  TQST_TEST_PROFILE_DB.hack_features where run_id={0}
            EXCEPT
            select trim(feature_name) from TQST_TEST_PROFILE_DB.hack_features  where run_id={1}) as addition
            ,
            (select trim(feature_name) from TQST_TEST_PROFILE_DB.hack_features  where run_id={1}
            EXCEPT
            select trim(feature_name) from TQST_TEST_PROFILE_DB.hack_features where run_id={0}) as removed;
            """.format(run_id1, run_id2)

        # ("(select trim(feature_name) from TQST_TEST_PROFILE_DB.hack_features "
        #  "where run_id={0} EXCEPT select trim(feature_name) "
        #  "from TQST_TEST_PROFILE_DB.hack_features where run_id={1}) as addition, "
        #  "(select trim(feature_name) from TQST_TEST_PROFILE_DB.hack_features "
        #  "where run_id={1} EXCEPT select trim(feature_name) "
        #  "from TQST_TEST_PROFILE_DB.hack_features where run_id={0}) as removed;").format(run_id1, run_id2)

        res_data = con.execute(sql_query)
        for r in res_data:
            if r['addition']:
                feature_data['add'].append(r['addition'])
            elif r['removed']:
                feature_data['rm'].append(r['removed'])
    return feature_data


def get_dbsc_diff(run_id1, run_id2):
    dbsc_data = []
    udaExec = teradata.UdaExec(appName="qanalyzer", version="1.0")
    with udaExec.connect(method="odbc",
                         system="italy",
                         username="tqpe_uda_solutions_admin",
                         password="tqpe_uda_solutions_admin") as con:
        sql_dbsc_data = \
            ("select trim(a.fieldname) as name, trim(a.fieldvalue) as aval, trim(b.fieldvalue) as bval from "
             "(select * from TQST_TEST_PROFILE_DB.hack_dbscontrol where run_id={}) a, "
             "(select * from TQST_TEST_PROFILE_DB.hack_dbscontrol where run_id={}) b "
             "where a.groupName = b.groupName and a.FieldNum = b.FieldNum and a.FieldName = b.FieldName "
             "and a.fieldvalue <> b.fieldvalue;").format(run_id1, run_id2)
        res_data = con.execute(sql_dbsc_data)
        for r in res_data:
            dbsc_data.append({'name': str(r['name']).strip(),
                              'new': str(r['aval']).strip(),
                              'old': str(r['bval']).strip()})
    return dbsc_data


def get_query_data():
    udaExec = teradata.UdaExec(appName="qanalyzer", version="1.0")
    with udaExec.connect(method="odbc",
                         system="italy",
                         username="tqpe_uda_solutions_admin",
                         password="tqpe_uda_solutions_admin") as con:
        rows = con.execute(
            ("select * from TQST_TEST_PROFILE_DB.hack_runtime order by sql_name asc, run_num;"))
        data = {}

        json_path = os.path.realpath(os.path.join("static", "json"))
        files_list = [
            "tdwmdmp_03232017_1639.json",
            "tdwmdmp_03232017_1714.json",
            "tdwmdmp_06122017_1403.json",
            "tdwmdmp_06132017_1430.json",
            "tdwmdmp_06142017_1454.json"
        ]
        for row in rows:
            sql_name = row['sql_name']
            run_num = row['run_num']
            run_id = str(row['run_id'])
            run_duration = float(row['run_duration']) / 60.0
            StartTime = time.mktime(row['startTime'].timetuple()) * 1000
            label = row['label']
            try:
                unique_query_data = data[sql_name]
                unique_query_data[run_num] = {
                    'run_id': run_id,
                    'run_duration': run_duration,
                    'StartTime': StartTime,
                    'label': label,
                    'tasm_file': os.path.join(json_path, random.choice(files_list))
                }
            except KeyError:
                data[sql_name] = {
                    run_num: {
                        'run_id': run_id,
                        'run_duration': run_duration,
                        'StartTime': StartTime,
                        'label': label,
                        'tasm_file': os.path.join(json_path, random.choice(files_list))
                    }
                }

    series = []
    for k_sql_name, sql_name_dict in data.items():
        points = []
        for k_run_num, run_num_dict in sql_name_dict.items():
            points.append({
                'x': run_num_dict['StartTime'],
                'y': run_num_dict['run_duration'],
                'run_num': int(k_run_num),
                'run_id': run_num_dict['run_id'],
                'label': run_num_dict['label'],
                'tasm_file': run_num_dict['tasm_file']
            })

        series.append({
            "name": k_sql_name,
            "color": "rgba(71, 206, 244, 0.5)",
            "data": points
        })

        sorted_series = sorted(series, key=lambda k: k['name'])
        for i in range(len(sorted_series)):
            sorted_series[i]["legendIndex"] = i
    return sorted_series


@app.route("/")
@app.route("/index")
def index():
    series = get_query_data()
    return render_template('index.html', series=series)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8081, passthrough_errors=True)
