from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
import pandas as pd


chrome_options = Options()
chrome_options.add_experimental_option("detach",True)

locate=input("지역명을 입력하세요: ")

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


namelist = []
gradelist = []
etclist = []
kindlist =[]
done = True

for pageNum in range(1,11):
    url = f"https://www.mangoplate.com/search/{locate}?keyword={locate}&page={pageNum}"
    driver.get(url)
    driver.implicitly_wait(10)
    
    items = driver.find_elements(By.CSS_SELECTOR,".list-restaurant-item[data-subcusine_code]")

    for item in items:
        name = item.find_element(By.CSS_SELECTOR,".title").text # 가게 이름
        grade = item.find_element(By.CSS_SELECTOR,".point").text # 평점
        etc = item.find_element(By.CSS_SELECTOR,".etc").text # 위치

        if(grade):
            namelist.append(name)
            grade = float(grade)
            gradelist.append(grade)
            location = etc.split("-")[0]
            etclist.append(location)
            kind = etc.split("-")[1]
            kindlist.append(kind)
        else:
            done=False
            break

    print(f'{pageNum} 페이지 완료')
    if(done == False):
        print('프로그램을 종료합니다.')
        break
    

print(namelist)
print(gradelist)
print(etclist)
print('\n')

data = {'name':namelist, 'grade':gradelist, 'location':etclist, 'kind':kindlist}
df = pd.DataFrame(data)

df.to_csv(f"hotplacelist_{locate}.csv", encoding = "utf-8-sig")

print(df,'\n')

# 평균값
average_grade = round(df['grade'].mean(),2)
print(f'{locate}의 평균 평점 : {average_grade}\n')

# 평점별 빈도수 계산
grade_counts = df['grade'].value_counts().sort_index()

# 그래프 그리기
plt.rc('font', family="NanumGothic")
plt.plot(grade_counts.index, grade_counts.values, marker='.', linestyle='-', color='blue')
plt.xlabel('평점')
plt.ylabel('개수')
plt.title(f'{locate}의 평점 분포')
plt.show(block=False)


print("==========지역별 평점이 일정 이상인 식당 출력==========")


while True:
    location=input(f"{locate}의 상세지역을 입력하세요. ex)사상, 해운대, 마포 등(종료는 0을 입력)\n")
    if(location == '0'):
        print('종료합니다.')
        exit()
    grade2 = float(input("평점을 입력하세요. (3.0~5.0)\n"))

    select1 = df[(df['location'].str.contains(location)) & (df['grade'] >= grade2)]
    print(select1,'\n')

input()

