import pandas as pd
import datetime
import os

# df = pd.read_excel('analyze7.xlsx')
# df = pd.read_excel('analyze30.xlsx')
df = pd.read_excel('analyzeNO90.xlsx')

# 按URL分组统计
url_counts = df.groupby('url').size()

url_stats = df.groupby('url')['file_level'].agg(['max', lambda x: x.value_counts().to_dict()]).reset_index()
url_stats.columns = ['url', 'max_level', 'level_counts']

results = []
for _, row in url_stats.iterrows():
    url = row['url']
    count = url_counts[url]
    max_level = row['max_level']
    level_counts = row['level_counts']
    
    # 检查条件：事件数量>=20且最高等级为L5或L6
    if count >= 20 and max_level in ['L5', 'L6']:
        level_count = level_counts.get(max_level, 0)
        results.append({
            'url': url,
            'total_events': count,
            'max_level': max_level,
            'max_level_count': level_count
        })

results.sort(key=lambda x: x['total_events'], reverse=True)

os.makedirs('result', exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'result/analysis_result_{timestamp}.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("分析结果：\n")
    f.write("符合条件的URL (事件数量>=20且最高等级为L5或L6)：\n\n")
    for item in results:
        f.write(f"URL: {item['url']}\n")
        f.write(f"总事件数量: {item['total_events']}\n")
        f.write(f"最高文件等级: {item['max_level']}\n")
        f.write(f"最高等级出现次数: {item['max_level_count']}\n")
        f.write("-" * 50 + "\n")

print(f"分析完成！结果已保存到文件：{output_file}")

