# Python 기본문법

### 참고1. 밑바닥부터 시작하는 딥러닝
 - 기본문법(변수,연산,함수,클래스,라이브러리 로딩, 그래프 등)  
 https://www.evernote.com/shard/s222/sh/cbdefc88-41d7-4b88-b718-aaf9659262c0/15f336ad07be694497a3c586a0ed14cc 
 
 - squeeze : 차원축소  
 https://www.evernote.com/shard/s222/sh/43636d07-ca5b-4a18-93e9-6574e5032046/93b5d84a57ceb3258516c410a58cd0e1  
 
 - argmax/axis : 차원별 최대값의 index  
 https://www.evernote.com/shard/s222/sh/11ed9209-4b4f-4c89-a083-05ac94f1a45a/202d75ccc343ca82fb96ef1b6c2dd97f  
 
 - key/value 집합(dictional) 소팅
 https://www.evernote.com/shard/s222/sh/a6aa8211-6e2b-4b7b-a69f-9e85e63381c4/4b9755151f266156034026e077d7e314  
 
 
 

<hr />

### 참고2. 웹사이트
 - 점푸투파이썬: https://wikidocs.net/13  
 - 파이썬 자습서: https://docs.python.org/ko/3/tutorial/index.html  
 - 왕초보를 위한 파이썬: https://wikidocs.net/77  

<hr />

#### 1. pickle을 이용한 dictionary 저장/로딩
```
import pickle

dic = {}
dic["word"] = ['a', 'b', 'c']
dic["weight"] = ['1.1', '2.5', '0.1']
dic["hs"] = ['1234', '5678', '0001']

print(dic)
>> {'word': ['a', 'b', 'c'], 'weight': ['1.1', '2.5', '0.1'], 'hs': ['1234', '5678', '0001']}

file_name='dic_test.pickle'
with open(file_name, 'wb') as w_handler:
    pickle.dump(dic, w_handler, protocol=pickle.HIGHEST_PROTOCOL)

with open(file_name, 'rb') as r_handler:
    l_dic = pickle.load(r_handler)

print('loaded_dic:', l_dic)      
>> loaded_dic: {'word': ['a', 'b', 'c'], 'weight': ['1.1', '2.5', '0.1'], 'hs': ['1234', '5678', '0001']}
```
<br>

#### 5. python list정렬 후 정렬전 index 뽑기
: https://github.com/jukyellow/artificial-intelligence-study/blob/master/02_%ED%8C%8C%EC%9D%B4%EC%8D%AC(Python)-%EA%B8%B0%EB%B3%B8%EB%AC%B8%EB%B2%95/05_python_dictionary_sort.py
<br>

#### 6. python Excel read/write
https://github.com/jukyellow/artificial-intelligence-study/blob/master/02_%ED%8C%8C%EC%9D%B4%EC%8D%AC(Python)-%EA%B8%B0%EB%B3%B8%EB%AC%B8%EB%B2%95/06_python_excel_read.md  
<br>

#### 7. Python 모듈
- 참고: https://wikidocs.net/29  
> 모듈이란 함수나 변수 또는 클래스를 모아 놓은 파일이다.  
- 모듈 만들기  
```
# mod1.py
def add(a, b):
return a + b
def sub(a, b): 
return a-b
```
- 모듈 불러오기  
> from 모듈이름 import 모듈함수    
```
from mod1 import add, sub
#from mod1 import *
add(3, 4)
```
- if __name__ == "__main__"  
if __name__ == "__main__"을 사용하면, python mod1.py처럼 직접 이 파일을 실행했을 때는 __name__ == "__main__"이 참이 되어 if문 다음 문장이 수행된다.  
반대로 대화형 인터프리터나 다른 파일에서 이 모듈을 불러서 사용할 때는 __name__ == "__main__"이 거짓이 되어 if문 다음 문장이 수행되지 않는다.  
- __name__ 변수란?  
파이썬의 __name__ 변수는 파이썬이 내부적으로 사용하는 특별한 변수 이름이다.  
만약 python mod1.py처럼 직접 mod1.py 파일을 실행할 경우 mod1.py의 __name__ 변수에는 __main__ 값이 저장된다.  
하지만 파이썬 셸이나 다른 파이썬 모듈에서 mod1을 import 할 경우에는 mod1.py의 __name__ 변수에는 mod1.py의 모듈 이름 값 mod1이 저장된다.  
<br>
