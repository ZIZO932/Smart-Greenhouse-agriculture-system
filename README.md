# Smart Greenhouse agriculture system
## Description
The Smart Greenhouse agriculture system uses a 4-layer design to protect crops like Basil from Egypt's heat and water shortages. A Raspberry Pi Pico W monitors industrial NPK and moisture sensors, then automatically triggers pumps and fans to keep everything in the perfect range. To top it off, an AI-powered camera on a circular track patrols the plants to catch diseases early.
---


## Why I Built This (The "Problem")
Farming in Egypt is genuinely getting harder. Water stress and heatwaves are a real problem, and sensitive crops like Basil and Stevia are expensive to lose. Most of the "smart farming" products I found were just monitors — they'd send you an alert saying the soil was dry, and that was it. You still had to go do something about it.
That gap is what pushed me to build this. I wanted a system that doesn't just report a problem, but fixes it. Nitrogen drops? The system pumps nitrogen. Temperature spikes? The fans come on. The whole point was to move from observation to actual automation.

---

## The 3D Model: A Three-Layer Stack
![Final 3D Model](https://stasis.hackclub-assets.com/images/1773986201013-t6jx9w.png)

I designed this in a vertical configuration (inspired by city planning) to keep things clean and functional.

* **Layer 1 (The Pump Room):** This is the foundation. It holds a 5L main water tank for irrigation and three 1L tanks for N, P, and K nutrients. I mapped out four water pumps here, each hooked up to its own plumbing line.
* **Layer 2 (The Brain & Sensors):** This is where the electronics live. I installed industrial-grade NPK and moisture sensors here. The plumbing from the bottom passes through this layer to reach the top, which was a total nightmare to route without kinks.
* **Layer 3 (The Grow Bed):** I went with a transparent acrylic finish for the soil bed so you can actually see the root health. It uses 360-degree bubblers to make sure water reaches everywhere with zero waste.
* **The AI Track:** Encircling the top is a custom circular track. I built a small car that carries the Pi Zero and Camera, revolving around the plants every 30 minutes to catch every angle.

   **This is the link for the 3d model in step i didnt upload it here because of its size** https://drive.google.com/file/d/1caedlcHiUJ2DHqxGwvVZIDkTWpKjw0eq/view?usp=drive_link
  it is also found as a .zip file in the CAD folder

---

## Schematic & PCB Design
I spent a lot of time making sure this board wouldn't catch fire. Since the Pico is a low-power "brain," it can't handle the 12V needed for pumps and heaters.

### The Schematic
![Schematic Design](https://stasis.hackclub-assets.com/images/1773969096763-pgv2fr.png)

The heart of the protection is the ULN2803A Darlington array. It acts as the mediator—taking tiny 3.3V signals from the Pico and using them to trigger the heavy-duty relays. I also built three distinct power rails to keep the noise down:
* **12V:** For the (pumps/fans/heaters).
* **5V:** For the MCUs (stepped down via LM2596T-5).
* **3.3V:** For the sensitive sensors (stepped down via AMS1117-3.3).

I added 560-ohm resistors and a MAX485E chip to handle the RS-485 Modbus communication with the NPK sensor. It’s industrial-grade stuff, not that cheap analog junk.

### The PCB
![PCB Layout](https://stasis.hackclub-assets.com/images/1773975539047-9t9nk7.png)

I had to fix mistakes with relay footprints and ensure the power rails were wide enough to handle the current. I added decoupling capacitors everywhere to soak up voltage spikes from the pumps. After a few DRC (Design Rule Check), the board is officially intersection free and ready for production.

---

## AI Disease Detection
The patrol car sends images back to the Pi Zero 2W for processing. I'm training the disease detection model on the**[New Plant Diseases Dataset on Kaggle](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)**, which has a solid variety of labeled leaf conditions.
The workflow is simple: the car wakes up every 30 minutes, does one full lap around the plants scanning for spots or wilting, then returns to its dock to charge. Keeping it parked between scans was a deliberate choice to extend battery life.





---
## BOM

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
