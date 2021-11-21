import json

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from jenkinsapi.jenkins import Jenkins

"""
访问地址：http://127.0.0.1:5000/testcase
"""

app = Flask(__name__)
CORS(app)
api = Api(app)

host = "localhost"
port = 3306
user = "root"
password = "zhy123456"
db = "testplatform"
charset = "utf8mb4"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset={charset}'.format(
    user=user, password=password, host=host, db=db, charset=charset)

db = SQLAlchemy(app)

jenkins = Jenkins(
    'http://192.168.30.8:8080/',
    username='admin',
    password='11d41f2fe7535bed739ce63c11f34a0216'
)

# testcases = []

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    steps = db.Column(db.String(1000), unique=False, nullable=True)

    def __repr__(self):
        return '<TestCase %r>' % self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'steps': self.steps
        }


# 测试用例的管理
class TestCaseService(Resource):
    def get(self):
        name = request.args.get('name', None)
        app.logger.info({'name': name})
        if name:
            testcase = TestCase.query.filter_by(name=name).first()
            return str(testcase)
        else:
            testcases = TestCase.query.all()
            app.logger.info({'testcases': testcases})
            return [testcase.as_dict() for testcase in testcases]

    def post(self):
        testcase = TestCase(
            id=request.json.get("id"),
            name=request.json.get('name'),
            steps=json.dumps(request.json.get("steps"))
        )

        # 插入数据
        db.session.add(testcase)
        db.session.commit()

        testcases = TestCase.query.all() # 取出所有数据
        return [str(testcase) for testcase in testcases]

    def put(self):
        pass

    def delete(self):
        name = request.json['name']
        testcase = TestCase.query.filter_by(name=name).first()
        db.session.delete(testcase)
        testcases = TestCase.query.all()
        app.logger.info({'testcases': testcases})
        return [str(testcase) for testcase in testcases]


# 测试套件，一个条件包含带有顺序的测试用例列表。
# 更复杂的情况是一个套件，可以包含子套件，子套件之间具备串并行关系
# xUnit概念
# pytest dir => [test_1.py::test_a, test_1.py::test_b, test_2.py::test_c]
# suite test_python.py
# suite [test_1.py::test_a, test_1.py::test_b, test_2.py::test_c]
class Suite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    testcases = db.Column(db.String(1000), unique=False, nullable=True)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'testcases': json.loads(self.testcases)
        }

    def __repr__(self):
        return '<Suite id=%d name=%r >' % (self.id, self.name)


class SuiteService(Resource):
    def get(self):
        id = request.args.get('id', None)
        app.logger.info({'id': id})
        if id:
            suite = Suite.query.filter_by(id=id).first()
            return str(suite)
        else:
            suites = Suite.query.all()
            app.logger.info({'suites': suites})
            return [suite.as_dict() for suite in suites]

    def post(self):
        suite = Suite(
            name=request.json.get('name'),
            testcases=json.dumps(request.json.get("testcases"))
        )

        db.session.add(suite)
        db.session.commit()

        suites = Suite.query.all()
        return [str(suite) for suite in suites]


# 根据套件的id，取到对应的存在的套件，并把套件的数据发送给jenkins进行执行
class ExecutionService(Resource):
    def post(self):
        suite_id = request.json.get('suite_id')
        suite = Suite.query.filter_by(id=suite_id).first()

        jenkins.jobs['testplatform_demo'].invoke(
            build_params={
                'suite': json.dumps(suite.as_dict()),
                'command': f'echo git clone https://github.com/hiyongz/demo.git .;'
                           f'echo 安装虚拟环境与依赖'
                           f'echo pytest {suite.testcases}'
                           f'echo 回传结果 curl'

            }
        )


class Result:
    pass


# jenkins通过curl命令或者全天的客户端工具，把测试结果，主要是junit.xml allure报告上传回来
class ResultService(Resource):
    pass


class Report:
    pass


api.add_resource(TestCaseService, '/testcase')
api.add_resource(SuiteService, '/suite')
api.add_resource(ExecutionService, '/execution')

if __name__ == '__main__':
    app.run(debug=True)
