# AstroPi
Astro Pi is a small Raspberry Pi computer developed by the Raspberry Pi Foundation (RPF), in collaboration with the UK Space Agency and the European Space Agency (ESA).

# How does it work?
At its core, the device is simply a Raspberry Pi bolstered by several add-ons such as a camera and pre-installed libraries that enable image acquisition and sensor data capture (yaw / pitch / infra-red images / acceleration). These data sets provide ample fodder for exploration via two designated experiments: Life in Space or Life on Earth. For the former stipulation, plan an experiment related directly to ISS conditions; as for the latter option - focus should relate back to life here on planet earth.

# What my file does:
This file will periodically collect Magnetic, Acceleration, Orientation, Location and Time data and input them in a text file. The code will run for 3 hours, collecting data for every few seconds while displaying an image on the LEDs to show that the script is running. It is not a very complex script as I am only collecting and storing the data wanted. Feel free to take a look at my code for further understanding. 

# What is the purpose of this experiment?
The goal of this experiment is to use the data collected (such as Magnetic and Location data) and input this data into Google Earth to create a visual showing the magnetic field strength of different locations on the Earth.
