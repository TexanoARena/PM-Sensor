# Rilevatore di Particolato Atmosferico

L'idea è quella di iniziare a costruire un rilevatore di particolato atmosferico programmando il tutto ad alto livello, usando appunto un raspberry o un odroid (occhio alla piedinatura del GPIO che cambia tra raspberry e odroid) con installato un sistema operativo linux Ubuntu e/o Raspbian e programmare i sensori in python, per poi scendere di livello ad andare su MCU programmando in C.

Per questo progetto è stato usato un Odroid-C1+

Ringrazio chi si è gentilmente offerto di aiutarmi a capire un po' di più riguardo vari aspetti come x esempio la lettura dei datasheet ed a trovare la corretta formula da applicare per convertire i valori letti dall'adc + sensore

il codice sorgente è stato scritto in Python e poi installato su un Odroid-C1+ (paritetico ad un Raspberry Pi 3 model B)

Sono ben accetti consigli e migliorie

*Note: il codice non è stato revisionato quindi se ci sono errori o imperfezioni non me ne vogliate..*

## Materiale necessario
1 x Ordoid C1+

1 x ADS1115-4-channel-16-bit-ADC-Module

1 x Display LCD, IIC / I2C / TWI Modulo Display LCD 2004/20 x 4, 5V

1 x keyestudio Pm2.5 Sensor Dust Sensor Detector Module

1 x breadboard

20 x Cavetti Jumper Multicolore Maschio-Maschio 

20 x Cavetti Jumper Multicolore Femmina-Femmina 

## Installazione dei moduli python

Usare il package manager [pip](https://pip.pypa.io/en/stable/) per installare i moduli python.

```bash
# --- Installazione moduli python
python -m pip install smbus
git clone https://github.com/jfath/RPi.GPIO-Odroid.git
cd RPi.GPIO-OdroidC1-master
python setup.py install

# --- Clone del progetto in locale
git clone git@github.com:TexanoARena/PM-Sensor-Python-.git
cd PM-Sensor-Python
```

## Usage
```python
python start.py
```

## Contribuire

Le richieste pull sono benvenute. Per modifiche importanti, ti preghiamo di aprire prima un problema per discutere di cosa vorresti cambiare.

---

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)