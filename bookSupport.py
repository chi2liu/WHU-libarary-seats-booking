import json
import time

def getjson(sessions, url, headers):
    resp = sessions.get(url=url, headers=headers)
    #print(resp.text)
    return json.loads(resp.text)

def getToken(sessions, username, password):
    loginURL = 'http://seat.lib.whu.edu.cn/rest/auth?username='+username+'&password='+password
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
    data = getjson(sessions, loginURL, loginHeaders)
    return data['data']['token']

def printlibinfo(sessions, headers, lib):
    roomsinfo = getjson(sessions=sessions, url='http://seat.lib.whu.edu.cn/rest/v2/free/filters', headers=headers)
    libs = []
    for room in roomsinfo['data']['rooms']:
        if room[2] == int(lib):
            libs.append({room[0]:room[1]})
    for room in libs:
        for key in room.keys():
            print(str(key) + ':' + room[key])

def freeBook(sessions, headers,startTime, endTime, seatID):
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
    book = json.loads(sessions.post('http://seat.lib.whu.edu.cn/rest/v2/freeBook', headers=headers, data=data).text)
    if book['status'] == 'fail':
        print('预约失败')
        print('失败原因：'+book['message'])
    elif book['status'] == 'success':
        print('预约成功')
        print('时间：', book['data']['onDate'], book['data']['begin'], '--', book['data']['end'])
        print('地址：', book['data']['location'])



def getseats(seatInfo):
    res = []
    seatKeys = seatInfo.keys()
    for key in seatKeys:
        if seatInfo[key]['type'] == 'empty':
            continue
        res.append(seatInfo[key])
    return res

def getallseats(sessions, headers, roomlist, endTime):
    allSeats = []
    for room in roomlist:
        roomSearchURL = 'http://seat.lib.whu.edu.cn/rest/v2/room/layoutByEndMinutes/'+ room + '/' + endTime
        roomSeatInfo = getjson(sessions, url=roomSearchURL, headers=headers)['data']['layout']
        allSeats += getseats(roomSeatInfo)
        time.sleep(1)
    return allSeats

def searchseat(sessions, headers, seats, roomlist,startTime, endTime):
    notFound = True
    count = 0
    print('正在为您搜索空闲座位，请稍候...')
    print('......')
    while notFound:
        for seat in seats:
            if seat['status'] == 'FREE':
                freeBook(sessions, headers,startTime, endTime, seat['id'])
                notFound = False
                break
        if notFound:
            print('当前暂时没有空闲座位...正在为您继续搜索...请耐心等待')
            print('......')
            time.sleep(1)
            count = (count + 1) * len(roomlist)
            if count > 30 :
                print('为了避免被系统加入黑名单，将暂停15s后继续为您搜索')
                print('.......')
                time.sleep(15)
                print('重新开始为您搜索')
                count = 0
            seats = getallseats(sessions, headers, roomlist, endTime)
            count = count / len(roomlist)