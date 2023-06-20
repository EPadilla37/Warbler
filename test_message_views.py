import os
import unittest
from flask import Flask
from flask_testing import TestCase
from app import db, User, Message, app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:padilla@localhost/warbler')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class MessageViewsTestCase(BaseTestCase):
    def test_messages_index(self):
        """Test if the messages index page is displayed correctly."""
        response = self.client.get("/messages")
        self.assert200(response)

    def test_delete_message(self):
        """Test if a message is successfully deleted."""
        # Create a test user
        user = User(
            username="test_user",
            email="test@example.com",
            password="test_password"
        )
        db.session.add(user)
        db.session.commit()

        # Create a test message
        message = Message(
            text="Test message",
            user_id=user.id
        )
        db.session.add(message)
        db.session.commit()

        response = self.client.post(f"/messages/{message.id}/delete", follow_redirects=True)
        self.assert200(response)
        self.assertNotIn(b"Test message", response.data)


if __name__ == '__main__':
    unittest.main()

