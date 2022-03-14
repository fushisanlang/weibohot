import mysql.connector
import datetime
from Tools import Alert, ReadConf, GetColor


def selectOperaction(sqlString):
    conn = mysql.connector.connect(
        user=ReadConf("Mysql-Database", "user"),
        password=ReadConf("Mysql-Database", "password"),
        host=ReadConf("Mysql-Database", "host"),
        database=ReadConf("Mysql-Database", "database"),
        auth_plugin='mysql_native_password',
        port=ReadConf("Mysql-Database", "port")
    )
    conn.start_transaction()
    cursor = conn.cursor()
    cursor.execute(sqlString)
    SqlResult = cursor.fetchall()
    conn.close()
    return SqlResult


def InsertOperaction(sqlString):
    conn = mysql.connector.connect(
        user=ReadConf("Mysql-Database", "user"),
        password=ReadConf("Mysql-Database", "password"),
        host=ReadConf("Mysql-Database", "host"),
        database=ReadConf("Mysql-Database", "database"),
        auth_plugin='mysql_native_password',
        charset='utf8mb4'
    )
    conn.start_transaction()
    cursor = conn.cursor()
    cursor.execute(sqlString)
    conn.commit()
    conn.close()
    return


def DataJson(SelectTime):
    month = SelectTime[:6]
    startTime = datetime.datetime.strptime(SelectTime, "%Y%m%d")
    endTime = startTime+datetime.timedelta(days=1)
    sql = 'SELECT hot_num, node,date_format( DATE_ADD(time,interval -1 minute), \'%H:%i\' )  FROM (SELECT  hot_num, 	node, time, ROW_NUMBER() OVER ( PARTITION BY time ORDER BY hot_num DESC ) AS row_num  FROM weibohot_' + month + ' where time between \'' + \
        startTime.strftime('%Y-%m-%d') + '\' and \'' + \
        endTime.strftime('%Y-%m-%d') + '\' ) t  WHERE t.row_num < 11;'
    sqlResult = selectOperaction(sql)
    finalResult = str(sqlResult).replace(
        '), (', '], [').replace(')]', ']]').replace('[(', '[[')
    FinalResult = eval(finalResult)
    return FinalResult


def DataShow(SelectTime):
    month = SelectTime[:6]
    startTime = datetime.datetime.strptime(SelectTime, "%Y%m%d")
    endTime = startTime+datetime.timedelta(days=1)
    sql = 'select node FROM weibohot_' + month + ' where time between \'' + startTime.strftime(
        '%Y-%m-%d') + '\' and \'' + endTime.strftime('%Y-%m-%d') + '\' group by node; '

    sqlResult = selectOperaction(sql)
    ColorJson = {}
    for nodes in sqlResult:
        node = nodes[0]
        ColorJson[node] = GetColor()
    return ColorJson


def DailyReport(SelectTime):
    month = SelectTime[:6]
    startTime = datetime.datetime.strptime(SelectTime, "%Y%m%d")
    endTime = startTime+datetime.timedelta(days=1)

    sqlString = 'select node ,count(*) FROM weibohot_' + month + ' where time between \'' + startTime.strftime(
        '%Y-%m-%d') + '\' and \'' + endTime.strftime('%Y-%m-%d') + '\' GROUP  BY 1 ORDER BY 2 desc'
    sqlResult = selectOperaction(sqlString)
    return sqlResult


def AutoCreateTable():
    month = datetime.datetime.now().strftime('%Y%m')
    sqlString = 'CREATE TABLE `weibohot_' + \
        month + '` (  `id` int NOT NULL AUTO_INCREMENT,  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,  `node` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `hot_num` int NOT NULL,  PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;'
    try:
        InsertOperaction(sqlString)
    except:
        Alert('添加weibohot_' + month + '表异常')
    return
