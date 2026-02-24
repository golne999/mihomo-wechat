import requests
import json

# sing-box 原始 JSON 链接
source_url = "https://raw.githubusercontent.com/senshinya/singbox_ruleset/main/rule/WeChat/WeChat.json"

# 您需要固定的企业微信及通用依赖域名 (去除 - 和 DIRECT，符合 Clash List Payload 格式)
custom_rules = [
    # 企业微信专用
    "DOMAIN-SUFFIX,wxwork.qq.com",
    "DOMAIN-SUFFIX,work.weixin.qq.com",
    "DOMAIN-SUFFIX,wecom.work",
    "DOMAIN-SUFFIX,wxworklive.com",
    
    # 资源与图片
    "DOMAIN-SUFFIX,qpic.cn",
    "DOMAIN-SUFFIX,qlogo.cn",
    "DOMAIN-SUFFIX,qlog.cn",
    
    # 腾讯通用依赖
    "DOMAIN-SUFFIX,weixin.qq.com",
    "DOMAIN-SUFFIX,servicewechat.com",
    
    # 关键字兜底
    "DOMAIN-KEYWORD,wxwork",
    "DOMAIN-KEYWORD,wecom"
]

def convert():
    try:
        print(f"正在转换至纯文本 List 格式...")
        response = requests.get(source_url)
        response.raise_for_status()
        data = response.json()
        
        # 映射关系：sing-box 键名 -> Clash List 规则前缀
        rule_map = {
            "domain": "DOMAIN",
            "domain_suffix": "DOMAIN-SUFFIX",
            "domain_keyword": "DOMAIN-KEYWORD",
            "ip_cidr": "IP-CIDR",
            "ip_prefix": "IP-CIDR"
        }
        
        # 使用 set 可以自动去重
        result_list = set()
        
        # 1. 解析线上 JSON 规则
        for rule_item in data.get("rules", []):
            for sb_key, clash_prefix in rule_map.items():
                values = rule_item.get(sb_key, [])
                if isinstance(values, str): values = [values]
                
                for val in values:
                    if clash_prefix == "IP-CIDR":
                        # IP 类型按照你的要求加上 ,no-resolve
                        result_list.add(f"{clash_prefix},{val},no-resolve")
                    else:
                        # 域名类型直接拼接
                        result_list.add(f"{clash_prefix},{val}")
        
        # 2. 将固定的自定义规则加入到集合中
        for custom_rule in custom_rules:
            result_list.add(custom_rule)
            
        # 排序并转为列表
        final_output = sorted(list(result_list))

        # 写入文件
        with open("WeChat.list", "w", encoding="utf-8") as f:
            f.write("\n".join(final_output))
            
        print(f"转换成功！已生成 WeChat.list，共 {len(final_output)} 条规则。")

    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    convert()
