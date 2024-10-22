# User queries stream

Procedure: Create two terminal windows into the same Linux machine.

1. In the listener:
```
    nc -lk localhost 9999 | ~/big-data-repo/spark-examples/first_streaming/read_stdin.py
```

2. In the sender:
```
    ~/big-data-repo/spark-examples/first_streaming/click-feeder.py 2>/dev/null | nc localhost 9999
```

User queries should start appearing in the listener window. `^C` to terminate.

