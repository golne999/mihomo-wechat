import requests
import json

# sing-box 原始 JSON 链接
source_url = "https://raw.githubusercontent.com/senshinya/singbox_ruleset/main/rule/WeChat/WeChat.json"

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
        
        result_list = set()
        
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
        
        # 排序并去重
        final_output = sorted(list(result_list))

        # 写入文件，后缀建议改为 .list 或 .txt
        with open("WeChat.list", "w", encoding="utf-8") as f:
            f.write("\n".join(final_output))
            
        print(f"转换成功！已生成 WeChat.list，共 {len(final_output)} 条规则。")

    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    convert()
