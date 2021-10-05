import time
from datetime import datetime
import tzlocal

class UnixConverter:
    def convertUnixToUTC(unix):
        timestamp = float(unix)
        return datetime.utcfromtimestamp(timestamp)
        
    def convertUnixToLocal(unix):
        timestamp = float(unix)
        local_tz = tzlocal.get_localzone()
        return datetime.fromtimestamp(timestamp, local_tz)