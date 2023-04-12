import random


class EXC_PROFILE_USER:
    def __init__(self, username=None, ip_addresses=None, password=None, id_=random.randrange(10000000, 99999999)):
        if ip_addresses is None:
            ip_addresses = []
        self.username = username,
        self.password = password,
        self.ip_addresses = ip_addresses,
        self.id_ = id_
        self.isActive = False


