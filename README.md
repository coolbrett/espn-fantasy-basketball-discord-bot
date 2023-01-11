# ESPN Fantasy Basketball Discord Bot
 ### Developer: **Brett Dale**

PROCESS
-------
1. Make the bot as feature-rich with stats and helpful commands as possible for YOUR OWN LEAGUE
2. Deploy this bot somewhere and set up automated deployments 
3. Focus on how to make this a SAAS
4. Redesign the bot's structure as you need to when making this work for other league formats


TO-DO 
-----
<<<<<<< HEAD:README.md
- % of top (league roster size * (half number of teams in league)) players on roster -- avg and totals
=======
- Add /boxscore command to report player totals for a team on a given week or year
- % of top (league roster size * (half number of teams in league)) players on roster -- avg and totals
- injury rate stat
- Write /setup command to take parameters needed to build a League object
>>>>>>> 1f4f98292c82760fbe6d3d466f9bc8dc8b4df446:notes.txt

BEGINNER TASKS
--------------
- Write a command that sends a saying based upon a random number
- Write a command that sends a message of a list of all the commands LeBot knows
- Write a basic README file using markdown that has a title, description, and authors listed
- Add descriptions to parameters of commands (https://github.com/Pycord-Development/pycord/discussions/1861)


FUTURE WORK - once the bot is polished, bulletproof, and well-designed
-----------
- refactor and figure out an initial set up process so that this bot can be used
    for other H2H FBB leagues
- Add roto support??
- Add error handling for incorrect parameters for commands
- deploy the bot somewhere
- set up github actions for automated deployments
- Look into adding team logo's on certain commands -- teams have logo url fields
    There is a branch on the repo called logos -- fetching the pics and sending them
    through the bot is working, but the logos have weird lines coming off the right


NOTES
-----
- If the FBB league is, or has ever been, a private league then you need to provide 
    espn_s2 and swid when building the league object -- instructions below
    (https://github.com/cwendt94/espn-api/discussions/150)

- the /standings command on NBA Bot shows the limit on mobile

- Once deployed, scaling vertically seems to be the better and cheaper way. 
    I want to each discord server to have their own instance of the bot 
- Injury rate cannot be done using the espn_api -- the game_played field gets marked to 100 if 
    they play one game that week, not all