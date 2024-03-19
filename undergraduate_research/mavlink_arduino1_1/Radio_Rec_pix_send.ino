
int32_t strint(uint8_t *Byte, int *Start){
  int16_t inter = 0;
  bool Negative = 0;
  if(Byte[*Start] == '-'){
    (*Start)++;
    Negative = 1;
  }
  while(Byte[*Start] >='0' && Byte[*Start] <='9'){
    inter *= 10;
    inter += Byte[*Start] - 48;
    (*Start)++;
  }
  if(inter > 100){
    inter = 100;
  }
  return Negative==0?inter:-inter;
}

int Pos_X, Pos_Y = 0, Pos_Z = 0;
void radio_Rec_pix_send(){
  char Radio_Serial;
  static uint8_t Rec_index = 0;
  static bool commend = 0;
  
  while(Serial.available()){
    Radio_Serial = Serial.read();
    if(Radio_Serial == 'S') Rec_index = 0;
    else if(Radio_Serial == 'E') commend = 1;
    Server_Rece_byte[Rec_index] = Radio_Serial;
    Rec_index++;
    if(Rec_index > Receive_MAX){
      Rec_index = Receive_MAX;
    }
  }

  if(commend){
    commend = 0;
    if(Server_Rece_byte[1] == 'O'){ // 시동 on
      mavlink_msg_command_long_pack(1, 0xBE, &msg, 1, 1, MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0);
      mav_len = mavlink_msg_to_send_buffer(buf, &msg); 
      Serial2.write(buf, mav_len);
    }
    else if(Server_Rece_byte[1] == 'F'){ // 시동 off
      mavlink_msg_command_long_pack(1, 0xBE, &msg, 1, 1, MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0);
      mav_len = mavlink_msg_to_send_buffer(buf, &msg); 
      Serial2.write(buf, mav_len);
    }
    else if(Server_Rece_byte[1] == 'M'){ // 드론 모드 1 : guided, 2 : home, 3 : land 
      if(Server_Rece_byte[2] == '1'){
        mavlink_msg_set_mode_pack(1, 0xBE, &msg, 1, 1, 4); // gui
      }
      else if(Server_Rece_byte[2] == '2'){
        mavlink_msg_set_mode_pack(1, 0xBE, &msg, 1, 1, 6); // home
      }
      else if(Server_Rece_byte[2] == '3'){
        mavlink_msg_set_mode_pack(1, 0xBE, &msg, 1, 1, 9); // land
      }
      mav_len = mavlink_msg_to_send_buffer(buf, &msg); 
      Serial2.write(buf, mav_len);
    }
    else if(Server_Rece_byte[1] == 'T'){ // 이륙
      Pos_Z = 5;
      mavlink_msg_command_long_pack(1,0xBE, &msg, 1, 1, MAV_CMD_NAV_TAKEOFF,0, 0,0,0,0,0,0,Pos_Z);
      mav_len = mavlink_msg_to_send_buffer(buf, &msg); 
      Serial2.write(buf, mav_len);
    }
    else if(Server_Rece_byte[1] == 'G' && Server_Rece_byte[2] == '1'){ // 이동 명령어
      for(int Start=0;Start<20;Start++){
        if(Server_Rece_byte[Start] == 'X' || Server_Rece_byte[Start] == 'x'){
          Start++;
          Pos_X = strint(Server_Rece_byte, &Start);
        }
        if(Server_Rece_byte[Start] == 'Y' || Server_Rece_byte[Start] == 'y'){
          Start++;
          Pos_Y = strint(Server_Rece_byte, &Start);
        }
        if(Server_Rece_byte[Start] == 'Z' || Server_Rece_byte[Start] == 'z'){
          Start++;
          Pos_Z = strint(Server_Rece_byte, &Start);
        }
      }
      
      mavlink_msg_set_position_target_local_ned_pack(1, 0xBE, &msg, millis(), 0, 0, MAV_FRAME_LOCAL_NED, 0b110111111000, Pos_X,Pos_Y, -Pos_Z, 0,0,0, 0,0,0, 0,0);
      mav_len =  mavlink_msg_to_send_buffer(buf, &msg);
      Serial2.write(buf, mav_len);
    }
    else if(Server_Rece_byte[1] == 'R'){
      MQ9_setup();
      Co2_setup();
    }
    
    uint8_t ack = 0;
    while(Server_Rece_byte[ack] != 'D'){
      ack++;
    }
    if(Server_Rece_byte[ack] == 'D'){
      Server_Send_byte[35] = Server_Rece_byte[ack+1];
    }
    
  }
}
