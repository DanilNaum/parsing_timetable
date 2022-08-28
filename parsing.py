from bs4 import BeautifulSoup
import requests as req
import datetime as dt

ruMonths = ['января', 'февраля', 'мара', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
          'октября', 'ноября', 'декабря']

date = dt.datetime.now()
current_day = str(date.year)+'-'+'{:02d}'.format(date.month)+'-'+'{:02d}'.format(date.day)
url = "https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/334302/"+current_day
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.3.822 Yowser/2.5 Safari/537.36",
    "Accept-Language": "ru"
}
days=[]
resp = req.get(url, headers=headers)
src = resp.text
with open("index2.html", "w", encoding="utf-8")as file:
    file.write(src)

with open("index2.html", encoding="utf-8") as file:
    src = file.read()
soup = BeautifulSoup(src, 'lxml')
days = soup.findAll(class_="panel-collapse nopadding nomargin")

for day in days:
    s = (' '.join(day.parent.find(class_="panel-heading").text.split()))
    s = s[s.find(",") + 2:]
    day_pars,month_pars = s.split()[0],ruMonths.index(s.split()[1])
    print(day_pars,month_pars)
    lessons = []
    lessons = day.findAll(class_="common-list-item row")
    for lesson in lessons:
        print('\t'+ ' '.join(lesson.text.split()))
    print('\n')
