* Race Condition Lab
This is a client/server file transfer protocol, where there are multiple
clients sending the same file at the same time. The server must handle that
correctly while using multithreading.

** How to run
Run the server first.
```
$ python3 framedThreadServer.py
```

And then run the client.
```
$ python3 framedThreadClient.py
```
After than, you will have to specify the file name and the client will send
that file multiple times.

The server will receive the file data and create an output file.
