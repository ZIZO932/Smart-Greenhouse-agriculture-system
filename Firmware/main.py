import machine
from utime import sleep_ms, time
import onewire
import ds18x20
import struct
import json
from machine import Pin, ADC, I2C, UART


class BasilParams:
    TEMP_AIR_MIN        = 18.0
    TEMP_AIR_OPTIMAL    = 24.0
    TEMP_AIR_MAX        = 29.0
    TEMP_AIR_CRITICAL   = 35.0
    MOISTURE_MIN        = 55.0
    MOISTURE_TARGET     = 65.0
    MOISTURE_MAX        = 75.0
    LIGHT_MIN_LUX       = 15000
    LIGHT_MAX_LUX       = 50000
    LIGHT_ON_HOUR       = 6
    LIGHT_OFF_HOUR      = 22
    NITROGEN_MIN        = 120
    NITROGEN_MAX        = 200
    PHOSPHORUS_MIN      = 50
    PHOSPHORUS_MAX      = 100
    POTASSIUM_MIN       = 120
    POTASSIUM_MAX       = 200
    PUMP_MAX_ON_SEC     = 30
    PUMP_COOLDOWN_SEC   = 300
    WATERING_HOUR_START = 6
    WATERING_HOUR_END   = 20
    FAN_MIN_ON_SEC      = 10
    HEATER_MAX_ON_SEC   = 120
    HEATER_COOLDOWN_SEC = 60


class Pins:
    RS485_TX    = 0
    RS485_RX    = 1
    RS485_DE_RE = 2
    ONEWIRE     = 4
    I2C_SDA     = 6
    I2C_SCL     = 7
    MOISTURE    = 26
    PIZERO_TX   = 8
    PIZERO_RX   = 9
    PUMP_1      = 10
    PUMP_2      = 11
    PUMP_3      = 12
    PUMP_4      = 13
    FAN         = 14
    HEATER      = 15
    GROW_LIGHT  = 16


MOISTURE_DRY_RAW = 52000
MOISTURE_WET_RAW = 19000


class BH1750:
    ADDR          = 0x23
    CMD_CONT_HIGH = 0x10

    def __init__(self, i2c):
        self.i2c = i2c
        self.i2c.writeto(self.ADDR, bytes([self.CMD_CONT_HIGH]))
        sleep_ms(200)

    def read_lux(self):
        try:
            data = self.i2c.readfrom(self.ADDR, 2)
            raw = (data[0] << 8) | data[1]
            return raw / 1.2
        except:
            return -1


class NPKSensor:
    QUERY = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x07, 0x04, 0x08])

    def __init__(self, uart, de_re_pin):
        self.uart  = uart
        self.de_re = de_re_pin

    def _crc16(self, data):
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                crc = (crc >> 1) ^ 0xA001 if crc & 0x0001 else crc >> 1
        return crc

    def read(self):
        self.de_re.value(1)
        sleep_ms(2)
        self.uart.write(self.QUERY)
        sleep_ms(10)
        self.de_re.value(0)
        sleep_ms(500)
        if self.uart.any() >= 19:
            raw = self.uart.read(19)
            if self._crc16(raw[:17]) != ((raw[18] << 8) | raw[17]):
                return None
            def reg(i):
                return (raw[3 + i*2] << 8) | raw[4 + i*2]
            return {
                "moisture_pct" : reg(0) / 10.0,
                "temp_c"       : reg(1) / 10.0,
                "ec_us_cm"     : reg(2),
                "ph"           : reg(3) / 10.0,
                "nitrogen"     : reg(4),
                "phosphorus"   : reg(5),
                "potassium"    : reg(6),
            }
        return None


class Relay:
    def __init__(self, pin_num, active_high=True):
        self.pin         = Pin(pin_num, Pin.OUT)
        self.active_high = active_high
        self.state       = False
        self.on_since    = 0
        self.off_since   = time()
        self.off()

    def on(self):
        self.pin.value(1 if self.active_high else 0)
        if not self.state:
            self.on_since = time()
        self.state = True

    def off(self):
        self.pin.value(0 if self.active_high else 1)
        if self.state:
            self.off_since = time()
        self.state = False

    def on_duration(self):
        return (time() - self.on_since) if self.state else 0

    def off_duration(self):
        return (time() - self.off_since) if not self.state else 0


class TempSensors:
    def __init__(self, pin_num):
        self.ow   = onewire.OneWire(Pin(pin_num))
        self.ds   = ds18x20.DS18X20(self.ow)
        self.roms = self.ds.scan()

    def read_air(self):
        try:
            self.ds.convert_temp()
            sleep_ms(800)
            return self.ds.read_temp(self.roms[0]) if self.roms else None
        except:
            return None


def read_moisture_pct(adc):
    raw = adc.read_u16()
    pct = (MOISTURE_DRY_RAW - raw) / (MOISTURE_DRY_RAW - MOISTURE_WET_RAW) * 100.0
    return max(0.0, min(100.0, pct))


class LightScheduler:
    def __init__(self):
        self.current_hour = 6
        self.synced       = False

    def update_hour(self, hour):
        self.current_hour = hour
        self.synced       = True

    def should_light_be_on(self, lux):
        p = BasilParams
        return (p.LIGHT_ON_HOUR <= self.current_hour < p.LIGHT_OFF_HOUR
                and lux < p.LIGHT_MIN_LUX
                and lux < p.LIGHT_MAX_LUX)


class PiZeroComm:
    def __init__(self):
        self.uart = UART(1, baudrate=115200,
                         tx=Pin(Pins.PIZERO_TX),
                         rx=Pin(Pins.PIZERO_RX),
                         timeout=50)
        self.buf = ""

    def send(self, data_dict):
        try:
            self.uart.write((json.dumps(data_dict) + "\n").encode())
        except:
            pass

    def receive(self):
        try:
            if self.uart.any():
                chunk = self.uart.read(256)
                if chunk:
                    self.buf += chunk.decode("utf-8", "ignore")
                    if "\n" in self.buf:
                        line, self.buf = self.buf.split("\n", 1)
                        return json.loads(line.strip())
        except:
            self.buf = ""
        return None


def check_npk_alerts(npk):
    if not npk:
        return []
    p      = BasilParams
    alerts = []
    if npk["nitrogen"]   < p.NITROGEN_MIN:   alerts.append(f"LOW_N:{npk['nitrogen']}")
    if npk["phosphorus"] < p.PHOSPHORUS_MIN: alerts.append(f"LOW_P:{npk['phosphorus']}")
    if npk["potassium"]  < p.POTASSIUM_MIN:  alerts.append(f"LOW_K:{npk['potassium']}")
    if npk["nitrogen"]   > p.NITROGEN_MAX:   alerts.append(f"HIGH_N:{npk['nitrogen']}")
    return alerts


def control_fan(fan_relay, temp_air):
    p = BasilParams
    if temp_air is None:
        return
    if temp_air >= p.TEMP_AIR_MAX:
        fan_relay.on()
    elif temp_air < p.TEMP_AIR_OPTIMAL - 1.0:
        if fan_relay.state and fan_relay.on_duration() >= p.FAN_MIN_ON_SEC:
            fan_relay.off()


def control_heater(heater_relay, temp_air):
    p = BasilParams
    if temp_air is None:
        return
    if heater_relay.state and heater_relay.on_duration() >= p.HEATER_MAX_ON_SEC:
        heater_relay.off()
        return
    if not heater_relay.state and heater_relay.off_duration() < p.HEATER_COOLDOWN_SEC:
        return
    if temp_air < p.TEMP_AIR_MIN:
        heater_relay.on()
    elif temp_air >= p.TEMP_AIR_OPTIMAL:
        heater_relay.off()


def control_pumps(pump_relays, moisture_pct, current_hour, last_pump_time):
    p   = BasilParams
    now = time()
    if not (p.WATERING_HOUR_START <= current_hour < p.WATERING_HOUR_END):
        for relay in pump_relays:
            relay.off()
        return last_pump_time
    if now - last_pump_time < p.PUMP_COOLDOWN_SEC:
        return last_pump_time
    for relay in pump_relays:
        if relay.state and relay.on_duration() >= p.PUMP_MAX_ON_SEC:
            relay.off()
    if moisture_pct < p.MOISTURE_MIN:
        if not pump_relays[0].state:
            pump_relays[0].on()
            return now
    elif moisture_pct >= p.MOISTURE_MAX:
        for relay in pump_relays:
            relay.off()
    return last_pump_time


def control_light(light_relay, lux, scheduler):
    if scheduler.should_light_be_on(lux) and not light_relay.state:
        light_relay.on()
    elif not scheduler.should_light_be_on(lux) and light_relay.state:
        light_relay.off()


def emergency_off(*relays):
    for r in relays:
        r.off()


def main():
    uart0 = UART(0, baudrate=9600,
                 tx=Pin(Pins.RS485_TX),
                 rx=Pin(Pins.RS485_RX),
                 timeout=600)
    de_re = Pin(Pins.RS485_DE_RE, Pin.OUT)
    de_re.value(0)
    npk_sensor = NPKSensor(uart0, de_re)

    i2c   = I2C(1, sda=Pin(Pins.I2C_SDA), scl=Pin(Pins.I2C_SCL), freq=400000)
    light = BH1750(i2c)
    temps = TempSensors(Pins.ONEWIRE)
    adc   = ADC(Pin(Pins.MOISTURE))

    pump1    = Relay(Pins.PUMP_1)
    pump2    = Relay(Pins.PUMP_2)
    pump3    = Relay(Pins.PUMP_3)
    fan      = Relay(Pins.FAN)
    heater   = Relay(Pins.HEATER)
    grow_led = Relay(Pins.GROW_LIGHT)
    pumps    = [pump1, pump2, pump3]

    pizero         = PiZeroComm()
    scheduler      = LightScheduler()
    last_pump_time = 0
    last_npk_time  = 0
    last_send_time = 0
    npk_data       = None

    while True:
        now          = time()
        air_c        = temps.read_air()
        lux          = light.read_lux()
        moisture_pct = read_moisture_pct(adc)

        if now - last_npk_time >= 60:
            npk_data      = npk_sensor.read()
            last_npk_time = now

        cmd = pizero.receive()
        if cmd:
            if "hour"       in cmd: scheduler.update_hour(cmd["hour"])
            if cmd.get("emergency_off"): emergency_off(pump1, pump2, pump3, fan, heater, grow_led)
            if "pump1"      in cmd: pump1.on()    if cmd["pump1"]      else pump1.off()
            if "grow_light" in cmd: grow_led.on() if cmd["grow_light"] else grow_led.off()

        if air_c is not None:
            control_fan(fan, air_c)
            control_heater(heater, air_c)

        if air_c and air_c >= BasilParams.TEMP_AIR_CRITICAL:
            fan.on()
            heater.off()

        last_pump_time = control_pumps(pumps, moisture_pct, scheduler.current_hour, last_pump_time)
        control_light(grow_led, lux, scheduler)

        if now - last_send_time >= 10:
            pizero.send({
                "t"        : now,
                "air_c"    : round(air_c, 2)       if air_c   else None,
                "lux"      : round(lux, 1)          if lux > 0 else None,
                "moisture" : round(moisture_pct, 1),
                "npk"      : npk_data,
                "alerts"   : check_npk_alerts(npk_data),
                "relays"   : {
                    "pump1"     : pump1.state,
                    "pump2"     : pump2.state,
                    "pump3"     : pump3.state,
                    "fan"       : fan.state,
                    "heater"    : heater.state,
                    "grow_light": grow_led.state,
                }
            })
            last_send_time = now

        sleep_ms(500)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass