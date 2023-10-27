import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from tabulate import tabulate
import sys

def getName(id):
  url = "https://tw-camping.tw/hotel_info.asp?hid={}".format(id)
  response = requests.get(url)
  content = response.content.decode('utf-8')

  body = BeautifulSoup(content, 'html.parser')
  titleDiv = body.find('section', id="page-title")
  name = titleDiv.find('h1').text
  info = titleDiv.find('span').text
  return (name, info)

def getDatas(id):
  now = datetime.now()
  monday = now - timedelta(days=now.weekday())
  current = monday + timedelta(days=5)
  end = current.replace(year=current.year + 1, day=1)

  nameMap = {}
  results = {}
  while current.timestamp() < end.timestamp():
    date = "{}-{:02d}-{:02d}".format(current.year, current.month, current.day)
    print("Handling {}".format(date))
    response = requests.get("https://tw-camping.tw/ajax/hlist.asp?hid={}&d1={}&daynight=2".format(id, date))
    content = response.content.decode('utf-8')

    body = BeautifulSoup(content, 'html.parser')
    sections = body.find_all('div', class_='oc-item')
    result = {}
    empty = False
    for section in sections:
      try:
        name = section.find('div', class_='entry-title').text.strip()
        status = section.find('div', class_='entry-date').text.strip()
        result[name] = status
        if name not in nameMap:
          nameMap[name] = True
        if status != '已滿':
          empty = True
      except Exception as e:
        print(e)
    results[date] = result

    # if empty:
    #   print("{}".format(date))
    #   for key in result:
    #     if result[key] != '已滿':
    #       print("\t{}{}".format(result[key].ljust(10), key))

    # else:
    #   print("{} 全滿".format(date))
    current = current + timedelta(days=7)


  names = [key for key in nameMap.keys()]
  data = []

  dates = [key for key in results.keys()]
  dates.sort()
  for date in dates:
    row = [date]
    for name in names:
      if name in results[date]:
        row.append(results[date][name])
    data.append(row)

  headers = ['Date'] + names
  return tabulate(data, headers=headers, tablefmt="github")

if len(sys.argv) < 2:
  print("Usage: python main.py <id>")

id = sys.argv[1]
(name, info) = getName(id)
tableData = getDatas(id)

print(name)
print(info)
print(tableData)
