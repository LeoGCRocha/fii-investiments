from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import os
import yaml
import time

YAML_PATH = "database/"
current_time = datetime.now().strftime("%d-%m-%Y")
yaml_file = "{}_dividends.yaml".format(current_time)
yaml_file_path = YAML_PATH + yaml_file

if os.path.exists(yaml_file_path):
  print("Today dividends file already exists.")
else:
  driver = webdriver.Chrome()
  driver.get("https://fiis.com.br/resumo/")
  # Accept cookies
  try:
    time.sleep(5)
    accept_cookies_button = driver.find_element(By.ID, "adopt-accept-all-button")
    accept_cookies_button.click()
  except Exception:
      print("Failed to click button")
  # Get information from table
  table = driver.find_element(By.CLASS_NAME, "default-fiis-table__container__table") 
  table_data = []
  rows = table.find_elements(By.TAG_NAME, "tr")
  for row in rows:
      cells = row.find_elements(By.TAG_NAME, "td")
      cell_data = [cell.text.replace(".","").replace(",",".") for cell in cells]
      table_data.append(cell_data)
  table_data.pop(0)
  dividend_elements = []
  list_of_all_reits = []
  for element in table_data:
    list_of_all_reits.append(element[0])
    dividend_elements.append({
      element[0]: {
        "patrimony_price": float(element[-1]) if element[-1] != "N/A" else 0.0,
        "price": float(element[-2]) if element[-2] != "N/A" else 0.0,
        "average_payment": float(element[-4]) if element[-4] != "N/A" else 0.0,
        "last_payment": float(element[1]) if element[1] != "N/A" else 0.0
      }
    })
  with open(yaml_file_path, 'w') as file:
    yaml.dump(dividend_elements, file)
  with open(YAML_PATH + "reits.txt", 'w') as file:
    string_list = "\n".join(list_of_all_reits)
    file.write(string_list)
  driver.quit()