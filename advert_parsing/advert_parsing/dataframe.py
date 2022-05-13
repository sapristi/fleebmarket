class DataFrame:
    def __init__(self, rows):
        self.rows = rows
        nb_cols = len(self.rows[0])
        self.columns = [[] for _ in range(nb_cols)]
        for row in self.rows:
            for i, cell in enumerate(row):
                self.columns[i].append(cell)

    def applymap(self, fn):
        return DataFrame(
            [
                [fn(cell) for cell in row]
                for row in self.rows
            ]
        )
