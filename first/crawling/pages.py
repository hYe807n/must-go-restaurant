from urllib.parse import quote_plus
import pyautogui
import requests
from bs4 import BeautifulSoup       # 정적 페이지 크롤링

from selenium import webdriver          # 동적 페이지 크롤링
from time import sleep

import asyncio                          # 성능 개선을 위한 동기적 크롤링 지원


request_headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36'
    }

name = address = point = cntreview = ""
resobj = []


async def search(a, b, c):
    global name, address, point, cntreview

    if ( a == 0 ):
        try: name = b.select_one(c).text
        except AttributeError: name = None
    elif ( a == 1 ):
        try: address = b.select_one(c).text
        except AttributeError: address = None
    elif ( a == 2 ):
        try: point = b.select_one(c).text
        except AttributeError: point = None
    elif ( a == 3 ):
        try: cntreview = b.select_one(c).text
        except AttributeError: cntreview = None
    

async def mango(a):
    '''
        #22: 1~5페이지까지 검색된 음식점을 links에 담고,
        26: 음식점의 정보를 담고있는 href로 접근해서
        30~: 정보 추출

        except IndexError : index 접근으로 인한 예외처리
        except AttributeError : NoneType 처리로 인한 예외처리
    '''
    global resobj, request_headers, name, address, point, cntreview

    for i in range(1, 5):
        response = requests.get(f'https://www.mangoplate.com/search/{a}?keyword={a}&page={i}', headers = request_headers,  verify = False).text
        soup  = BeautifulSoup(response, 'html.parser')
        links = soup.select(".info")

        for link in links:
            try: res_link = link.select('a')[0]['href']   #index 접근으로 인한 예외처리
            except IndexError: break
            url = f'https://www.mangoplate.com{res_link}'
            res = requests.get(url, headers = request_headers, verify = False).text
            food  = BeautifulSoup(res, 'html.parser')

            await asyncio.gather(search(0, food, ".restaurant_name"),search(1, food, ".Restaurant__InfoItemLabel--RoadAddressText"), search(2, food, ".rate-point>span"),search(3, food, "span.cnt.review"))

            try : img = food.find(class_='center-croping')['src']   #<이미지>   
            except TypeError: img = None

            if name != None and address != None:      
                resobj.append([name, address, point, cntreview, img, "mango"])     #가게 이름만이라도 있다면 출력
    return 
                    

async def dinning(a):
    '''
        #22: 1~5페이지까지 검색된 음식점을 links에 담고,
        26: 음식점의 정보를 담고있는 href로 접근해서
        30~: 정보 추출
        except IndexError : index 접근으로 인한 예외처리
        except AttributeError : NoneType 처리로 인한 예외처리
    '''
    global resobj, name, address, point, cntreview

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    dr = webdriver.Chrome(options=options)
    url = 'https://www.diningcode.com/list?distance=10000&lat=37.51936&lng=127.1136256&query='+quote_plus(a)
    dr.get(url)

    scroll = dr.find_element_by_xpath('//*[@id="root"]/div/div/div[1]')     # 마우스를 맛집 리스트 위치로 이동
    try: dr.move_to_element(scroll)
    except AttributeError: pass

    for i in range(3):
        dr.execute_script("arguments[0].scrollBy(0, 4500)", scroll)           # 스크롤 내림
        sleep(0.3)	
    links = dr.find_elements_by_class_name('PoiBlock')

    for link in links:
        try : name = link.find_element_by_css_selector('div.InfoHeader>h2').text      #<이름>
        except AttributeError: name = None

        for a in range(len(name)):          
            if name[a] != ".":         
                continue
            else:                           # 숫자와 가게 이름 사이에 공백부터
                a += 2
                _name = name[a:]            # 가게 이름 str로 저장

        try : address = link.find_element_by_css_selector('div.RHeader>div>p>span').text      #<주소>
        except AttributeError: address = None

        try : rset = link.find_element_by_css_selector('div.Rate > p.UserScore').text
        except AttributeError: rset = None

        point = []
        cntreview = []
        for a in range(len(rset)):     #리뷰 점수와 리뷰 개수를 나누기 위한 반복문
            if rset[a] != " ":      # 점수와 개수 사이에 공백 전까지 point 배열에 저장
                point += rset[a]
            else:                   # (와 "명" 사이가 리뷰 개수
                a += 2
                while(True):
                    cntreview += rset[a]
                    a += 1
                    if rset[a] == "명":
                        break
                break
        
        point = ''.join(point)      #join(): list를 str로 변환
        cntreview = ''.join(cntreview)

        try : img = link.find_element_by_css_selector('div.RHeader>img').get_attribute('src')  #<이미지>   
        except AttributeError: img = None

        resobj.append([_name, address, point, cntreview, img, "dinning"])     #가게 이름만이라도 있다면 출력
    return


async def siksin(a):
    '''
        #22: 1~5페이지까지 검색된 음식점을 links에 담고,
        26: 음식점의 정보를 담고있는 href로 접근해서
        30~: 정보 추출
        except IndexError : index 접근으로 인한 예외처리
        except AttributeError : NoneType 처리로 인한 예외처리
    '''
    global resobj, request_headers

    response = requests.get(f'https://www.siksinhot.com/search?keywords={a}', headers = request_headers,verify = False).text
    soup  = BeautifulSoup(response, 'html.parser')
    links = soup.select(".cont")

    for link in links:
        try: res_link = link.select('a')[0]['href']       
        except IndexError: break
        url = f'https://www.siksinhot.com{res_link}'
        res = requests.get(url, headers = request_headers, verify = False).text
        food  = BeautifulSoup(res, 'html.parser')

        await asyncio.gather(search(0, food, 'div>strong'),search(1, food, ".txt_adr"), search(2, food, "div.store_name_score>h3>strong"),search(3, food, "div.txt_total>ul>li>span"))

        try : img = food.find(class_='slick-slide slick-cloned').find('img')['src']  #<이미지>   
        except AttributeError: img = None

        if name != None:
            resobj.append([name, address, point, cntreview, img, "siksin"])     #가게 이름만이라도 있다면 출력
    return 


def crawling():
    global resobj
    return resobj


def reset():
    global resobj
    resobj = []