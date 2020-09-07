import unittest
from apptest.models import User
from . import BaseTestClass


class TestAuth(BaseTestClass):
    """Suite de tests del modelo de autenticación"""

    # comprueba OK si la request contiene la key authorization
    def test_authorization_in_request(self):
        pass


    # comprueba error si la request no contiene la key authorization
    def test_authorization_not_in_request(self):
        """
        with self.app.app_context():
            admin = User.get_by_email('admin@xyz.com')
            post = Post(user_id=admin.id, title='Post de prueba',
                        content='Lorem Ipsum')
            post.save()
            self.assertEqual('post-de-prueba', post.title_slug)
        """
        pass


    # Comprueba OK si la request incluye username
    def test_username_in_request(self):

        pass

    # Comprueba error si la request no incluye username
    def test_username_not_in_request(self):
        pass


    # Comprueba OK si la request incluye password
    def test_password_in_request(self):
        pass


    # Comprueba error si la request no incluye password
    def test_password_not_in_request(self):
        pass


    # Comprueba OK si la request incluye el username de un usuario que existe en la bdd
    def test_user_exists(self):
        pass

    # Comprueba error si la request incluye el username de un usuario que no existe en la bdd
    def test_user_do_not_exists(self):
        pass


    # Comprueba OK si el hash de la contraseña del usuario a autenticar es igual al hash de la contraseña del usuario en bdd
    def test_user_pwd_hash_equals_user_pwd_bdd(self):
        pass


    # Comprueba error si el hash de la contraseña del usuario a autenticar no igual all hash de la contraseña del usuario en bdd
    def test_auth_user_pwd_hash_not_equals_user_pwd_bdd(self):
        pass
