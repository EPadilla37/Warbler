import os
import sys
import unittest

from flask import Flask
from models import db, connect_db, User
from app import app

from unittest import TestCase
from flask import session

# Set the Flask app in testing mode
app.config['TESTING'] = True
# Use an in-memory SQLite database for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:padilla@localhost/warbler_test'
# Disable CSRF protection for simplicity in testing
app.config['WTF_CSRF_ENABLED'] = False

# Create the database and tables
db.create_all()


class WarblerTestCase(TestCase):
     def setUp(self):
        """Set up the test environment."""
        # Clear the session and database before each test
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()
        self.client = app.test_client()

        def tearDown(self):
            """Clean up the test environment."""
            with app.app_context():
                db.session.remove()
                db.drop_all()

        def test_signup(self):
            """Test user signup."""
            with self.client:
                with app.app_context():
                    response = self.client.post('/signup', data={
                        'username': 'testuser',
                        'password': 'testpassword',
                        'email': 'test@example.com',
                        'image_url': ''
                    }, follow_redirects=True)

                    self.assertEqual(response.status_code, 200)
                    self.assertIn(b'Account created!', response.data)
                    self.assertEqual(session['user_id'], 1)

        def test_login(self):
            """Test user login."""
            with self.client:
                with app.app_context():
                    test_user = User.signup(
                        username='testuser',
                        password='testpassword',
                        email='test@example.com',
                        image_url=''
                    )
                    db.session.commit()

                    response = self.client.post('/login', data={
                        'username': 'testuser',
                        'password': 'testpassword'
                    }, follow_redirects=True)

                    self.assertEqual(response.status_code, 200)
                    self.assertIn(b'You are logged in!', response.data)
                    self.assertEqual(session['user_id'], test_user.id)

        def test_logout(self):
            """Test user logout."""
            with self.client:
                with app.app_context():
                    test_user = User.signup(
                        username='testuser',
                        password='testpassword',
                        email='test@example.com',
                        image_url=''
                    )
                    db.session.commit()

                    # Log in the test user
                    self.client.post('/login', data={
                        'username': 'testuser',
                        'password': 'testpassword'
                    })

                    response = self.client.get('/logout', follow_redirects=True)

                    self.assertEqual(response.status_code, 200)
                    self.assertIn(b'You are logged out!', response.data)
                    self.assertNotIn('user_id', session)

        def test_user_profile(self):
            """Test updating user profile."""
            with self.client:
                with app.app_context():
                    test_user = User.signup(
                        username='testuser',
                        password='testpassword',
                        email='test@example.com',
                        image_url=''
                    )
                    db.session.commit()

                    # Log in the test user
                    self.client.post('/login', data={
                        'username': 'testuser',
                        'password': 'testpassword'
                    })

                    response = self.client.post('/profile', data={
                        'username': 'newusername',
                        'email': 'newemail@example.com',
                        'image_url': ''
                    }, follow_redirects=True)

                    self.assertEqual(response.status_code, 200)
                    self.assertIn(b'Profile updated!', response.data)
                    updated_user = User.query.get(test_user.id)
                    self.assertEqual(updated_user.username, 'newusername')
                    self.assertEqual(updated_user.email, 'newemail@example.com')


if __name__ == '__main__':
    import unittest

    unittest.main()



