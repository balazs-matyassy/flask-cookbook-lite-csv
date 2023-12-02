from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, username='', digest=None, admin=False, user_id=None, password=None, role=None):
        self.user_id = user_id
        self.username = username
        self.digest = digest
        self.admin = admin
        self.password = password
        self.role = role

    @property
    def entity_id(self):
        return self.user_id

    @property
    def role(self):
        return 'admin' if self.admin else 'user'

    @role.setter
    def role(self, value):
        if value and len(value.strip()) > 0:
            self.admin = value.strip().lower() == 'admin'

    @property
    def password(self):
        return None

    @password.setter
    def password(self, value):
        if value and len(value) > 0:
            self.digest = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.digest, password)

    def update(self, data):
        self.username = (data.get('username') or '').strip().lower()
        self.password = data.get('password') or ''
        self.admin = (data.get('role') or '').strip().lower() == 'admin'

    def validate(self):
        errors = []

        if self.username == '':
            errors.append('Username missing.')

        if self.digest is None:
            errors.append('Password missing.')

        return errors

    def to_line(self, delimiter='\t'):
        return (
            f'{self.user_id}{delimiter}{self.username}'
            f'{delimiter}{self.digest}{delimiter}{self.role}'
        )

    @staticmethod
    def create_from_line(line, delimiter='\t'):
        if not line or line.strip() == '':
            return None

        values = line.strip().split(delimiter)

        return User(
            user_id=int(values[0].strip()),
            username=values[1].strip(),
            digest=values[2].strip(),
            role=values[3]
        )
