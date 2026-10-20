import mongoengine as me
import datetime

class User(me.Document):
    email = me.EmailField(required = True, unique = True)
    first_name = me.StringField(max_length = 50)
    last_name = me.StringField(max_length = 50)
    created_at = me.DateTimeField(default=datetime.datetime.now(datetime.datetime.utc))
    
    def __str__(self):
        return (f"User(email = '{self.email}', name = '{self.self.first_name} {self.last_name}')")    