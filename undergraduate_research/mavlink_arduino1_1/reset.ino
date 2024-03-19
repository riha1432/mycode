void Arduino_Reset(){
  MQ9_setup();
  Co2_setup();
  
  Serial2.begin(57600);
  Serial.begin(57600);
  Serial3.begin(9600);
  
//  pms.passiveMode(); 
  
   // 아두이노 시리얼 모니터 체크용
  
  for(int send_reset = 0; send_reset<=Send_MAX; send_reset++){
    Server_Send_byte[send_reset] = 0x00;
  }
  Server_Send_byte[0] = 'S';
  Server_Send_byte[1] = 'T';
  Server_Send_byte[Send_MAX - 2] = 'N';
  Server_Send_byte[Send_MAX - 1] = 'E';

  Mav_Message[0] = MAVLINK_MSG_ID_ATTITUDE; // 30
  Mav_Message[1] = MAVLINK_MSG_ID_LOCAL_POSITION_NED; // 32
  Mav_Message[2] = MAVLINK_MSG_ID_GLOBAL_POSITION_INT; // 33
  Mav_Message[3] = MAVLINK_MSG_ID_RC_CHANNELS; // 65
  Mav_Message[4] = MAVLINK_MSG_ID_VFR_HUD; // 74
  Mav_Message[5] = MAVLINK_MSG_ID_BATTERY_STATUS; // 147
  Mav_Message[6] = MAVLINK_MSG_ID_COMMAND_ACK; // 77
  Mav_Message[7] = MAVLINK_MSG_ID_SET_MODE; // 11
}
