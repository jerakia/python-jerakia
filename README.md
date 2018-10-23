# python-jerakia

A Python client library for Jerakia server (https://jerakia.io)

## Usage example

With a Jerakia server running on localhost, do

```
python
import jerakia
token = 'dev:ac4093fec97c6d52f3b419db9b744d214d7428b0e0f75f2d98b8016df5b79dd819743583c047f47f'
client = jerakia.Client(token=token)
client.lookup(key='test',namespace='common')
```

