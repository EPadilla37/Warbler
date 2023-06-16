from csv import DictReader
from app import create_app, db
from models import User, Message, Follows


# Create the Flask app and push an application context
app = create_app()
app.app_context().push()

# Drop all existing tables
db.drop_all()
# Create the tables
db.create_all()

with open('generator/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))

with open('generator/messages.csv') as messages:
    db.session.bulk_insert_mappings(Message, DictReader(messages))

with open('generator/follows.csv') as follows:
    db.session.bulk_insert_mappings(Follows, DictReader(follows))

# Commit the changes
db.session.commit()

print("Database tables dropped and seeded successfully.")



