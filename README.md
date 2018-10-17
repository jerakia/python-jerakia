# python-jerakia

## POC use example

```
from jerakia import Jerakia

metadata = dict( hostname = 'agent1.localdomain')
token = 'ansible:4142672cd08d4dbb9eb3c1234567e46c1b85b20d75501ebc319c17a62dae636c1509b8bea1a66b3e'
content_type = 'json'
jerakia = Jerakia()

r1_json = jerakia.lookup(key='ntp_timezone', namespace='ntp', content_type=content_type, token=token)
r2_json = jerakia.lookup(key='ntp_timezone', namespace='ntp', content_type=content_type, token=token, metadata_dict=metadata)
r3_json = jerakia.lookup(namespace='ntp', content_type=content_type, token=token)
r4_json = jerakia.lookup(namespace='ntp', content_type=content_type, token=token, metadata_dict=metadata)
r1_msgpack = jerakia.lookup(key='ntp_timezone', namespace='ntp', token=token)
r2_msgpack = jerakia.lookup(key='ntp_timezone', namespace='ntp', token=token, metadata_dict=metadata)
r3_msgpack = jerakia.lookup(namespace='ntp', token=token)
r4_msgpack = jerakia.lookup(namespace='ntp', token=token, metadata_dict=metadata)

print('r1_json result: {}'.format(r1_json))
print('r1_json result: {}'.format(r2_json))
print('r1_json result: {}'.format(r3_json))
print('r1_json result: {}'.format(r4_json))

print('r1_msgpack result: {}'.format(r1_msgpack))
print('r2_msgpack result: {}'.format(r2_msgpack))
print('r3_msgpack result: {}'.format(r3_msgpack))
print('r4_msgpack result: {}'.format(r4_msgpack))
```

