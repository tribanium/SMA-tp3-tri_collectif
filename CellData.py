class Cell:

    def __init__(self, obj=None, agent=None):
        self.objects = obj
        self.agent = agent


class Object:

    def __init__(self, key, category, position):
        self.key = key
        self.category = category
        self.position = position


class AgentData:

    def __init__(self, key, agent, position):
        self.key = key
        self.agent = agent
        self.position = position
