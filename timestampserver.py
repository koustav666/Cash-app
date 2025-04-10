
import datetime
import thriftpy2 as thriftpy
from thriftpy2.rpc import make_server
timestamp_thrift = thriftpy.load('timestampservice.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService
class TimestampHandler:
    def get_timestamp(self):
        return datetime.datetime.now().isoformat()

if __name__ == '__main__':
    handler = TimestampHandler()
    server = make_server(Timestamp, handler, '127.0.0.1', 9090)
    server.serve()
