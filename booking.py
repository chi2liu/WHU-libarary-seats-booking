import requests

from seatlib import bookSupport
from seatlib import timetrans

username = input('请输入您的用户名：')
password = input('请输入您的密码：')
sessions = requests.session()
token = bookSupport.getToken(sessions, username, password)
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'token': token,
    'Host': 'seat.lib.whu.edu.cn:80',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

print('1：信息分馆\n'
      '2: 工学分馆\n'
      '3: 医学分馆\n'
      '4: 总馆\n')

lib = input('输入您要预约的图书馆的编号： ')


bookSupport.printlibinfo(sessions, headers, lib=lib)

bookrooms = input('请输入您需要预约的房间的编号（可以输入多个，请用逗号隔开，如：1，2，3）:\n')
roomlist = bookrooms.split(',')

timelist = timetrans.gettimelist()
timetrans.printstarttime(timelist)

print('--------------------')

inputStartTime = input('输入您要预约的开始时间的编号: ')
startTime = timetrans.trans(int(inputStartTime))


timetrans.printendtime(timelist, int(inputStartTime))
inputEndTime = input('输入您要预约的结束时间的编号: ')
endTime = timetrans.trans(int(inputEndTime))

seats = bookSupport.getallseats(sessions, headers, roomlist, endTime)

bookSupport.searchseat(sessions, headers, seats, roomlist,startTime, endTime)

print('finish')