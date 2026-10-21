import mongoengine as me
import datetime

class User(me.Document):
    email = me.EmailField(required = True, unique = True)
    first_name = me.StringField(max_length = 50)
    last_name = me.StringField(max_length = 50)
    created_at = me.DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))

    def __str__(self):
        return (f"User(email = '{self.email}', name = '{self.first_name} {self.last_name}')")    
    
class Articulo(me.Document):
    name = me.StringField(max_length=50)
    description = me.StringField(max_length=100, min_length=10)
    brand = me.StringField(max_length=50)
    user_modified = me.ReferenceField(User)

    def __str__(self):
        return (f"Articulo(name = '{self.name}', description = '{self.description}', brand = '{self.brand}', user_modified = '{self.user_modified}')")

