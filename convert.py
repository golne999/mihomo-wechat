import requests
import re


source_url = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/WeChat/WeChat.list"

def convert():
    try:
        response = requests.get(source_url)
        response.raise_for_status()
        lines = response.text.splitlines()
        
        yaml_lines = ["payload:"]
        
        for line in lines:
            line = line.strip()
            # 跳过注释和空行
            if not line or line.startswith(('#', ';', '//')):
                continue
            
            # Surge 格式通常是: TYPE,VALUE,POLICY,OPTIONS
            # Mihomo classical 格式需要: - 'TYPE,VALUE'
            parts = line.split(',')
            if len(parts) >= 2:
                rule_type = parts[0].strip()
                rule_value = parts[1].strip()
                
                # 过滤掉 Mihomo 不支持或不建议在 rule-set 中使用的类型（如 USER-AGENT）
                if rule_type in ['DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'IP-CIDR', 'IP-CIDR6', 'IP-ASN']:
                    yaml_lines.append(f"  - '{rule_type},{rule_value}'")
        
        # 写入文件
        with open("WeChat.yaml", "w", encoding="utf-8") as f:
            f.write("\n".join(yaml_lines))
        print("转换成功：WeChat.yaml")

    except Exception as e:
        print(f"转换失败: {e}")

if __name__ == "__main__":
    convert()
