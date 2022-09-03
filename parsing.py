from bs4 import BeautifulSoup
import requests as req
import datetime as dt

class Lesson:
    def __init__(self, date ,timeOfLesson, nameOfLesson, typeOfLesson, addresOfLesson,teacherNameOfLesson):
        """Constructor"""
        self.date = date
        self.time = timeOfLesson
        self.name = nameOfLesson
        self.type = typeOfLesson
        self.addres = addresOfLesson
        self.teacherName = teacherNameOfLesson

class Day:
    def __init__(self, date, *les):
        self.date = date
        self.lessons = les
    def MyPrint(self):
        for ls in self.lessons:
            les = ''
            for lesson in ls:
                les += ''.join(lesson.time+" "+lesson.name+' '+lesson.type+' '+lesson.addres)
                les += '\n'
        return self.date + les

date = dt.datetime.now()
findingYear, findingMonth,findingDay = date.year,date.month,date.day
current_day = str(findingYear)+'-'+'{:02d}'.format(findingMonth)+'-'+'{:02d}'.format(findingDay)

def ParsingTimeTable():
    ans= ''
    SavingDays = []
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
        ans +=  str(findingYear) +'-' +'{:02d}'.format(monthPars) + '-' + '{:02d}'.format(dayPars)+'\n'
        date = str(findingYear) + '-' + '{:02d}'.format(monthPars) + '-' + '{:02d}'.format(dayPars) + '\n'
        lessons = day.findAll(class_="common-list-item row")
        SavingLesson = []
        for lesson in lessons:

            timeOfLesson = ' '.join(lesson.find(class_="col-sm-2 studyevent-datetime").text.split())
            nameOfLesson = ' '.join(lesson.find(class_="col-sm-4 studyevent-subject").text.split())
            nameOfLesson,typeOfLesson = nameOfLesson.split(',')
            typeOfLesson = typeOfLesson.strip()
            teacherNameOfLesson = ' '.join(lesson.find(class_="col-sm-3 studyevent-educators").text.split())
            try:

                addresOfLesson = ' '.join(lesson.find(class_="col-sm-3 studyevent-locations").text.split())


            except AttributeError:
                try:
                    addresOfLesson = ' '.join(lesson.find(class_="hoverable link").text.split())

                except AttributeError:
                    addresOfLesson = ''

            if addresOfLesson.find('Университетский проспект, д. 35, корп') != -1:
                if not (addresOfLesson[-1] in "1234567890"):
                    addresOfLesson = addresOfLesson[addresOfLesson.rfind(','):]
                else:
                    addresOfLesson = ''.join(addresOfLesson[addresOfLesson.rfind('.') + 2:].split(',')[::-1])
            # print('\t'+ ' '.join(lesson.text.split()))
            print('\t', timeOfLesson, nameOfLesson,typeOfLesson,addresOfLesson,teacherNameOfLesson,sep='|')
            ans += '\t' + ' ' + timeOfLesson + ' ' + nameOfLesson + ' ' + typeOfLesson + ' ' + addresOfLesson + ' ' + teacherNameOfLesson + '\n'
            SavingLesson.append(Lesson(date ,timeOfLesson, nameOfLesson, typeOfLesson, addresOfLesson,teacherNameOfLesson))
        SavingDays.append(Day(date, SavingLesson))
        print('\n')
        ans += '\n'
    #return ans
    return SavingDays
