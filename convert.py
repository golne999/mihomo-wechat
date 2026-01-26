import requests
import json


source_url = "https://raw.githubusercontent.com/senshinya/singbox_ruleset/main/rule/WeChat/WeChat.json"

def convert():
    try:
        print(f"正在抓取 sing-box 规则: {source_url}")
        response = requests.get(source_url)
        response.raise_for_status()
        data = response.json()
        
        # 映射关系：sing-box 字段名 -> Mihomo 规则名
        rule_map = {
            "domain": "DOMAIN",
            "domain_suffix": "DOMAIN-SUFFIX",
            "domain_keyword": "DOMAIN-KEYWORD",
            "ip_cidr": "IP-CIDR",
            "ip_prefix": "IP-CIDR"
        }
        
        yaml_rules = set()
        
        # 遍历 JSON 中的 rules 数组
        for rule_item in data.get("rules", []):
            for sb_key, mihomo_type in rule_map.items():
                values = rule_item.get(sb_key, [])
                if isinstance(values, str): # 有时是单条字符串而非列表
                    values = [values]
                
                for val in values:
                    # 统一格式为：'TYPE,VALUE'
                    yaml_rules.add(f"  - '{mihomo_type},{val}'")
        
        # 写入文件
        with open("WeChat.yaml", "w", encoding="utf-8") as f:
            f.write("payload:\n")
            # 排序后写入，方便在 GitHub 查看差异
            f.write("\n".join(sorted(list(yaml_rules))))
            
        print(f"转换成功！共生成 {len(yaml_rules)} 条规则。")

    except Exception as e:
        print(f"转换过程中出错: {e}")

if __name__ == "__main__":
    convert()
