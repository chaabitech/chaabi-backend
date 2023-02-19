class DefaultException(Exception):
    def __init__(self, msg=""):
        message = {
            "error": {
                "message": msg,
                "code": 4070,
                "status_code": 400,
                "developer_message": "Default Exception: " + msg
            },
            "success": False}

        self.message = message

class GoogleLoginException(Exception):

    def __init__(self, e, msg="Ops Something went wrong"):
        message = {"error": {
            "message": msg,
            "status_code": 503,
            "code": 4035,
            "developer_message": str(e)},
            "success": False
        }
        self.message = message

        # self message

    def __str__(self):
        return repr(self.message)


class UnAuthorisedException(Exception):

    def __init__(self, msg="Ops Something went wrong"):
        message = {"error": {
            "message": msg,
            "status_code": 401,
            "code": 4036,
            "developer_message": msg},
            "success": False
        }
        self.message = message

        # self message

    def __str__(self):
        return repr(self.message)