import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, freqs

st.title("S-параметры полосового фильтра Баттерворта")

# Пользовательский ввод
fc = st.number_input("Центральная частота (ГГц)", 0.1, 20.0, 2.4)
bw = st.number_input("Полоса пропускания (МГц)", 1.0, 1000.0, 200.0)
N = st.slider("Порядок фильтра", 1, 10, 3)

# Преобразование единиц
fc_hz = fc * 1e9
bw_hz = bw * 1e6
lowcut = fc_hz - bw_hz / 2
highcut = fc_hz + bw_hz / 2
wc = [2 * np.pi * lowcut, 2 * np.pi * highcut]

# Расчёт коэффициентов фильтра
b, a = butter(N, wc, btype='bandpass', analog=True)

# Частотная сетка
w = np.logspace(8, 11, 1000)
w_hz = w / (2 * np.pi)

# Расчёт отклика
_, h = freqs(b, a, w)
S21 = np.abs(h)
S21_dB = 20 * np.log10(S21)
S11_dB = 10 * np.log10(1 - S21**2 + 1e-10)

# График
fig, ax = plt.subplots()
ax.semilogx(w_hz / 1e9, S21_dB, label="|S21|, дБ")
ax.semilogx(w_hz / 1e9, S11_dB, label="|S11|, дБ", linestyle='--')
ax.axvline(fc, color='gray', linestyle=':')
ax.set_title("Частотная характеристика")
ax.set_xlabel("Частота, ГГц")
ax.set_ylabel("Амплитуда, дБ")
ax.grid(True, which='both')
ax.legend()
st.pyplot(fig)