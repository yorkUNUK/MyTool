import flask

api = flask.Flask(__name__)


@api.route('/callback', methods=['post'])
def callback():
    body = flask.request.json
    return body


if __name__ == '__main__':
    api.run(port=8999, debug=True, host='127.0.0.1')  # 启动服务
    # debug=True,改了代码后，不用重启，它会自动重启
    # 'host='127.0.0.1'别IP访问地址
