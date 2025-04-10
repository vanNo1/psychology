

import json
import pandas as pd

def parse_log_file(file_path):
    results = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # 跳过空行
                try:
                    # 解析每行的 JSON
                    log_entry = json.loads(line.strip())
                    
                    # 获取 content 中的 JSON 字符串
                    content = log_entry['content']
                    
                    # 解析 IP ID
                    ip_start = content.find('ip=|') + 4  # 跳过'ip=|'
                    ip_end = content.find('|', ip_start)  # 找到下一个'|'的位置
                    ip_id = content[ip_start:ip_end]
                    
                    # 解析 result = 后面的 JSON
                    json_start = content.find('result =') + 8
                    result_json = content[json_start:]
                    result_dict = json.loads(result_json)
                    
                    # 将 ip_id 添加到结果字典中
                    result_dict['ip_id'] = ip_id
                    
                    results.append(result_dict)
                    
                except json.JSONDecodeError as e:
                    print(f"解析错误: {e}")
                    continue
                except Exception as e:
                    print(f"其他错误: {e}")
                    continue
    
    return results


if __name__ == "__main__":
    # 使用示例
    file_path = 'app/test/downloaded_data.txt'
    parsed_results = parse_log_file(file_path)
    res =[]
    excel_list = []
    for line in parsed_results:
        res.append({"data":{"result":line.get("result"),"success":line.get("success")},"ip_id":line.get("ip_id")})
    for obj in res:
        excel_list.append({"data": json.dumps(obj.get("data"), ensure_ascii=False),"ip_id":obj.get("ip_id")})
    print(len(res))
     # 创建DataFrame
    df = pd.DataFrame(excel_list)
    
    # 保存为Excel
    output_file = 'output_results_2.xlsx'
    df.to_excel(output_file, index=False)
    
    print(f"共处理 {len(parsed_results)} 条记录")
    print(f"结果已保存到 {output_file}")

    # # 打印解析结果
    # for idx, result in enumerate(parsed_results):
    #     print(f"Log Entry {idx + 1}:")
    #     print(result)
    #     print("-" * 50)
