import os
from instagrapi.exceptions import LoginRequired
from dotenv import load_dotenv
from rich.prompt import Prompt

def input_erfa_code(status) -> str:
    ERFA_code = ""
    status.stop()
    ERFA_code = Prompt.ask("🚀 Input verification code")
    status.start()
    return ERFA_code

def send_login_request(cl, username, password, ERFA_code = "") -> None:
    cl.login(username, password, verification_code=ERFA_code)

def login_user(cl, status) -> None:

    load_dotenv()
    username = os.environ.get('ACCOUNT')
    password = os.environ.get('PASSWORD')
    ERFA = os.environ.get('ERFA', "false") == "true"  # 2fa
    


    if os.path.exists("session.json"):
        session = cl.load_settings("session.json")
        try:
            cl.set_settings(session)
            send_login_request(cl, username, password)
            
            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                print("🙊 Session is not valid, please login again")
                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                send_login_request(cl, username, password, input_erfa_code(status) if ERFA else "")
        except Exception as e:
            print(f"error logging: {e}")
    else:
        send_login_request(cl, username, password, input_erfa_code(status) if ERFA else "")
    cl.dump_settings("session.json")
