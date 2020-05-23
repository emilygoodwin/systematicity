class Ident:
    nextid = 0

    def __init__(self):
         self.id = Ident.nextid
         Ident.nextid += 1