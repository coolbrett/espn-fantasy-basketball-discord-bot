# ESPN Fantasy Basketball Discord Bot
 ### **Developer: Brett Dale**

 DESCRIPTION
 -----------
This Discord bot is built with the pycord library and an espn-api specifically for ESPN fantasy sports

The goal is to build this bot so that it can handle all Discord servers that it is invited to with a single instance of itself

I want the bot to be able to display most things that you can find in the app as well as give insights through advanced statistics

PROCESS
-------
1. Make the bot as feature-rich with stats and helpful commands as possible for your
    own league
2. Deploy this bot somewhere and set up automated deployments 
3. Focus on how to make this a SAAS


TO-DO 
-----
- Try and make the commands uniform -- scoreboard kind of sucks, get rid of '|'across commands if possible
- replace usages of scoreboard()
- get_record_vs_all_teams doesn't work if team has a bye
- make /issue command to report issues
- Add logging?
- bot token and firebase service account creds need to be regenerated since they were pushed to git
- deploy the bot to Azure
- set up github actions for automated deployments
- Add new useful and advanced stats



FUTURE WORK - once the bot is polished, bulletproof, and well-designed
-----------
- Add roto support??
- Look into adding team logo's on certain commands -- teams have logo url fields
    There is a branch on the repo called logos -- fetching the pics and sending them
    through the bot is working, but the logos have weird lines coming off the right


NOTES
-----
- If the FBB league is, or has ever been, a private league then you need to provide 
    espn_s2 and swid when building the league object -- instructions below
    (https://github.com/cwendt94/espn-api/discussions/150)

- the /standings command on NBA Bot shows the limit on mobile

- Injury rate cannot be done using the espn_api -- the game_played field gets marked to 100 if 
    they play one game that week, not all

- Add descriptions to parameters of commands (https://github.com/Pycord-Development/pycord/discussions/1861)