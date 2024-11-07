import cmath
import numpy as np

def DFT(signal):
    N = len(signal)
    result = []
    for k in range(N):
        sum_real = 0
        sum_imag = 0
        for n in range(N):
            angle = 2 * cmath.pi * k * n / N
            sum_real += signal[n] * cmath.cos(angle)
            sum_imag += -signal[n] * cmath.sin(angle)
        result.append(complex(sum_real, sum_imag))
    return result

def FFT(signal):
    N = len(signal)
    if N == 1:  
        return signal#재귀함수 종료 후 리턴함
    
    # 짝수와 홀수 인덱스 신호로 분할 ===> 이 과정이 FFT에서 시간복잡도를 획기적으로 줄이는 아이디어임
    even = FFT(signal[0::2])
    odd = FFT(signal[1::2])

    T = [cmath.exp(-2j * cmath.pi * k / N) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]


def inverse_FFT(signal):
    N = len(signal)
    if N == 1:
        return signal  # 재귀함수 종료 후 리턴함

    even = inverse_FFT(signal[0::2])
    odd = inverse_FFT(signal[1::2])

    T = [cmath.exp(2j * cmath.pi * k / N) * odd[k] for k in range(N // 2)]
    return [(even[k] + T[k]) / 2 for k in range(N // 2)] + [(even[k] - T[k]) / 2 for k in range(N // 2)]


#===================================== functions for signal =============================================
def signal_generator(N, signal_frequency, sampling_rate):
    t = np.arange(N) / sampling_rate
    return np.sin(2 * np.pi * signal_frequency * t)

# 상위 주파수 성분 추출 함수
def get_freq_domain(after_transform, num_indices):
    # 복소수 크기 기준으로 정렬된 인덱스 추출
    top_n_indices = np.argsort(np.abs(after_transform))[-num_indices:]
    top_n_indices = top_n_indices[::-1]
    top_n_values = [after_transform[i] for i in top_n_indices]

    return top_n_indices, top_n_values


def main():
    input_signal = signal_generator(8, 2, 8)
    print("Input Signal:", input_signal)
    # after_transform_res = DFT(input_signal)
    after_transform_res = FFT(input_signal)
    print("Transform Result:", after_transform_res)

    num_indices = 3
    top_indices, top_values = get_freq_domain(after_transform_res, num_indices)
    print("Top Indices:", top_indices)
    print("Top Values:", top_values)


if __name__ == "__main__":
    main()
