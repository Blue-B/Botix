import logging
import os
import subprocess
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

load_dotenv()
TOKEN = os.getenv("Bot_Token")

ALLOWED_USERS = list(map(int, os.getenv("U_Number", "").split(",")))

# 로깅 설정
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

def is_allowed(update: Update) -> bool:
    """사용자가 허용된 ID인지 확인"""
    user_id = update.effective_user.id
    return user_id in ALLOWED_USERS

def is_gui_program(command: str) -> bool:
    """명령어가 GUI 프로그램인지 확인"""
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            executable="/bin/bash",
            env={**os.environ, "DISPLAY": "", "WAYLAND_DISPLAY": "", "XDG_SESSION_TYPE": ""}  # GUI 환경 변수 제거
        )
        stdout, stderr = process.communicate(timeout=2)

        # 실행 결과에 특정 오류 메시지가 있으면 GUI 프로그램일 가능성이 높음
        gui_errors = [
            "Gtk-WARNING",  # GTK 기반 GUI 프로그램
            "Qt-WARNING",  # QT 기반 GUI 프로그램
            "Unable to init server",  # X 서버가 없음
            "cannot open display"  # X 서버가 없음
        ]

        for error in gui_errors:
            if error in stderr:
                return True

        return False
    except Exception:
        return True  # 실행 자체가 안 되면 GUI 프로그램일 가능성이 높음

def shell(update: Update, context: CallbackContext) -> None:
    """텔레그램에서 명령어를 입력받아 실행"""
    message = update.effective_message  # 안전한 메시지 객체 가져오기
    if message is None:
        return  # 메시지가 없으면 함수 종료

    if not is_allowed(update):
        message.reply_text("🚫 접근이 거부되었습니다.")
        return

    command = " ".join(context.args)
    if not command:
        message.reply_text("❌ 실행할 명령어를 입력하세요.")
        return

    if is_gui_program(command):
        message.reply_text("⛔️ GUI가 필요한 프로그램은 실행할 수 없습니다.")
        return

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            executable="/bin/bash",
            cwd=os.getcwd()  # 현재 디렉터리 유지
        )
        stdout, stderr = process.communicate()
        output = stdout.strip() if stdout.strip() else stderr.strip()

        if not output:
            output = "✅ 명령이 성공적으로 실행되었지만 출력이 없습니다."

        message.reply_text(f"💻 실행 결과:\n```{output}```", parse_mode="Markdown")
    except Exception as e:
        message.reply_text(f"⚠️ 오류 발생:\n{str(e)}")

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
