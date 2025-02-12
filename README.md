# Log2Evt

Log2Evt is a tool that converts log messages into SystemTap events. It can be used to trace the execution of a program by monitoring its log messages. The tool is implemented as a Python script that generates a SystemTap script. The SystemTap script can be used to trace the program execution by monitoring the log messages.

## Requirements
- CentOS 7
- Python 3.8+
- SystemTap 4.0+
- Kernel debug symbols (kernel-debuginfo)

## Installation
```bash
sudo yum install systemtap kernel-devel kernel-debuginfo
pip install -r requirements.txt