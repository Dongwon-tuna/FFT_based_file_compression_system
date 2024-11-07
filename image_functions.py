from PIL import Image
import numpy as np
import cmath
from FT_functions import FFT
from FT_functions import inverse_FFT
import re

def get_bytes_per_pixel(mode):
    """
    이미지 모드에 따라 한 픽셀이 차지하는 바이트 수를 리턴합니다.
    
    Parameters:
        mode (str): 이미지 모드 (e.g., 'RGB', 'RGBA', 'L', 'CMYK')
        
    Returns:
        int: 한 픽셀당 바이트 수
    """
    mode_to_bytes = {
        "1": 1,        # 흑백, 1비트 (약 0.125바이트)지만 바이트 단위로 반환
        "L": 1,        # 그레이스케일, 1바이트
        "P": 1,        # 팔레트 모드, 1바이트
        "RGB": 3,      # RGB, 3바이트
        "RGBA": 4,     # RGBA, 4바이트
        "CMYK": 4,     # CMYK, 4바이트
        "YCbCr": 3,    # YCbCr, 3바이트 (주로 JPEG에서 사용)
        "LAB": 3,      # LAB, 3바이트
        "HSV": 3,      # HSV, 3바이트
        "I": 4,        # 32비트 정수형, 4바이트
        "F": 4         # 32비트 부동 소수점, 4바이트
    }
    
    return mode_to_bytes.get(mode, 0)  # 지원되지 않는 모드일 경우 0을 반환



def convert_to_grayscale(image_path, output_path):
    img = Image.open(image_path)
    gray_img = img.convert("L")
    gray_img.save(output_path)





def pad_to_power_of_two(signal):
    N = len(signal)
    power_of_two = 1
    while power_of_two < N:
        power_of_two *= 2
    return signal + [0] * (power_of_two - N), power_of_two

def image_to_txt(image_path, freq_idx_threshold):
    img = Image.open(image_path)
    flat_pixels = []


    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            flat_pixels.append(pixel)

    with open("./Data/originalData.txt", "w") as file:
        flat_string = " ".join(map(str, flat_pixels))
        file.write(flat_string + "\n")

    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            flat_pixels.append(pixel)

    padded_pixels, padded_length = pad_to_power_of_two(flat_pixels)
    FFT_result = FFT(padded_pixels)
    
    # 주요 주파수 성분만 추출 (절댓값이 큰 순서대로)
    magnitude = [abs(value) for value in FFT_result]
    sorted_indices = sorted(range(len(magnitude)), key=lambda i: magnitude[i], reverse=True)[:freq_idx_threshold]
    
    # 필요한 성분만 압축 데이터로 저장
    compressed_data = [(i, round(FFT_result[i].real), round(FFT_result[i].imag)) for i in sorted_indices]

    output_txt_path = "./Data/compressedData.txt"
    output_bin_path = "./Data/compressedData.bin"
    with open(output_txt_path, "w") as file:
        for index, real, imag in compressed_data:
            file.write(f"{index}:{real}+{imag}j")

    txt_to_binary(output_txt_path,output_bin_path)

    return padded_length, output_bin_path  # 패딩된 길이와 압축한 파일 경로 리턴
    

def txt_to_image(bin_path, output_image_path, width, height, mode, padded_length):
    bytes_per_pixel = get_bytes_per_pixel(mode)
    if bytes_per_pixel == 0:
        raise ValueError("Unsupported image mode.")
    

    txt_path = "./Data/decompressedData.txt"
    binary_to_txt(bin_path, txt_path)

    img = Image.new(mode, (width, height))
    with open(txt_path, "r") as file:
        pixel_values = file.readlines()

    complex_values = [0] * padded_length  
    if isinstance(pixel_values, list):  # 리스트를 문자열로 변환 각 항목을 합쳐서 하나의 문자열로 진행함
        pixel_values = ''.join(pixel_values)
    else:
        pixel_values = pixel_values  # 이미 문자열이라면 그대로 사용    

    pattern = r"\d+:[+-]?\d+\+?-?\d*j"
    parsed_pixel_value = re.findall(pattern, pixel_values)

    for item in parsed_pixel_value:
        index, value = item.split(":")
        # '+' 또는 '-'를 기준으로 real과 imag 부분을 분리하고 'j' 제거  ==>압축데이터를  txt로 저장할 때 최대한 적은 크기로 압축하기위하여 스페이스바 제거했음. 그래서 각 데이터 파싱필요함
        if '+' in value:
            real, imag = value.split('+')
        elif '-' in value[1:]:  
            real, imag = value.split('-', 1)
            imag = '-' + imag
        imag = imag.replace("j", "")
        complex_values[int(index)] = complex(float(real), float(imag))

    # inverse FFT 적용
    restored_signal = inverse_FFT(complex_values)
    original_length = width * height
    restored_signal = restored_signal[:original_length]  # 원래 데이터 길이로 자름

    # 복원된 픽셀 값들을 이미지로 변환
    restored_pixels = [int(min(max(x.real, 0), 255)) for x in restored_signal]
    img = Image.new(mode, (width, height))

    for y in range(height):
        for x in range(width):
            index = (y * width + x) * bytes_per_pixel
            pixel = tuple(restored_pixels[index + j] for j in range(bytes_per_pixel))
            img.putpixel((x, y), pixel)

    img.save(output_image_path)
    print(f"Converted text file to {output_image_path}")



def txt_to_binary(input_text_file, output_binary_file):
    with open(input_text_file, 'r') as text_file:
        text_data = text_file.read()  

    with open(output_binary_file, 'wb') as binary_file:
        binary_file.write(text_data.encode('utf-8')) 

def binary_to_txt(input_binary_file, output_text_file):
    with open(input_binary_file, 'rb') as binary_file:
        binary_data = binary_file.read()  

    with open(output_text_file, 'w') as text_file:
        text_file.write(binary_data.decode('utf-8'))  























