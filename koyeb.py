import os
import json
import time
import logging
import requests
from datetime import datetime, timedelta

# 配置日志格式
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def validate_env_variables():
    """验证环境变量"""
    koyeb_accounts_env = os.getenv("KOYEB_ACCOUNTS")
    if not koyeb_accounts_env:
        raise ValueError("❌ KOYEB_ACCOUNTS 环境变量未设置或格式错误")
    try:
        return json.loads(koyeb_accounts_env)
    except json.JSONDecodeError:
        raise ValueError("❌ KOYEB_ACCOUNTS JSON 格式无效")
def validate_env_variables(): """验证环境指标""" koyeb_accounts_env = os.getenv("KOYEB_ACCOUNTS") if not koyeb_accounts_env: raise ValueError("❌ KOYEB_ACCOUNTS 环境指标未设置或格式错误") try: return json.loads(koyeb_accounts_env) except json.JSONDecodeError: raise ValueError("❌ KOYEB_ACCOUNTS JSON 格式无效")

def send_tg_message(message):
    """发送 Telegram 消息"""
    bot_token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
def send_tg_message(message): """发送电报消息""" bot_token = os.getenv("TG_BOT_TOKEN") chat_id = os.getenv("TG_CHAT_ID")

    if not bot_token or not chat_id:
        logging.warning("⚠️ TG_BOT_TOKEN 或 TG_CHAT_ID 未设置，跳过 Telegram 通知")
        return
if not bot_token or not chat_id:logging.warning("⚠️ TG_BOT_TOKEN 或 TG_CHAT_ID 未设置，跳过 Telegram 通知") return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}

    try:
        response = requests.post(url, data=data, timeout=30)
        response.raise_for_status()
        logging.info("✅ Telegram 消息发送成功")
    except requests.RequestException as e:
        logging.error(f"❌ 发送 Telegram 消息失败: {e}")
尝试：response = requests.post（url，data = data，timeout = 30）response.raise_for_status（）logging.info（“✅ Telegram 消息发送成功”）除了 requests.RequestException as e：logging.error（f“❌发送 Telegram 消息失败：{e}”）

def check_koyeb_token(email, token):
    """
    使用 Koyeb API Token 校验账号是否可用
    访问 /v1/apps，只要返回 200 即视为成功
    """
    if not token:
        return False, "Token 为空"
def check_koyeb_token(email, token): """ 使用 Koyeb API Token 校验账号是否可用访问/v1/apps，只要返回 200 即视为成功""" if not token: return False, "Token 为空"

    url = "https://app.koyeb.com/v1/apps"
    headers = {
        "Authorization": f"Bearer {token.strip()}",
        "Accept": "application/json",
        "User-Agent": "KoyebTokenChecker/1.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return True, "Token 校验成功"
    except requests.Timeout:
        return False, "请求超时"
    except requests.RequestException as e:
        return False, str(e)

def main():
    """主流程"""
    try:
        koyeb_accounts = validate_env_variables()
        if not koyeb_accounts:
            raise ValueError("❌ 没有找到有效的 Koyeb 账户信息")

        # 获取北京时间（UTC+8）
        current_time = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
        messages = []

        for account in koyeb_accounts:
            email = account.get("email", "未命名账号")
            token = account.get("token", "").strip()

            if not token:
                logging.warning(f"⚠️ 账户未配置 Token，跳过: {email}")
                messages.append(f"⚠️ 账户: {email}\nToken 未配置，跳过")
                continue
if not token:logging.warning(f"⚠️账户未配置 Token，跳过:{email}") messages.append(f"⚠️账户:{email}\nToken 未配置，跳过") continue

            logging.info(f"🔄 正在检查账户: {email}")
            success, message = check_koyeb_token(email, token)

            result = "🎉 登录成功（Token）" if success else f"❌ Token 校验失败 | 原因: {message}"
            messages.append(f"📧 账户: {email}\n\n{result}")
result = "🎉 电影成动成功（Token）" if success else f"❌ Token 校生电影 | Cause: {message}" messages.append(f"📧 新视: {email}\n\n{result}")

            time.sleep(5)

        summary = f"🗓️ 北京时间: {current_time}\n\n" + "\n\n".join(messages) + "\n\n✅ 任务执行完成"

        logging.info("📋 任务完成，发送 Telegram 通知")
        send_tg_message(summary)

    except Exception as e:
        error_message = f"❌ 执行出错: {e}"
        logging.error(error_message)
        send_tg_message(error_message)

if __name__ == "__main__":
    main()

如果 __name__ == "__main__": main()
