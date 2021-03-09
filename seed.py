from app import app
from models import db, connect_db, User, Champion, Item, Piece, Composition
import json
import os

with open('static/data/champions.json') as f:
    data = json.load(f)

source = []

for filename in os.listdir('static/data/champions'):
    source.append(filename)

db.drop_all()
db.create_all()
i = 0
while i < len(source):

    print(data[i]['name'])
    print(source[i])
    champ = Champion(champ_name=data[i]['name'], img=source[i])
    db.session.add(champ)
    db.session.commit()
    i = i+1


# champ = Champion()
# champ2 = Champion()
# champ3 = Champion()
# champ4 = Champion()
# champ4 = Champion()


# db.session.add_all([champ,champ2,champ3,champ4])
# db.session.commit()

# user = User(email="john@gmail.com",username="1234test",password='1234test')
# db.session.add(user)
# db.session.commit

# piece1 = Piece(champion_id= champ.id, position=1)
# piece2 = Piece(champion_id= champ2.id, position=2)
# db.session.add_all([piece1,piece2])
# comp = Composition(name='tester', creator_id=user.id, piece1_id=piece1.id, piece2_id=piece2.id)

# db.session.add(comp)
# db.session.commit()