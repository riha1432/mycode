#include "c_library_v2-master/common/mavlink.h"
#include "math.h"
#include "CO2Sensor.h"
#include <MQUnifiedsensor.h>

#define LED13 PB3
#define LED14 PB4
#define Receive_MAX 45
#define Send_MAX 45
#define Mav_Message_MAX 8

#include "PMS.h"
PMS pms(Serial3);
PMS::DATA data;

uint8_t Server_Send_byte[Send_MAX];
uint8_t Server_Rece_byte[Receive_MAX];
uint16_t Mav_Message[Mav_Message_MAX];

mavlink_message_t msg;
mavlink_status_t Status;
uint8_t buf[MAVLINK_MAX_PACKET_LEN];
uint16_t mav_len;
uint8_t Ack = 0;

int32_t strint(uint8_t *, int *);

void setup() {
  afio_cfg_debug_ports(AFIO_DEBUG_SW_ONLY);
  pinMode(LED13,OUTPUT); 
  pinMode(LED14,OUTPUT);
  
  digitalWrite(LED14, HIGH);
  digitalWrite(LED13, HIGH);

  delay(20000);
  Arduino_Reset();
  
  digitalWrite(LED14, LOW);
  digitalWrite(LED13, LOW);
  
  while(!(pms.read(data)));
  Serial.println("start");

}
long ti;
void loop() {
  Pixhawk_Rece();
  MQ9_sensor();
  Co2_sensor();
  PM();
  mics4514_Sensor();
  Radio_Send();
  radio_Rec_pix_send();
}
