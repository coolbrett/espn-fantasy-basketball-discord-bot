import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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
        print("firebase connected")

    def add_new_guild(self, data: dict) -> None:
        """
        Add new guild to the database for the bot to recognize

        @param data -> Key should be guild_id and value should be another object with guild_id, league_id, and private league creds if needed
        """
        ref = db.reference('fbbot')
        guild_ref = ref.child('guilds')
        print(f"Add New Guild: data -> {data}")
        guild_ref.set(data)

    def update_guild(self, data: dict) -> None:
        """
        Updates data stored at the key of the dict or JSON passed in

        :param data: Key should be guild_id and value should be another object with guild_id, league_id, and private league creds if needed
        """
        ref = db.reference('fbbot')
        ref.child('guilds').update({data})


    def delete():
        """
        NOT WRITTEN YET - HAVEN'T NEEDED IT
        """
        pass

    def get_all_guild_ids(self):
        """
        Gets all guild id's that are in firebase
        """
        ref = db.reference('fbbot')
        data = ref.get('guilds')
        print(f"data: {data}")
        guild_ids = list()
        if data[0] != None:
            keys_as_list = list(data[0]['guilds'].keys())
            for key in keys_as_list:
                guild_ids.append(key)
        print(f"FirebaseData guild_ids: {guild_ids}")
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
        

