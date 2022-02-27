# import json
# f = open("user_exercise.json", encoding="utf-8")
# ex = json.load(f)
# f.close()

# f = open("subject.json", encoding="utf-8")
# sj = json.load(f)
# f.close()

# f = open("data.json", "w", encoding="utf-8")
# f.write("{\n\t")
# for j in range(2):
# 	if j == 0:
# 		temp = "2051063451"
# 	else:
# 		temp = "1"

# 	f.write(f'"{temp}":@\n\t\t"name" : "Nguyễn Tuấn Vũ",\n\t\t"subject" : @\n\t\t\t"id" : "TTUD",\n\t\t\t"name" : "Thuật toán ứng dụng",\n\t\t\t"title_total" : 10,\n\t\t\t"mark" : 100\n\t\t\t#,\n\t\t"exercise" : @')
# 	for i in ex:
# 		f.write(f'\n\t\t\t"{i["exercise_id"]}":@\n\t\t\t\t"mark" : {i["mark"]},\n\t\t\t\t"submit_times" : {i["submit"]},\n\t\t\t\t"subject_id" : "TTUD"\n\t\t\t\t#\n\t\t\t#,')
# 	f.write('\n\t,\n\t')
# f.write("#")



import json

f = open("data.json", encoding="utf-8")
data = json.load(f)
# print(data.keys())

print(list(data["2051063451"]["subject"]["TTUD"]["exercise"]))