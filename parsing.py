from bs4 import BeautifulSoup
import requests as req
import datetime as dt

ruMonths = ['','января', 'февраля', 'мара', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
          'октября', 'ноября', 'декабря']

date = dt.datetime.now()
findingYear, findingMonth,findingDay = date.year,date.month,date.day
current_day = str(findingYear)+'-'+'{:02d}'.format(findingMonth)+'-'+'{:02d}'.format(findingDay)
url = "https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/334302/"+current_day
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.3.822 Yowser/2.5 Safari/537.36",
    "Accept-Language": "ru"
}

resp = req.get(url, headers=headers)
src = resp.text
with open("index2.html", "w", encoding="utf-8")as file:
    file.write(src)

with open("index2.html", encoding="utf-8") as file:
    src = file.read()
soup = BeautifulSoup(src, 'html.parser')
# soup = BeautifulSoup(src, 'lxml')
days = soup.findAll(class_="panel-collapse nopadding nomargin")

for day in days:
    s = (' '.join(day.parent.find(class_="panel-heading").text.split()))
    s = s[s.find(",") + 2:]
    dayPars, monthPars = int(s.split()[0]), ruMonths.index(s.split()[1])
    print(str(findingYear) +'-' +'{:02d}'.format(monthPars) + '-' + '{:02d}'.format(dayPars))

    lessons = day.findAll(class_="common-list-item row")
    for lesson in lessons:
        timeOfLesson = ' '.join(lesson.find(class_="col-sm-2 studyevent-datetime").text.split())
        nameOfLesson = ' '.join(lesson.find(class_="col-sm-4 studyevent-subject").text.split())
        try:
            addresOfLesson = ' '.join(lesson.find(class_="col-sm-3 studyevent-locations").text.split())
            teacherNameOfLesson = ' '.join(lesson.find(class_="col-sm-3 studyevent-educators").text.split())
        except AttributeError:
            addresOfLesson = ''
            teacherNameOfLesson = ''
        # print('\t'+ ' '.join(lesson.text.split()))
        print('\t' + timeOfLesson + nameOfLesson + addresOfLesson + teacherNameOfLesson)
    print('\n')
