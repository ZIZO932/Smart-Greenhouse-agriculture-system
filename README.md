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


