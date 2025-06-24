import os
import json
from datetime import datetime
from openai import OpenAI
import pandas as pd

def read_software_list(excel_path):
    df = pd.read_excel(excel_path)
    if "软件版本" not in df.columns:
        df["软件版本"] = "未知"  
    return df

def create_prompt(software_data):
    software_list = []
    for _, row in software_data.iterrows():
        version = row['软件版本'] if pd.notna(row['软件版本']) else "未知"
        software_list.append(f"{row['软件名称']} {version}")
    
    system_prompt = """作为团队的DLP安全分析师, 请根据[软件名称]和[软件版本]简洁地分析软件的文件外发风险，重点关注所有可能泄露敏感信息的渠道：

1. 软件可信度判定: 
   - 全球知名的大型软件企业（微软/谷歌/苹果/XMind/阿里/腾讯/百度等）的正版软件
   - 在官方应用商店 (如Microsoft Store) 或官方网站下载
   - 有正规数字签名认证（可在属性页面查看）
   - 长期市场表现良好和稳定用户群体
   如果以上都不满足，判定为不可信

2. 文件外发渠道检查（重点关注敏感信息外发风险）：
   [社交分享]（必须满足以下条件之一才能判定为社交分享功能，注意浏览器访问社交网站不算此类）：
    A. 软件自身具备发布公开动态功能：
        * 软件内置社区且支持发布公开可见的图文/视频，具有独立的社区/动态界面
        * 软件本身具有发布到社交平台的直接对接功能
        * 软件本身集成社交平台API（如微博/微信/QQ等）且支持直接发布内容
        * 软件内置社区/朋友圈且支持发布公开可见的内容
    B. 软件自身具备即时通讯功能：
        * 内置独立的即时通讯模块且支持文件传输
        * 软件本身集成IM服务且支持直接发送文件
    注意事项：
    - 仅能通过浏览器访问社交网站的不计入此类
    - 仅有分享按钮但实际是跳转网页的不计入此类
    - 第三方插件提供的功能不计入此类
    - 必须是软件自身具备的功能才计入

    [云存储]（必须满足以下条件才能判定为云存储功能）：
    - 软件本身具备文件/图片上传功能:（类似于网盘）
      * 支持用户主动上传自定义文件到云端（网盘/邮箱等）
      * 有明确的文件上传入口或界面
      * 支持多种文件格式的上传
    - 软件本身具备文件同步功能:
      * 协作性在线文档编辑（如Google Docs/Office 365）
      * 支持文件自动同步到云端（个人设备）
    注意事项：
    - 仅存储用户数据/密码/浏览记录等不算此类
    - 必须支持用户自定义文件的上传
    - 必须有明确的上传入口
    - 自动同步的系统数据不计入此类
    - 必须是软件自身提供的存储服务


   [开发通道]
   - 代码托管（GitHub上传后设为private再转public）
   - 开发工具中转（Docker容器导出/日志写入）
   - 虚拟机（共享文件夹/发送到外部等）

   [远程控制]
   - 远程桌面（TeamViewer/向日葵/Todesk控制办公电脑）然后外发文件
   - 虚拟网络（VPN接入内网后访问文件服务器）

   [网页中转]
   - 通过浏览器插件或脚本将文件上传到外部网站（浏览器都会有的不要漏了）

   [文件传输]
   - 软件本身具备文件传输功能（如FTP/SFTP/HTTP上传）
3. 外发风险评估：
    - 高风险：存在社交分享、云存储、开发通道、远程控制等功能，且功能完善；软件主要功能就是文件传输/同步
    - 中风险：仅有部分外发渠道或功能不完善、仅仅能通过浏览器间接操作
    - 低风险：无明显外发渠道或功能  

注意事项：
- 对于部分软件的功能评估还不太准确，比如功能会有遗漏等
- 输出外发渠道的时候不要输出括号内的内容，输出时要带[]
- 必须基于官方文档或实际测试，​必须联网搜索确认功能存在性（如官网文档、用户手册），一定要联网搜索清楚，比如官网写的功能一定要录入。不要根据名字妄下定论，比如之前有说115浏览器其实还有社交功能的你都没写上
- 忽略系统日志、后台自动上传等非用户主动操作。
- 输出简洁，避免段落描述。
- 只列出软件已实现的功能（注意联网搜索）
- 不存在的功能对应标签不显示
- 重点关注敏感信息外发风险
- 外发渠道的说明只需要给出关键词即可
- 有些浏览器的网页中转功能不要判断漏了
- 谨慎判断云存储和社交分享功能

输出格式要求（按顺序显示以下字段，外发渠道只显示存在的功能标签）：
软件名称: [名称]
软件版本: [版本号]
应用描述: [用一句话描述软件的主要功能]
可信度: [可信/不可信]
外发风险: [高/中/低]
外发渠道：[社交分享]，[云存储]，[开发通道]，[远程控制]，[网页中转]，[文件传输]
外发操作：
- [渠道1]: [具体的操作步骤，如菜单位置、按钮名称等]
- [渠道2]: [具体的操作步骤]

---"""

    user_prompt = "请分析软件中所有可能导致文件外发的功能，重点关注上传、导出、分享和第三方集成等渠道，不存在的功能对应的标签不要显示：\n" + "\n".join(software_list)
    return system_prompt, user_prompt


def analyze_software(excel_path):
    output_dir = "result"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        software_data = read_software_list(excel_path)
        print(f"读取到 {len(software_data)} 条软件数据")
        
        client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        
        system_prompt, user_prompt = create_prompt(software_data)        
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
        analysis_result = result['choices'][0]['message']['content']
        
       
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_dir}/analysis_result_{timestamp}.txt"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(analysis_result)
        
        print(f"\n分析完成，结果已保存到: {output_file}")
            
    except Exception as e:
        print(f"处理出错: {str(e)}")

if __name__ == "__main__":
    # analyze_software("testmini.xlsx")
    # analyze_software("testWeb.xlsx")
    # analyze_software("testWeb2.xlsx")
    analyze_software("test.xlsx")
    # analyze_software("bangongmini.xlsx")