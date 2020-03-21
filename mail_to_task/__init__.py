from flask import Flask, request
import requests

app = Flask('mail_to_task')


@app.route('/', methods=['POST'])
def main():
    msg = request.json['plain'].strip()

    target = request.args['target']
    requests.post(target, msg.encode('utf-8'))
    return 'ok'


if __name__ == '__main__':
    app.run()
