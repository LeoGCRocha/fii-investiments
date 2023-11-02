class InvestimentException(Exception):
    def __init__(self, message:str="Investiment class default error."):
        self.message=message
        super().__init__(self.message)