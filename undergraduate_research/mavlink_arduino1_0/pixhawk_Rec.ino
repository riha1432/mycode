uint8_t system_id = 1;
uint8_t component_id = 1;
uint8_t target_sys = 0;
uint8_t target_component = 0;

void Pixhawk_Rece(){
  heartbeat_pack();
  
  while(Serial2.available() > 0){
    uint8_t pix = Serial2.read();
    if(mavlink_parse_char(MAVLINK_COMM_0, pix, &msg, &Status)){
//      Serial.println(msg.msgid);
      switch(msg.msgid){
        case MAVLINK_MSG_ID_ATTITUDE:{
//          mavlink_attitude_t attitude;
//          mavlink_msg_attitude_decode(&msg, &attitude);
        }break;
        case MAVLINK_MSG_ID_LOCAL_POSITION_NED:{
          mavlink_local_position_ned_t local_position;
          mavlink_msg_local_position_ned_decode(&msg, &local_position);
          int16_t x = (int16_t)(local_position.x * 10);
          int16_t y = (int16_t)(local_position.y * 10);
          int16_t z = (int16_t)(local_position.z * 10);
          Server_Send_byte[2] = x >> 8;
          Server_Send_byte[3] = x;
          Server_Send_byte[4] = y >> 8;
          Server_Send_byte[5] = y;
          Server_Send_byte[6] = z >> 8;
          Server_Send_byte[7] = z;
        }break;
        case MAVLINK_MSG_ID_GLOBAL_POSITION_INT:{
          mavlink_global_position_int_t global_position;
          mavlink_msg_global_position_int_decode(&msg, &global_position);
          Server_Send_byte[8] = global_position.lat>>24;
          Server_Send_byte[9] = global_position.lat>>16;
          Server_Send_byte[10] = global_position.lat>>8;
          Server_Send_byte[11] = global_position.lat;
          Server_Send_byte[12] = global_position.lon>>24;
          Server_Send_byte[13] = global_position.lon>>16;
          Server_Send_byte[14] = global_position.lon>>8;
          Server_Send_byte[15] = global_position.lon;
          Server_Send_byte[16] = global_position.alt>>24;
          Server_Send_byte[17] = global_position.alt>>16;
          Server_Send_byte[18] = global_position.alt>>8;
          Server_Send_byte[19] = global_position.alt;
        }break;
        case MAVLINK_MSG_ID_RC_CHANNELS:{
//          mavlink_rc_channels_t rc_channel;
//          mavlink_msg_rc_channels_decode(&msg, &rc_channel);
        }break;
        case MAVLINK_MSG_ID_VFR_HUD:{
//          mavlink_vfr_hud_t vfr_hud;
//          mavlink_msg_vfr_hud_decode(&msg, &vfr_hud);
        }break;
        case MAVLINK_MSG_ID_BATTERY_STATUS:{
          mavlink_battery_status_t bettery;
          mavlink_msg_battery_status_decode(&msg,&bettery);
          Server_Send_byte[20] = bettery.voltages[0]>>8;
          Server_Send_byte[21] = bettery.voltages[0];
        }break;
        case MAVLINK_MSG_ID_COMMAND_ACK:{
//          mavlink_command_ack_t vspeed;
//          mavlink_msg_command_ack_decode(&msg, &vspeed);
//          Server_Send_byte[42] = vspeed.result;
        }break;
        case MAVLINK_MSG_ID_SET_MODE:{
//          mavlink_set_mode_t mode;
//          mavlink_msg_set_mode_decode(&msg, &mode);
//          Server_Send_byte[41] = mode.custom_mode;
        }break;
      }
    }
  }
}

unsigned long previousMillisMAVLink;
int num_hbs_pasados;
void heartbeat_pack(){  
  unsigned long currentMillisMAVLink = millis();
  if (currentMillisMAVLink - previousMillisMAVLink >= 100) {
    previousMillisMAVLink = currentMillisMAVLink;
    uint8_t base_mode = MAV_MODE_FLAG_SAFETY_ARMED | MAV_MODE_FLAG_CUSTOM_MODE_ENABLED;
    mavlink_msg_heartbeat_pack(system_id, component_id, &msg, MAV_TYPE_QUADROTOR, MAV_AUTOPILOT_GENERIC, base_mode, 0, MAV_STATE_STANDBY);
    mav_len = mavlink_msg_to_send_buffer(buf, &msg);
    Serial2.write(buf, mav_len);
//    num_hbs_pasados++;
//    if(num_hbs_pasados>=5){
//      Request_message();
//      num_hbs_pasados = 0;
//    } 
    Request_message();
  }
}

inline void Request_message(){
  const int  maxStreams = 2;
  const uint8_t MAVStreams[maxStreams] = {MAV_DATA_STREAM_ALL,MAV_DATA_STREAM_POSITION};
  const uint16_t MAVRates[maxStreams] = {0x05,0x0F};
    
  for (int i=0; i < maxStreams; i++) {
    mavlink_msg_request_data_stream_pack(1, 100, &msg, target_sys, target_component, MAVStreams[i], MAVRates[i], 1);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    Serial2.write(buf, len);
  }
  
//  for(int request = 0; request<Mav_Message_MAX; request++){
//    mavlink_msg_command_long_pack(system_id, component_id, &msg, target_sys, target_component, MAV_CMD_REQUEST_MESSAGE, 0, Mav_Message[request], 0,0,0,0,0,0);
//    mav_len = mavlink_msg_to_send_buffer(buf, &msg);
//    Serial2.write(buf, mav_len);
//    
//    while(Serial2.available() > 0){
//      uint8_t pix = Serial2.read();
//      if(mavlink_parse_char(MAVLINK_COMM_0, pix, &msg, &Status)){
//        Serial.println(msg.msgid);
//      }
//    }
//  }
//  for(int request = 0; request<Mav_Message_MAX; request++){
//    mavlink_msg_command_long_pack(system_id, component_id, &msg, target_sys, target_component, MAV_CMD_REQUEST_MESSAGE, 0, 244, 32,0,0,0,0,0);
//    mav_len = mavlink_msg_to_send_buffer(buf, &msg);
//    Serial2.write(buf, mav_len);
//    
//    while(Serial2.available() > 0){
//      uint8_t pix = Serial2.read();
//      if(mavlink_parse_char(MAVLINK_COMM_0, pix, &msg, &Status)){
//        Serial.println(msg.msgid);
//      }
//    }
//  }
}
