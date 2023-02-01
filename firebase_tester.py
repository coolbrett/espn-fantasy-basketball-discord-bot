import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fantasy-basketball-bot-default-rtdb.firebaseio.com/'
})

ref = db.reference('fbbot')
guild_ref = ref.child('guilds')
guild_ref.set({
    'deez': {
        'first_name': 'BRETT',
        'last_name': 'dale'
    }
})

data = ref.get('guilds')
print(data)
print(data[0]['guilds'])