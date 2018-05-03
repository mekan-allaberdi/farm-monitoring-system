Egg Farm System
======================
Farm system for egg production. Developed using Python-Flask.

*Developed in 2015.*

# Farm System has 4 modules:
- **Feed** : Hen's feed production from raw materials.
   - In *Feed* module we have raw material warehouse and feed warehouse.
   - Feeds are producing according to formula (ratios of raw materials).
- **Hencoop** : Monitoring hens and eggs in hencoop.
  - Hencoop status.
  - Daily egg production, hens died.
- **Egg** : Egg production, store and sales.
  - Egg warehouse
  - Customers
- **Cash** : Cashflow (debits, payments, salaries)
  - All expenses and payments
  
  
# Requirements
- Python3
- Falsk
- SQLAlchemy
- Uwsgi

# Installation

Go to root directory.
  ```
  $ virtualenv -p python3 venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt
  ```

# Running
Create DB. For one time *db.create_all()* in **run.py** file.
  ```
  if __name__ == "__main__":
    db.create_all()
    app.run()
  ```
Once you created DB you can remove *db.create_all()* line.

- Running on localhost:
  ```
  $ python run.py
  ```
- Running **uwsgi**
  ```
  $ uwsgi --ini uwsgi.ini
  ```

# Blueprint
I used blueprint to organize my application into distinct components*(feed, hencoop, egg, cash)*.
  

  ```
  app = Flask(__name__)
  
  .....
  .....
  
  from app.feed import feed_bp
  from app.cash import cash_bp
  from app.hencoop import hencoop_bp
  from app.egg import egg_bp

  app.register_blueprint(feed_bp)
  app.register_blueprint(cash_bp)
  app.register_blueprint(hencoop_bp)
  app.register_blueprint(egg_bp)
  ```
