
import thriftpy
from thriftpy.rpc import make_client
from thriftpy.thrift import TException
timestamp_thrift = thriftpy.load('timestampservice.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService
def get_remote_timestamp():
    try:
        # Instantiate a synchronous client
        client = make_client(Timestamp, '127.0.0.1', 9090)
        result = client.get_timestamp()
        print("Current timestamp:", result)
        return result

    except TException as e:
        print(e)

if __name__ == '__main__':
    get_remote_timestamp()
