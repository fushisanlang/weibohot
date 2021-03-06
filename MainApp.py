
from flask import Flask, render_template, jsonify
from flask_apscheduler import APScheduler
from OperacteData import DataJson, DataShow, DailyReport, AutoCreateTable
import json
import datetime
from GetData import GetData
from WordPic import WordPic

class Config:

    JOBS = [
        {
            'id': 'GetData',
            'func': GetData,
            'trigger': 'cron',
            'minute': '*/5',
        },
        {
            'id': 'AutoCreateTable',
            'func': AutoCreateTable,
            'trigger': 'cron',
            'month': '*',
        },
                {
            'id': 'WordPic',
            'func': WordPic,
            'trigger': 'cron',
            'hour': '0',
            'minute': 17,

        },
    ]

    SCHEDULER_API_ENABLED = True


app = Flask(__name__)


@app.route('/weibo/hello_json', methods=['POST', 'GET'])
def hello_json():
    a = {'hello': "fushisanlang"}
    return jsonify(a)


@app.route('/weibo/data/<SelectTime>', methods=['POST', 'GET'])
def dataJson(SelectTime):
    FinalResult = DataJson(SelectTime)
    return jsonify(FinalResult)


@app.route('/weibo/<SelectTime>')
def dataShow(SelectTime):
    if SelectTime < '20220315' or datetime.datetime.strptime(SelectTime, "%Y%m%d") > datetime.datetime.today():
        return render_template('error.html')

    else:
        ColorJson = DataShow(SelectTime)
        return render_template('race.html', SelectTime=SelectTime, ColorJson=json.dumps(ColorJson))


@app.route('/weibo/report/<SelectTime>')
def dailyReport(SelectTime):
    if SelectTime < '20220315' or datetime.datetime.strptime(SelectTime, "%Y%m%d") > datetime.datetime.today():
        return render_template('error.html')

    else:
        DailyReportList = DailyReport(SelectTime)

        return render_template('report.html', SelectTime=SelectTime, DailyReportList=DailyReportList)

scheduler = APScheduler()
app.config.from_object(Config())
scheduler.init_app(app)
scheduler.start()
app.run(debug=False, host='0.0.0.0', port=31000)

