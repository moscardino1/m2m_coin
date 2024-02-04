
from __init__ import app,db
from models import db, Participant, CentralBank, Transaction
from routes import bp

app.register_blueprint(bp)

if __name__ == '__main__':
  db.create_all()
  app.run()
 
