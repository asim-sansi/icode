class Webpage:
    def __init__(self):
        self.elements = []

    def addElement(self, e):
        self.elements.append(e);

    def setElements(self, e):
        self.elements = e

    def getelements(self):
        return self.elements
