# Gyro Mouse

Gyro_Mouse is an Arduino based system I've made as a first project. this system controls windows cursor according to the system momentary velocity.

## Getting Started

First power on the arduino system, pair windows with bluetooth device. then run **`mouse_server.py`** after bluetooth scan the terminal will prompt the user to choose bluetooth COM port from a list. input the right COM and the server will start receiving data from the arduino and move the cursor accordingly.
when the arduino gets an interrupt signal from the buttons, it send a uniqe value to the server. the server then issue mouse event.

### Prerequisites

Circuit components:
- Arduino UNO
- ZS-040 HC05 Module
- 2 x GY-521 MPU6050 Module
- 2 x Button

### Installing
the following block diagram describe the circuit
![Schem Img](https://github.com/polzbit/Gyro_Mouse/raw/master/resource/final_proj_schem.png)
the following image describe the connection
![Con Img](https://github.com/polzbit/Gyro_Mouse/raw/master/resource/b.png)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


