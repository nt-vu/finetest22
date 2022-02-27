from flask import *
import json, time


app = Flask(__name__)


f = open("data.json", encoding="utf-8")
data = json.load(f)
f.close()

@app.route('/', methods=['GET'])
def home_page():
	data_set = {"Page": "Home", "Message": "Successfully loaded the Home Page"}
	json_dump = json.dumps(data_set)
	return json_dump


@app.route('/user_id/', methods=['GET'])
def request_page():
	data_set = {"id": list(data.keys())}
	return json.dumps(data_set)


@app.route('/subject/', methods=['GET'])
def request_subject():
	user_id = str(request.args.get('id'))
	data_set = {"subject": list(data[user_id]["subject"].keys())}
	return json.dumps(data_set)

@app.route('/exercise/', methods=['GET'])
def request_exercise():
	# print(data["2051063451"]["subject"]["TTUD"]["exercise"])
	user_id = str(request.args.get('usid'))
	subject_id = str(request.args.get('sjid'))
	data_set = {"exercise": dict(data[user_id]["subject"][subject_id]["exercise"])}
	# data_set = {"1" : True}
	return json.dumps(data_set)
	
if __name__ == '__main__':
	app.run()
