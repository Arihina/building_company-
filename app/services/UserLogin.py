from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email, post, id):
        self.email = email
        self.id = int(id)

        if post == 'Директор':
            self.post = 'admin'
        else:
            self.post = 'manager'

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_post(self):
        return self.post
