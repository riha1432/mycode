bool led = 0;
unsigned long radio_time;


void Radio_Send(){
  if(millis() - radio_time> 500){
    byte hammin = 0;
//    for(int i=1;i<Send_MAX-2;i++) hammin = hammin^Server_Send_byte[i];
//    Server_Send_byte[Send_MAX - 2] = hammin;
//      for(int i=0;i<Send_MAX;i++){
//        Serial.print(Server_Send_byte[i]);
//        Serial.print(" ");
//      }
//      Serial.print("35 : ");
//      Serial.print(Server_Send_byte[35]);
//      Serial.println();
      
      for(int i=0;i<Send_MAX;i++){
        Serial.write(Server_Send_byte[i]);
      }      
    led = led^1;
    radio_time = millis();
  }
  digitalWrite(LED13, led);
}
