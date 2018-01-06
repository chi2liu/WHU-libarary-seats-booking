import datetime


class TimeNode(object):
    """
    TimeNode工具类封装了预约时间节点的相关操作，并且提供与用户交互的信息及设置用户选择的预约时间
    1.打印当前可选择的预约开始时间节点
    2.打印出当前可选择的预约结束时间节点
    3.将普通时间转换成系统后台的时间格式，如：17:00转换成1020
    4.提供与用户交互的信息及设置用户选择的预约时间d
    """

    def __init__(self):
        """
        初始化系统基准时间，即8:00
        """
        self.baseTime = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))

    def get_time_node_list(self):
        """
        根据基准时间，计算出全部的可预约的时间节点
        例：
        No  time
        1   8：00
        2   8：30
        ...
        :return: time_list 即可预约的时间字典
        """
        time_node_list = {}
        # 键值即为上述的No编号
        key = 1
        for i in range(0, 870, 30):
            # 系统的可预约的时间点初始是8:00--22:00，每半个小时一个节点
            # 从抓包分析得到，后台表示时间是通过分钟的方式00:00为0分钟
            # 8:00即为480分钟，所以8:00在系统中对应的是480
            # 所以计算出所有时间节点的分钟形式，每30分钟一个间隔
            time_node_list[key] = self.baseTime + datetime.timedelta(minutes=i)
            key = key + 1
        return time_node_list

    def print_book_start_time(self, time_node_list, print_now=True):
        """
        打印出可选择的预约开始时间
        :param time_node_list: 可预约时间节点的列表
        :param print_now: 控制是否输出‘0-现在’这个时间节点，True则输出，False则不输出
        :return: 无返回值，输出时间节点信息到控制台
        """

        # 计算当前时间与baseTime的小时差和分钟差
        delta_hour = datetime.datetime.today().time().hour - self.baseTime.hour
        delta_minute = datetime.datetime.today().time().minute

        # 确定距离当前时间最近的一个时间节点
        if delta_hour >= 0:
            if delta_minute >= 30:
                begin = (delta_hour + 1) * 2 + 1
            else:
                begin = (delta_hour + 1) * 2
        else:
            begin = 1

        # 判断是否打印现在节点
        if print_now:
            print('0', '--', '现在')
        # 打印可选择的开始节点
        for i in range(begin, len(time_node_list) + 1):
            print(i, '--', time_node_list[i].strftime('%H:%M'))

    def print_book_end_time(self, time_node_list, start):
        """
        打印出可选择的预约结束时间
        :param time_node_list: 可预约时间节点的列表
        :param start: 选择的预约开始时间节点
        :return: 无返回值，打印出可选择的预约结束时间的节点
        """
        # 如果开始节点为现在，则只需打印出不带现在的开始节点列表
        if start == 0:
            self.print_book_start_time(time_node_list, print_now=False)
        # 如果开始节点不为现在，则从开始节点后面的一个节点开始打印
        else:
            for i in range(start, len(time_node_list)):
                print(i + 1, '--', time_node_list[i + 1].strftime('%H:%M'))

    def trans(self, time_node):
        """
        转换普通的时间格式到系统时间格式
        17:00 转换到 1020
        :type time_node: object
        :param time_node: 时间节点的编号
        :return: 返回转换之后的值
        """
        # 如果时间节点编号为0 ，说明选择的是现在，那么根据抓包分析得知，现在在系统里用-1来表示
        if time_node == 0:
            return '-1'
        # 获取时间节点的列表
        time_node_list = self.get_time_node_list()
        # 根据编号得到需要转换的普通时间
        target = time_node_list[time_node]
        # 具体转换过程
        delta = target - self.baseTime
        return str(int(delta.total_seconds() / 60) + 480)

    def set_start_and_end_time_node(self):
        time_node_list = self.get_time_node_list()
        self.print_book_start_time(time_node_list)
        print('--------------------')
        input_start_time = input('输入您要预约的开始时间的编号: ')
        start_time = self.trans(int(input_start_time))
        print('-------------------------------')
        self.print_book_end_time(time_node_list, int(input_start_time))
        print('-------------------------------')
        input_end_time = input('输入您要预约的结束时间的编号: ')
        end_time = self.trans(int(input_end_time))
        return start_time, end_time
