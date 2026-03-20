

# 3/19/2026 - Building the Firmware last day

_Time spent: 3h_

Today I worked on the Pi Zero communication code, using UTF-8 to make sure everything reads correctly and keeping it all in JSON format so the data stays organized. I also built an NPK alert system to catch any big nutrient problems before they cause damage. After that, I added the specific functions for the water pumps, fans, and heaters to control them based on what the sensors are actually seeing. I made sure to include an emergency function too, just so I have a quick way to shut down all the actuators at once if something goes wrong.

This was the last day for the firmware since I finally got into the main.py file. I started with a simple welcome message and declared all my variables. The main while loop is now running—it reads through the sensors one by one, checks the Pi Zero connection, and sends the data over. I added a 500ms delay at the end to keep the timing stable. To wrap things up, I made a keyboard interrupt function so I can kill the whole process and close every relay instantly if I need to stop the system manually.
![image](https://stasis.hackclub-assets.com/images/1773985356171-wdy69u.png)

![image](https://stasis.hackclub-assets.com/images/1773985373442-qdvhzb.png)

![image](https://stasis.hackclub-assets.com/images/1773985387214-sve0n7.png)

![image](https://stasis.hackclub-assets.com/images/1773985400504-ju0t4i.png)

![image](https://stasis.hackclub-assets.com/images/1773985356171-wdy69u.png)
![image](https://stasis.hackclub-assets.com/images/1773985373442-qdvhzb.png)
![image](https://stasis.hackclub-assets.com/images/1773985387214-sve0n7.png)
![image](https://stasis.hackclub-assets.com/images/1773985400504-ju0t4i.png)

# 3/18/2026  - Building the Firmware 1

_Time spent: 4h_

This was the firs day in which I started on the firmware for the project. I began by setting up the optimal values for the Basil plants, putting all the min and max parameters into one class. I also made a separate class to define what every pin on the Pico actually does so the code stays organized.

For the sensors, I started with the BH1750 light sensor. I wrote the code to check the I2C connection, handle the read delays, and then I used a formula I found to convert the raw data into actual light levels. Next, I worked on the NPK sensor, which has 7 registers. I built a function for it to self-read and return the soil nutrient data.

After the sensors, I moved on to the relays. I wrote functions to handle opening, closing, and timing for each one. For the temperature sensors, I used the OneWire library to scan the DS18B20 sensors. I set them to 12-bit conversion for better accuracy and added an "if" condition to sort the readings between soil and air temperature.

The moisture sensor was simpler since it just reads the data directly. Finally, I coded the light schedule to manage the plant's day/night cycles, which is pretty important for the photosynthesis and respiration process.
![image](https://stasis.hackclub-assets.com/images/1773984990596-lxctb0.png)

![image](https://stasis.hackclub-assets.com/images/1773985006952-dl4tmt.png)

![image](https://stasis.hackclub-assets.com/images/1773985025307-jqxg6j.png)

![image](https://stasis.hackclub-assets.com/images/1773984990596-lxctb0.png)
![image](https://stasis.hackclub-assets.com/images/1773985006952-dl4tmt.png)
![image](https://stasis.hackclub-assets.com/images/1773985025307-jqxg6j.png)

# 3/17/2026  - AI Tracking System

_Time spent: 2h_

I finally got the physical model for the tracking system done. I designed a circular track that runs along the perimeter of the top layer to give the camera a full view of the plants. I also built a small car that sits on this track to carry the Raspberry Pi Zero 2W and the Pi Camera.

The idea is for the car to revolve around the growing area so it can catch every angle of the plants. I made sure the car is stable enough to hold the electronics and the battery pack while it moves. It took some time to get the curves of the track right so the car wouldn't get stuck, but it’s now a smooth loop. This setup is what will allow the AI to scan for diseases every 30 minutes before returning to its home position to save power.

![image](https://stasis.hackclub-assets.com/images/1773984329382-544oi2.png)

![image](https://stasis.hackclub-assets.com/images/1773984331934-b67oev.png)


![Screenshot 2026-03-20 072844](https://stasis.hackclub-assets.com/images/1773986201013-t6jx9w.png)

![image](https://stasis.hackclub-assets.com/images/1773984329382-544oi2.png)
![image](https://stasis.hackclub-assets.com/images/1773984331934-b67oev.png)
![image](https://stasis.hackclub-assets.com/images/1773986201013-t6jx9w.png)

# 3/16/2026  - PCB Design and footprint

_Time spent: 5h_

Today, I began mapping my pcb design and preparing the footprints for the sensors and actuators. And I began with connecting each part like the RS485 sensors and capacitors and every sensors as a different system. Which take some time. I faces some problem which is the capacitors was different sizes and I didn't see that so I searched on every capacitor and its footprints.then by connecting the main power rails for every system and made sure every thing is connected without intersections. Also, I made sure to connect everything with it's rails. I connected the relays system and discovered I made a mistake in the footprints of the relays and I searched on the true ones and I made them and reconnected the relays systems. So, I ran a DRC check and found some errors like the silicon pring and the edge cuts. And some pins which is not allained with the schematic of the pi pico. So I got the true footprints and reconnected the system again and made made sure every thing is connected the right way and ran another DRC every thing was working.
![image](https://stasis.hackclub-assets.com/images/1773975539047-9t9nk7.png)

![image](https://stasis.hackclub-assets.com/images/1773975547489-8zqu00.png)

![image](https://stasis.hackclub-assets.com/images/1773975539047-9t9nk7.png)
![image](https://stasis.hackclub-assets.com/images/1773975547489-8zqu00.png)

# 3/15/2026  - High-Power Actuators with a Low-Power Brain

_Time spent: 4h_

Today was all about the "muscles" of the system, getting the ULN2803A Darlington array wired up. Think of it as the mediator between the Raspberry Pi Pico and the Relay Modules. Since the Pico is a low-power "brain," it doesn't have the strength to flip the heavy-duty switches (the relays) that control my water pumps, fans, and heaters. The ULN2803A acts as the driver that allows those tiny 3.3V signals to trigger the high-power actuators without blowing anything up.

I spent the rest of the day in a deep-focus wiring marathon, connecting the sensors to the Pico. This wasn't just plug-and-play; I had to add the specific capacitors and resistors for each sensor to keep the data lines clean and protected. The real puzzle was the pin mapping, I had to go through the datasheets one by one to make sure every sensor's specific protocol (like I2C or Analog) was matched to a compatible pin on the Pico. It was a lot of double-checking, but the core "control center" is finally wired and ready to talk to the environment.
![image](https://stasis.hackclub-assets.com/images/1773968950346-84z0kl.png)

![image](https://stasis.hackclub-assets.com/images/1773969076588-iew94d.png)

![image](https://stasis.hackclub-assets.com/images/1773969096763-pgv2fr.png)

![image](https://stasis.hackclub-assets.com/images/1773968950346-84z0kl.png)
![image](https://stasis.hackclub-assets.com/images/1773969076588-iew94d.png)
![image](https://stasis.hackclub-assets.com/images/1773969096763-pgv2fr.png)

# 3/14/2026  - Bridging the Pico and the Pi Zero

_Time spent: 5h_

This phase of the schematic was all about the "handshake" between the different brains of the system. After spending yesterday hunting down the exact libraries and PCB footprints for my components, I finally got everything imported and verified. Today’s mission was power and communication: getting the Raspberry Pi Pico and the Pi Zero 2W wired up to the same power rails and linked together. Since the Pi Zero will be moving on that circular track around the plants (rather than sitting on the main board), I designed header pins into the schematic so I can easily plug it in via a ribbon cable or jumper wires.

The real technical hurdle was the RS-485 communication. I integrated a MAX485E to act as the translator between the Pico’s logic and the industrial NPK sensor. Since the sensor runs on 12V, I tapped into the high-voltage rail, but I had to be careful with the signal lines. I used 560-ohm resistors to bias the lines and manage the charge so it’s perfectly safe for the MAX485 and the Pico to handle.

I also threw in a dedicated decoupling capacitor for the MAX485 chip itself; it’s a small detail, but it’s there to soak up any voltage spikes or "kickback" when the power gets cut, ensuring I don’t fry my communication bridge. It’s starting to look like a real industrial controller now.
![image](https://stasis.hackclub-assets.com/images/1773968761510-s22mqx.png)

![image](https://stasis.hackclub-assets.com/images/1773968785633-ri89xg.png)

![image](https://stasis.hackclub-assets.com/images/1773968820704-z2tpg5.png)

![image](https://stasis.hackclub-assets.com/images/1773968761510-s22mqx.png)
![image](https://stasis.hackclub-assets.com/images/1773968785633-ri89xg.png)
![image](https://stasis.hackclub-assets.com/images/1773968820704-z2tpg5.png)

# 3/13/2026  - Staring Schematic

_Time spent: 3h_

Today was all about diving into the schematic design, which turned out to be a lot more about "protection" than just making connections. After doing some digging, I realized that every MCU and IC is actually pretty fragile—they need specific capacitors and resistors just to survive voltage spikes or prevent short-circuit damage. It’s one of those things you don't think about until you realize a tiny spark could fry your whole project.

To keep things organized, I mapped out three distinct power rails: 12V for the heavy-duty actuators, 5V for the MCUs, and 3.3V for the more sensitive sensors. Having these rails makes the wiring way less of a headache. I’m using a single 12V adapter as the main heart of the system, then stepping it down using an LM2596T-5 for the 5V line and an AMS1117-3.3 for the 3.3V line.

I didn't want to take any chances with stability, so I added four capacitors to each regulator to smooth out the voltage and act as a tiny buffer if the power flickers. I also integrated an inductor with the LM2596 to cut down on energy loss and threw in a diode to make sure current doesn't accidentally flow backward and wreck the source. It’s a lot of extra components, but it’s the only way to make sure the "brain" of the system doesn't lose its mind the second a pump kicks in. 
![image](https://stasis.hackclub-assets.com/images/1773968537807-u09umy.png)

![image](https://stasis.hackclub-assets.com/images/1773968582625-dd6lg7.png)

![image](https://stasis.hackclub-assets.com/images/1773968537807-u09umy.png)
![image](https://stasis.hackclub-assets.com/images/1773968582625-dd6lg7.png)

# 3/12/2026  - AI disease detection

_Time spent: 3h_

I also came up with a pretty ambitious plan for an AI disease detection subsystem to sit right on top of everything. The idea is to have a Raspberry Pi Zero 2W and a Pi Camera Module mounted on a wheeled platform that actually travels along a circular track around the perimeter of the growing area in Layer 3. This way, instead of a static view, the camera revolves around the plants to catch every single angle from a consistent distance.

To keep it efficient, the plan is for the system to run on a 30-minute cycle: every half hour, the platform wakes up, completes a full loop to capture images of the plants, and then returns to its home position to power down the motors completely. It’s designed to be a totally independent circuit from the main monitoring board, but it will feed all its visual data into the same cloud. I haven't built the physical model for this part yet, but having the concept mapped out gives me a clear path for adding high-tech "eyes" to the setup later on. The first image shows raspberry pi zero 2w connected to pi camera. and for the second image i got it from a research that trained an ai model to detect diseases.
![image](https://stasis.hackclub-assets.com/images/1773967968475-e20jzh.png)

![image](https://stasis.hackclub-assets.com/images/1773968113911-8hj6kc.png)

![image](https://stasis.hackclub-assets.com/images/1773967968475-e20jzh.png)
![image](https://stasis.hackclub-assets.com/images/1773968113911-8hj6kc.png)

# 3/11/2026  - Layer 2 and 3

_Time spent: 5h_

It took some serious effort, but I finally finished the three-layer stack. After the pump layer was set, I moved on to the second level, which acts as the brain for the electronics and sensors. The real grind was making sure the pipes from the bottom pumps were actually routed and connected properly to the bubblers on top without any kinks. Once the plumbing was secure, I installed the NPK and moisture sensors into the second layer, carefully positioning them so they’d be fully submerged in the soil once the bed was filled.

For the final layer, I went with a transparent acrylic finish for the soil bed so I can actually see the root health and water flow from the outside. Getting all three layers to line up, pumps on the bottom, sensors in the middle, and soil on top, was a massive coordination task, but seeing it all stacked together with the bubblers in place makes the whole system feel real. These are some figures of the whole model till now.

![image](https://stasis.hackclub-assets.com/images/1773967339796-q80q2w.png)

![image](https://stasis.hackclub-assets.com/images/1773967342582-ii920u.png)

![image](https://stasis.hackclub-assets.com/images/1773967339796-q80q2w.png)
![image](https://stasis.hackclub-assets.com/images/1773967342582-ii920u.png)

# 3/10/2026  - Layer 1

_Time spent: 1.5h_

I started the 3D model by setting up Layer 1 and getting the plumbing foundation right. It actually took me quite a while just to track down the exact 3D models I needed to match my parts, but once I had them, I mapped out the base and installed the four water pumps. I connected each one to its own tank, one 5-liter main tank for irrigation and three 1-liter tanks for the N, P, and K nutrients, and made sure every pump was properly hooked up to its own pipe. It’s a clean setup, and now that the physical layout is finished, the first layer is officially ready. i attached two pictures of the model.
![image](https://stasis.hackclub-assets.com/images/1773966259295-lvh8zo.png)

![image](https://stasis.hackclub-assets.com/images/1773966272578-ye7l48.png)

![image](https://stasis.hackclub-assets.com/images/1773966259295-lvh8zo.png)
![image](https://stasis.hackclub-assets.com/images/1773966272578-ye7l48.png)

# 3/9/2026 - Actuators selection

_Time spent: 4h_

After the sensors selection i shifted my focus on the actuators. My goal was simple on paper but a nightmare in practice: build a dedicated correction system for every single parameter I’m monitoring.

For the soil, I mapped out a 5-liter main water tank with a water pump for basic irrigation. But the NPK part is where it got complicated; I decided to add three separate pumps to dose Nitrogen, Phosphorus, and Potassium independently based on what the sensors say. I also found that to irrigate with least loss in water i need a 360 degree bubbler which i found in multiple websites.

For the climate, I settled on a fan and a heater to lock the temperature between 25°C and 30°C, plus a high-output LED. 

With 4 sensors and 7 actuators, I needed a controller that could handle a lot of I/O. I chose the Raspberry Pi Pico W. I love the Pico for its speed, and the "W" version gives me the Wi-Fi I’ll eventually need for a real-time feedback dashboard. The struggle today was mapping the pins. I realized that the Pico’s 3.3V logic can't directly talk to 12V pumps or the RS-485 sensor.
In the first image it shows the bubbler i want to use where to irrigate the whole soil i needed 360 one that has high reach.
In the second image it shows the schematic of a smart greenhouse system in which i took the idea of using a pico. 

![image](https://stasis.hackclub-assets.com/images/1773963737169-e9ru0c.png)
![image](https://stasis.hackclub-assets.com/images/1773964122911-kg0fbu.png)

![image](https://stasis.hackclub-assets.com/images/1773963737169-e9ru0c.png)
![image](https://stasis.hackclub-assets.com/images/1773964122911-kg0fbu.png)

# 3/8/2026 - Solution parameters and sensors selection

_Time spent: 5h_

Today i struggled in choosing parameters in the end i chose : NPK, Temperature, Light, and Soil Moisture. I figured if I could actually control these variables, I could grow high-value stuff like Basil or Stevia basically anywhere. Once I had the plan, I needed the "eyes" of the system and that’s where the real headache started. I spent hours looking for soil sensors, only to realize most of the cheap ones are basically toys; they just give you a vague conductivity reading and can't tell Nitrogen from Potassium.
I finally found an industrial RS-485 Modbus RTU NPK sensor. It’s way more expensive, and I know the code is going to be a total nightmare compared to a simple analog sensor, but it actually gives me real data i wanted. I also grabbed a capacitive moisture sensor because I knew the standard resistive ones would just rust and die in the soil. At least now I know the hardware can actually handle the job. The first image shows the NPK sensor i chose where its a bit expensive compared to something like 7 in 1 sensor the problem is the accuracy in which i want to make sure that the plant wont die not just a theortical thingy.
The second image is an image of the module used to connect the NPK sensor to any microcontroller. The third image shows the moisture soil sensor that was chosen due to the covarge of its forks which prevents rust.

![image](https://stasis.hackclub-assets.com/images/1773961753810-d3rcqw.png)

![image](https://stasis.hackclub-assets.com/images/1773962080338-s6vjz4.png)

 
![image](https://stasis.hackclub-assets.com/images/1773962228739-apzckr.png)

![image](https://stasis.hackclub-assets.com/images/1773961753810-d3rcqw.png)
![image](https://stasis.hackclub-assets.com/images/1773962080338-s6vjz4.png)
![image](https://stasis.hackclub-assets.com/images/1773962228739-apzckr.png)

# 3/7/2026 - The Problem and past solutions

_Time spent: 4h_

For the first day it was all about the "Problem Selection" phase for my Capstone. I can't just build something "cool" it has to solve a legitimate Egyptian challenge. I spent hours looking into the agricultural sector. Egypt is struggling with environmental instability and major water stress. High-value aromatic crops like **Basil and Stevia** are taking a hit because they are so sensitive to heatwaves and irregular irrigation.

The Struggle i faced when searching for solutions is that Most smart pots only monitor; they don't fix. I realized I needed a system that actually manioulate the environment.
The Solution i chose was A 4-layered vertical infrastructure. It mimics city planning in which (Water pumbs and tank - Electronics - Soil - Environment). The first image shows a figure that i found in this paper (Smart Greenhouse Automation
System) where they developed the system in layers to make it easy to bulid and modify.
In the second image i attached there was the process that the system works in.

![image](https://stasis.hackclub-assets.com/images/1773934639475-ctrc09.png)

![image](https://stasis.hackclub-assets.com/images/1773934689488-gmyfpu.png)

![image](https://stasis.hackclub-assets.com/images/1773934639475-ctrc09.png)
![image](https://stasis.hackclub-assets.com/images/1773934689488-gmyfpu.png)
