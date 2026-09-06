import machine
import time

# Pin assignments for ADC channels
adc_throttle = machine.ADC(26)  # GP26 / ADC0
adc_temp = machine.ADC(27)      # GP27 / ADC1

# RP2040 ADC reads 16-bit unsigned integers (0 to 65535) against a 3.3V reference
V_REF = 3.3
ADC_MAX = 65535

# Circular buffer / rolling filter for baseline noise suppression
WINDOW_SIZE = 5
throttle_buffer = [0.0] * WINDOW_SIZE
temp_buffer = [0.0] * WINDOW_SIZE
buf_index = 0

def read_sensors():
    global buf_index
    
    # 1. Read raw ADC counts and convert to actual voltages
    v_throttle_raw = (adc_throttle.read_u16() * V_REF) / ADC_MAX
    v_temp_raw = (adc_temp.read_u16() * V_REF) / ADC_MAX
    
    # 2. Moving Average Filter (eliminates high-frequency noise spikes)
    throttle_buffer[buf_index] = v_throttle_raw
    temp_buffer[buf_index] = v_temp_raw
    buf_index = (buf_index + 1) % WINDOW_SIZE
    
    v_throttle = sum(throttle_buffer) / WINDOW_SIZE
    v_temp = sum(temp_buffer) / WINDOW_SIZE
    
    # 3. Engineering Unit Transformations:
    # Throttle: 0.3V to 3.0V linear range mapped to 0.0% - 100.0%
    throttle_pct = ((v_throttle - 0.3) / (3.0 - 0.3)) * 100.0
    throttle_pct = max(0.0, min(100.0, throttle_pct))
    
    # Battery Temp: 0.0V to 3.3V mapped to 20.0°C - 110.0°C
    temp_c = 20.0 + (v_temp / 3.3) * 90.0
    
    # 4. FMEA Hardware Fault Isolation:
    # Out-of-range checks detect broken sensor harnesses or short circuits
    status = "OK"
    if v_throttle < 0.15 or v_throttle > 3.15:
        status = "ERR_APPS_SENSOR_OOR"  # Short-to-GND or Short-to-VCC
    elif temp_c > 92.0:
        status = "ERR_OVERTEMP_CRITICAL"
        
    return throttle_pct, temp_c, status

# CSV Telemetry Stream Header
print("Timestamp_ms,Throttle_Pct,Temp_C,Status")

# Fixed 20 Hz sample loop (50 ms task execution period)
while True:
    t_now = time.ticks_ms()
    th, tc, st = read_sensors()
    
    # Broadcast formatted telemetry packet
    print(f"{t_now},{th:.2f},{tc:.2f},{st}")
    time.sleep(0.05)
