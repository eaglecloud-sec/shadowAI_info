import os
import json
from datetime import datetime
from openai import OpenAI
import pandas as pd

def read_software_list(excel_path):
    return pd.read_excel(excel_path)

def create_prompt(software_data):
    software_list = []
    for _, row in software_data.iterrows():
        software_list.append(f"{row['域名']}")
        
    system_prompt = """作为一个专业的域名分析和命名专家，你需要：
1. 分析每个域名的含义、功能和特点
2. 为每个域名创建合适的中文描述名称

请按照以下格式输出结果，每行一个域名，用制表符(\\t)分隔域名和名称：

example.com    Example在线商城
cloudapp.net   Cloud应用平台
dataservice.com    数据服务平台

命名规则：
1. 品牌名称、产品名保持英文原样
2. 突出产品功能和用途
3. 可以中英文混合，但要确保易读易记
4. 对通用词汇和功能性描述进行中文翻译
5. 名称长度控制在2-6个词之间

分类要求：
- 根据域名特征准确判断其可能的使用场景
- 选择恰当的分类标签
- 保持分类的一致性和准确性

---"""

    user_prompt = f"请分析并为以下域名设计合适的中文名称：\n{chr(10).join(software_list)}"
    return system_prompt, user_prompt


def process_domains(df, batch_size=50):
    """批量处理域名"""
    results = []
    total = len(df)
    
    for i in range(0, total, batch_size):
        batch = df[i:i + batch_size]
        system_prompt, user_prompt = create_prompt(batch)
        
        try:
            client = OpenAI(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
            
            completion = client.chat.completions.create(
                model="qwen-max",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                extra_body={
                    "enable_thinking": True,
                    "search_options": {
                        "enable": True
                    },
                    "enable_search": True
                }
            )
            
            result = json.loads(completion.model_dump_json())
            content = result['choices'][0]['message']['content']
            # 将内容按行分割，去掉空行
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            results.extend(lines)
            
        except Exception as e:
            print(f"处理批次 {i//batch_size + 1} 时发生错误: {str(e)}")
            continue
            
    return results

def save_results(results, output_file=None):
    """保存处理结果"""
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"result/analysis_result_{timestamp}.txt"
        
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(results))
        print(f"结果已保存到: {output_file}")
    except Exception as e:
        print(f"保存结果时发生错误: {str(e)}")
        return False
    return True

def analyze_software(excel_path):
    output_dir = "result"
    os.makedirs(output_dir, exist_ok=True)
    
    software_data = read_software_list(excel_path)
    print(f"读取到 {len(software_data)} 条域名数据")
    
    results = process_domains(software_data)
    save_results(results)

def main():
    input_file = "testWeb.xlsx"
    df = pd.read_excel(input_file)
    print(f"读取到 {len(df)} 条域名数据")
    
    results = process_domains(df)
    if results:
        save_results(results)
    else:
        print("处理过程中没有生成结果")

if __name__ == "__main__":
    main()