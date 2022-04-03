import os
# used for local run, to avoid overcomplicated PyCharm settings
#from dotenv import load_dotenv, find_dotenv
#load_dotenv(find_dotenv(filename=f"secrets.ini", raise_error_if_not_found=True))

class GlobalVariables:

    try:
        PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
        TEST_DATA_FOLDER = f"{PROJECT_ROOT}/features/test_data"
        OTP = os.environ.get("OTP")
        API_KEY = os.environ.get("API_KEY")
        SECRET_KEY = os.environ.get("PRIVATE_KEY")
        DEMO_API_KEY = os.environ.get("DEMO_API_KEY")
        DEMO_SECRET_KEY = os.environ.get("DEMO_PRIVATE_KEY")
        REAL_API_URL = os.environ.get("REAL_API_URL")
        DEMO_API_URL = os.environ.get("DEMO_API_URL")
    except KeyError as e:
        print(f"KeyError: Missing {e} environment variable")
        exit(1)