
Please use the rspec file to setup the encironment, log into each node and copy the corresponding files to the node. Use script.sh in each folder to install the required dependencies for each node.

The web interface and backend should be running until Dec 30th.

To test the program, log into one of the client, upload client1/client.py and run

```
python3 client.py --message "input text".
```

Replace the [input text] with any sentence that you would like to send.

To reproduce our experiments, log into one of the client, upload client1/clientTest.py and run
```

python3 clientTest.py
```

This should measure the performance metrics and generate the values of these metrics.
