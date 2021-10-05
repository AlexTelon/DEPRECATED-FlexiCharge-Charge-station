import time
from datetime import datetime
import tzlocal

class DateHandler:
    def convertUnixToUTC(unix):
        timestamp = int(unix)
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
    def convertUnixToLocal(unix):
        timestamp = int(unix)
        local_tz = tzlocal.getlocalzone()
        return datetime.fromtimestamp(timestamp, local_timezone)
        pass