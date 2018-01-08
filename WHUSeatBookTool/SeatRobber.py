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
        self.xin = {
            4: '一楼3C创客空间',
            5: '一楼创新学习讨论区',
            6: '二楼西自然科学图书借阅区',
            7: '二楼东自然科学图书借阅区',
            8: '三楼西社会科学图书借阅区',
            9: '四楼西图书阅览区',
            10: '三楼东社会科学图书借阅区',
            11: '四楼东图书阅览区',
            12: '三楼自主学习区',
            13: '3C创客-电子资源阅览区（20台）',
            14: '3C创客-双屏电脑（20台）',
            15: '创新学习-MAC电脑（12台）',
            16: '创新学习-云桌面（42台）'
        }

        self.gong = {
            19: '201室+东部自科图书借阅区',
            29: '2楼+中部走廊',
            31: '205室+中部电子阅览室笔记本区',
            32: '301室+东部自科图书借阅区',
            33: '305室+中部自科图书借阅区',
            34: '401室+东部自科图书借阅区',
            35: '405室+中部期刊阅览区',
            37: '501室+东部外文图书借阅区',
            38: '505室+中部自科图书借阅区'
        }

        self.yi = {
            20: '204教学参考书借阅区',
            21: '302中文科技图书借阅B区',
            23: '305科技期刊阅览区',
            24: '402中文文科图书借阅区',
            26: '502外文图书借阅区',
            27: '506医学人文阅览区',
            28: '503培训教室'
        }

        self.zong = {
            39: 'A1-座位区',
            40: 'C1自习区',
            51: 'A2',
            52: 'A3',
            56: 'B3',
            59: 'B2',
            60: 'A4',
            61: 'A5',
            62: 'A1-沙发区',
            65: 'B1',
            66: 'A1-苹果区'
        }
        self.rooms_of_lib = [self.xin, self.gong, self.yi, self.zong]

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
        try:
            resp = self.sessions.get(login_url, headers=login_headers)
            resp.raise_for_status()
            resp.encoding = code
            data = json.loads(resp.text)
        except Exception:
            print('登录失败！')
            return 'login failed!'
        else:
            if data['status'] == 'fail':
                print(data['message'])
                raise SystemExit
            return data['data']['token']

    def get_response_json(self, url: str, code: str = 'utf-8') -> dict:
        """
        接受url和headers获取请求的返回json
        :param url: 请求的url
        :param code: 编码
        :return: 返回response的json
        """
        try:
            resp = self.sessions.get(url=url, headers=self.headers)
            resp.raise_for_status()
            resp.encoding = code
            json_str = json.loads(resp.text)
        except Exception:
            print('连接座位系统服务器出现错误，请稍后重试！')
            return 'network wrong!'
        else:
            return json_str


    # def get_rooms_of_lib(self, lib_selected):
    #     """
    #     获取指定场馆的房间信息
    #     :param lib_selected: 用户输入的所选择的预约场馆的编号
    #     :return: 返回该场馆的房间信息
    #     """
    #     libs_info = self.get_response_json(url='http://seat.lib.whu.edu.cn/rest/v2/free/filters')
    #     rooms = []
    #     for room in libs_info['data']['rooms']:
    #         if room[2] == int(lib_selected):
    #             rooms.append({room[0]: room[1]})
    #     return rooms

    def print_rooms(self, lib_selected):
        """
        打印出房间信息，供用户选择
        编号：房间名
        :param rooms: 指定场馆的房间信息，list
        :return: 无返回值
        """
        room = self.rooms_of_lib[int(lib_selected)-1]
        for key in room.keys():
            print(str(key) + ' : ' + room[key])

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
        self.print_rooms(lib)
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
            text = '欢迎使用武汉大学图书馆自动抢座预约神器，支持全部四个图书馆的抢座'\
                   '\n预约结果: 预约失败'\
                   '\n失败原因: ' + book['message']
            send_email(self.address, '武汉大学预约系统通知', content=text)
        elif book['status'] == 'success':
            # 构造邮件正文
            text = '欢迎使用武汉大学图书馆自动抢座预约神器，支持全部四个图书馆的抢座'\
                   '\n预约结果: 预约成功'\
                   '\n---------------------座位预约凭证----------------------'\
                   + '\nID：' + str(book['data']['id']) + '\n凭证号码：' + \
                   book['data']['receipt'] + '\n时间：' + book['data']['onDate'] + ' ' + book['data']['begin'] + '～' + \
                   book['data']['end'] + '\n状态：' + ('已签到' if book['data']['checkedIn'] else '预约') + '\n地址：' + \
                   book['data']['location'] + '\n-----------------------------------------------------' + \
                   '\n\nPowered by Seat Robber'
            send_email(self.address, '武汉大学预约系统通知',
                       content=text)
        print(text)

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
            if room_seat_info[key]['type'] != 'seat':
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
        time.sleep(len(rooms_selected))
        all_seats = []
        for room in rooms_selected:
            room_search_url = 'http://seat.lib.whu.edu.cn/rest/v2/room/layoutByEndMinutes/' + room + '/' + end_time
            room_seat_info = self.get_response_json(url=room_search_url)['data']['layout']
            all_seats += self.get_seats_info(room_seat_info)
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
                # time.sleep(1)
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
