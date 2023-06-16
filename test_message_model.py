from unittest import TestCase
from models import db, User, Message
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:padilla@localhost/warbler_test'
app.config['SQLALCHEMY_ECHO'] = False

class MessageModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up class-level resources."""
        cls.app = app.test_client()
        cls.username = 'test_user'
        cls.password = 'password'
        cls.email = 'test@example.com'
        cls.text = 'Test message'

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

            message = Message(text=cls.text, user_id=user.id)
            db.session.add(message)
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
            message = Message.query.filter_by(text=self.text).one()
            self.assertEqual(repr(message), f"<Message #{message.id}: {message.text[:20]}>")



