# RabbitMQ toolkit for SuperAGI
 A toolkit that enables natural language communication between agents using RabbitMQ as a messaging broker

1. <b>Natural Language Communication:</b> The toolkit is capable of sending and receiving messages in natural language. This is done by encoding the messages as JSON objects, which include the sender, receiver, timestamp, type, and content of the message.
2. <b>Message Prioritization:</b> The toolkit supports prioritizing messages. When sending a message, you can specify a priority level. Messages with higher priority levels are delivered before those with lower priority levels.
3. <b>Basic RabbitMQ Operations:</b> The toolkit supports basic RabbitMQ operations such as sending and receiving messages, adding and removing consumers, and sending acknowledgements. These operations are executed through the 'execute* method of the
'RabbitMQTool' class.
4. <b>Connection Management:</b> The toolkit manages the connection to the RabbitMQ server. It establishes the connection when an operation is executed and handles any connection errors that may occur.
5. <b>Logging:</b> The toolkit logs important events and errors. This can help with debugging and understanding the behavior of the toolkit.
6. <b>Environment Variables:</b> The toolkit uses environment variables to configure the RabbitMQ server, username, and password. This allows for easy configuration without modifying the code.
7. <b>Asynchronous Messaging:</b> The toolkit supports asynchronous messaging. This means that it can send and receive messages without blocking, allowing for more efficient communication.
8. <b>Message Persistence:</b> The toolkit supports message persistence. This means that messages are not lost if the RabbitMQ server crashes or restarts.
