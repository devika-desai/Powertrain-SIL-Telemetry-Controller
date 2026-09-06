powertrain-sil-telemetry-controller/
│
├── README.md                          # Executive project summary and architecture
├── LICENSE                            # MIT License
│
├── firmware/                          # Microcontroller implementation
│   ├── main.py                        # RP2040 MicroPython acquisition & FDI logic
│   └── wokwi_hardwear.png             # Wokwi virtual hardware configuration
│
├── pipeline/                          # Data engineering & pipeline
│   ├── process_telemetry.py           # Ingestion, validation, and normalization
│   └── telemetry_raw.csv              # Raw telemetry log from virtual node
│
├── sim/                               # Model-Based Design (MBD)
│   ├── run_telemetry.m                # Script defining workspace timeseries objects
│   └── telemetry.slx                  # Simulink supervisory safety controller
│
└── docs/                              # Evidence & specifications
    ├── SRS_STS_Powertrain_Safety.pdf
    ├── Calibration_Report.pdf
    ├── simulink_model.png
    ├── scope_trace_50C.png
    ├── scope_trace_92C.png
    └── scope_trace_98C.png
