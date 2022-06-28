# modules ##
import os, sys # 운영체제에서 제공되는 여러 기능
import subprocess # python program 내에서 외부함수를 실행하기 위해 사용한 모듈
import re
import time
import urllib.request as urllib2 # 주어진 url에서 데이터를 가져오는 기본 기능을 제공
import urllib.parse as urlparse # url의 분해, 조립 변경 등을 처리하는 함수를 제공

### 상수 선언 ###
CONST_COMMAND = "iwlist wlan0 scan"   # wifi의 정보를 확인할 수 있는 wifi scan 명령어

# python에서 외부 명령어를 실행하기 위한 메서드
def getCallResult(CONST_COMMAND):
    fd_popen = subprocess.Popen(CONST_COMMAND.split(), stdout=subprocess.PIPE).stdout
    data = fd_popen.read()
    fd_popen.close()
    return data

# wifi scan을 통해 정보를 수집하는 메서드
def get_wifi_info(CONST_COMMAND):
    # "iwlist wlan scan"의 출력값을 info에 대입 
    info = getCallResult(CONST_COMMAND)
    info = str(info)

    # Cell number를 기준으로 wifi를 구분하여 각 정보를 수집
    # index1의 값이 -1이면 find를 실패한것
    Time = getCallResult('date').decode("utf-8")
    Time = str(Time).rstrip('\n')
    index1 = info.find('Cell 01')
        
    # info를 문자열 슬라이싱을 이용해 이전 Cell의 정보를 다시 수집하지 않도록 함
    info = info[index1:]
    print('Cell 01')
    print(Time)

    if(index1 == -1):
        print("null")
    else:
        ### macAddress ###
        index1 = info.find('Address: ')
        info = info[index1:]

        if(index1 != -1):
            index1 = 9
            index2 = info.find('\\n')
            macAddr = info[index1:index2]
            print('MACaddr : ' + macAddr)
        else:
            print('MACaddr search error!')

        ### frequency ###
        index1 = info.find('Frequency:')
        info = info[index1:]

        if(index1 != -1):
            index1 = 10
            index2 = info.find('z')
            index2 += 1
            frequency = info[index1:index2]
            print('Frequency : ' + frequency)

        ### quality ###
        index1 = info.find('Quality=')
        info = info[index1:]

        if(index1 != -1):
            index1 = 8
            index2 = info.find(' ')
            quality = info[index1:index2]
            print('Quality : ' + quality)

        ### dBm ###
        index1 = info.find('level=')
        info = info[index1:]

        if(index1 != -1):
            index1 = 6
            index2 = info.find(' ')
            dBm = info[index1:index2]
            print('dBm : ' + dBm)
        else:
            print('dBm search error!')

        ### ESSID ###
        index1 = info.find('ESSID:')
        info = info[index1:]

        if(index1 != -1):
            index1 = 6
            index2 = info.find('\\n')
            ESSID = info[index1:index2]
            print('ESSID : ' + ESSID)
        else:
            print('ESSID search error!')
            
# client의 MAC address를 수집하는 메서드
def find_info_client(str_ifconfig):
    ifconfig = getCallResult(str_ifconfig)
    ifconfig = str(ifconfig)

    index1 = ifconfig.find('ether ')
    ifconfig = ifconfig[index1:]

    if(index1 != -1):
        index1 = 6
        index2 = ifconfig.find('  ')
        client_MACaddr = ifconfig[index1:index2]
        print('client MAC address : ' + client_MACaddr)
    else:
        print('client MACaddr search error!')
    
    return 0

        
if __name__ == "__main__":
    find_info_client('ifconfig wlan0')  # client의 MAC_address를 확인할 수 있는 명령어
    while(True):
        get_wifi_info(CONST_COMMAND)
        time.sleep(10)
