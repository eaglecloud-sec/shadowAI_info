import os
import json
from datetime import datetime
from openai import OpenAI
import pandas as pd

def read_software_list(excel_path):
    df = pd.read_excel(excel_path)
    return df

def create_prompt(software_data):
    software_list = []
    for _, row in software_data.iterrows():
        software_list.append(f"{row['域名']} ")
    
    system_prompt = """作为团队的DLP安全分析师, 请根据[域名]简洁地分析域名的文件外发风险，重点关注所有可能泄露敏感信息的渠道：

1. 域名可信度判定: 
   - 全球知名的大型企业（微软/谷歌/苹果/XMind/阿里/腾讯/百度等）的正版域名
   - 有正规数字签名认证（可在属性页面查看）
   - 长期市场表现良好和稳定用户群体
   如果以上都不满足，判定为不可信

2. 文件外发渠道检查（重点关注敏感信息外发风险）：
   [社交分享]（必须满足以下条件之一才能判定为社交分享功能，注意浏览器访问社交网站不算此类）：
    A. 域名自身具备发布公开动态功能：
        * 内置社区且支持发布公开可见的图文/视频，具有独立的社区/动态界面
        * 本身具有发布到社交平台的直接对接功能
        * 本身集成社交平台API（如微博/微信/QQ等）且支持直接发布内容
        * 内置社区/朋友圈且支持发布公开可见的内容
    [即时通讯]
    B. 域名自身具备即时通讯功能：
        * 内置独立的即时通讯模块且支持文件传输
        * 本身集成IM服务且支持直接发送文件
        * 像现在的部分AI软件也可以算是即时通讯功能，因为可以传文件而且账号再多端共享
    注意事项：
    - 仅能通过浏览器访问社交网站的不计入此类
    - 仅有分享按钮但实际是跳转网页的不计入此类
    - 第三方插件提供的功能不计入此类
    - 必须是域名自身具备的功能才计入

    [云存储]（必须满足以下条件之一才能判定为云存储功能）：
    - 域名本身具备文件/图片上传功能:（类似于网盘网页版）
      * 支持用户主动上传自定义文件到云端（网页版网盘/网页版邮箱等）
      * 有明确的文件上传入口或界面
      * 支持多种文件格式的上传
    - 域名本身具备文件同步功能:
      * 协作性在线文档编辑（如Google Docs/Office 365）
      * 支持文件自动同步到云端（个人设备）
    注意事项：
    - 仅存储用户数据/密码/浏览记录等不算此类
    - 必须支持用户自定义文件的上传
    - 必须有明确的上传入口
    - 自动同步的系统数据不计入此类
    - 必须是域名自身提供的存储服务

   [远程控制]
   - 远程桌面（TeamViewer/向日葵/Todesk控制办公电脑）然后外发文件
   - 虚拟网络（VPN接入内网后访问文件服务器）

3. 外发风险评估：
    - 高风险：存在社交分享、云存储、远程控制等功能，且功能完善；域名主要功能就是文件传输/同步
    - 中风险：仅有部分外发渠道或功能不完善、仅仅能通过浏览器间接操作
    - 低风险：无明显外发渠道或功能  

注意事项：
- 对于部分域名的功能评估还不太准确，比如功能会有遗漏等
- 输出外发渠道的时候不要输出括号内的内容，输出时要带[]
- 必须基于官方文档或实际测试，​必须联网搜索确认功能存在性（如官网文档、用户手册），一定要联网搜索清楚，比如官网写的功能一定要录入。不要根据名字妄下定论
- 忽略系统日志、后台自动上传等非用户主动操作。
- 输出简洁，避免段落描述。
- 只列出域名已实现的功能（注意联网搜索）
- 不存在的功能对应标签不显示
- 重点关注敏感信息外发风险
- 外发渠道的说明只需要给出关键词即可
- 谨慎判断云存储和社交分享功能
- doubao是豆包AI聊天平台：www.doubao.com

输出格式要求（按顺序显示以下字段，外发渠道只显示存在的功能标签）：
域名名称: [名称]
域名描述: [用一句话描述域名的主要功能]
可信度: [可信/不可信]
外发风险: [高/中/低]
外发渠道：[社交分享]，[即时通讯]，[云存储]，[远程控制]
外发操作：
- [渠道1]: [具体的操作步骤，如菜单位置、按钮名称等]
- [渠道2]: [具体的操作步骤]

---"""
    
    # user_prompt = "请务必先联网搜索验证每个域名的真实用途，基于官方文档或实际测试结果分析。不要仅凭域名名称判断，对于无法确认的功能请标注'待验证'：\n" + "\n".join(software_list)
    user_prompt = "请分析域名中所有可能导致文件外发的功能，重点关注上传、导出、分享和第三方集成等渠道，不存在的功能对应的标签不要显示：\n" + "\n".join(software_list)
    return system_prompt, user_prompt

def analyze_software(excel_path):
    output_dir = "result"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        software_data = read_software_list(excel_path)
        print(f"读取到 {len(software_data)} 条域名数据")
        
        client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        
        system_prompt, user_prompt = create_prompt(software_data)        
        completion = client.chat.completions.create(
            model="qwen-max",
            # model="qwen-long",
            # model="qwen-plus",
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
        
        # 直接保存分析结果到txt文件
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
    # analyze_software("test.xlsx")
    # analyze_software("bangongmini.xlsx")
    analyze_software("lanjie.xlsx")