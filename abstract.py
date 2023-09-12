import pandas as pd
import json

# 读取Excel文件
df = pd.read_excel('./data.xls', usecols=[9, 40])


# 将数据转换为字典格式
data = df.to_dict(orient='records')

json_obj = {
    "type": "text_only",
    "instances": []
}

for row in data:
    # for text, output_text in zip(row["Article Title"],row["Abstract"]):
    zp1 = str(row["Article Title"])
    zp2 = str(row["Abstract"])
    instance = {
        "text": f"{zp1}\n Output: {zp2} \n\n"
    }
    json_obj["instances"].append(instance)

# # 将 JSON 对象保存为文件
# with open("./output.json", "w") as f:
#     json.dump(json_obj, f)
json.dump(json_obj, open("./output.json", "w"), indent=4)
