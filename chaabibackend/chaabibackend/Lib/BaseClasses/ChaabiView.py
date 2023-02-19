from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView


class ChaabiView(APIView):

    def getResKeyValue(self, key, data):
        return Response({
            "success": True,
            key: data
        }, 200)

    def getResWithData(self, data):
        data.update({"success": True})
        return Response(
            data
            , 200)

    def getFailureWithData(self, data, response_code=200):
        data.update({"success": False})
        return Response(
            data,
            response_code
        )


    def setJsonEncodedBody(self):
        try:
            self.body = self.request.data
            self.session = self.request.session
        except Exception as e:
            e.message = self.getKeyErrorMessage(str(e))
            raise e
