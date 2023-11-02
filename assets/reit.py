# Real Estate Investment Trust (Fundo Imobiliário)
from math import ceil
from typing import Union
class Reit:
    def __init__(self, name: str, 
                price: float, 
                last_payment: float, 
                dividend_yield:float=None, 
                magic_number_in_shares:float=None):
        self.name = name
        self.price = price
        self.last_payment = last_payment
        self.dividend_yield = dividend_yield
        self.magic_number_in_shares = magic_number_in_shares 
    def calculate_magic_number(self) -> None:
        self.magic_number_in_shares = ceil(self.price / self.last_payment)
    def magic_number_total_value(self) -> Union[float, ValueError]:
        if self.magic_number_in_shares != None:
            return self.magic_number_in_shares * self.price
        raise ValueError("Magic number cannot be None when trying to calculate TOTAL_VALUE.")