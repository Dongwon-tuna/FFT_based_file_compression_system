# FFT_based_file_compression_system

집가는 버스에서 [The Remarkable Story Behind The Most Important Algorithm Of All Time](https://www.youtube.com/watch?v=nmgFG7PUHfo) 보다가 3정류장 더 지나서 내렸음. 이 영상 마지막부분에 FFT알고리즘의 다양한 활용성에 대해서 설명하였는데, 파일을 압축 시킬때 FFT를 사용한다는 사실을 처음 알았음. FFT의 위력을 몸소(3정거장이나 늦게 내리며)느꼈고 위대함을 깨달아버렸음. 그래서 이 프로젝트를 진행했음.

## 개요

**FFT_based_file_compression_system**은 FFT 알고리즘을 활용하여 데이터의 유의미한 부분을 살리며 파일을 압축하고, 해제하여 원본 이미지의 특성이 보이게 복원하는 것을 목표로 했음.


### 원본 Grayscale  이미지
![grayimage](https://github.com/user-attachments/assets/9fa1e868-2c5d-497b-8188-3d4ed834262b)


### FFT_based_file_compression을 진행하고, 다시 복원한 사진
![reconstructed_image](https://github.com/user-attachments/assets/b6575e5d-96e7-46e6-b4d4-2f9202f1cd51) 고양이의 이미지적인 특징은 살렸다고 볼 수 있음.


### 데이터 압축정보

```plaintext
Image Resolution: 383 x 345 pixels
Total pixels: 132135 pixels
Image Mode: L
Converted text file to ./Data/reconstructed_image.jpg
Size of Original txt file size: 466.66 KB
Size of Compressed txt file size: 43.331 KB
Compression Ratio: 90.71%
```

## 고찰
이번엔 각 픽셀의 정보를 1행의 데이터로 분석하였음. 하지만 Height와 Width의 행과 열에 대하여 각각 FFT를 적용하여 압축한다면 같은 압축비율에 더 선명한 이미지로 복원이 가능할듯.(더이상 하기는 귀찮아서 여기까지만)
