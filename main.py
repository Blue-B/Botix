import logging
import os
import subprocess
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

load_dotenv()
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

ALLOWED_USERS = list(map(int, os.getenv("U_Number", "").split(",")))

# 로깅 설정
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

def is_allowed(update: Update) -> bool:
    """사용자가 허용된 ID인지 확인"""
    user_id = update.effective_user.id
    return user_id in ALLOWED_USERS

def shell(update: Update, context: CallbackContext) -> None:
    """텔레그램에서 명령어를 입력받아 실행"""
    if not is_allowed(update):
        update.message.reply_text("🚫 접근이 거부되었습니다.")
        return

    command = " ".join(context.args)
    if not command:
        update.message.reply_text("❌ 실행할 명령어를 입력하세요.")
        return

    # GUI 명령어 실행 방지
    BLOCKED_COMMANDS = ["nano", "vi", "top", "htop"]
    if any(cmd in command for cmd in BLOCKED_COMMANDS):
        update.message.reply_text("⛔ 지원되지 않는 명령어입니다.")
        return

    try:
        # 명령 실행 (현재 쉘 환경을 유지)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            executable="/bin/bash"
        )
        stdout, stderr = process.communicate()
        output = stdout if stdout else stderr
        update.message.reply_text(f"💻 실행 결과:\n```{output}```", parse_mode="Markdown")
    except Exception as e:
        update.message.reply_text(f"⚠️ 오류 발생:\n{str(e)}")

def main():
    """텔레그램 봇 실행"""
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # /s 명령어 실행
    dp.add_handler(CommandHandler("s", shell))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
