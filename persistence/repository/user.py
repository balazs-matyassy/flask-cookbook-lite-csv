from persistence import get_path, get_delimiter
from persistence.model.user import User


class UserRepository:
    @staticmethod
    def install():
        UserRepository.__store_all([])

    @staticmethod
    def find_all():
        with open(get_path('users.txt'), encoding='utf-8') as file:
            delimiter = get_delimiter()
            users = []

            file.readline()  # header

            for line in file:
                user = User.create_from_line(line, delimiter)
                users.append(user)

            return users

    @staticmethod
    def find_by_id(user_id):
        for user in UserRepository.find_all():
            if user.user_id == user_id:
                return user

        return None

    @staticmethod
    def find_by_username(username):
        for user in UserRepository.find_all():
            if user.username.lower() == username.lower():
                return user

        return None

    @staticmethod
    def save(user):
        users = UserRepository.find_all()

        for i in range(len(users)):
            if users[i].username == user.username \
                    and users[i].user_id != user.user_id:
                raise ValueError(f'Duplicate username {user.username}.')

        if user.user_id is None:
            max_id = 0

            for i in range(len(users)):
                if users[i].user_id > max_id:
                    max_id = users[i].user_id

            user.user_id = max_id + 1
            users.append(user)
        else:
            for i in range(len(users)):
                if users[i].user_id == user.user_id:
                    users[i] = user
                    break

        UserRepository.__store_all(users)

        return user

    @staticmethod
    def delete_by_id(user_id):
        users = UserRepository.find_all()

        for i in range(len(users)):
            if users[i].user_id == user_id:
                users.pop(i)
                break

        UserRepository.__store_all(users)

    @staticmethod
    def __store_all(users):
        with open(get_path('users.txt'), 'w', encoding='utf-8') as file:
            delimiter = get_delimiter()

            file.write(f'id{delimiter}username{delimiter}digest{delimiter}role\n')

            for user in sorted(users, key=lambda item: f'{item.role}\0{item.username}'):
                file.write(f'{user.to_line(delimiter)}\n')
