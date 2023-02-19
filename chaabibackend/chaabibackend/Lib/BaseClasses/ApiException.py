from rest_framework.response import Response
# import raven
import os
from django.http import HttpResponse
from rest_framework.views import exception_handler
# from commodity.ThirdParty.CrFileLogger import CrFileLogger
# from raven import Client
# client = Client('https://a0b0551e82294decbe32f00702c2332b:da45af401aff419583158a94ea1ce0cc@app.getsentry.com/89462')

# from raven.contrib.django.raven_compat.models import sentry_exception_handler



def custom_exception_handler(exc, context):
    """
    Every Exception will go here
    and if the exception i user defined Exception
    then ok
    otherwise we will make our message 
    """
     

    a=exc.__dict__
    
    if a and isinstance(a,dict):
        print("found a dictionary")
        print(a)
        message=a['message']
        try:
            status_code = a['message']["error"]["status_code"]
        except KeyError as e:
            import sentry_sdk
            sentry_sdk.capture_exception(exc)
            message = {"error":{
            "message":"Sorry my bad",
            "code":5003,
            "developer_message":str(exc),
            "status_code":503},
            "success":False}
            status_code = 503

    else:
        import sentry_sdk
        sentry_sdk.capture_exception(exc)
        message = {"error":{
        "message":"Sorry my bad",
        "code":5003,
        "developer_message":str(exc),
        "status_code":503},
        "success":False}
        status_code = 503

    return Response(message , status_code)


















   
    # response = exception_handler(exc, context)
    # print("response",response)
    # if response is not None:
    #     response.data['status_code'] = response.status_code
    #     return response
    # else:
    #     message = {"error":{
    #     "message":"Oops Something went Wrong",
    #     "code":5003,
    #     "developer_message":str(exc),
    #     "status_code":503},
    #     "success":False}
    #     status_code = 503

    # #     # CrFileLogger.log("sentry_product_catalogue", str(traceback.format_exc()))

    # return Response(message , status_code)



    #client.captureException(exc)
    # import ipdb
    #ipdb.set_trace()
    # if isinstance(exc.message, dict):
    #     message = exc.message

        
    #     try:
    #         status_code = exc.message["error"]["status_code"]
    #     except KeyError as e:
    #         import traceback
    #         traceback.print_exc()  
    #         # import sentry_sdk
    #         # sentry_sdk.capture_exception(exc)
    #         # sentry_exception_handler(request=request)
    #         message = {"error":{
    #             "message":"Oops! something went wrong ",
    #             "code":5003,
    #             "developer_message":exc.message,
    #             "status_code":503},
    #             "success":False}
    #         status_code = 503

    #         # CrFileLogger.log("sentry_product_catalogue", str(traceback.format_exc()))



    # else:
    #     # sentry_exception_handler(request=request)
    #     import traceback
    #     traceback.print_exc()
    #     # import sentry_sdk
    #     # sentry_sdk.capture_exception(exc)
    #     message = {"error":{
    #             "message":"Oops Something went Wrong",
    #             "code":5003,
    #             "developer_message":exc.message,
    #             "status_code":503},
    #             "success":False}
    #     status_code = 503

    #     # CrFileLogger.log("sentry_product_catalogue", str(traceback.format_exc()))

    # return Response(message , status_code)
