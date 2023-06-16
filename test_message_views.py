from unittest import TestCase
from models import db, User, Message
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler-test'
app.config['SQLALCHEMY_ECHO'] = False

class MessageViewsTestCase(TestCase):
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

    def test_messages_index(self):
        """Test if the messages index page is displayed correctly."""
        response = self.app.get('/messages')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test message', response.data)

    def test_delete_message(self):
        """Test if a message is successfully deleted."""
        with self.app.session_transaction() as session:
            user = User.query.filter_by(username=self.username).one()
            session['user_id'] = user.id

        message = Message.query.filter_by(text=self.text).one()
        response = self.app.post(f'/messages/{message.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Test message', response.data)
