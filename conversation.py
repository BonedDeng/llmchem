import pandas as pd
import json
import os
def process(file_path):
    # 读取Excel文件
    # df = pd.read_excel('./data.xls', usecols=[9, 40])
    json_obj = {
        "type": "text_only",
        "instances": []
    }
    for file in file_path:
        df = pd.read_excel(file, usecols=[9, 40])
        data = df.to_dict(orient='records')
        for row in data:
            # for text, output_text in zip(row["Article Title"],row["Abstract"]):
            zp1 = str(row["Article Title"])
            zp2 = str(row["Abstract"])
            instance = {
                "text": f"{zp1}\n abstract: {zp2} \n\n"
            }
            json_obj["instances"].append(instance)
    json.dump(json_obj, open("./output.json", "w"), indent=4)
    # # 将数据转换为字典格式
    # data = df.to_dict(orient='records')
    #
    # json_obj = {
    #     "type": "text_only",
    #     "instances": []
    # }
    #
    # for row in data:
    #     # for text, output_text in zip(row["Article Title"],row["Abstract"]):
    #     zp1 = str(row["Article Title"])
    #     zp2 = str(row["Abstract"])
    #     instance = {
    #         "text": f"{zp1}\n Output: {zp2} \n\n"
    #     }
    #     json_obj["instances"].append(instance)
    #
    # # # 将 JSON 对象保存为文件
    # # with open("./output.json", "w") as f:
    # #     json.dump(json_obj, f)
    # json.dump(json_obj, open("./output.json", "w"), indent=4)

current_dir = os.getcwd()
print(current_dir)
json_obj = {
    "type": "text2text",
    "instances": []
}

conver = current_dir + '/input.json'
# print(conver)
#
# from_list = []
# value_list = []
#
with open(conver, 'r') as f:
    data = json.load(f)

for i, obj in enumerate(data):
    tm_obj = {
        "type": "text2text",
        "instances": []
    }
    for j, row in enumerate(obj['conversations']):
        print(i,row)
        # print(f'from: {conv["from"]}  value: {conv["value"]}')
        zp1 = str(row["value"])
        # zp2 = str(row["value"])
        if j == 0:
            instance = {
                # "input": f"{zp1}\n" , "output": f"{zp2}\n"
                "input": f"{zp1}\n"
            }
        if j == 1:
            instance = {
                # "input": f"{zp1}\n" , "output": f"{zp2}\n"
                "output": f"{zp1}\n"
            }
        tm_obj["instances"].append(instance)
    merged_dict = tm_obj['instances'][0]
    merged_dict.update(tm_obj['instances'][1])
    if i%2 != 0:
        json_obj["instances"].append(merged_dict)
json.dump(json_obj, open("./conversition.json", "w"), indent=4)

# for conversation in data:
# for message in conversation["conversations"]:
# from_list.append(message["from"])
# value_list.append(message["value"])
