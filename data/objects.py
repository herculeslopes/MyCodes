class User:
    def __init__(self, id, username, password, img_path):
        self.id = id
        self.username = username
        self.password = password
        self.img_path = img_path


    def __repr__(self) -> str:
        return f'{self.id} | {self.username} | {self.password} | {self.img_path}'


class Card:
    def __init__(self, id, title, language, code, user_id):
        self.id = id
        self.title = title
        self.language = language
        self.code = code
        self.user_id = user_id
    

    def __repr__(self) -> str:
        return f'{self.id} | {self.title} | {self.code} | {self.language}'


class Tab:
    def __init__(self, code):
        self.code = code


    def __repr__(self) -> str:
        return f'code: {self.code}'