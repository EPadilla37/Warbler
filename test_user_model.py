from unittest import TestCase
from models import db, User
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:padilla@localhost/warbler_test'
app.config['SQLALCHEMY_ECHO'] = False

class UserModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up class-level resources."""
        cls.app = app.test_client()
        cls.username = 'test_user'
        cls.password = 'password'
        cls.email = 'test@example.com'

        with app.app_context():
            db.drop_all()
            db.create_all()

            user = User(
                username=cls.username,
                password=cls.password,
                email=cls.email
            )
            db.session.add(user)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up class-level resources."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_repr_method(self):
        """Test if the __repr__ method works as expected."""
        with app.app_context():
            user = User.query.filter_by(username=self.username).one()
            self.assertEqual(repr(user), f"<User #{user.id}: {user.username}, {user.email}>")


