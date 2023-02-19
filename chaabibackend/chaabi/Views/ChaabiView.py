from chaabibackend.Lib.BaseClasses.ChaabiView import ChaabiView

class HealthCheckView(ChaabiView):
    def get(self, request, version_id):
        return self.getResWithData({"message": "Health Check is Ok"})
