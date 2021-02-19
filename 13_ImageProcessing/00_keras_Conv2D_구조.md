# Face Detctor 개발을 위해, Keras CNN을 사용하면서, CNN 학습내용 정리

### 1) 구조
: convolution Layer -> relu ->  poolling layer -> {반복} -> Fully connected  

### 2) 역할
- 참고: https://89douner.tistory.com/57  
- 참고2: https://buomsoo-kim.github.io/keras/2018/05/02/Easy-deep-learning-with-Keras-8.md/  
#### 2-1) convolution layer : 특징 추출(feature map)  
- kernel: 필터의 네모박스(window) 크기(이미지를 순회하는 필터 사이즈 정의)  
- Filter(필터): 3X3(예) 크기를 이미지를 window sliding하면서 특징값(?)들을 추출함   
-filters: 몇 개의 다른 종류의 필터를 활용할 것인지를 나타냄. 출력 모양의 깊이(depth) 를 결정한다.  
> stride: 필터와 입력층을 합성곱을 계산할때, 옮겨다니는 픽셀 단위  
> stiride갯수에 따라 출력(output) (width,height)가 결정됨  
- padding:  stride가 수행될때 여백의 부족함을 해소하기위해, data밖으로 zero-padding을 수행  
> valid:  패딩을 하지 않음  
> same: 필터의 사이즈가 k이면 사방으로 k/2 만큼의 패딩을 준다.  

#### 2-2) pooling: feature map을 뽑을때 기준
- max-pooling: kernel?에서 가장 큰값을 뽑음  
-pooling_size: pool_size 는 윈도우의 크기를 의미하며, 패딩은 합성곱 레이어와 똑같이 적용되며(valid혹은 same), strides가 미리 설정되지 않을 경우 pool_size와 동일하게 설정된다.  
> 큰 이미지에서 특징을 뽑으며 sub-sampling하여  축소된 feautre-map을 갖는다.  

### 3) 동작원리
- 참고: https://nittaku.tistory.com/264  
#### 3-1) 이미지 분류  
: 칼라사진(28*28*3) RGB(3개가 각 0~255)을 입력-> 고양이/개 출력   
#### 3-2) 이미지 data 분석
: 컬러사진->RGB로 구성된 pixel->픽셀 주변의 픽셀->눈코입식별->눈코입조합->얼굴식별  
#### 3-3) locally-connected
: 특정 픽셀에 가까운 거리는 연관성을 높게 계산하고, 거리가 먼 픽셀은 연관성이 낮게 계산  
#### 3-3) FC로 계산시 문제점
: 이미지에서 먼 필셀끼리도 같은 계산으로 처리됨->비효율  
#### 3-4) convolution layer
: 가로*세로 위치정보를 가지면서 CNN필터(shared weight)가 sliding window방식으로 돌면서 dot product 한다.  
: 여러개의 filter를 묶어놓은 것을 convolution(합성곱) layer라고 한다.  
#### 3-5) input/output size
- input_shape: (width, height, channel), ex) (10,10,3)  
- 참고: conv2D/1D 차이점(https://qastack.kr/datascience/51470/what-are-the-differences-between-convolutional1d-convolutional2d-and-convoluti )  
:Conv2D - (가로*세로)의 이미지를 input으로-> (batch_size, (width, height), channel)  
:Conv1D - 1Dim (가로) 정보를 input으로 -> (batch_size, w, channel)  
- output_shape(keras): (batch_size, (w, h), filter_size)  

