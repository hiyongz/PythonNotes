from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from jenkinsapi.jenkins import Jenkins

app = Flask(__name__)
# done: 输出中文json
app.config["JSON_AS_ASCII"] = False

#允许跨域访问
CORS(app)

# 使用了RESTFul扩展
api = Api(app)

# 数据库的配置
host = "localhost"
port = 3306
user = "root"
password = "zhy123456"
db = "testdb"
charset = "utf8mb4"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset={charset}'.format(
    user=user, password=password, host=host, db=db, charset=charset)
# 使用sqlalchemy扩展
db = SQLAlchemy(app)

# token管理
app.config['JWT_SECRET_KEY'] = 'ceshiren.com'  # Change this!
jwt = JWTManager(app)

# 使用jenkins做任务分发
jenkins = Jenkins(
    'http://stuq.ceshiren.com:8020/',
    username='seveniruby',
    password='11743b5e008e546ec1e404933d00b35a07'
)


# 用户数据存储的表结构
class User(db.Model):
    # 可选，指定对应的表
    __tablename__ = "seveniruby_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# 测试用例存储的表结构
class TestCase(db.Model):
    __tablename__ = "seveniruby_testcase"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    data = db.Column(db.String(1024), unique=False, nullable=False)

    def __repr__(self):
        return '<TestCase %r>' % self.name


# 对外的api定义
class TestCaseApi(Resource):
    # 需要token验证
    @jwt_required
    def get(self):
        r = []
        # 查询所有表内数据
        for t in TestCase.query.all():
            res = {}
            res['id'] = t.id
            res['name'] = t.name
            res['description'] = t.description
            res['data'] = t.data
            r.append(res)
        return r

    @jwt_required
    def post(self):
        t = TestCase(
            name=request.json['name'],
            description=request.json['description'],
            data=request.json['data']
        )
        # 新增数据
        db.session.add(t)
        db.session.commit()
        return {
            'msg': 'ok'
        }

    # todo：更新用例
    @jwt_required
    def put(self):
        pass

    # todo: 删除用例
    @jwt_required
    def delete(self):
        pass


class LoginApi(Resource):
    # 无需验证
    def get(self):
        # User.query.all()
        return {'hello': 'world'}

    # 用户登录
    def post(self):
        # done: 查询数据库
        username = request.json.get('username', None)
        # todo: 通常密码不建议原文存储
        password = request.json.get('password', None)
        # 查数据库，取出符合条件的第一条
        user = User.query.filter_by(username=username, password=password).first()
        # done：生成返回结构体
        if user is None:
            return jsonify(
                errcode=1,
                errmsg='用户名或者密码不对'
            )
        else:
            # done: 生成token
            return {
                'errcode': 0,
                'errmsg': 'ok',
                'username': user.username,
                # 生成token，用于后续的testcase访问
                'token': create_access_token(identity=user.username)
            }

    # todo: 注册
    def put(self):
        pass

    # todo:注销
    def delete(self):
        pass


# 用例调度
class TaskApi(Resource):
    # todo: 查询所有的任务
    def get(self):
        pass

    @jwt_required
    def post(self):
        # todo: 用例获取
        testcases = request.json.get('testcases', None)
        # done: 调度jenkins，驱动job执行
        jenkins['testcase'].invoke(
            securitytoken='11743b5e008e546ec1e404933d00b35a07',
            build_params={
                'testcases': testcases
            })

        return {
            'errcode': 0,
            'errmsg': 'ok'
        }

        # todo: 结果交给其他接口异步处理


# 数据获取与数据展示
class ReportApi(Resource):
    def get(self):
        # 展示报告数据和曲线图

        pass

    def post(self):
        # todo: pull模式 主动从jenkins中拉取数据
        jenkins['testcase'].get_last_build().get_resultset()
        # todo: push模式 让jenkins node主动push到服务器
        # todo: 把测试报告数据与测试报告文件保存
        pass


api.add_resource(TestCaseApi, '/testcase')
api.add_resource(LoginApi, '/login')
api.add_resource(TaskApi, '/task')
# todo: 注册
# api.add_resource(RegistryApi, '/regist')


if __name__ == '__main__':
    app.run(debug=True)
