import mysql.connector, json
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)

# 连接数据库
def connect():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        #passwd = '264405'
        passwd = '',
        database = 'bloodline'
    )

# 查询头像列表
@app.route('/face')
def face():
    try:
        db = connect()
    except mysql.connector.Error as err:
        print('连接数据库失败:{}'.format(err))
    cursor = db.cursor()
    try:
        cursor.execute('select * from face')
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        print('查询头像列表失败:{}'.format(err))
    finally:
        cursor.close()
        db.close()
    template = ('id', 'type', 'job')
    res = [dict(zip(template, item)) for item in result]
    return json.dumps(res, ensure_ascii=False)

# 查询公会列表
@app.route('/guild')
def guild():
    try:
        db = connect()
    except mysql.connector.Error as err:
        print('连接数据库失败:{}'.format(err))
    cursor = db.cursor()
    try:
        cursor.execute('select id, name from guild')
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        print('查询公会列表失败:{}'.format(err))
    finally:
        cursor.close()
        db.close()
    template = ('id', 'name')
    res = [dict(zip(template, item)) for item in result]
    return json.dumps(res, ensure_ascii=False)

# 查询公会名
@app.route('/home')
def home():
    params = request.args
    try:
        db = connect()
    except mysql.connector.Error as err:
        print('连接数据库失败:{}'.format(err))
    cursor = db.cursor()
    try:
        cursor.execute('select name from guild where id = {}'.format(params['id']))
        result = cursor.fetchone()
    except mysql.connector.Error as err:
        print('查询公会信息失败:{}'.format(err))
    finally:
        cursor.close()
        db.close()
    if result:
        #template = ('name',)
        #return json.dumps(dict(zip(template, result)), ensure_ascii=False)
        return result[0]
    return ''

# 创建公会
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        params = request.json
        try:
            db = connect()
        except mysql.connector.Error as err:
            print('连接数据库失败:{}'.format(err))
        cursor = db.cursor()
        try:
            cursor.execute("insert into guild(name) values ('{}')".format(params['name']))
            db.commit()
            lastrowid = cursor.lastrowid
        except mysql.connector.Error as err:
            print('创建公会失败:{}'.format(err))
        finally:
            cursor.close()
            db.close()
        return str(lastrowid)
    return ''

# 登录公会
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        params = request.json
        try:
            db = connect()
        except mysql.connector.Error as err:
            print('连接数据库失败:{}'.format(err))
        cursor = db.cursor()
        try:
            cursor.execute("select count(*) from guild where id={0} and password='{1}'".format(params['id'], params['password']))
            result = cursor.fetchone()
        except mysql.connector.Error as err:
            print('登录密码校验失败:{}'.format(err))
        finally:
            cursor.close()
            db.close()
        return str(result[0])
    return ''

# 修改密码
@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        params = request.json
        try:
            db = connect()
        except mysql.connector.Error as err:
            print('连接数据库失败:{}'.format(err))
        cursor = db.cursor()
        try:
            rowcount = 0
            cursor.execute("select count(*) from guild where id={0} and password='{1}'".format(params['id'], params['pre_passwd']))
            result = cursor.fetchone()
            if result[0] > 0:
                cursor.execute("update guild set password='{0}' where id={1}".format(params['new_passwd'], params['id']))
                db.commit()
                rowcount = cursor.rowcount
        except mysql.connector.Error as err:
            print('修改密码失败:{}'.format(err))
        finally:
            cursor.close()
            db.close()
        return str(rowcount)
    return ''

# 查询队伍列表
@app.route('/team')
def team():
    params = request.args
    try:
        db = connect()
    except mysql.connector.Error as err:
        print('连接数据库失败:{}'.format(err))
    cursor = db.cursor()
    try:
        cursor.execute('select * from team where guild={} order by update_time'.format(params['id']))
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        print('查询队伍列表失败:{}'.format(err))
    finally:
        cursor.close()
        db.close()
    template = (
        'id',
        'name',
        'face1',
        'face2',
        'face3',
        'face4',
        'face5',
        'score',
        'update_time',
        'guild'
    )
    res = [ dict(zip(template, item)) for item in result ]
    return json.dumps(res, ensure_ascii=False)

# 新增队伍信息
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        params = request.json
        try:
            db = connect()
        except mysql.connector.Error as err:
            print('连接数据库失败:{}'.format(err))
        cursor = db.cursor()
        try:
            sql = "insert into team(name,update_time,guild) values ('{0}',{1},{2})".format(params['name'], params['update_time'], params['guild'])
            cursor.execute(sql)
            db.commit()
            lastrowid = cursor.lastrowid
        except mysql.connector.Error as err:
            print('新增队伍信息失败:{}'.format(err))
        finally:
            cursor.close()
            db.close()
        return str(lastrowid)
    return ''

# 查询队伍信息
@app.route('/user')
def user():
    params = request.args
    try:
        db = connect()
    except mysql.connector.Error as err:
        print('连接数据库失败:{}'.format(err))
    cursor = db.cursor()
    try:
        cursor.execute('select * from team where id = {}'.format(params['id']))
        result = cursor.fetchone()
    except mysql.connector.Error as err:
        print('查询队伍信息失败:{}'.format(err))
    finally:
        cursor.close()
        db.close()
    if not result:
        return ''
    template = (
        'id',
        'name',
        'face1',
        'face2',
        'face3',
        'face4',
        'face5',
        'score',
        'update_time',
        'guild'
    )
    res = dict(zip(template, result))
    return json.dumps(res, ensure_ascii=False)

# 更新队伍信息
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        params = request.json
        try:
            db = connect()
        except mysql.connector.Error as err:
            print('连接数据库失败:{}'.format(err))
        cursor = db.cursor()
        try:
            sql = 'update team set face1={0},face2={1},face3={2},face4={3},face5={4},score={5},update_time={6} where id={7}'.format(params['face1'] or 'NULL', params['face2'] or 'NULL', params['face3'] or 'NULL', params['face4'] or 'NULL', params['face5'] or 'NULL', params['score'], params['update_time'], params['id'])
            cursor.execute(sql)
            db.commit()
            rowcount = cursor.rowcount
        except mysql.connector.Error as err:
            print('更新队伍信息失败:{}'.format(err))
        finally:
            cursor.close()
            db.close()
        return str(rowcount)
    return ''

# 删除队伍信息
@app.route('/delete')
def delete():
    params = request.args
    try:
        db = connect()
    except mysql.connector.Error as err:
        print('连接数据库失败:{}'.format(err))
    cursor = db.cursor()
    try:
        cursor.execute('delete from team where id = {}'.format(params['id']))
        db.commit()
        rowcount = cursor.rowcount
    except mysql.connector.Error as err:
        print('删除队伍信息失败:{}'.format(err))
    finally:
        cursor.close()
        db.close()
    return str(rowcount)

# 公会防御设置
@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    if request.method == 'POST':
        params = request.json
        try:
            db = connect()
        except mysql.connector.Error as err:
            print('连接数据库失败:{}'.format(err))
        cursor = db.cursor()
        # 拼接sql
        sql = 'insert into defender(hold1,wall1,wall2,position,guild) values '
        for i in range(15):
            if i > 0:
                sql += ','
            hold1_id = 'NULL'
            if len(params['hold1']) > i:
                hold1_id = params['hold1'][i]['id']
            wall1_id = 'NULL'
            if len(params['wall1']) > i:
                wall1_id = params['wall1'][i]['id']
            wall2_id = 'NULL'
            if len(params['wall2']) > i:
                wall2_id = params['wall2'][i]['id']
            sql += '({0},{1},{2},{3},{4})'.format(hold1_id, wall1_id, wall2_id, i + 1, params['guild'])
        try:
            # 更新数据
            cursor.execute('delete from defender where guild={}'.format(params['guild']))
            db.commit()
            cursor.execute(sql)
            db.commit()
            rowcount = cursor.rowcount
        except mysql.connector.Error as err:
            print('更新防御部署失败:{}'.format(err))
        finally:
            cursor.close()
            db.close()
        return str(rowcount)
    return ''

# 布防详情
@app.route('/defender')
def defender():
    params = request.args
    try:
        db = connect()
    except mysql.connector.Error as err:
        print('连接数据库失败:{}'.format(err))
    cursor = db.cursor()
    try:
        sql = 'select hold1,wall1,wall2 from defender where guild={} order by position'.format(params['guild'])
        cursor.execute(sql)
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        print('查询防御信息失败:{}'.format(err))
    finally:
        cursor.close()
        db.close()
    template = ('hold1', 'wall1', 'wall2')
    res = [dict(zip(template, item)) for item in result]
    return json.dumps(res, ensure_ascii=False)

if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    #app.run(host='0.0.0.0')
    app.run(host='0.0.0.0', debug=True)
