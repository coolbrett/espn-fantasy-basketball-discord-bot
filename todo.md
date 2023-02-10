TO-DO 
-----
- Add logging?
    - restructure guild id collections to have separate collections for credentials and logging
    - check notes below for good logging practice
- bot token and firebase service account creds need to be regenerated since they were pushed to git
- Test on another server to make sure all functionalities work there too
- Support server?
- Cleanup git repo and README before going public
- deploy the bot to Firebase?
- set up github actions for automated deployments
- Cleanup git repo and README before going public
- Add new useful and advanced stat
    - Add commands that fire every so often (weekly and yearly awards)
    - Add compare players command (player1 season1 player2 season2)
    - Add schedule command
        - team specific or week in league specific
- Look into message options thing that Elijah showed you
- Add commands that fire every so often (weekly and yearly awards)




FUTURE WORK - once the bot is polished, bulletproof, and well-designed
-----------
- Add roto support??
- Look into adding team logo's on certain commands -- teams have logo url fields
    There is a branch on the repo called logos -- fetching the pics and sending them
    through the bot is working, but the logos have weird lines coming off the right
- Add commands that fire every so often (weekly and yearly awards)


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