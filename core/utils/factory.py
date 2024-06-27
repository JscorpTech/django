import abc

import faker


class BaseFaker(abc.ABC):
    def __init__(self):
        self.faker = faker.Faker()
