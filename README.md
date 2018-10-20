Tool for Hitachi L200 power inverter

**Requirements**

Python 3.6

USB - RS485 serial adapter

**Installation**

Setup and run virtualenv on linux:
```
python3 -m pip install --user virtualenv
mkdir project
cd project
python3 -m virtualenv venv
```
Install dependencies
```
python -m pip install -r requirements.txt
```


**Controlling device**

1. Connect adapter with Hitachi device and plug into usb port
2. Inside project run following command
```
python modbus.py --port <adapter_port> --addr <slave_address>
```
You should be prompet for desired frequency
