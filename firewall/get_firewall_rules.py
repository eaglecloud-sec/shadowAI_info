import requests
import json
from datetime import datetime
import os

CONFIG_URL = "http://10.1.2.15:3000/api/rules"

def get_firewall_rules():
    """获取防火墙规则配置"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Firewall-Test-Suite/1.0"
    }
    
    try:
        response = requests.get(CONFIG_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 尝试解析响应内容
        try:
            rules = response.json()
        except json.JSONDecodeError:
            print(f"错误：无法解析响应内容为JSON格式")
            print(f"响应头：{dict(response.headers)}")
            print(f"响应状态码：{response.status_code}")
            print(f"原始响应内容：\n{response.text[:1000]}...")  # 只打印前1000个字符
            return None
            
        return rules
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")
        return None

def format_rules(rules):
    """格式化规则配置为易读的格式"""
    if not rules:
        return "未获取到规则配置"
        
    output = []
    output.append("=== 防火墙规则配置 ===")
    output.append(f"获取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 遍历所有规则类别
    for category, category_rules in rules.items():
        output.append(f"\n## {category}")
        output.append("-" * 50)
        
        # 如果是列表类型的规则
        if isinstance(category_rules, list):
            for i, rule in enumerate(category_rules, 1):
                output.append(f"\n规则 {i}:")
                for key, value in rule.items():
                    output.append(f"  {key}: {value}")
        
        # 如果是字典类型的规则
        elif isinstance(category_rules, dict):
            for key, value in category_rules.items():
                output.append(f"\n{key}:")
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        output.append(f"  {sub_key}: {sub_value}")
                else:
                    output.append(f"  {value}")
        
        output.append("\n" + "=" * 50)
    
    return "\n".join(output)

def save_rules(rules_text):
    """保存规则配置到文件"""
    # 创建results目录（如果不存在）
    results_dir = "test_results"
    os.makedirs(results_dir, exist_ok=True)
    
    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(results_dir, f"firewall_rules_{timestamp}.txt")
    
    # 保存规则配置
    with open(filename, "w", encoding="utf-8") as f:
        f.write(rules_text)
    
    return filename

def main():
    print("正在获取防火墙规则配置...")
    
    # 获取规则
    rules = get_firewall_rules()
    if not rules:
        print("获取规则失败")
        return
    
    # 格式化规则
    formatted_rules = format_rules(rules)
    
    # 保存规则到文件
    filename = save_rules(formatted_rules)
    
    # 打印规则到终端
    print("\n" + formatted_rules)
    print(f"\n规则配置已保存到文件：{filename}")

if __name__ == "__main__":
    main() 