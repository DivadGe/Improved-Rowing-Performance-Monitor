# Introduction

Rowing is a sport that has been around for centuries, and it is known for its physical and mental demands on athletes. As a result, it has become a popular sport at both the recreational and competitive levels. However, despite its popularity, rowing remains a challenging sport to master due to the technical nature of the movements involved. In recent years, advancements in technology have led to the development of tools and devices that can aid in training and performance evaluation for rowers. These tools range from simple stopwatches and heart rate monitors to more advanced systems that incorporate sensors and other tracking technologies. The use of technology has enabled coaches and athletes to gain deeper insights into performance and technique, allowing for more effective training and improved results. However, the current technology has limitations, and there is a need for more advanced systems that can provide even more in-depth data on rowing performance.

The current NK Speedcoach system, which incorporates the Empower Oarlock, is one of the most popular performance monitoring systems in rowing. However, the system has limitations that affect its usefulness for athletes and coaches. One major limitation is its high cost, which can be a barrier for many rowing teams. Additionally, the system is a closed system, meaning the data collected is not readily available for analysis by external software or devices. This can limit the possibilities for athletes and coaches to gain in-depth insights into their performance and make informed training decisions.

In response to these limitations, alternative performance monitoring systems have emerged in the market, such as Rowing in Motion, a phone app that offers a lot more functionality than the NK Speedcoach system. However, Rowing in Motion has its own drawbacks. For example, athletes have to bring their phone into the boat, which may not always be practical or safe. Additionally, the app is relatively expensive.

Coxmate, an Australian brand, offers a performance monitoring system that addresses the price point better than the NK Speedcoach system. However, it has even less functionality than the NK Speedcoach, which can limit the possibilities for athletes and coaches to gain insights into their performance. In light of these limitations, there is a need for a new and advanced performance monitoring system that is affordable, easy to use, and provides athletes and coaches with in-depth insights into their performance and technique.
 
This thesis presents a new approach to monitoring rowing performance through the development of an advanced performance monitoring system. The system provides more precise measurements than current performance monitors and utilizes accelerometer and orientation data to generate an acceleration curve and identify balancing problems. The results obtained from the system can potentially aid in the optimization of rowing technique and performance, making it valuable for both rowing athletes and coaches. The development process and evaluation of the system are presented in this thesis, providing a new perspective on monitoring rowing performance. 

In this research, a prototype will be designed and developed that incorporates a mesh of sensors to enhance the performance monitoring capabilities of a rowing team. Multiple sensor-equipped devices positioned around the boat will work in tandem to collect data that can be used to evaluate the rowers' performance. The data will be transmitted wirelessly to a central node for storage and analysis, and subsequently disseminated to various monitoring devices for real-time feedback.
 
# Communication

The role of the coach in analysing rowing performance is crucial. With the development of a new performance monitoring system, effective communication between the system and the coach becomes paramount. This communication ensures that the real-time data collected by the system is promptly analysed and acted upon. This section discusses the different options for communicating between the monitoring system and the coach.


## LoRa

LoRa (Long Range) is a wireless communication protocol that uses unlicensed frequency bands, in Europe it uses 868 MHz. It provides long-range, low-power wireless data communication for IoT (Internet of Things) devices with low bandwidth requirements. LoRa is a type of LPWAN (low-power wide-area network) technology that enables devices to communicate over long distances, even in areas with poor cellular coverage.

LoRa uses a proprietary modulation scheme that is designed to enable long-range wireless communication using low data rates and minimal power consumption. It operates in the sub-GHz frequency bands, which are less crowded than the 2.4GHz bands used by many other wireless communication technologies. This allows LoRa to provide reliable and robust communication over distances of several kilometres, making it ideal for applications that require long-range connectivity.

When considering communication with the coach during on-water rowing, LoRa technology presents certain benefits. Firstly, LoRa's long-range communication capability is a notable advantage, as it alleviates concerns regarding the coach being out of range. Additionally, the low power consumption of LoRa devices facilitates a smaller device size and less battery consumption.

However, despite these benefits, there are significant limitations to the use of LoRa in the context of rowing performance monitoring. Specifically, the maximum transmit duty cycle of 1% restricts the amount of data that can be transmitted and results in a significant drop in data rate. Furthermore, while LoRa technology was developed for transmitting small amounts of data over long distances for IoT devices, this is not the intended use case for the performance monitoring system developed in this thesis. Consequently, alternative technologies must be explored to effectively communicate with the coach during on-water rowing.


## NRF24L01

The NRF24L01 is a widely used wireless communication module in the field of embedded systems. The module has gained popularity due to its low cost, small size and ease of integration into a variety of systems. The NRF24L01 operates in the 2.4 GHz ISM (Industrial, Scientific and Medical) band and provides a reliable and robust communication link. The module also supports a range of data rates, allowing for flexibility in the amount of data transmitted. These features make the NRF24L01 an attractive option for wireless communication in various applications, including this thesis.

The NRF24L01 offers several advantages, including a high data rate that allows real-time transmission of captured data for analysis by the coach from the water's edge. Additionally, the module is relatively inexpensive, which can help to reduce the overall cost of the monitoring system.

The main disadvantage of the NRF24L01 is the potential for interference from other electronic devices. Because most electronic devices operate on the 2.4 GHz band, there may be a significant amount of interference that could affect the accuracy and reliability of the data transmitted.

When compared to LoRa, the NRF24L01 is a more cost-effective option with a higher data rate that is not limited by a duty cycle. While the range may be shorter than LoRa, it is still sufficient for the application, as the coach is always within the line of sight. Although LoRa is less prone to interference, the high data rate offered by the NRF24L01 makes up for this and, in practice, the number of devices on a river or lake where the system will be used is likely to be low.


## WiFi/Bluetooth

Both Wi-Fi and Bluetooth operate on the 2.4 GHz ISM band, similar to the NRF24L01. However, unlike the NRF24L01, extensive research has been conducted to ensure the reliability of communication over these channels. Nevertheless, both Wi-Fi and Bluetooth suffer from a limited range of 10 to 20 meters. As a result, these alternatives are unsuitable for communicating with the coach during rowing sessions.

In addition to communicating with the coach on the side of the water, the system also requires a means of communication between the various sensor nodes and the main module inside the boat. In this regard, WiFi presents a suitable option as it allows for a constant connection with multiple nodes while simultaneously transmitting data. With its high data rate, WiFi can be used to create a mesh network within the boat, connecting all the sensor nodes and transmitting data to the main module in real-time. Data from the main module can also be received and presented by other devices for the coxswain and rower on stroke.

# System architecture and components

The suggested system is shown as a flowchart in Figure 1, and it revolves around a single-board computer (SBC), which receives, processes, and delivers data to a wireless transceiver module. A number of sensor nodes communicate data to the SBC through WiFi, while the accelerometer and GPS module are attached to the SBC for direct data receipt. Displaying the data to the coach is done by a microcontroller that is attached to the other side of the transceiver module. The system is made to effectively gather, analyse, and transfer data for analysis and feedback.

![Flowchart of the complete project including future additions](/FlowChart.png)  
Figure 1: Flow chart of the different components in the proposed system.


## SBC

The OrangePi Zero 2 shown in Figure 2 is a powerful single-board computer (SBC) that provides a suitable platform for implementing the proposed system. It features a Quad-core ARM Cortex-A35 processor, 1 GB DDR3 memory and built-in wireless capabilities, making it a highly cost-effective and versatile option. Additionally, it has 26 GPIO pins, UART, SPI and I2C interfaces, which are crucial for connecting and controlling the various sensors and modules required for the system.

The decision to use the OrangePi Zero 2 instead of other popular SBCs, such as the Raspberry Pi, was due to availability issues caused by the global semiconductor shortage. Raspberry Pi's have become increasingly difficult to purchase due to supply chain disruptions, making them unsuitable for our project's needs. The OrangePi Zero 2 provides a viable alternative, with similar capabilities and a smaller form factor.

![OrangePi Zero 2](http://www.orangepi.org/img/computersAndMmicrocontrollers/Zero%202/Rectangle%20740.png)  
Figure 2: OrangePi Zero 2 SBC

## GPS

The GPS module shown in Figure 3 is an essential component of the proposed system as it enables the determination of the boat's precise location on the water. The Quectel L80-R GPS module was chosen for this application due to its high sensitivity, low power consumption and compact size. The L80-R uses advanced GPS technology to provide highly accurate positioning information in real-time, with a positional accuracy of up to 2.5 meters. The module can also support up to 66 channels and has a high update rate of up to 10 Hz, which makes it well-suited for fast-moving applications such as a rowing boat.

![GPS module used in the project](https://ae01.alicdn.com/kf/S4b5cb9b1b2e64269ac365f4e8f61cef2S/GPS-Module-with-Antenna-Quectel-L80-R-GNSS-Module-TTL-Serial-Port-GPS-Development-Board-NMEA0183.jpg)  
Figure 3: GPS module

The GPS module will also provide speed data to help the coach monitor the boat's pace. By keeping a consistent pace, rowers can conserve energy and achieve better overall performance. With the GPS module, the coach and coxswain can track the boat's speed in real-time and adjust rowing pace accordingly. This will help the team to improve their performance and achieve better results in competitions.


## Accelerometer

Figure 4 shows the MPU9250, it is a 9-axis motion tracking device that contains a 3-axis accelerometer, 3-axis gyroscope and 3-axis magnetometer. It offers high accuracy and stability for measuring motion, orientation and magnetic fields, making it a popular choice in various applications such as drones, robots and wearable devices.

![MPU9250 I²C development board](https://imgaz1.staticbg.com/thumb/large/oaupload/banggood/images/27/3F/5e88c701-0d11-4540-ad80-61f5e44ed197.JPG)  
Figure 4: MPU9250 board

The accelerometer component of the MPU9250 is capable of measuring acceleration in three axes, providing accurate data on movement and position. The gyroscope measures angular velocity and can detect rotational changes, while the magnetometer measures the magnetic field around the device. The combination of these sensors allows for accurate tracking of movements and orientation in 3D space. Additionally, the MPU9250 has an onboard digital motion processor (DMP) that can perform complex calculations and sensor fusion, reducing the computational load on the main microcontroller.

The accelerometer module is a crucial component of the proposed system. It provides the coach with an acceleration curve that can be analysed to determine different parts of the stroke and how efficiently they are executed. This novel tool allows coaches to monitor rowing performance more effectively and gain a better understanding of the acceleration curve to improve technique.


## Gyroscope

The gyroscope, in combination with the other sensors, enables the system to obtain essential information about the boat's heading, balance, as well as the position of the oar and the rotation of the blade. This information can be analysed by the coach to improve the rowing technique and optimize the performance of the boat. The gyroscope's ability to measure the angular velocity of the device provides crucial data for determining the boat's stability and changes in direction. Hence, the gyroscope plays a crucial role in providing valuable insights into the performance of the rowing team.


## Communication

For communication between the different sensor nodes and the main module inside the boat, the system utilizes the built-in wireless chip of the Orangepi Zero 2 v1.5 SBC, which offers a constant connection with different nodes and simultaneous communication. In addition, an NRF24L01 module is used for longer range communication with the coach, with its high data rate allowing for real-time data visualisation. This module is shown in Figure 5.

![NRF24L01 module with antenna](https://lastminuteengineers.b-cdn.net/wp-content/uploads/arduino/nRF24L01-PA-LNA-External-Antenna-Wireless-Transceiver-Module.jpg)  
Figure 5: NRF24L01 module

# Functionality

The main goal of this thesis is to improve upon already available performance monitoring systems, to do so it must first be able to accomplish the same as other available products. This chapter will discuss the functionality the developed performance monitor will need to be relevant in the world of rowing.


## Stroke rate

The stroke rate is a pivotal metric in rowing, representing the number of strokes performed per minute during rowing. While a lower stroke rate is generally associated with greater efficiency, a higher stroke rate can lead to increased boat speed. Accurately monitoring and tracking the stroke rate in real-time is of significant value for both training purposes and adhering to race plans.

As previously mentioned, the stroke rate is expressed as the number of strokes per minute. It can be computed using Formula 4.1, which calculates the stroke rate by dividing 60 (minutes) by the time it takes to do one full stroke.  

$Stroke Rate=60/(Stroke Time)$         **4.1**  

To measure the stroke rate with the primary node, the connected accelerometer is utilized. A selective low-pass filter is applied to specifically capture oscillations below two Hertz. This filtering technique ensures that the system can accurately capture stroke rates up to a maximum of 120 strokes per minute, which is more than sufficient for rowing applications.


## Speed

The boat speed is arguably the most important measurement simply because it is the only metric that decides which rower will win a race. Utilizing speed for training purposes comes with multiple problems and inaccuracies because there are three speeds to take into account to be able to relate the boat speed to the boats performance. The water speed, the air speed and the boat speed. These speeds need to be combined to determine the actual boat performance.

The current device will only measure the absolute boat speed, the measurements will come from the GPS module and will be translated to a rowing split using Formula 4.2.  

$Split=500/(kt*0.51444)$               **4.2**  

The GPS module provides boat speed measurements in knots, while the split is quantified in seconds required to row a distance of 500 meters. To give a rower an understandable metric, it is necessary to convert the seconds into minutes and seconds.


## Balance

The boats balance is a metric that is not usually shown in performance monitoring systems due to the fact it requires a stable way to mount a sensor. Because the primary node is mounted in the boat in a stable way, the balance of the boat can be measured. This data can be useful to correct errors in technique by correctly analysing the timing and the speed at which the boat becomes unbalanced. It is commonly known amongst rowing coaches that a stable boat is more efficient and also a lot more enjoyable to row in.

The balance will be measured using the acceleration data of the three axes combined with gyroscope data and magnetometer data to receive an accurate orientation matrix. The data is fused together using a Madgwick sensor fusion algorithm, a well known algorithm also used in flight computers to accurately stabilize drones. The algorithm will not be explained in this paper but is referenced for further reading.

The output is three Euler angels: pitch, roll and yaw. For measuring Balance in the rowing boat only roll will be used. Yaw will be used in other measurement applications that will be discussed further in another chapter.


## oar angle

Another metric that is not included in standard rowing performance monitors is the oar angle. There are three interesting angles of the oar which are evidently the three Euler angles: pitch, roll and yaw. Pitch is the angle the oar makes with the water surface, roll is the angle of the blade referenced to the water surface and yaw is the angle the oar makes in reference to the side of the boat.

The measurement of oar pitch is interesting because the blades can be seen as balancing sticks. The analogy can be made with a rope walker that uses a balancing stick to stay balanced on the rope. When the blades of one side of the rowing boat move up, the boat will fall to their side. When the blades move down, the boat will fall to the opposite side. It is important to keep the oar angle, with a reference to the flat top of the boat, as stable as possible to reduce roll in the boat. The stability of this angle can be used as a per rower performance metric.

The measurement of oar roll gives information about the feathering of the blade. For efficient rowing it is important that the blade is completely upright before it starts entering the water in the catch position, equally important is the blade being completely upright until it has fully emerged from the water in the finish position. In the recovery phase the blade is feathered as long as possible to reduce aerodynamic drag.

The measurement of oar yaw combined with the afore mentioned measurement of boat yaw can be used to calculate the length of a stroke using the stroke starting angle and the ending angle, the longer the stroke, the more time to apply force on the handle and the more energy a rower can give to the boat in one stroke. Combining the oar yaw with the oar pitch can be used to calculate slip and wash which are the angles at the beginning of the stroke where the blade is not yet submerged into the water or already emerged  from the water at the end of the stroke. Minimizing slip and wash is just as beneficial as elongating the stroke length.


## Timing

Timing is also extremely important for rowing efficiency, rowers that do exactly the same at the same time are generally faster. The main node will keep the exact time of every measurement and the oar sensor nodes will relay time information together with their measurements to keep the timing as accurate as possible. The real time of the main node is updated every time it starts up using the GPS. The oar sensor nodes will each receive the real time from the main node once every training session.


## Coach monitor

All this data is of no use if it cannot be instantly analysed by a coach. To communicate to the side of the water or to a following boat in the water, a 2.4 GHz transceiver module is placed in the main node and the coach monitor. The coach monitor also includes a microcontroller and a screen, to receive and display the captured data in real time.


## Cox and stroke monitor

The coxswain and stroke rower monitor are very similar to the coach monitor, also consisting of a microcontroller and a screen, but using the WiFi connection of the primary node to receive the captured data. The coxswain will evidently get a tailored view of the main technical data captured and the rower on stroke gets a more minimalist view with only the most important metrics like stroke rate and split.


# Implementation

To implement al these features into a working prototype the SBC is programmed with a python script. The script will receive and store all measurements in a .csv file for easy access and later analysis. This chapter will go over the basic functionality of the python code and the script to start it when the device is powered on. The full code can be found in Appendix A


## Setting the time and date

As mentioned before the time and date are set every time the device is turned on by connecting to GPS satellites and using the exact timestamp in the NMEA-protocol.  The python script uses serial communication to collect data from the Quectel L80-R GPS module. It reads a line and only acts if it is of the RMC (Recommended Minimum) format and the status is “A” for active. It will then extract the exact date, time and location from the message and convert the location to a time zone and the date and time to the correct value for that time zone. Finally it sets the time and time zone of the SBC to the correct value and ends the script.


## waiting for the training to start

For ease of use the main module can be mounted in the boat and used stand alone. In order to not be in the way of the athletes the device is mounted in the boat before the boat is carried to the water when the boat is in trestles. This means the data collection should not start immediately but wait until the boat has been upside down (the way it is carried on the shoulders) and right side up again (when the boat is in the water). This is done with the MPU9250 module. The module is connected to the I²C line of the SBC and using the Madgwick sensor fusion algorithm the received data is converted to a value for roll, pitch and yaw. The roll of the boat is 180° when it is upside down and 0° when it is lifted into the water. After this scenario is read by the sensor a variable boatInWater is set to true and the training session can be started.


## Training data collection

Before the program starts capturing data a csv file is created with the exact date and time as the name. The file is then opened and a first line is written that contains the name of all the columns. After this while the boat is in the water a script will run that reads the data from the MPU9250 module, computes and updates the roll, pitch and yaw values using the sensor fusion algorithm, reads the data from the GPS-queue for speed, longitude and latitude data, checks whether the GPS thread is finished to start it again and finally writes all the collected data to the csv file.


## Stopping the data collection

In the same script where the data is collected, the roll value of the boat is evaluated every loop to identify when the boat is being lifted out of the water. When this scenario is played the boatInWater value is reset to false and the data collection is stopped, the csv file is closed and the script ends. Finally the device shuts down to be powered back on for the next training session or to review and analyse the data.


# Replicating the device

This chapter will go in to all the necessary steps to replicate the main device. It is important to note that the device is still a prototype and this chapter is only for further development.


## Bill of materials

| Item	| Description	| Link |
|-------|:-----------:|------|
| SBC	| OrangePi Zero 2 |	a.aliexpress.com/_EzkrPc9 |
| GPS module |	Quectel L80-R |	a.aliexpress.com/_ExDRfdP |
| Motion sensor |	MPU9250 |	a.aliexpress.com/_Eywt67R |
| Enclosure	| 3D printed enclosure | |
| Mount | 3D printed mount| |


# Results

The results are promising and the captured data is extremely interesting for the UCLL Sharks rowing coaches to review. At this point the data is still very cryptic and needs a lot of post-processing work to be made understandable. This chapter will gloss over the working prototype, explain how it has been working and discuss the future work necessary to bring this project to the next level.


## Working prototype

The only prototype that has been tested thoroughly is the main module explained in the implementation chapter. This prototype was brought to the UCLL Sharks yearly training camp in Nantes and tested on the river Erdre. The device worked as expected and the analysis of the captured data corresponded nicely to the data provided by the already available NK SpeedCoach. The coaches were thrilled about the results and the future possibilities of the device.


## Future work

The functionality chapter of this paper has provided an overview of the proposed system, highlighting its various components and their intended functions. However, it is important to note that many aspects discussed in this chapter are yet to be developed and tested. While the primary and rudimentary functions have been tested successfully, further work is required to enhance the device and expand the sensor ecosystem in the rowing boat.

One area of future work involves the improvement of the existing system. This includes refining the data collection process and optimizing algorithms for data analysis. This can be done by looking at newer sensor modules for more accurate data, improving the program for data collection to run faster and thus increase the amount of data points per second and looking for newer sensor fusion algorithms to improve the accuracy of the collected orientation data.

Future work can also involve adding new functionality to the system. This can be done by implementing the features discussed is the functionality chapter, but may also involve developing algorithms to detect and analyse specific rowing techniques or patterns and providing more comprehensive feedback to coaches and rowers for technique refinement and performance enhancement.


# Conclusion

In conclusion, while this thesis has laid the groundwork for the development of a rowing performance monitoring system, there is still significant potential for further advancements. The future work outlined here serves as a roadmap for future researchers and developers to build upon the existing foundation, ultimately contributing to the continued evolution and innovation in the field of rowing performance analysis.

 
 
 

 
 
 
 
