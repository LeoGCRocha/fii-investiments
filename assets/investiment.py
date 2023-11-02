from datetime import datetime
from dateutil.relativedelta import relativedelta
from .reit import Reit
from math import floor
from .exceptions import InvestimentException
import logging

class Investiment:
    def __init__(self, 
                start_date:datetime, 
                asset:Reit, 
                monthly_apply:float,
                amount_goal:float=None,
                monthly_earning_goal:float=None,
                date_goal:datetime=None,
                profit_goal=None,
                start_amount = 0.0):
        self.start_date = start_date
        self.asset = asset
        self.current_date = start_date
        self.start_amount = 0.0
        self.current_amount = 0.0
        self.earnings = []
        self.total_shares = 0.0
        self.current_monthly_earning = 0.0
        self.monthly_apply = monthly_apply
        self.amount_goal = amount_goal
        self.monthly_earning_goal = monthly_earning_goal
        self.date_goal = date_goal
        self.rest_of_investiments = 0.0
        self.profit = 0.0
        self.profit_goal = profit_goal
        self.start_amount = start_amount
        FORMAT = '%(name)s - %(message)s'
        logging.basicConfig(format=FORMAT, level=logging.INFO)
        self.logger = logging.getLogger(self.asset.name)

    def log_results(self):
        self.logger.info(">> RELATÓRIO FINAL DOS RENDIMENTOS <<")
        self.logger.info(">> Montante total investido: R$ %.2f", self.current_amount)
        self.logger.info(">> Valor de lucro em investimento: R$ %.2f", self.profit)
        self.logger.info(">> Valor Real investido: R$ %.2f", self.current_amount - self.profit)
        self.logger.info(">> Número total de cotas: %d", self.total_shares)
        self.logger.info(">> Rendimento mensal: R$ %.2f", self.current_monthly_earning)
        time_investiments_in_months = (self.current_date.year - self.start_date.year) * 12 + \
            (self.current_date.month - self.start_date.month)
        self.logger.info(">> Tempo total de investimento: %d meses", time_investiments_in_months)
        self.logger.info(">> Tempo total de investimento: %d anos e %d meses", 
                        time_investiments_in_months // 12, time_investiments_in_months % 12)

    def get_results(self):
      time_investiments_in_months = (self.current_date.year - self.start_date.year) * 12 + \
            (self.current_date.month - self.start_date.month)
      return {
        "name": self.asset.name,
        "amount": self.current_amount,
        "profit": self.profit,
        "real_value_investiment": self.current_amount - self.profit,
        "total_shares": int(self.total_shares),
        "monthly_earning": self.current_monthly_earning,
        "time_investiments_in_months": time_investiments_in_months,
        "time_investiments_in_years": [ int(time_investiments_in_months // 12), int(time_investiments_in_months % 12) ]
      }

    def reach_goal(self, explicit=False):
        if explicit:
            self.logger.setLevel(logging.DEBUG)
        # Goals priority:
        # 1. End Date
        # 2. Total Amount
        # 3. Monthly Earnings
        # 4. Profit
        # 5. Magic Number
        if (self.monthly_apply % self.asset.price != 0):
            self.monthly_apply = (self.monthly_apply // self.asset.price) * self.asset.price
            self.logger.info("Valor mensal de aplicação ajustado para %.2f para valor ficar multiplo do preço da cota.",
                            self.monthly_apply)
            self.logger.info("Com este valor serão compradas %d cotas ao mês.", (self.monthly_apply // self.asset.price))
        
        # Adjust values if start_amount is diff. of 0.0
        if self.start_amount > 0.0:
            # Adjust price to correct amount using current asset price
            self.start_amount = (self.start_amount // self.asset.price) * self.asset.price
            self.logger.info("Valor de montate foi ajustado para compra exata do número de cotas, montante atual de: R$ %.2f", 
                      self.start_amount)
            self.total_shares = self.start_amount // self.asset.price
            self.logger.info("Com este valor foi possivel comprar um total de %d cotas", self.total_shares)
            self.current_monthly_earning = self.total_shares * self.asset.last_payment
            self.logger.info("Rendimento atual destas ações é de R$ %.2f ", self.current_monthly_earning)

        if self.date_goal:
            while self.current_date < self.date_goal:
                self.next_month()
        elif self.amount_goal:
            self.logger.debug('Iniciando o cálculo de rendimentos até alcançar o montante de R$ %.2f',
                            self.amount_goal)
            while self.current_amount < self.amount_goal:
                self.next_month()
        elif self.monthly_earning_goal:
            # Monthly Earnings goal
            self.logger.debug('Iniciando o cálculo de rendimentos até alcançar o valor mensal de %.2f', 
                            self.monthly_earning_goal)
            while self.current_monthly_earning < self.monthly_earning_goal:
                self.next_month()
        elif self.profit_goal:
            self.logger.debug('Iniciando o cálculo de rendimento até o alcançar o lucro de %.2f',
                              self.profit_goal)
            while self.profit < self.profit_goal:
              self.next_month()
        else:
            self.logger.info('Iniciando o cálculo do prazo para atingir o MAGIC NUMBER')
            self.asset.calculate_magic_number()
            while self.total_shares < self.asset.magic_number_in_shares:
                self.next_month()

    def next_month(self):
        # Eearning object monthly
        earning = Earning(self.current_date, 
                        self.current_amount, 
                        self.total_shares, 
                        self.current_monthly_earning)
        self.logger.debug('Calculando rendimentos para %s', self.current_date.strftime("%d-%m-%Y"))
        self.current_date = self.current_date + relativedelta(months=1)
        # Calculate values
        month_earning = self.total_shares * self.asset.last_payment
        self.profit = self.profit + month_earning
        self.current_amount = self.current_amount + self.current_monthly_earning + self.monthly_apply
        temp_new_shares = (self.monthly_apply + self.current_monthly_earning) / self.asset.price
        self.total_shares = self.total_shares + floor(temp_new_shares)
        self.current_monthly_earning = self.total_shares * self.asset.last_payment
        # Use the rest of monthly earning
        temp_calc = (self.monthly_apply + self.current_monthly_earning) % self.asset.price
        self.rest_of_investiments += temp_calc
        if self.rest_of_investiments >= self.asset.price:
            self.rest_of_investiments -= self.asset.price
            self.total_shares += 1
        # Update earning informations for the end of the month
        earning.end_amount = self.current_amount
        earning.end_number_of_shares = self.total_shares
        earning.current_monthly_earning = self.current_monthly_earning
        self.earnings.append(earning)

class Earning:
    def __init__(self, 
                date:datetime, 
                start_amount:float, 
                start_number_of_shares:int,
                current_monthly_earning:float):
        self.date = date
        self.current_amount = start_amount
        self.end_amount = 0.0
        self.start_number_of_shares = start_number_of_shares
        self.end_number_of_shares = 0.0
        self.current_monthly_earning = current_monthly_earning