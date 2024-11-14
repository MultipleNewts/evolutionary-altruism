import random


class Member:
    def __init__(self, id):
        self.id = id
        self.score = 0

    def receive_2(self, choice):
        pass

    def receive_3(self, choice1, choice2):
        pass

    def reset(self):
        pass

    def score_reset(self):
        self.score = 0

    def update_score(self, points):
        self.score += points


class AlwaysCheat(Member):
    def __init__(self, id, label="Always Cheat"):
        super().__init__(id)
        self.label = label

    def eval(self):
        return False


class AlwaysCoop(Member):
    def __init__(self, id, label="Always Coop"):
        super().__init__(id)
        self.label = label

    def eval(self):
        return True


class Random(Member):
    def __init__(self, id, label="Random"):
        super().__init__(id)
        self.label = label

    def eval(self):
        return bool(random.randint(0, 1))


class Grudger(Member):
    def __init__(self, id, label="Grudger"):
        super().__init__(id)
        self.label = label
        self.grudge = True

    def eval(self):
        if self.grudge is False:
            return False
        else:
            return True

    def reset(self):
        self.grudge = True

    def receive_2(self, choice):
        if choice is False:
            self.grudge = choice

    def receive_3(self, choice1, choice2):
        if (choice1 is False) or (choice2 is False):
            self.grudge = False


class CopyCat(Member):
    def __init__(self, id, label="CopyCat"):
        super().__init__(id)
        self.label = label
        self.last = True

    def eval(self):
        return self.last

    def reset(self):
        self.last = True

    def receive_2(self, choice):
        self.last = choice

    def receive_3(self, choice1, choice2):
        if (choice1 is False and choice2 is False):
            # if (choice1 is False and choice2 is False):
            self.last = False
        else:
            self.last = True


class CopyCatVariant(CopyCat):
    def receive_3(self, choice1, choice2):
        if (choice1 is False or choice2 is False):
            # if (choice1 is False and choice2 is False):
            self.last = False
        else:
            self.last = True


class CopyKitten(CopyCat):
    def __init__(self, id, label="CopyCat"):
        super().__init__(id, label)
        self.last1 = True
        self.last2 = True

    def receive_2(self, choice):
        self.last2 = self.last1
        self.last1 = choice

    def receive_3(self, choice1, choice2):
        self.last2 = self.last1
        if (choice1 is False and choice2 is False):
            # if (choice1 is False and choice2 is False):
            self.last = False
        else:
            self.last = True

    def eval(self):
        if (self.last1 is False and self.last2 is False):
            return False
        return True


class CopyKittenVariant(CopyKitten):
    def receive_3(self, choice1, choice2):
        self.last2 = self.last1
        if (choice1 is False or choice2 is False):
            # if (choice1 is False and choice2 is False):
            self.last = False
        else:
            self.last = True
