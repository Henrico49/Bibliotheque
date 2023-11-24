from bibli import bibli

class bibli_scrap(bibli):
    def __init__(self, path):
        self.livres = []
        super().__init__(path)
