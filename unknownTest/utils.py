import whois
import requests
import socket
import json
import re
import os
import urllib.parse
from typing import Dict, Optional, List, Any
from datetime import datetime

def get_domain_info(domain: str) -> Dict[str, Any]:
    """获取域名的whois信息"""
    try:
        w = whois.whois(domain)
        return {
            "registrar": w.registrar,
            "creation_date": w.creation_date,
            "country": w.country,
            "org": w.org,
            "registrant": w.registrant,
            "emails": w.emails,
            "name_servers": w.name_servers
        }
    except Exception as e:
        return {"error": f"Domain info not found: {str(e)}"}

def get_icp_info(domain: str) -> Optional[Dict]:
    """获取网站ICP备案信息"""
    try:
        # 使用第三方API获取ICP信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        api_url = f"https://api.vvhan.com/api/icp?url={domain}"
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return {"error": f"ICP info not found: {str(e)}"}

def get_server_location(domain: str) -> Dict[str, Any]:
    """获取服务器地理位置信息"""
    try:
        ip = socket.gethostbyname(domain)
        # 使用IP地理位置API
        api_url = f"https://ip.taobao.com/outGetIpInfo?ip={ip}&accessKey=alibaba-inc"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"ip": ip, "error": "Location lookup failed"}
    except Exception as e:
        return {"error": f"Server location not found: {str(e)}"}

def analyze_risk_level(data: Dict[str, Any]) -> Dict[str, Any]:
    """风险等级评估"""
    risk_score = 0
    risk_factors = []
    
    # 1. 数据跨境传输风险评估
    if data.get("is_foreign_company"):
        risk_score += 30
        risk_factors.append({
            "type": "data_transfer",
            "level": "高",
            "reason": "境外企业,存在数据跨境传输风险"
        })
    
    # 2. 服务器位置风险评估
    server_location = data.get("server_location", "未知")
    if server_location not in ["中国", "China", "CN"]:
        risk_score += 20
        risk_factors.append({
            "type": "server_location", 
            "level": "中",
            "reason": f"服务器位于{server_location},存在数据出境风险"
        })
    
    # 3. 合规风险评估
    if not data.get("has_icp"):
        risk_score += 15
        risk_factors.append({
            "type": "compliance",
            "level": "中",
            "reason": "未发现ICP备案信息"
        })
    
    # 4. 数据收集风险评估
    sensitive_data_types = data.get("sensitive_data_types", [])
    if sensitive_data_types:
        risk_score += len(sensitive_data_types) * 5
        risk_factors.append({
            "type": "data_collection",
            "level": "中" if len(sensitive_data_types) < 5 else "高",
            "reason": f"收集敏感数据类型: {', '.join(sensitive_data_types)}"
        })
    
    # 5. 安全传输评估
    if not data.get("uses_encryption"):
        risk_score += 15
        risk_factors.append({
            "type": "transmission",
            "level": "中",
            "reason": "未发现加密传输方式"
        })
    
    # 计算总体风险等级
    final_risk_level = "低" if risk_score < 30 else "中" if risk_score < 60 else "高"
    
    return {
        "risk_level": final_risk_level,
        "risk_score": risk_score,
        "risk_factors": risk_factors,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def extract_sensitive_info_types(privacy_policy: str) -> List[str]:
    """从隐私政策中提取敏感信息类型"""
    sensitive_patterns = {
        "个人身份信息": r"身份证|护照|驾驶证|社会保障|银行卡",
        "位置信息": r"GPS|定位|地理位置|位置信息",
        "生物特征": r"指纹|面部|虹膜|声纹|生物特征",
        "通讯信息": r"通讯录|联系人|电话号码|短信|邮箱",
        "设备信息": r"设备标识|MAC地址|IMEI|设备名称",
        "网络信息": r"IP地址|浏览记录|Cookie|日志",
        "支付信息": r"支付|银行卡|交易|账户"
    }
    
    found_types = []
    for type_name, pattern in sensitive_patterns.items():
        if re.search(pattern, privacy_policy):
            found_types.append(type_name)
    
    return found_types

def format_analysis_result(software_name: str, version: str, domain_info: Dict, 
                         icp_info: Dict, server_info: Dict, risk_analysis: Dict, 
                         ai_analysis: str) -> str:
    """格式化分析结果"""
    result = f"""
# {software_name} v{version} 安全分析报告
生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 基础信息分析
### 域名信息
- 注册商: {domain_info.get('registrar', '未知')}
- 注册时间: {domain_info.get('creation_date', '未知')}
- 注册组织: {domain_info.get('org', '未知')}
- 注册国家/地区: {domain_info.get('country', '未知')}

### ICP备案信息
{json.dumps(icp_info, ensure_ascii=False, indent=2) if icp_info else '未找到ICP备案信息'}

### 服务器信息
{json.dumps(server_info, ensure_ascii=False, indent=2)}

## 风险评估结果
### 总体风险等级: {risk_analysis['risk_level']}
### 风险得分: {risk_analysis['risk_score']}
### 具体风险因素:
{json.dumps(risk_analysis['risk_factors'], ensure_ascii=False, indent=2)}

## AI分析结果
{ai_analysis}
"""
    return result

def search_official_domain(software_name: str) -> str:
    """
    通过搜索方式获取软件的官方域名
    """
    try:
        # 构建搜索词
        search_terms = [
            f"{software_name} official website",
            f"{software_name} 官网",
            f"{software_name} privacy policy",
            f"{software_name} terms of service"
        ]
        
        found_domains = set()
        for term in search_terms:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # 使用搜索引擎API搜索
            search_url = f"https://api.bing.microsoft.com/v7.0/search"
            params = {
                "q": term,
                "count": 5,
                "responseFilter": "Webpages"
            }
            headers["Ocp-Apim-Subscription-Key"] = os.getenv("BING_API_KEY")
            
            response = requests.get(search_url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                results = response.json().get("webPages", {}).get("value", [])
                for result in results:
                    url = result.get("url", "")
                    # 提取域名
                    if url:
                        try:
                            parsed = urllib.parse.urlparse(url)
                            domain = parsed.netloc
                            if any(keyword in result.get("name", "").lower() + result.get("snippet", "").lower() 
                                  for keyword in ["official", "官网", "privacy", "terms", "隐私", "条款"]):
                                found_domains.add(domain)
                        except:
                            continue
        
        # 找出出现频率最高的域名
        if found_domains:
            return max(found_domains, key=lambda x: len([d for d in found_domains if x in d]))
            
        return "domain_not_found"
        
    except Exception as e:
        print(f"域名搜索失败: {str(e)}")
        return "domain_not_found"
