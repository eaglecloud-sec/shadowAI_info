import os
import json
from datetime import datetime
from openai import OpenAI
import pandas as pd
import requests
import whois
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urlparse
import googleapiclient.discovery
from serpapi import google_search
import json
import trafilatura
from urllib.parse import urljoin

def get_domain_info(domain):
    """获取域名WHOIS信息"""
    try:
        w = whois.whois(domain)
        return {
            "registrar": w.registrar,
            "creation_date": w.creation_date,
            "expiration_date": w.expiration_date,
            "name_servers": w.name_servers,
            "registrant": w.registrant
        }
    except Exception as e:
        return {"error": str(e)}

def check_icp_beian(domain):
    """检查网站ICP备案信息"""
    try:
        url = f"https://icp.chinaz.com/{domain}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 这里需要根据实际网页结构调整选择器
        beian_info = soup.find('div', class_='beian-info')
        return beian_info.text if beian_info else "未找到备案信息"
    except Exception as e:
        return f"查询备案信息失败: {str(e)}"

def extract_domain(url):
    """从URL中提取域名"""
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc
    except:
        return None

def search_specific_info(software_name, info_type):
    """搜索特定类型的信息"""
    try:
        search_queries = {
            "legal_entity": [
                f"{software_name} company registration",
                f"{software_name} legal entity",
                f"{software_name} 公司注册信息"
            ],
            "data_retention": [
                f"{software_name} data retention policy",
                f"{software_name} 数据保留政策"
            ],
            "data_collection": [
                f"{software_name} data collection policy",
                f"{software_name} 数据收集政策"
            ],
            "data_usage": [
                f"{software_name} data usage policy",
                f"{software_name} 数据使用政策"
            ],
            "data_sharing": [
                f"{software_name} data sharing policy",
                f"{software_name} 数据共享政策"
            ],
            "data_location": [
                f"{software_name} data center location",
                f"{software_name} 数据中心位置",
                f"{software_name} server location",
                f"{software_name} 服务器位置"
            ],
            "security_measures": [
                f"{software_name} security certifications",
                f"{software_name} 安全认证",
                f"{software_name} encryption protocols",
                f"{software_name} 加密协议",
                f"{software_name} TLS version",
                f"{software_name} SSL version",
                f"{software_name} security standards",
                f"{software_name} 安全标准",
                f"{software_name} ISO 27001",
                f"{software_name} SOC 2",
                f"{software_name} PCI DSS"
            ],
            "encryption_protocols": [
                f"{software_name} encryption protocols",
                f"{software_name} 加密协议",
                f"{software_name} TLS version",
                f"{software_name} SSL version",
                f"{software_name} transport encryption",
                f"{software_name} 传输加密",
                f"{software_name} security protocols",
                f"{software_name} 安全协议"
            ],
            "security_certifications": [
                f"{software_name} security certifications",
                f"{software_name} 安全认证",
                f"{software_name} security standards",
                f"{software_name} 安全标准",
                f"{software_name} ISO 27001",
                f"{software_name} SOC 2",
                f"{software_name} PCI DSS",
                f"{software_name} security compliance",
                f"{software_name} 安全合规"
            ]
        }
        
        results = []
        for query in search_queries.get(info_type, []):
            params = {
                "engine": "google",
                "q": query,
                "api_key": os.getenv("SERPAPI_API_KEY"),
                "num": 3
            }
            search_result = google_search(params)
            if search_result and "organic_results" in search_result:
                for result in search_result["organic_results"]:
                    results.append({
                        "title": result.get("title"),
                        "link": result.get("link"),
                        "snippet": result.get("snippet")
                    })
        
        return results
    except Exception as e:
        return f"搜索特定信息失败: {str(e)}"

def extract_privacy_policy_info(url, software_name):
    """从隐私政策页面提取具体信息"""
    try:
        # 下载并解析页面
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
            
            # 提取关键信息
            info = {
                "legal_entity": None,
                "data_collection": [],
                "data_usage": [],
                "data_retention": [],
                "data_sharing": [],
                "data_location": [],
                "security_measures": [],
                "encryption_protocols": [],  # 新增：加密协议
                "security_certifications": []  # 新增：安全认证
            }
            
            if text:
                # 提取法律实体信息
                legal_entity_patterns = [
                    r"(?:我们|We)\s+([A-Za-z\s,\.]+(?:LLC|Inc\.|Ltd\.|Corporation|Company))",
                    r"([A-Za-z\s,\.]+(?:LLC|Inc\.|Ltd\.|Corporation|Company))\s+(?:是|作为|as)\s+数据控制者",
                    r"([A-Za-z\s,\.]+(?:LLC|Inc\.|Ltd\.|Corporation|Company))\s+(?:负责|负责处理|processes)\s+您的数据"
                ]
                
                for pattern in legal_entity_patterns:
                    match = re.search(pattern, text)
                    if match:
                        info["legal_entity"] = match.group(1).strip()
                        break
                
                # 提取数据保留政策
                retention_sections = re.finditer(
                    r"(?:数据保留|数据存储|retention|storage).*?(?:天|月|年|days|months|years).*?(?=\n\n|\Z)",
                    text,
                    re.IGNORECASE | re.DOTALL
                )
                
                for section in retention_sections:
                    # 提取具体时间
                    time_match = re.search(r'(\d+)\s*(?:天|月|年|days|months|years)', section.group())
                    if time_match:
                        retention_time = time_match.group()
                        # 提取上下文
                        context = section.group()
                        info["data_retention"].append({
                            "time": retention_time,
                            "context": context.strip()
                        })
                
                # 提取数据收集信息
                collection_sections = re.finditer(
                    r"(?:我们收集|我们获取|we collect|we gather).*?(?=\n\n|\Z)",
                    text,
                    re.IGNORECASE | re.DOTALL
                )
                
                for section in collection_sections:
                    # 提取具体收集的数据类型
                    data_types = re.findall(r'(?:包括|including|such as)\s*([^。，,\.]+)', section.group())
                    if data_types:
                        info["data_collection"].append({
                            "types": data_types,
                            "context": section.group().strip()
                        })
                
                # 提取数据使用信息
                usage_sections = re.finditer(
                    r"(?:我们使用|we use|we process).*?(?=\n\n|\Z)",
                    text,
                    re.IGNORECASE | re.DOTALL
                )
                
                for section in usage_sections:
                    # 提取具体用途
                    purposes = re.findall(r'(?:用于|for|to)\s*([^。，,\.]+)', section.group())
                    if purposes:
                        info["data_usage"].append({
                            "purposes": purposes,
                            "context": section.group().strip()
                        })
                
                # 提取数据共享信息
                sharing_sections = re.finditer(
                    r"(?:我们共享|we share|we disclose).*?(?=\n\n|\Z)",
                    text,
                    re.IGNORECASE | re.DOTALL
                )
                
                for section in sharing_sections:
                    # 提取共享对象
                    recipients = re.findall(r'(?:与|with|to)\s*([^。，,\.]+)', section.group())
                    if recipients:
                        info["data_sharing"].append({
                            "recipients": recipients,
                            "context": section.group().strip()
                        })
                
                # 提取数据位置信息（增强版）
                location_sections = re.finditer(
                    r"(?:数据存储|服务器位置|数据中心|data storage|server location|data center).*?(?=\n\n|\Z)",
                    text,
                    re.IGNORECASE | re.DOTALL
                )
                
                for section in location_sections:
                    # 提取具体位置，包括国家、城市、具体地址
                    locations = re.findall(r'(?:位于|located in|stored in|data center in)\s*([^。，,\.]+)', section.group())
                    if locations:
                        info["data_location"].append({
                            "locations": locations,
                            "context": section.group().strip(),
                            "specific_address": re.findall(r'(?:地址|address|location):\s*([^。，,\.]+)', section.group())
                        })
                
                # 提取加密协议信息（新增）
                encryption_sections = re.finditer(
                    r"(?:加密协议|传输加密|encryption protocol|transport encryption|security protocol).*?(?=\n\n|\Z)",
                    text,
                    re.IGNORECASE | re.DOTALL
                )
                
                for section in encryption_sections:
                    # 提取具体的加密协议名称
                    protocols = re.findall(r'(?:使用|using|采用|adopting)\s*([A-Za-z0-9\.\-]+(?:\s+[A-Za-z0-9\.\-]+)*)', section.group())
                    if protocols:
                        info["encryption_protocols"].append({
                            "protocols": protocols,
                            "context": section.group().strip(),
                            "version": re.findall(r'(?:版本|version)\s*([0-9\.]+)', section.group())
                        })
                
                # 提取安全认证信息（新增）
                certification_sections = re.finditer(
                    r"(?:安全认证|安全标准|security certification|security standard).*?(?=\n\n|\Z)",
                    text,
                    re.IGNORECASE | re.DOTALL
                )
                
                for section in certification_sections:
                    # 提取具体的认证标准名称
                    certifications = re.findall(r'(?:符合|complies with|certified by|meets)\s*([A-Za-z0-9\.\-]+(?:\s+[A-Za-z0-9\.\-]+)*)', section.group())
                    if certifications:
                        info["security_certifications"].append({
                            "certifications": certifications,
                            "context": section.group().strip(),
                            "issuer": re.findall(r'(?:由|issued by|certified by)\s*([^。，,\.]+)', section.group())
                        })
                
                # 提取安全措施（增强版）
                security_sections = re.finditer(
                    r"(?:安全措施|security measures|encryption|保护|security protocol).*?(?=\n\n|\Z)",
                    text,
                    re.IGNORECASE | re.DOTALL
                )
                
                for section in security_sections:
                    # 提取具体措施，包括协议版本
                    measures = re.findall(r'(?:包括|including|such as|使用|using)\s*([^。，,\.]+)', section.group())
                    if measures:
                        info["security_measures"].append({
                            "measures": measures,
                            "context": section.group().strip(),
                            "protocol_versions": re.findall(r'(?:版本|version)\s*([0-9\.]+)', section.group())
                        })
            
            # 检查每个字段是否有具体数据，如果没有则搜索补充
            if not info["legal_entity"]:
                search_results = search_specific_info(software_name, "legal_entity")
                if search_results:
                    for result in search_results:
                        # 从搜索结果中提取公司名称
                        company_match = re.search(r'([A-Za-z\s,\.]+(?:LLC|Inc\.|Ltd\.|Corporation|Company))', result["snippet"])
                        if company_match:
                            info["legal_entity"] = company_match.group(1).strip()
                            break
            
            if not info["data_retention"]:
                search_results = search_specific_info(software_name, "data_retention")
                if search_results:
                    for result in search_results:
                        # 从搜索结果中提取保留时间
                        time_match = re.search(r'(\d+)\s*(?:天|月|年|days|months|years)', result["snippet"])
                        if time_match:
                            info["data_retention"].append({
                                "time": time_match.group(),
                                "context": result["snippet"],
                                "source": result["link"]
                            })
            
            if not info["data_collection"]:
                search_results = search_specific_info(software_name, "data_collection")
                if search_results:
                    for result in search_results:
                        # 从搜索结果中提取数据类型
                        data_types = re.findall(r'(?:收集|collects|gathers)\s*([^。，,\.]+)', result["snippet"])
                        if data_types:
                            info["data_collection"].append({
                                "types": data_types,
                                "context": result["snippet"],
                                "source": result["link"]
                            })
            
            if not info["data_usage"]:
                search_results = search_specific_info(software_name, "data_usage")
                if search_results:
                    for result in search_results:
                        # 从搜索结果中提取使用目的
                        purposes = re.findall(r'(?:用于|uses|for)\s*([^。，,\.]+)', result["snippet"])
                        if purposes:
                            info["data_usage"].append({
                                "purposes": purposes,
                                "context": result["snippet"],
                                "source": result["link"]
                            })
            
            if not info["data_sharing"]:
                search_results = search_specific_info(software_name, "data_sharing")
                if search_results:
                    for result in search_results:
                        # 从搜索结果中提取共享对象
                        recipients = re.findall(r'(?:与|shares with|discloses to)\s*([^。，,\.]+)', result["snippet"])
                        if recipients:
                            info["data_sharing"].append({
                                "recipients": recipients,
                                "context": result["snippet"],
                                "source": result["link"]
                            })
            
            # 补充搜索数据存储位置
            if not info["data_location"]:
                search_results = search_specific_info(software_name, "data_location")
                if search_results:
                    for result in search_results:
                        location_match = re.search(r'(?:located in|stored in|data center in)\s*([^。，,\.]+)', result["snippet"])
                        if location_match:
                            info["data_location"].append({
                                "locations": [location_match.group(1).strip()],
                                "context": result["snippet"],
                                "source": result["link"]
                            })
            
            # 补充搜索加密协议
            if not info["encryption_protocols"]:
                search_results = search_specific_info(software_name, "security_measures")
                if search_results:
                    for result in search_results:
                        protocol_match = re.search(r'(?:using|adopting)\s*([A-Za-z0-9\.\-]+(?:\s+[A-Za-z0-9\.\-]+)*)', result["snippet"])
                        if protocol_match:
                            info["encryption_protocols"].append({
                                "protocols": [protocol_match.group(1).strip()],
                                "context": result["snippet"],
                                "source": result["link"]
                            })
            
            return info
    except Exception as e:
        return {"error": str(e)}

def format_privacy_info(info):
    """格式化隐私政策信息"""
    formatted_info = []
    
    # 法律实体信息
    if info.get("legal_entity"):
        formatted_info.append(f"- **法律实体**：{info['legal_entity']}")
    
    # 数据收集信息
    if info.get("data_collection"):
        formatted_info.append("\n- **数据收集**：")
        for collection in info["data_collection"]:
            formatted_info.append(f"  - 收集类型：{', '.join(collection['types'])}")
            formatted_info.append(f"  - 上下文：{collection['context']}")
    
    # 数据使用信息
    if info.get("data_usage"):
        formatted_info.append("\n- **数据使用**：")
        for usage in info["data_usage"]:
            formatted_info.append(f"  - 使用目的：{', '.join(usage['purposes'])}")
            formatted_info.append(f"  - 上下文：{usage['context']}")
    
    # 数据保留信息
    if info.get("data_retention"):
        formatted_info.append("\n- **数据保留**：")
        for retention in info["data_retention"]:
            formatted_info.append(f"  - 保留时间：{retention['time']}")
            formatted_info.append(f"  - 上下文：{retention['context']}")
    
    # 数据共享信息
    if info.get("data_sharing"):
        formatted_info.append("\n- **数据共享**：")
        for sharing in info["data_sharing"]:
            formatted_info.append(f"  - 共享对象：{', '.join(sharing['recipients'])}")
            formatted_info.append(f"  - 上下文：{sharing['context']}")
    
    # 数据存储位置信息（增强版）
    if info.get("data_location"):
        formatted_info.append("\n- **数据存储位置**：")
        for location in info["data_location"]:
            formatted_info.append(f"  - 位置：{', '.join(location['locations'])}")
            if location.get("specific_address"):
                formatted_info.append(f"  - 具体地址：{', '.join(location['specific_address'])}")
            formatted_info.append(f"  - 上下文：{location['context']}")
            if location.get("source"):
                formatted_info.append(f"  - 来源：{location['source']}")
    
    # 加密协议信息（新增）
    if info.get("encryption_protocols"):
        formatted_info.append("\n- **加密协议**：")
        for protocol in info["encryption_protocols"]:
            formatted_info.append(f"  - 协议：{', '.join(protocol['protocols'])}")
            if protocol.get("version"):
                formatted_info.append(f"  - 版本：{', '.join(protocol['version'])}")
            formatted_info.append(f"  - 上下文：{protocol['context']}")
            if protocol.get("source"):
                formatted_info.append(f"  - 来源：{protocol['source']}")
    
    # 安全认证信息（新增）
    if info.get("security_certifications"):
        formatted_info.append("\n- **安全认证**：")
        for cert in info["security_certifications"]:
            formatted_info.append(f"  - 认证标准：{', '.join(cert['certifications'])}")
            if cert.get("issuer"):
                formatted_info.append(f"  - 认证机构：{', '.join(cert['issuer'])}")
            formatted_info.append(f"  - 上下文：{cert['context']}")
    
    # 安全措施信息（增强版）
    if info.get("security_measures"):
        formatted_info.append("\n- **安全措施**：")
        for measure in info["security_measures"]:
            formatted_info.append(f"  - 措施：{', '.join(measure['measures'])}")
            if measure.get("protocol_versions"):
                formatted_info.append(f"  - 协议版本：{', '.join(measure['protocol_versions'])}")
            formatted_info.append(f"  - 上下文：{measure['context']}")
    
    return "\n".join(formatted_info)

def search_privacy_policy(software_name, domain=None):
    """搜索软件的隐私政策"""
    try:
        # 构建搜索查询
        search_query = f"{software_name} privacy policy"
        if domain:
            search_query += f" site:{domain}"
        
        params = {
            "engine": "google",
            "q": search_query,
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "num": 3  # 获取前3个结果
        }
        
        results = google_search(params)
        
        privacy_links = []
        for result in results.get("organic_results", []):
            if "privacy" in result.get("link", "").lower():
                link = result.get("link")
                # 提取隐私政策信息
                policy_info = extract_privacy_policy_info(link, software_name)
                # 格式化信息
                formatted_info = format_privacy_info(policy_info)
                privacy_links.append({
                    "title": result.get("title"),
                    "link": link,
                    "snippet": result.get("snippet"),
                    "policy_info": policy_info,
                    "formatted_info": formatted_info
                })
        
        return privacy_links
    except Exception as e:
        return f"搜索隐私政策失败: {str(e)}"

def search_security_certifications(software_name):
    """搜索软件的安全认证"""
    try:
        search_query = f"{software_name} security certification ISO27001 SOC2"
        params = {
            "engine": "google",
            "q": search_query,
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "num": 3
        }
        
        results = google_search(params)
        
        cert_info = []
        for result in results.get("organic_results", []):
            if any(cert in result.get("snippet", "").lower() for cert in ["iso", "soc", "certification", "认证"]):
                cert_info.append({
                    "title": result.get("title"),
                    "link": result.get("link"),
                    "snippet": result.get("snippet")
                })
        
        return cert_info
    except Exception as e:
        return f"搜索安全认证失败: {str(e)}"

def search_data_storage(software_name, domain=None):
    """搜索软件的数据存储信息"""
    try:
        search_query = f"{software_name} data storage location server"
        if domain:
            search_query += f" site:{domain}"
        
        params = {
            "engine": "google",
            "q": search_query,
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "num": 3
        }
        
        results = google_search(params)
        
        storage_info = []
        for result in results.get("organic_results", []):
            if any(term in result.get("snippet", "").lower() for term in ["server", "storage", "data center", "数据中心"]):
                storage_info.append({
                    "title": result.get("title"),
                    "link": result.get("link"),
                    "snippet": result.get("snippet")
                })
        
        return storage_info
    except Exception as e:
        return f"搜索数据存储信息失败: {str(e)}"

def search_data_retention(software_name, domain=None):
    """搜索软件的数据保留政策"""
    try:
        search_query = f"{software_name} data retention policy"
        if domain:
            search_query += f" site:{domain}"
        
        params = {
            "engine": "google",
            "q": search_query,
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "num": 3
        }
        
        results = google_search(params)
        
        retention_info = []
        for result in results.get("organic_results", []):
            if any(term in result.get("snippet", "").lower() for term in ["retention", "retain", "delete", "保留", "删除"]):
                retention_info.append({
                    "title": result.get("title"),
                    "link": result.get("link"),
                    "snippet": result.get("snippet")
                })
        
        return retention_info
    except Exception as e:
        return f"搜索数据保留政策失败: {str(e)}"

def get_software_info(software_name, version):
    """获取软件详细信息"""
    info = {
        "domain_info": None,
        "icp_info": None,
        "privacy_policy": None,
        "security_certifications": None,
        "data_storage": None,
        "data_retention": None,
        "additional_info": {}
    }
    
    # 尝试从软件名称中提取可能的域名
    domain = extract_domain(software_name)
    if domain:
        info["domain_info"] = get_domain_info(domain)
        info["icp_info"] = check_icp_beian(domain)
        
        # 获取隐私政策
        info["privacy_policy"] = search_privacy_policy(software_name, domain)
        
        # 获取数据存储信息
        info["data_storage"] = search_data_storage(software_name, domain)
        
        # 获取数据保留政策
        info["data_retention"] = search_data_retention(software_name, domain)
    
    # 获取安全认证信息（不需要域名）
    info["security_certifications"] = search_security_certifications(software_name)
    
    return info

def read_software_list(excel_path):
    df = pd.read_excel(excel_path)
    if "软件版本" not in df.columns:
        df["软件版本"] = "未知"  # 如果没有版本号列,添加默认值
    return df

def create_prompt(software_data):
    software_list = []
    additional_info = {}
    
    for _, row in software_data.iterrows():
        version = row['软件版本'] if pd.notna(row['软件版本']) else "未知"
        software_name = row['软件名称']
        software_list.append(f"{software_name} {version}")
        
        # 获取额外信息
        additional_info[software_name] = get_software_info(software_name, version)
    
    # 简化的系统提示词
    system_prompt = """作为DLP安全分析师，请分析软件的文件外发和数据泄露风险。请严格按照以下格式输出每个软件的分析结果，注意：所有信息必须具体明确，禁止使用"未知"、"可能"、"大概"等模糊描述。如果确实无法获取信息，请标注"未找到官方信息"。

软件名称：[软件名称]

1. 基本信息
   - 域名：[具体域名，如www.example.com]
   - 类型：[具体类型，如web应用/插件/客户端应用等，可多选]
   - 风险等级：[高/中/低，必须基于具体分析给出]
   - 应用类型：[具体类型，如AI助手/知识问答等，可多选]

2. 威胁情报
   - 应用用途：[具体用途，列出所有主要功能]
   - 运营厂商：[具体厂商名称]
   - 数据存储位置：[具体服务器位置，如AWS us-east-1]
   - 数据传输加密方式：[具体加密协议，如TLS 1.3]
   - 是否境外应用：[是/否，如果是请说明具体国家]
   - 厂商合规性：[是否在中国设立数据中心，如有请说明具体位置]
   - 隐私政策：[具体政策名称和链接，如"隐私政策v2.0" https://example.com/privacy]
   - 安全认证标准：[具体认证名称，如SOC 2/ISO/IEC 27001/HiTrust/HIPAA/PCI DSS/GDPR]

3. 风险维度分析
应用用途评估：应用用途是否安全、数据、服务器是否位于京外、运营厂商情况
安全与隐私评估：数据跨境传输风险、敏感信息泄露风险、数据合规性风险、隐私政策、传输安全性
   - 数据跨境传输：[详细分析具体传输路径和风险点，给出高/中/低评级]
   - 敏感信息泄露：[详细分析具体泄露渠道和风险点，给出高/中/低评级]
   - 数据合规性：[详细分析具体合规要求和风险点，给出高/中/低评级]
   - 隐私政策：[详细分析具体政策内容和风险点，给出高/中/低评级]
   - 传输安全性：[详细分析具体传输方式和风险点，给出高/中/低评级]
处理建议：紧急处置建议、缓解措施、定期处置措施

4. 厂商合规性分析
   - 厂商名称：[具体公司名称]
   - 成立时间：[具体日期，如2020-01-01]
   - 总部位置：[具体地址]
   - 法律实体：[具体公司名称和类型，如"XX科技有限公司"]
   - 中国合规性：[具体合规情况，如"已获得ICP备案号：京ICP备XXXXXXXX号"]
   - 数据处理：[具体隐私政策名称和数据处理说明，如"根据《用户隐私政策v3.0》，会收集用户邮箱用于账号验证"]
   - 合规性评估：[结合前面所有具体要素的详细分析]

5. 功能分析
   - 主要功能：[具体功能列表，如"1. 文本生成 2. 图像处理 3. 数据分析"]
   - 数据传输方式：[具体传输方式，如"1. HTTPS API 2. WebSocket 3. SFTP"]
   - 数据存储位置：[具体服务器名称，如"AWS S3 us-east-1"]
   - 数据保留政策：[具体保留期限和用途，如"用户数据保留30天，用于服务优化"]
   - 功能风险评估：[结合前面所有具体要素的详细分析]

请确保：
- 所有信息必须具体明确，禁止使用模糊描述
- 所有数据必须有官方来源
- 所有分析必须基于具体事实
- 所有时间必须具体到日期
- 所有链接必须完整可访问

补充信息：
{additional_info}

注意：每个软件的分析结果之间用"---"分隔。"""

    # 将软件列表分批处理，每批最多3个软件
    batch_size = 3
    software_batches = [software_list[i:i + batch_size] for i in range(0, len(software_list), batch_size)]
    
    prompts = []
    for batch in software_batches:
        user_prompt = "请分析以下软件：\n" + "\n".join(batch)
        prompts.append((system_prompt, user_prompt))
    
    return prompts

def parse_analysis_result(analysis_text):
    results = []
    current_entry = {}
    current_section = None
    print("\n===开始解析结果===")
    
    # 预处理文本，移除可能的前导说明
    if "以下是" in analysis_text:
        analysis_text = analysis_text[analysis_text.find("软件名称:"):]
    
    for line in analysis_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        if line == '---':
            if current_entry and '软件名称' in current_entry:
                results.append(current_entry.copy())
                print(f"已解析一条记录: {current_entry['软件名称']}")
                current_entry = {}
                current_section = None
            continue
        
        # 检测章节标记
        if line.startswith('[') and line.endswith(']'):
            current_section = line.strip('[]')
            if current_section not in current_entry:
                current_entry[current_section] = []
            continue
        

        # 处理键值对
        if ':' in line:
            key, value = [x.strip() for x in line.split(':', 1)]
            key = key.replace('**', '').strip()
            if key in ['软件名称', '可信度', '外发风险']:
                current_entry[key] = value
            elif current_section and line.startswith('- '):
                current_entry[current_section].append(line[2:])  # 移除"- "前缀
    
    # 处理最后一条记录
    if current_entry and '软件名称' in current_entry:
        results.append(current_entry.copy())
    
    print(f"\n===解析完成===")
    print(f"共解析出 {len(results)} 条记录")
    return results

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
        
        prompts = create_prompt(software_data)
        all_results = []
        
        for i, (system_prompt, user_prompt) in enumerate(prompts, 1):
            print(f"\n处理第 {i}/{len(prompts)} 批软件...")
            
            completion = client.chat.completions.create(
                model="qwen-max",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.9,
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
            all_results.append(analysis_result)
            
            # 每批处理完后暂停一下，避免请求过于频繁
            if i < len(prompts):
                time.sleep(2)
        
        # 合并所有结果
        final_result = "\n\n".join(all_results)
        
        # 保存分析结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_dir}/analysis_result_{timestamp}.txt"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_result)
        
        print(f"\n分析完成，结果已保存到: {output_file}")
            
    except Exception as e:
        print(f"处理出错: {str(e)}")

if __name__ == "__main__":
    # analyze_software("testmini.xlsx")
    # analyze_software("testWeb.xlsx")
    # analyze_software("testWeb2.xlsx")
    analyze_software("detailTest.xlsx")
    # analyze_software("bangongmini.xlsx")