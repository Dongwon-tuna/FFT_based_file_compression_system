import os
from PIL import Image
from image_functions import get_bytes_per_pixel
from image_functions import image_to_txt
from image_functions import txt_to_image
from image_functions import convert_to_grayscale
import os

def compare_file_sizes(file1, file2):#file1 원본 , #file2 압축본

    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)

    print(f"Size of Original txt file size: {size1/1000} KB")
    print(f"Size of Compressed txt file size: {size2/1000} KB")
    compression_ratio = (size1 - size2) / size1 * 100
    print(f"Compression Ratio: {compression_ratio:.2f}%")


file_path = "./Cat.jpg"#해당 디릭토리에 아무 이미지나 넣고 파일명만 바꿔서 하시용
output_file_path = "./Data/grayimage.jpg"
convert_to_grayscale(file_path, output_file_path)#RGB정보 모두 FFT, inverse FFT 구현하기 귀찮아서 걍 grayScale로 하였음
file_path =  "./Data/grayimage.jpg"

with Image.open(file_path) as img:
    width, height = img.size
    print(f"Image Resolution: {width} x {height} pixels")
    print(f"Total pixels: {width*height} pixels")
    print(f"Image Mode: {img.mode}")  
 
    
    padded_length, compressedData = image_to_txt(file_path,6000)#여기의 두번째 파라미터는 몇개의 이산적인 주파수 도메인 샘플로 압축할건지 입력받음
    txt_to_image(compressedData, "./Data/reconstructed_image.jpg", width, height, img.mode,padded_length)
    compare_file_sizes('./Data/originalData.txt', './Data/compressedData.txt')







