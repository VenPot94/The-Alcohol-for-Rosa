import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from itertools import repeat

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

new_excel_data_rose = pandas.read_excel('wine3.xlsx', sheet_name='Лист1',
                                        usecols=[
                                            "Категория",
                                            "Название",
                                            "Сорт",
                                            "Цена",
                                            "Картинка",
                                            "Акция"])
new_excel_data_rose = new_excel_data_rose.fillna('')

drinks = new_excel_data_rose.to_dict('record')

total_alcohol = collections.defaultdict(list)

category_list = []
for drink in drinks:
    drink_info = list(drink.values())
    category_list.append(drink_info[0])
final_category_list = sorted(list(dict.fromkeys(category_list)))

for drink in drinks:
    category = drink['Категория']
    total_alcohol[category].append(drink)

founded = datetime.datetime(year=1920, month=3, day=3, hour=0)
current_time = datetime.datetime.now().year

age = current_time-founded.year

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(total_alcohol=total_alcohol,
                                category=category, our_age=age)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
