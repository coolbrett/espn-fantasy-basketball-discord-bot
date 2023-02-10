TO-DO 
-----
- make /issue command to report issues
    - file a github issue?
    - official support server?
- Add logging?
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