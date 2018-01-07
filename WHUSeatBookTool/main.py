from SeatRobber import Robber


def get_username_password():
    name = input('请输入您的用户名：')
    pwd = input('请输入您的密码：')
    return name, pwd


if __name__ == '__main__':
    print('>--------武汉大学抢座神器------by 633--<')
    username, password = get_username_password()
    robber = Robber(username=username, password=password)
    robber.robber_seat()
