from SeatRobber import Robber


def get_username_password():
    name = input('请输入您的图书馆帐号：')
    pwd = input('请输入您的密码：')
    email_address = input('请输入您接受预约结果通知的邮箱地址（如：123456@qq.com）：')
    return name, pwd, email_address


if __name__ == '__main__':
    print('>--------武汉大学抢座神器------by 633--<')
    username, password, address = get_username_password()
    robber = Robber(username=username, password=password, address=address)
    robber.robber_seat()
    # 避免打包exe之后，执行完cmd立即退出
    input()
