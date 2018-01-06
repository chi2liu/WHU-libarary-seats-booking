from SeatRobber import Robber

if __name__ == '__main__':
	username = input('请输入用户名：')
	password = input('请输入密码：')
    robber = Robber(username=username, password=password)
    robber.robber_seat()
