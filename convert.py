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
    "DOMAIN-SUFFIX,video.qq.com",        # 视频号、腾讯视频全家桶
    "DOMAIN-SUFFIX,gtimg.cn",            # 微信静态资源主干 (朋友圈、小程序图片)
    "DOMAIN-SUFFIX,gtimg.com",           # 腾讯资源主干
    "DOMAIN-SUFFIX,weixin.qq.com",       # 微信最核心域名 (通讯、登录)
    "DOMAIN-SUFFIX,servicewechat.com",   # 小程序核心
    "DOMAIN-SUFFIX,tencent-cloud.net",   # 腾讯云节点加速
    "DOMAIN-SUFFIX,tenpay.com",
    # --- 腾讯广点通与广告 (微信生态常用) ---
    "DOMAIN-SUFFIX,gdt.qq.com",
    # --- 微信静态资源与广告 ---
    "DOMAIN-SUFFIX,ssad.qq.com",        # 微信广告、朋友圈推广图
    "DOMAIN-SUFFIX,wximg.qq.com",       # 微信通用图片服务器
    "DOMAIN-SUFFIX,wxamedia.com",       # 微信视频号/媒体预览核心 (1500047674.vodpreview...)

# --- 腾讯云与基础架构 (关键，涵盖了那个 cos 域名) ---
    "DOMAIN-SUFFIX,myqcloud.com",       # 腾讯云公共存储/加速 (微信小程序/开发逻辑的核心)
    "DOMAIN-SUFFIX,myqcloud.com.cn",    # 腾讯云备份后缀

# --- 阿里系 CDN (国内 App 极其通用的字体/图标库) ---
    "DOMAIN-SUFFIX,alicdn.com",         # 阿里公共 CDN (at.alicdn.com 常用于图标字体)

# --- 其它第三方服务 (微信内嵌套的小程序/网页接口) ---
    "DOMAIN-SUFFIX,jianfannet.com",     # 简饭网络 (api.jianfannet.com)

# --- 微信/腾讯直播与实时流 (视频号直播、语音通话) ---
    "DOMAIN-SUFFIX,tlivesource.com",
    "DOMAIN-SUFFIX,qlivecdn.com",
    "DOMAIN-SUFFIX,wxgateway.com",
    "DOMAIN-SUFFIX,tc.qq.com",

# --- 腾讯云微信专用接口 (补齐 .com 后缀) ---
    "DOMAIN-SUFFIX,wxqcloud.qq.com",
    "DOMAIN-SUFFIX,wxqcloud.qq.com.cn",

# --- 文件下载 (补齐 IPv6 根) ---
    "DOMAIN-SUFFIX,dldir1v6.qq.com",
    
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
