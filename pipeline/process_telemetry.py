import pandas as pd

# Put your actual file name here
input_file =r"C:\Users\desai devika\OneDrive\Desktop\Documents\telemetry_raw.csv"

# 1. Read your saved CSV file
df = pd.read_csv(input_file)

# 2. Check the data in your terminal
print(f"Total rows read: {len(df)}")
print("First 3 rows of your data:")
print(df.head(3))

# 3. Calculate time in seconds starting from 0 (Simulink expects Time starting at 0)
df['Time_Sec'] = [i * 0.05 for i in range(len(df))]

if 'Timestamp_ms' in df.columns:
    df['Time_Sec'] = (df['Timestamp_ms'] - df['Timestamp_ms'].iloc[0]) / 1000.0

if 'Time' in df.columns:
    df['Time_Sec'] = df['Time'] - df['Time'].iloc[0]

# 4. Save the normalized data for MATLAB/Simulink
output_file = "clean_telemetry.csv"
df.to_csv(output_file, index=False)

print(f"\nSUCCESS: Generated '{output_file}' ready for MATLAB Online!")
