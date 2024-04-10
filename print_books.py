import sys 
from PyQt5.QtWidgets import *
#PyQt라는 소프트웨어에서 sys 모듈을 가져옴. sys 모듈:파이썬 인터프리터가 제공하는 변수와 함수를 직접 제어할 수 있게 해주는 모듈
import requests #웹 크롤링을 더 쉽게 만들어주는 모듈
from urllib.request import urlopen #urlopen이라는 모듈을 가져옴
from bs4 import BeautifulSoup #실질적인 웹 크롤링을 담당하는 모듈
def getBooks(mode,site_num,field):#책의 정보를 따오는 함수
    print("getBooks starts")
    for i in range(0,5):# 5번 반복
        html = urlopen('https://book.naver.com/category/index.nhn?cate_code='+str(site_num)+'&tab=top100&list_type=list&sort_type=salecount&page='+str(i+1))
#네이버 책 사이트의 url을 연다. 
        bsObject = BeautifulSoup(html, "html.parser")
#BeautifulSoup 라이브러리를 치환한다.
        book_page_urls = []#책의 url을 저장하는 리스트
        for index in range(0, 20):#스무번 반복
            dl_data = bsObject.find('dt', {'id':"book_title_"+str(index)})
		#특정부분 데이터 가져오기
            link = dl_data.select('a')[0].get('href')#링크 따오기
            book_page_urls.append(link)#리스트에 따온 링크 추가하기
        for index, book_page_url in enumerate(book_page_urls):
		#리스트 열거하기
            html = urlopen(book_page_url)
		#리스트의 (index+1)번째 항의 url 따오기
            bsObject = BeautifulSoup(html, "html.parser")#따온 url파싱하기
            title = bsObject.find('meta', {'property':'og:title'}).get('content')#파싱한 html에서 책 제목 저장
            author = bsObject.find('dt', text='저자').find_next_siblings('dd')[0].text.strip()#파싱한 html에서 책 저자 저장
            introduce=bsObject.find('meta',{'property':'og:description'}).get('content')
	#파싱한 html에서 책 소개 따오기
            print(index+i*20+1,"책:",title,"  저자:", author)
		# 책 제목 및 저자 출력
            print()
            print("소개:",introduce)# 책 소개 출력
            print("="*100)
#책의 제목, 저자, 난이도(화학 또는 법일 경우만), 소개 출력
class MyWindow2(QMainWindow):
    def __init__(self,cat):
        super().__init__()
        self.categories = cat#치환
        self.setupUI() #함수 시행

    def setupUI(self):#학과 창 생성
        self.setGeometry(800, 200, 300, 300)#화면에서의 위치 설정
        groupBox = QGroupBox("학과", self)#제목 설정
        groupBox.move(10, 10)#위치 설정
        groupBox.resize(180, 280)#크기 설정
        
        self.radio_btns = []#버튼 위치를 저장하는 리스트
        pos_y = 20 #버튼 위치에 관여하는 변수
        i=0
        for category in self.categories:#버튼을 생성하는 함수
            print(category[0])
            self.radio_btns.append(QRadioButton(category[0],self))
            self.radio_btns[i].move(20,pos_y)
            self.radio_btns[i].clicked.connect(self.radioButtonClicked)
            i += 1
            pos_y += 20
        self.statusBar = QStatusBar(self) #치환
        self.setStatusBar(self.statusBar) #창 생성하는 함수 시행

    def radioButtonClicked(self):#버튼 선택에 관한 함수
        cur = 0
        for btn in self.radio_btns:
            if btn.isChecked(): #만약 버튼이 체크된다면
                msg = self.categories[cur][0]
                site_num = self.categories[cur][1]
                break
            cur += 1
        self.statusBar.showMessage(msg + ", "+str(site_num) + " 선택" )
	#버튼이 선택됨을 보여줌
        getBooks("top100",site_num,self.categories[cur][0])
	#책 정보 가져오기
class MyWindow(QMainWindow):#계열 및 학과를 나타내는 버튼 설정
    def __init__(self):
        super().__init__()
        self.setupUI()
    def setupUI(self):#계열 창을 생성하는 함수
        self.setGeometry(800, 200, 300, 300)#창 크기 설정

        groupBox = QGroupBox("계열", self)#버튼 만들기
        groupBox.move(10, 10)# 위치 설정
        groupBox.resize(140, 200)# 크기 설정
        self.radio1 = QRadioButton("공학", self)
        self.radio1.move(20, 20)
        self.radio1.setChecked(True)#공학이 선택된 것처럼 보여줌
        self.radio1.clicked.connect(self.radioButtonClicked)
        self.eng_list = [("도시/토목/건축",250080),("기계/금속/전기/전자",250100),("산업",250090),("소프트웨어",280020020),("컴퓨터공학",280020040),("화학공학과",250050)]#학과 저장하는 리스트
        self.radio2 = QRadioButton("교육", self)
        self.radio2.move(20, 40)
        self.radio2.clicked.connect(self.radioButtonClicked)
        self.edu_list=[("교육학",120030)]
        self.radio3 = QRadioButton("사회", self)
        self.radio3.move(20, 60)
        self.radio3.clicked.connect(self.radioButtonClicked)
        self.soc_list=[("경영",160020),("경제",160010),("금융",160010060),("무역",180010030),("법",180040),("사회복지",180060),("행정",180020010),("언론/신문/방송",180070)]
        self.radio4 = QRadioButton("예체능", self)
        self.radio4.move(20, 80)
        self.radio4.clicked.connect(self.radioButtonClicked)
        self.yeah_list=[("디자인",210020050),("미술조형",210020),("연극/영화",210070),("음악",210030),("응용예술",210010)]
        self.radio5 = QRadioButton("인문", self)
        self.radio5.move(20, 100)
        self.radio5.clicked.connect(self.radioButtonClicked)
        self.in_list=[("국어",100010010),("영미어",100010020),("일본어",100010030),("중국어",100010040),("독일어",100010070),("프랑스어",100010060),("러시아어",100010050),("국제지역학",180010030),("심리학",120020020),("역사학",190010),("종교학",120070),("철학",120040020)]
        self.radio6 = QRadioButton("자연", self)
        self.radio6.move(20, 120)
        self.radio6.clicked.connect(self.radioButtonClicked)
        self.nat_list=[("산림원예학",130040020),("농업학",250110),("생명과학",250060),("생물학",250060),("화학",250050),("식품/의학",250120),("의류",150040),("생활과학",130040030),("수학",250030),("물리",250040),("천문/지구과학",250070),("지리",270040),("통계",250030)]
        self.radio7 = QRadioButton("경찰대", self)
        self.radio7.move(20, 140)
        self.radio7.clicked.connect(self.radioButtonClicked)
        self.pol_list=[("경찰대",180030030)]
        self.radio8 = QRadioButton("육군사관학교", self)
        self.radio8.move(20, 160)
        self.radio8.clicked.connect(self.radioButtonClicked)
        self.sol_list=[("육군사관학교",180030010)]
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
    def radioButtonClicked(self):# 계열 버튼 생성
        msg = ""
        if self.radio1.isChecked():#만약 버튼이 클릭 된다면
            msg = "공학"
            self.win = MyWindow2(self.eng_list)#리스트에서 학과 가져오기
            self.win.show()#학과 창으로 넘어가기
        elif self.radio2.isChecked():
            self.win = MyWindow2(self.edu_list)
            self.win.show()
            msg = "교육"
        elif self.radio3.isChecked():
            self.win = MyWindow2(self.soc_list)
            self.win.show()
            msg = "사회"
        elif self.radio4.isChecked():
            self.win = MyWindow2(self.yeah_list)
            self.win.show()
            msg = "예체능"
        elif self.radio5.isChecked():
            self.win = MyWindow2(self.in_list)
            self.win.show()
            msg = "인문"
        elif self.radio6.isChecked():
            self.win = MyWindow2(self.nat_list)
            self.win.show()
            msg = "자연"
        elif self.radio7.isChecked():
            self.win = MyWindow2(self.pol_list)
            self.win.show()
            msg = "경찰대"
        else:
            self.win = MyWindow2(self.sol_list)
            self.win.show()
            msg = "육군사관학교"
        self.statusBar.showMessage(msg + "선택됨")#계열이 선택됨을 보여줌
if __name__ == "__main__":#최종적인 실행
    app = QApplication(sys.argv)
    mywindow = MyWindow()#MyWinodw() class를 치환함
    mywindow.show()
    app.exec_()