from datetime import datetime

class CrFileLogger():
    
    @staticmethod
    def log(fileName, text):
        file = open('/var/log/apps/product/' + fileName + "_" + datetime.now().strftime("%Y%m%d") +'.txt', 'a')
        file.write(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ":: " + text + "\r\n")
        file.close()