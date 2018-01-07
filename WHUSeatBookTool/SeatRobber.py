import json
import time

import requests

from SetPeriod import TimeNode
from SendEmail import send_email


class Robber(object):
    """
    Robber类:实现抢座的核心功能类
    """
    def __init__(self, username='', password='', address=''):
        """
        初始化方法，接受用户名和密码
        1.初始化session
        2.模拟登陆获取token
        :param username: 用户名
        :param password: 密码
        """
        self.sessions = requests.session()
        self.username = username
        self.password = password
        self.address = address
        self.token = self.get_token_by_login()
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'token': self.token,
            'Host': 'seat.lib.whu.edu.cn:80',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KH'
                          'TML, like Gecko) Chrome/63.0.3239.84 Safari/537.36 '
        }

    def get_token_by_login(self, code: str = 'utf-8') -> str:
        """
        模拟登录获取token
        :param code:
        :return: 返回token
        """
        login_url = 'http://seat.lib.whu.edu.cn/rest/auth?username={0}&password={1}'.format(self.username,
                                                                                            self.password)
        login_headers = {
            'Host': 'seat.lib.whu.edu.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KH'
                          'TML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        # 登录认证，获取token
        resp = self.sessions.get(login_url, headers=login_headers)
        resp.raise_for_status()
        resp.encoding = code
        data = json.loads(resp.text)
        return data['data']['token']

    def get_response_json(self, url: str, code: str = 'utf-8') -> dict:
        """
        接受url和headers获取请求的返回json
        :param url: 请求的url
        :param code: 编码
        :return: 返回response的json
        """
        resp = self.sessions.get(url=url, headers=self.headers)
        resp.raise_for_status()
        resp.encoding = code
        return json.loads(resp.text)

    def get_rooms_of_lib(self, lib_selected):
        """
        获取指定场馆的房间信息
        :param lib_selected: 用户输入的所选择的预约场馆的编号
        :return: 返回该场馆的房间信息
        """
        libs_info = self.get_response_json(url='http://seat.lib.whu.edu.cn/rest/v2/free/filters')
        rooms = []
        for room in libs_info['data']['rooms']:
            if room[2] == int(lib_selected):
                rooms.append({room[0]: room[1]})
        return rooms

    @staticmethod
    def print_rooms(rooms):
        """
        打印出房间信息，供用户选择
        编号：房间名
        :param rooms: 指定场馆的房间信息，list
        :return: 无返回值
        """
        for room in rooms:
            for key in room.keys():
                print(str(key) + ':' + room[key])

    def set_rooms(self) -> list:
        """
        与用户进行交互，获取需要预约的房间
        :return: 用户选择需要预约的房间列表
        """
        print('-------------------------------')
        print('1：信息分馆\n'
              '2: 工学分馆\n'
              '3: 医学分馆\n'
              '4: 总馆')

        lib = input('输入您要预约的图书馆的编号： ')
        print('-------------------------------')
        rooms = self.get_rooms_of_lib(lib)
        self.print_rooms(rooms)
        print('--------------------')
        book_rooms = input('请输入您需要预约的房间的编号（可以输入多个，请用空格隔开，如：8 9 12）:\n')
        rooms_selected = book_rooms.split(' ')
        print('-------------------------------')
        return rooms_selected

    def book_free_seat(self, start_time, end_time, seat_id):
        """
        预定空闲座位
        :param start_time: 指定的开始时间
        :param end_time: 指定的结束时间
        :param seat_id: 所需预约的座位id
        :return:
        """
        data = {
            '"t': '1',
            'ip_restrict': 'true',
            'startTime': start_time,
            'endTime': end_time,
            'seat': seat_id,
            't2': '2"'
        }
        print('已为您搜索到空闲座位，正在为您预约')
        print('......')
        resp = self.sessions.post('http://seat.lib.whu.edu.cn/rest/v2/freeBook', headers=self.headers, data=data)
        book = json.loads(resp.text)
        if book['status'] == 'fail':
            print('预约失败')
            print('原因：'+book['message'])
            #print(book)
            send_email(self.address, '预约失败', time='原因', seat=book['message'])
        elif book['status'] == 'success':
            print('预约成功')
            print('时间：', book['data']['onDate'], book['data']['begin'], '--', book['data']['end'])
            print('地址：', book['data']['location'])
            send_email(self.address, '预约成功',
                       time='时间：' + book['data']['onDate'] + book['data']['begin'] + '--' + book['data']['end'],
                       seat=book['data']['location'])

    @staticmethod
    def get_seats_info(room_seat_info):
        """
        由于获取指定房间的座位信息，返回的json中，有较多的无用信息
        所以此函数的作用就是筛选出所需要的有用信息
        :param room_seat_info: 查询某个房间座位信息的json
        :return: 筛选出有用信息
        """
        res = []
        seat_keys = room_seat_info.keys()
        for key in seat_keys:
            if room_seat_info[key]['type'] == 'empty':
                continue
            res.append(room_seat_info[key])
        return res

    def get_all_seats(self, rooms_selected, end_time):
        """
        获取所有选中房间的座位信息
        :param rooms_selected: 指定需要预约的房间列表
        :param end_time: 指定的结束时间
        :return: 返回所有房间的座位信息的列表
        """
        all_seats = []
        for room in rooms_selected:
            room_search_url = 'http://seat.lib.whu.edu.cn/rest/v2/room/layoutByEndMinutes/' + room + '/' + end_time
            room_seat_info = self.get_response_json(url=room_search_url)['data']['layout']
            all_seats += self.get_seats_info(room_seat_info)
            time.sleep(1)
        return all_seats

    def search_seat(self, room_list, start_time, end_time):
        """
        从指定的房间列表中搜索空闲座位，并预约
        :param room_list: 指定需要预约的房间列表
        :param start_time: 指定的开始时间
        :param end_time: 指定的结束时间
        :return:
        """
        not_found = True
        count = 0
        num = 1
        seats = self.get_all_seats(room_list, end_time)
        print('正在为您搜索空闲座位，请稍候...')
        print('......')
        while not_found:
            for seat in seats:
                if seat['status'] == 'FREE':
                    self.book_free_seat(start_time, end_time, seat['id'])
                    not_found = False
                    break
            if not_found:
                print('当前暂时没有空闲座位...正在为您继续搜索第', num, '次...请耐心等待')
                print('......')
                num = num + 1
                time.sleep(1)
                count = (count + 1) * len(room_list)
                if count > 30:
                    print('为了避免被系统加入黑名单，将暂停15s后继续为您搜索')
                    print('.......')
                    time.sleep(15)
                    print('重新开始为您搜索')
                    count = 0
                seats = self.get_all_seats(room_list, end_time)
                count = count / len(room_list)

    def robber_seat(self):
        room_list = self.set_rooms()

        time_node = TimeNode()
        start_time, end_time = time_node.set_start_and_end_time_node()

        print('信息收集完成，开始为您搜索空闲座位，请稍候...')
        print('-------------------------------')

        self.search_seat(room_list, start_time, end_time)
