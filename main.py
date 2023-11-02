from datetime import datetime
from server.server import InvestmentApp
import os
import subprocess

def run_scrap():
  today_string = datetime.now().strftime("%d-%m-%Y")
  file_format = "{}_dividends.yaml".format(today_string)
  if not os.path.exists("database/"+file_format):
    try:
      print("Running operations to get dividends information.")
      proc = subprocess.Popen(["python", "update_dividends.py"])
      proc.wait()
      try:
        with open('database/'+file_format, 'r') as file_today:
          file_today_content = file_today.read()
      except Exception as e:
        with open('database/dividend_bckp.yaml', 'w') as file_bckp:
          file_bckp.write(file_today_content)
    except Exception as e:
      print("Failed to update_dividend: ", e)


def run_flask():
  investiment_app = InvestmentApp()
  investiment_app.run()

def main():
  # Verify if file of today rendiments already exists
  run_scrap()

  # Load layout and run all logic
  run_flask()

if __name__ == "__main__":
    main()
