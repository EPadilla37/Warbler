from unittest import TestCase
from models import db, User
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:padilla@localhost/warbler_test'
app.config['SQLALCHEMY_ECHO'] = False

class UserViewsTestCase(TestCase):
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

    def test_homepage_logged_out(self):
        """Test if the homepage is displayed correctly when the user is logged out."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h4>New to Warbler?</h4>', response.data)

    def test_homepage_logged_in(self):
        """Test if the homepage is displayed correctly when the user is logged in."""
        with self.app.session_transaction() as session:
            user = User.query.filter_by(username=self.username).one()
            session['user_id'] = user.id

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warbler', response.data)

    def test_user_show(self):
        """Test if a user's profile page is displayed correctly."""
        response = self.app.get(f'/users/{self.username}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h4>@test_user</h4>', response.data)

