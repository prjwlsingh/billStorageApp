import uuid

class Bill:

    def __init__(self, title, date, description, cloudPath, tag):
        self.id = uuid.uuid4().hex
        self.title = title
        self.date = date
        self.description = description
        self.cloudPath = cloudPath
        self.tag = tag

    def __str__(self):
        return  f'id:{self.id} ' \
                f'Title: {self.title}; ' \
                f'Date: {self.date}; ' \
                f'Description: {self.description}; ' \
                f'cloudPath = {self.cloudPath}; ' \
                f'tag = {self.tag}'
            