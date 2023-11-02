from flask import Flask, render_template, request, redirect, url_for
from assets.investiment import Investiment
from assets.reit import Reit
from helper.yaml import parse_yaml_to_dic
from datetime import datetime
import os

class InvestmentApp:
    def __init__(self):
        self.current_date = datetime.now()
        self.assets_dict = {}
        today_string = self.current_date.strftime("%d-%m-%Y")
        file_format = "database/{}_dividends.yaml".format(today_string)
        if not os.path.exists(file_format):
          print("Set to backup file because today file does not exists.")
          file_format = "database/dividend_bckp.yaml"
        inv_dic = parse_yaml_to_dic(file_format)
        for stock in inv_dic:
          for key, asset in stock.items():
            asset_tuple = (
                asset['price'],
                asset['last_payment'],
                asset['average_payment'],
                asset['patrimony_price'],
            )
            self.assets_dict[key] = Reit(key, *asset_tuple)

        self.app = Flask(__name__)

        @self.app.route("/")
        def home_page():
            return render_template("index.html")

        @self.app.route("/calculate", methods=["POST"])
        def calculate():
            print("ok")
            if request.method == "POST":
                goal = request.form['objetivo-input-choice']
                if goal != "Ao atingir magic number":
                  goal_value = float(request.form['objetivo-input'])
                monthly_apply = float(request.form['aporte-mensal-input'])
                start_amount = float(request.form['montante-inicial-input'])
                fii = request.form['cota-input']
                current_date = datetime.now()
                if fii not in self.assets_dict:
                    return redirect(url_for("home_page"))
                INVESTIMENT = Investiment(current_date, self.assets_dict[fii], monthly_apply)
                if goal == "Por lucro obtido":
                  INVESTIMENT.profit_goal = float(goal_value)
                elif goal == "Por montante total":
                  INVESTIMENT.amount_goal = float(goal_value)
                elif goal == "Por rendimento mensal":
                  INVESTIMENT.monthly_earning_goal = float(goal_value)
                if start_amount != 0:
                  INVESTIMENT.start_amount = start_amount
                INVESTIMENT.reach_goal()
                investiments_results = INVESTIMENT.get_results()
                return render_template("investiments.html", fii=investiments_results)

    def run(self):
      self.app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    app_instance = InvestmentApp()
    app_instance.run()
