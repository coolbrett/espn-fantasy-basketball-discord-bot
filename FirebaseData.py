import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from logger_config import logger
import datetime as datetime
class FirebaseData:
    """
    Class to handle all things related to Firebase such as calls to add, update, or delete data

    @github coolbrett
    """
    
    def __init__(self):
        """
        Code to run upon creation of FirebaseData object
        """
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://fantasy-basketball-bot-default-rtdb.firebaseio.com/'
        })
        logger.info("firebase connected")

    def add_new_guild(self, data: dict, guild_id: str) -> None:
        """
        Add new guild to the database for the bot to recognize.
        
        @param data: Dictionary containing the data for the guild.
        @param guild_id: The guild ID as a string.
        """
        ref = db.reference(f'fbbot/guilds/{guild_id}')
        ref.set(data)  # Replaces the entire entry under guild_id with the new data.
        #log name and id added
        logger.info(f"Added guild {data['guild_info']['discord_guild_name']} with id {guild_id}")

    def update_guild(self, data: dict) -> None:
        """
        THIS HASN'T BEEN TESTED -- Updates data stored at the key of the dict or JSON passed in

        :param data: Key should be guild_id and value should be another object with guild_id, league_id, and private league creds if needed
        """
        # guild_id = next(iter(data))
        ref = db.reference('fbbot/guilds/')
        ref.update({data})

    def log(self, level: str, message: str, guild_id: str, error=None, data=None) -> None:
        """
        Sends a log to Firebase to be stored under the guild_id passed in |
        data passed should have message, context object, and optionally an error object
        """

        #Logs should have timestamp, id, severity level, message, context object, and optionally an error object
        now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        ref = db.reference(f'fbbot/guilds/{guild_id}/logs')

        log = {
            f"{now}": {
                "timestamp": now,
                "message": message
                }
            }

        if error != None:
            #get error message and append it to log
            pass

        if data != None:
            #append data obj to log
            pass
        
        ref.update(log)
            
                

    def delete():
        """
        NOT WRITTEN YET - HAVEN'T NEEDED IT
        """
        pass

    def get_all_guild_ids(self):
        """
        Gets all guild IDs that are in Firebase and logs the count of registered servers.
        """
        ref = db.reference('fbbot/guilds')
        data = ref.get()
        guild_ids = list()

        if data:
            for guild_id, guild_data in data.items():
                guild_ids.append(guild_id)

            # Count registered servers
            registered_count = sum(
                1 for guild_data in data.values() if guild_data.get("guild_info", {}).get("is_registered", False)
            )

            # Log the count of registered servers
            logger.info(f"Total Servers: {len(guild_ids)}")
            logger.info(f"Registered Servers: {registered_count}")

        return guild_ids

    
    def get_guild_information(self, guild_id: str) -> dict:
        """
        Returns a dict containing information associated with guild id if it exists, otherwise returns None
        """
        ref = db.reference('fbbot')
        guilds = ref.get('guilds')[0]['guilds'][guild_id]
        if self.__check_guild_existence(guild_id):
            return guilds

        

    def __check_guild_existence(self, key: str) -> bool:
        """
        Helper function to check if a key already exists
        """
        # create a reference to the desired location in the database
        ref = db.reference('fbbot/guilds')

        # get the value at the specified location
        value = ref.get(key)

        # check if the value is None
        if value[0] is None:
            return False
        else:
            return True
        

