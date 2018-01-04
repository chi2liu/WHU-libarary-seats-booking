import SeatBook

username = input('请输入用户名: ')
passwd = input('请输入密码: ')
book = SeatBook.SeatBook(username=username, password=passwd)
book.book()