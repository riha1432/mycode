int measurePin = 0; //Connect dust sensor to Arduino A0 pin
int ledPower = 3;   //Connect 3 led driver pins of dust sensor to Arduino D2

int samplingTime = 280;
int deltaTime = 40;
int sleepTime = 9680;

float voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;

#define         Board                   ("Arduino UNO")
#define         Pin                     (PA1)  //Analog input 4 of your arduino
/***********************Software Related Macros************************************/
#define         Type                    ("MQ-9") //MQ9
#define         Voltage_Resolution      (3.3)//5v
#define         ADC_Bit_Resolution      (12) // For arduino UNO/MEGA/NANO
#define         RatioMQ9CleanAir        (9.9) //RS / R0 = 60 ppm 
/*****************************Globals***********************************************/
//Declare Sensor
MQUnifiedsensor MQ9(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin, Type);
//----------------------------
CO2Sensor co2Sensor(PA0, 0.6, 30);

void MQ9_setup(){
  MQ9.setRegressionMethod(1);
  MQ9.init(); 
  float calcR0 = 0;
  for(int i = 1; i<=10; i ++)
  {
    MQ9.update(); // Update data, the arduino will be read the voltage on the analog pin
    calcR0 += MQ9.calibrate(RatioMQ9CleanAir);
  }
  MQ9.setR0(calcR0/10);
}
void MQ9_sensor(){
  MQ9.update();
  /*
  Exponential regression:
  GAS     | a      | b
  LPG     | 1000.5 | -2.186
  CH4     | 4269.6 | -2.648
  CO      | 599.65 | -2.244
  */
  MQ9.setA(1000.5); MQ9.setB(-2.186); // Configurate the ecuation values to get LPG concentration
  float LPG = MQ9.readSensor(); // Sensor will read PPM concentration using the model and a and b values setted before or in the setup
  MQ9.setA(4269.6); MQ9.setB(-2.648); // Configurate the ecuation values to get LPG concentration
  float CH4 = MQ9.readSensor(); // Sensor will read PPM concentration using the model and a and b values setted before or in the setup
  MQ9.setA(599.65); MQ9.setB(-2.244); // Configurate the ecuation values to get LPG concentration
  float CO = MQ9.readSensor();
  int16_t ILPG = (LPG * 10);
  int16_t ICH4 = (CH4 * 10);
  int16_t ICO = (CO * 10);
  
//  Serial.print(" ILPG ");Serial.print(ILPG);
//  Serial.print(" ICH4 ");Serial.print(ICH4);
//  Serial.print(" ICO ");Serial.println(ICO);
  
  Server_Send_byte[22] = ILPG>>8;
  Server_Send_byte[23] = ILPG;
  Server_Send_byte[24] = ICH4>>8;
  Server_Send_byte[25] = ICH4;
  Server_Send_byte[26] = ICO>>8;
  Server_Send_byte[27] = ICO;
}

void Co2_setup(){
  co2Sensor.calibrate();
}

void Co2_sensor(){
  int val = co2Sensor.read();

  Server_Send_byte[28] = val>>8;
  Server_Send_byte[29] = val;
  
//  Serial.print(" co2 ");Serial.println(val);
}

void mics4514_Sensor(){
//  int vred_value= analogRead(PA4);
  int vnox_value = analogRead(PA5);
  float no2_voltage = (vnox_value * 3.3) / 4095; // NO2 센서 전압 읽기
//  float co_voltage = (vred_value * 3.3) / 4095; // CO 센서 전압 읽기


  float vout_no2 = vnox_value / 409.2;
  float Rs_n02 = 22000 / ((3.3 / vout_no2) -1);
  uint16_t NO2_ppm = (0.000008 * Rs_n02 - 0.0194) * 100; // NO2 농도 범위 제한
  
  Server_Send_byte[30] = NO2_ppm>>8;
  Server_Send_byte[31] = NO2_ppm;
//  
//  Serial.print("NO2 : ");
//  Serial.print(vnox_value);
//  Serial.print("     NO2 v : ");
//  Serial.print(no2_voltage);
//  Serial.print(" v      ");
//  Serial.print("NO2 Concentration: ");
//  Serial.print((0.000008 * Rs_n02 - 0.0194));
//  Serial.println(" ppm");
  
//  RS = (3.3 - co_voltage) * 10000.0 / co_voltage; // 센서 저항 계산
//  ratio = RS / 100000.0; // RS/R0 비율 계산
//  float CO_ppm = pow(ratio, -1.179) / 4.385; // CO 농도 계산
//  CO_ppm = constrain(CO_ppm, 1.0, 1000.0); // CO 농도 범위 제한

//  float vout_co = vred_value /409.2;
//  float Rs_co = 47000 / ((3.3/vout_co) -1);
//  float CO_ppm = 911.19 * pow(2.71828, (-8.577*Rs_co/100000));
//  
//  Serial.print("CO Concentration: ");
//  Serial.print(CO_ppm);
//  Serial.println(" ppm");
}

void PM(){
  if (pms.read(data))
  {
    Server_Send_byte[32] = data.PM_AE_UG_1_0;
    Server_Send_byte[33] = data.PM_AE_UG_2_5;
    Server_Send_byte[34] = data.PM_AE_UG_10_0;
    #if Data_Debug == 1
      Serial.println(data.PM_AE_UG_1_0);
      Serial.println(data.PM_AE_UG_2_5);
      Serial.println(data.PM_AE_UG_10_0);
    #endif 
  }
}
