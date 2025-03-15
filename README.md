Acoustic-Based Real-Time Cardiovascular Monitoring and Abnormality Detection System –

Objective
This project aims to create a non-invasive, real-time heart monitoring system that detects heart abnormalities using acoustic sensors and signal processing techniques. The goal is to provide a portable and cost-effective solution for continuous heart health monitoring.

How It Works
Heart Sound Capture

Uses a stethoscope head with a microphone to record heart sounds.
The sounds are converted into electrical signals for processing.
Signal Processing

The signals are amplified using an LM386 audio amplifier.
A bandpass filter (20–150 Hz) removes unwanted noise.
The processed signal is converted into digital form using an ESP32 microcontroller.
Data Analysis & Visualization

The data is sent to a computer via Wi-Fi for further processing.

A Python program analyzes the heartbeats and detects abnormalities.
The system plots time-domain and frequency-domain graphs to visualize heart sounds.
Abnormality Detection

The system identifies irregularities like murmurs and arrhythmias.
Future improvements include AI-based classification for better diagnosis.

Key Features
Real-time heart monitoring without the need for medical supervision.
Portable and cost-effective, making it accessible for home use.
Wireless data transmission for remote monitoring.
Machine learning integration (future enhancement) for automated diagnosis.

Future Improvements
Adding mobile app support for remote access.
Cloud storage for long-term heart health tracking.
AI-based detection for more accurate diagnosis.
This system helps bridge the gap between traditional stethoscopes and advanced diagnostic tools, making cardiovascular monitoring more efficient and accessible.
