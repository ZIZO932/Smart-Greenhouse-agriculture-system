# Smart Greenhouse

A greenhouse prototype I built to monitor growing conditions and control pumps, fans, lighting, and temperature hardware. I used sweet basil as the main crop for testing.

The project changed quite a bit between the CAD and the assembled version. The original design used a Raspberry Pi Pico W, and I switched to an ESP32 during the build after damaging the Pico. Both versions are kept in this repo.

## Why I built it

I wanted to connect sensor readings to something the greenhouse could actually do: water the soil, switch on a fan, or adjust the lights. Fitting the tanks, pumps, electronics, and growing bed into one structure was a big part of the work too.

## The layout

![Greenhouse CAD](https://stasis.hackclub-assets.com/images/1773986201013-t6jx9w.png)

The design has three main stacked sections, plus a camera track around the top:

- **Tanks and pumps:** a 5 L water tank and three 1 L nutrient tanks, each with its own pumping line.
- **Electronics:** the controller, power distribution, sensor connections, and relay circuitry.
- **Growing bed:** the soil and plants, with tubing routed up from the tanks.
- **Camera track:** a planned moving camera platform for taking pictures around the plants.

The CAD used a transparent bed. For the physical prototype, I built the frame from MDF and used a polyethylene cover for the growing layer.

[CAD files](CAD/) include the assembly and a ZIP archive. The larger STEP model is also [on Google Drive](https://drive.google.com/file/d/1caedlcHiUJ2DHqxGwvVZIDkTWpKjw0eq/view?usp=drive_link).

## Electronics

![Schematic](https://stasis.hackclub-assets.com/images/1773969096763-pgv2fr.png)

The original PCB design uses a ULN2803A to drive the relays, with separate power rails for the controller, sensors, and higher-power hardware. The sensor setup includes a BH1750 light sensor, DS18B20 temperature sensing, capacitive soil moisture sensing, and an RS-485 connection for an NPK sensor through a MAX485.

I had to fix relay footprints and adjust the routing while working through the board design.

![PCB layout](https://stasis.hackclub-assets.com/images/1773975539047-9t9nk7.png)

## Building it

![Assembled frame](https://stasis.hackclub-assets.com/images/1781289180506-8guwwl.png)

The first frame used nails and didn't hold the weight properly. I rebuilt the joints with screws, then routed the pumps and tubing through the layers.

![Prototype electronics](https://stasis.hackclub-assets.com/images/1781287824241-pr5loz.jpeg)

I assembled the regulated power supply and wired the sensors and relay-controlled hardware. This was also where I damaged the Pico and moved to the ESP32. My build notes record a six-hour integrated test of the sensors and actuators.

## Dashboard and code

![Dashboard](https://stasis.hackclub-assets.com/images/1781288574691-5xvsad.png)

The dashboard work uses MQTT, Flask, and MySQL to collect and display readings. Grafana is shown in the build documentation too.

There are a few different stages in the uploaded code:

| File or folder | What it contains |
| --- | --- |
| [Firmware/main.py](Firmware/main.py) | Pico MicroPython code for sensor reading, relay control, and UART communication with a Pi Zero |
| [website/app.py](website/app.py) | Flask app that receives MQTT messages, stores readings in MySQL, and serves dashboard endpoints |
| [website/final_code_10204.ino](website/final_code_10204.ino) | ESP32 code excerpt with sensor functions, relay helpers, and plant profiles |
| [code parts](code%20parts/) | Other Arduino and MQTT snippets from development |
| [templates](templates/) | Dashboard HTML |

The ESP32 excerpt currently generates sample NPK values in `updateFakeNPK()`. Those values aren't live nutrient measurements. It also doesn't include `setup()` and `loop()`, so the uploaded excerpt isn't a complete flashable sketch.

The Flask app expects `templates/index.html` next to the app, while the uploaded HTML is named `templates/index (1).html` at the repo root. That path needs matching before running the dashboard locally. Broker addresses and database settings also need to match the local setup.

## Camera and disease detection

I planned a Pi Zero 2 W and Camera V2 platform that moves around the plants, takes images, and parks between scans. The proposed scan interval was 30 minutes, with a model trained using the [New Plant Diseases Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset).

The repo doesn't include trained model files or disease-detection results yet. This part is documented as a planned extension of the monitoring system.

## Original parts estimate

This is the parts list from the original design stage, including the Pico and camera hardware. Prices are recorded estimates from that stage.

| Name | Cost Per Item (USD) | Quantity | Total (USD) | Link | Distributor |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Water pump** | 5.57 | 4 | 22.28 | [Link](https://www.ram-e-shop.com/shop/dc-pump-240l-water-pump12vdc-ultra-quiet-brushless-240l-h-7953) | Ram Electronics |
| **PCB Fabrication** | 5.74 | 1 | 5.74 | [Link](https://jlcpcb.com) | JLCPCB |
| **Pin Header 1x04** | 0.12 | 2 | 0.24 | [Link](https://makerselectronics.com/product/pin-headers-male-2-54mm-5pin-straight-black-11mm/) | Makers Electronics |
| **Pin Header 1x02** | 0.10 | 7 | 0.67 | [Link](https://makerselectronics.com/product/pin-headers-male-2-54mm-5pin-straight-black-11mm/) | Makers Electronics |
| **Ceramic Cap** | 0.04 | 10 | 0.38 | [Link](https://makerselectronics.com/product/ceramic-capacitor-100nf-50v/) | Makers Electronics |
| **Electrolytic Cap** | 0.10 | 4 | 0.40 | [Link](https://makerselectronics.com/product/capacitor-10uf-25v-4x7mm/) | Makers Electronics |
| **Resistor** | 0.04 | 10 | 0.40 | [Link](https://makerselectronics.com/product/carbon-resistor-10k%cf%89-2w-through-hole/) | Makers Electronics |
| **12V 5A Power Adapter** | 5.74 | 1 | 5.74 | [Link](https://makerselectronics.com/product/adapter-12v-3a-3/) | Makers Electronics |
| **Barrel Jack** | 0.29 | 1 | 0.29 | [Link](https://store.fut-electronics.com/products/dc-barrel-female-jack?_pos=2&_sid=9cbb68bec&_ss=r) | Future Electronics Egypt |
| **DIP-18 Socket** | 3.16 | 1 | 3.16 | [Link](https://store.fut-electronics.com/search?type=product&q=DIP-18+7.62mm) | Future Electronics Egypt |
| **Relay** | 1.34 | 7 | 9.38 | [Link](https://www.amazon.eg/-/en/Generic-12V-Relay-SRD-12VDC-SL-C-Automatic/dp/B09GNYCBJ8) | Amazon Egypt |
| **Schottky Diode** | 0.15 | 1 | 0.15 | [Link](https://store.fut-electronics.com/products/copy-of-diode-1n5408-3a-1000v-high-current-rectifier?_pos=1&_sid=7c0e00b0d&_ss=r) | Future Electronics Egypt |
| **Inductor** | 0.02 | 1 | 0.02 | [Link](https://makerselectronics.com/product/inductor-330uh-0510-1w/?srsltid=AfmBOopEyPfXRbjQeAZuTj9z0SJHXyytV2tzQKyfccnhfVPX7rr7i2Ne) | Makers Electronics Egypt |
| **NPK Soil Sensor** | 61.26 | 1 | 61.26 | [Link](https://store.fut-electronics.com/products/soil-npk-nitrogen-phosphorus-potassium-nutrient-sensor?_pos=1&_sid=cc849b4cb&_ss=r) | Future Electronics Egypt |
| **Soil Moisture Sensor** | 1.91 | 1 | 1.91 | [Link](https://www.ram-e-shop.com/shop/sen-soil-c-capacitive-analog-soil-moisture-sensor-v2-0-sku-soil-c-8116?srsltid=AfmBOookvggy4W1wl8oSb-pGGNBmixARQOTydpFUzx5W_-lss_Y-4-94) | RAM Electronics |
| **Light Sensor** | 3.73 | 1 | 3.73 | [Link](https://store.fut-electronics.com/products/digital-light-intensity-module) | Future Electronics Egypt |
| **Temp Sensor (air)** | 0.86 | 1 | 0.86 | [Link](https://makerselectronics.com/product/ds18b20-temperature-sensor-to-92/) | Makers Electronics Egypt |
| **Temp Sensor (soil)** | 1.63 | 1 | 1.63 | [Link](https://www.ram-e-shop.com/ar/shop/wire-ds18b20-ds18b20-waterproof-temperature-sensor-original-chip-7175) | RAM Electronics |
| **Darlington Driver** | 0.46 | 1 | 0.46 | [Link](https://makerselectronics.com/product/uln2803apg-darlington-transistor-arrays-dip-18-brand-toshiba/) | Makers Electronics |
| **RS485 Transceiver** | 0.55 | 1 | 0.55 | [Link](https://uge-one.com/product/max485-rs-485-transceiver-dip8/) | UGE Electronics Egypt |
| **Raspberry Pi Camera V2** | 15.31 | 1 | 15.31 | [Link](https://www.ram-e-shop.com/ar/shop/rpi-v2-camera-raspberry-pi-camera-module-v2-official-8-mp-hd-imx219-official-6887) | Ram Electronics |
| **LDO Regulator** | 0.06 | 1 | 0.06 | [Link](https://www.ram-e-shop.com/ar/shop/lt1117-3-3v-ams1117-3-3v-6628) | Ram Electronics Egypt |
| **Buck Converter IC** | 0.77 | 1 | 0.77 | [Link](https://makerselectronics.com/product/lm2596t-5-0-buck-fixed-40v-5v-3a-to-220-5l-dc-dc-converters-dip-ic/) | Makers Electronics Egypt |
| **Raspberry Pi Zero 2W** | 38.28 | 1 | 38.28 | [Link](https://devboardsmarket.com/products/raspberry-pi-zero-2-w) | DEV boards |
| **Raspberry Pi Pico W** | 16.27 | 1 | 16.27 | [Link](https://www.ram-e-shop.com/ar/shop/rpi-pico-w-raspberry-pi-pico-w-wifi-8524) | RAM electronics |
| **GRAND TOTAL** | | | **$189.94** | | |

## More files

- [Circuit, PCB, and Gerber files](Circuit%20%28Schematic%20and%20pcb%29/)
- [BOM](BOM.csv)
- [Build journal](JOURNAL%20%285%29.md)
- [Database schema](website/database.sql)
