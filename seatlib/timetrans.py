import datetime

start = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0))

def gettimelist():
    timeList = {}
    key = 1
    for i in range(480, 1350, 30):
        timeList[key] = start + datetime.timedelta(minutes=i)
        key = key + 1
    return timeList

def printstarttime(timeList, printNow=True):
    deltaHour = datetime.datetime.today().time().hour - 8
    deltaMinute = datetime.datetime.today().time().minute

    if deltaHour >= 0:
        if deltaMinute >= 30:
            begin = (deltaHour + 1) * 2 + 1
        else:
            begin = (deltaHour + 1) * 2
    else:
        begin = 1

    if printNow:
        print('0','--','现在')
    for i in range(begin, len(timeList)+1):
        print(i, '--', timeList[i].strftime('%H:%M'))

def printendtime(timeList, start):
    if start == 0:
        printstarttime(timeList, printNow=False)
    else:
        for i in range(start, len(timeList)):
            print(i+1, '--', timeList[i+1].strftime('%H:%M'))

# 17:00 转到 1020
def trans(timeNo):
    if timeNo == 0:
        return '-1'
    timelist = gettimelist()
    target = timelist[timeNo]
    delta = target - start
    return str(int(delta.total_seconds()/60))