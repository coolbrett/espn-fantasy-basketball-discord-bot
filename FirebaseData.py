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

    def add_new_guild(data: dict) -> None:
        """
        Add new guild to the database for the bot to recognize

        @param data -> Key should be guild_id and value should be another object with guild_id, league_id, and private league creds if needed
        """
        ref = db.reference('fbbot')
        guild_ref = ref.child('guilds')
        guild_ref.set({data})

    def update_guild(data: dict) -> None:
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

    def get_all_guild_ids():
        """
        Gets all guild id's that are in firebase
        """
        ref = db.reference('fbbot')
        data = ref.get('guilds')
        guild_ids = list()
        for id, obj in data.items():
            #should get guild_id
            print(f"{id} {obj}")
            guild_ids.append(obj[id])
        print(f"FirebaseData guild_ids: {guild_ids}")
        return guild_ids
        

