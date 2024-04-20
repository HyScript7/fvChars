class DuplicateTitleValueException(Exception):
    def __init__(self, title: str):
        super().__init__(f"A duplicate title with the value '{title}' already exists")
