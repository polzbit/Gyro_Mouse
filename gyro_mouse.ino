#include <Wire.h>
#include "SoftwareSerial.h"

// BT pins
#define BT_RX 4
#define BT_TX 5
// Buttons Pins
#define BTN_R 2
#define BTN_L 3
// BT object
SoftwareSerial bt(BT_RX, BT_TX);  // RX | TX
// MPU variables
const int MPU = 0x68;             // First MPU6050 I2C address
const int MPU2 = 0x69;            // Second MPU6050 I2C address
float gx, gy;

/* Setup Function */
void setup() {
  bt.flush();
  delay(500);
  /* Initialize Bluetooth Serial */
  bt.begin(9600);
  Wire.begin();                      // Initialize comunication
  /* Initialize First MPU */
  Wire.beginTransmission(MPU);       // Start communication with MPU6050, MPU=0x68
  Wire.write(0x6B);                  // Talk to the register 6B
  Wire.write(0x00);                  // Make reset - place a 0 into the 6B register
  Wire.endTransmission(true);        //end the transmission
  /* Initialize Second MPU */
  Wire.beginTransmission(MPU2);       // Start communication with MPU6050, MPU2=0x69
  Wire.write(0x6B);                  // Talk to the register 6B
  Wire.write(0x00);                  // Make reset - place a 0 into the 6B register
  Wire.endTransmission(true);        //end the transmission
  /* Initialize Interrupt Pins */
  attachInterrupt(digitalPinToInterrupt(BTN_R),right_press,RISING);  
  attachInterrupt(digitalPinToInterrupt(BTN_L),left_press,RISING);  
  delay(100);
}
/* Main Loop Function */
void loop() {
  // === Read gyroscope data === //
  gx = get_gyro(MPU);
  gy = get_gyro(MPU2);
  
  // === Bluetooth transmission === //
  bt_send(gx, gy);
}
/* INTERRUPT 0 Function */
void right_press() {
  bt.println("right");
}
/* INTERRUPT 1 Function */
void left_press() {
  bt.println("left");
}
/* Bluetooth Transmission Function */
void bt_send(float gx, float gy) {
  if(bt.available()) {
    bt_send(gx, gy);
  }
  else {
    bt.print(gx);
    bt.print("|");
    bt.println(gy);
  }
}
/* Get Data From Gyro Register */
float get_gyro(int i2c_add) {
    Wire.beginTransmission(i2c_add);
     // Gyro Z axis data first register at address 0x47
    Wire.write(0x47); 
    Wire.endTransmission(false);
     // get 2 registers total
     // each axis value stored in 2 registers
    Wire.requestFrom(i2c_add, 2, true); 
     // For a 250deg/s range we have to divide first 
     // the raw value by 131.0, according to the datasheet
    float GyroZ = (Wire.read() << 8 | Wire.read()) / 131.0;
    GyroZ = GyroZ - 0.79; // GyroErrorZ ~ (-0.8)
    return GyroZ;
}
