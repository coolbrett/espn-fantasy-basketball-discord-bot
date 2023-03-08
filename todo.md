TO-DO 
-----
- set up github actions for automated deployments
- Try the logos again
- Add new useful and advanced stats
    - Add commands that fire every so often (weekly and yearly awards)
    - Add compare players command (player1 season1 player2 season2)
    - Add schedule command
        - team specific or week in league specific
- Look into message options thing that Elijah showed you
- post on top.gg
- make frontend for registration?


NOTES
-----
- If the FBB league is, or has ever been, a private league then you need to provide 
    espn_s2 and swid when building the league object -- instructions below
    (https://github.com/cwendt94/espn-api/discussions/150)

- the /standings command on NBA Bot shows the limit on mobile

- Injury rate cannot be done using the espn_api -- the game_played field gets marked to 100 if 
    they play one game that week, not all

- Add descriptions to parameters of commands (https://github.com/Pycord-Development/pycord/discussions/1861)

- A common scheme for logging typically includes the following elements:

    - Severity levels: Log messages are assigned a severity level, such as "debug", "info", "warning", "error", or "critical", to indicate the importance or urgency of the message. This allows you to filter and prioritize log messages based on their severity.

    - Timestamps: Log messages are stamped with a timestamp indicating when the message was generated. This allows you to track the progression of events over time.

    - Message content: Log messages contain descriptive text that provides information about what is happening in the application. The message content should be clear, concise, and informative.

    - Contextual information: Log messages often include additional contextual information, such as the source of the log message (e.g., the module or class that generated the message), the log message's severity level, and any relevant data associated with the message (e.g., the parameters of a function call).

    - Storage: Log messages are stored in a central location, such as a file, a database, or a cloud-based service, where they can be easily retrieved and analyzed.
    
    - This basic scheme provides a starting point for logging in your application, but you can also add additional elements, such as unique IDs for log messages, custom metadata, and structured log data, to meet your specific needs and requirements.

- Good events to log typically include important and significant actions performed by an application, system, or user. Here are some examples of events that are commonly logged:

    - Authentication and authorization events, such as successful and unsuccessful login attempts
    - System startup and shutdown events
    - Resource access events, such as file or database access
    - Configuration changes to the system or application
    - Network events, such as incoming and outgoing network connections
    - Performance events, such as system performance metrics, resource utilization, and slow requests
    - Security events, such as detected intrusions, attacks, or unauthorized access attempts
    - Error and exception events, such as uncaught exceptions, unexpected errors, or system failures
    - It's important to log events that can provide context to security incidents and system failures, as well as events that can help monitor and diagnose performance issues. The specific events to log will depend on the requirements of the system or application, as well as any regulatory or compliance requirements.