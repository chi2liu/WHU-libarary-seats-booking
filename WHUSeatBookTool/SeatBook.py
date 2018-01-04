import json
import time

import requests

import timetrans

class SeatBook(object):

    def __init__(self, username='', password=''):
        self.sessions = requests.session()
        self.name = username
        self.passwd = password
        self.token = self.get_token_by_login()
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'token': self.token,
            'Host': 'seat.lib.whu.edu.cn:80',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }

    def get_resp_json(self, url):
        resp = self.sessions.get(url=url, headers=self.headers)
        return json.loads(resp.text)

    def get_token_by_login(self):
        loginURL = 'http://seat.lib.whu.edu.cn/rest/auth?username='+self.name+'&password='+self.passwd
        loginHeaders = {
            'Host': 'seat.lib.whu.edu.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'safedog-flow-item='
        }
        # 登录认证，获取token
        resp = self.sessions.get(loginURL, headers=loginHeaders)
        data = json.loads(resp.text)
        return data['data']['token']

    def print_lib_info(self, libSelected):
        libsInfo = self.get_resp_json(url='http://seat.lib.whu.edu.cn/rest/v2/free/filters')
        rooms = []
        for room in libsInfo['data']['rooms']:
            if room[2] == int(libSelected):
                rooms.append({room[0]:room[1]})
        for room in rooms:
            for key in room.keys():
                print(str(key) + ':' + room[key])

    def book_free_seat(self, startTime, endTime, seatID):
        data = {
            '"t': '1',
            'ip_restrict': 'true',
            'startTime': startTime,
            'endTime': endTime,
            'seat': seatID,
            't2': '2"'
        }
        print('已为您搜索到空闲座位，正在为您预约')
        print('......')
        resp = self.sessions.post('http://seat.lib.whu.edu.cn/rest/v2/freeBook', headers=self.headers, data=data)
        book = json.loads(resp.text)
        if book['status'] == 'fail':
            print('预约失败')
            print('原因：'+book['message'])
        elif book['status'] == 'success':
            print('预约成功')
            print('时间：', book['data']['onDate'], book['data']['begin'], '--', book['data']['end'])
            print('地址：', book['data']['location'])



    def get_seats_info(self, roomSeatInfo):
        res = []
        seatKeys = roomSeatInfo.keys()
        for key in seatKeys:
            if roomSeatInfo[key]['type'] == 'empty':
                continue
            res.append(roomSeatInfo[key])
        return res

    def get_all_seats(self, roomsSelected, endTime):
        allSeats = []
        for room in roomsSelected:
            roomSearchURL = 'http://seat.lib.whu.edu.cn/rest/v2/room/layoutByEndMinutes/' + room + '/' + endTime
            roomSeatInfo = self.get_resp_json(url=roomSearchURL)['data']['layout']
            allSeats += self.get_seats_info(roomSeatInfo)
            time.sleep(1)
        return allSeats

    def search_seat(self, seats, roomlist, startTime, endTime):
        notFound = True
        count = 0
        num = 1
        print('正在为您搜索空闲座位，请稍候...')
        print('......')
        while notFound:
            for seat in seats:
                if seat['status'] == 'FREE':
                    self.book_free_seat(startTime, endTime, seat['id'])
                    notFound = False
                    break
            if notFound:
                print('当前暂时没有空闲座位...正在为您继续搜索第',num,'次...请耐心等待')
                print('......')
                num = num + 1
                time.sleep(1)
                count = (count + 1) * len(roomlist)
                if count > 30 :
                    print('为了避免被系统加入黑名单，将暂停15s后继续为您搜索')
                    print('.......')
                    time.sleep(15)
                    print('重新开始为您搜索')
                    count = 0
                seats = self.get_all_seats(roomlist, endTime)
                count = count / len(roomlist)

    def book(self):
        print('1：信息分馆\n'
              '2: 工学分馆\n'
              '3: 医学分馆\n'
              '4: 总馆')
        print('-------------------------------')
        lib = input('输入您要预约的图书馆的编号： ')

        print('-------------------------------')
        self.print_lib_info(lib)
        print('--------------------')
        bookrooms = input('请输入您需要预约的房间的编号（可以输入多个，请用空格隔开，如：8 9 12）:\n')
        roomlist = bookrooms.split(' ')
        print('-------------------------------')
        timelist = timetrans.gettimelist()
        timetrans.printstarttime(timelist)
        print('--------------------')
        inputStartTime = input('输入您要预约的开始时间的编号: ')
        startTime = timetrans.trans(int(inputStartTime))
        print('-------------------------------')
        timetrans.printendtime(timelist, int(inputStartTime))
        print('-------------------------------')
        inputEndTime = input('输入您要预约的结束时间的编号: ')

        endTime = timetrans.trans(int(inputEndTime))

        print('信息收集完成，开始为您搜索空闲座位，请稍候...')
        print('-------------------------------')
        seats = self.get_all_seats(roomlist, endTime)
        self.search_seat(seats, roomlist, startTime, endTime)