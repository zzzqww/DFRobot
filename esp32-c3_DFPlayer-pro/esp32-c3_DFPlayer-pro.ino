/*!
 *@file play.ino
 *@brief Music Playing Example Program
 *@details  Experimental phenomenon: control MP3 play music, obtain song information
 *@copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 *@license     The MIT license (MIT)
 *@author [fengli](li.feng@dfrobot.com)
 *@version  V1.1
 *@date  2021-10-15
 *@url https://github.com/DFRobot/DFRobot_DF1201S
*/

//#include <Arduino.h>
#include <DFRobot_DF1201S.h>



DFRobot_DF1201S DF1201S;
void setup(void){
  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, /*rx =*/0, /*tx =*/1);
  while(!DF1201S.begin(Serial1)){
    Serial.println("Initialization failed, please check wiring!");
    delay(1000);
  }
  /*set the volume to 20*/
  DF1201S.setVol(/*VOL = */20);
  Serial.print("VOL:");
  /*get volume*/
  Serial.println(DF1201S.getVol());
  /*enter music mode*/
  DF1201S.switchFunction(DF1201S.MUSIC);
  /*Wait for the beep to finish playing*/
  delay(2000);
  /*Set the playback mode to loop all*/
  DF1201S.setPlayMode(DF1201S.ALLCYCLE);
  Serial.print("PlayMode:");
  /*get play mode*/
  Serial.println(DF1201S.getPlayMode());


  //Set baud rate to 115200(Need to power off and restart, power-down save)
  //DF1201S.setBaudRate(115200);
  //Turn on indicator LED (Power-down save)
  //DF1201S.setLED(true);
  //Turn on the prompt tone (Power-down save) 
  //DF1201S.setPrompt(true);
  //Enable amplifier chip 
  //DF1201S.enableAMP();
  //Disable amplifier chip 
  //DF1201S.disableAMP();
}

void loop(){
  Serial.println("Start playing");
  /*Start playing*/
  DF1201S.start();
  delay(3000);
  Serial.println("Pause");
  /*Pause*/
  DF1201S.pause();
  delay(3000);
  Serial.println("Next");
  /*Play the next song*/
  DF1201S.next();
  delay(3000);
  Serial.println("Previous");
  /*Play the previous song*/
  DF1201S.last();
  delay(3000);
  Serial.println("Start playing");
  //Fast forward 10S
  DF1201S.fastForward(/*FF = */10);
  //Fast Rewind 10S
  //DF1201S.fastReverse(/*FR = */10);
  //Start the song from the 10th second 
  //DF1201S.setPlayTime(/*Play Time = */10);

  Serial.print("File number:");
  //Get file number
  Serial.println(DF1201S.getCurFileNumber());

  Serial.print("The number of files available to play:");
  //The number of files available to play
  Serial.println(DF1201S.getTotalFile());

  Serial.print("The time length the current song has played:");
  //Get the time length the current song has played 
  Serial.println(DF1201S.getCurTime());

  Serial.print("The total length of the currently-playing song: ");
  //Get the total length of the currently-playing song 
  Serial.println(DF1201S.getTotalTime());
  Serial.print("The name of the currently-playing file: ");
  //Get the name of the playing file 
  Serial.println(DF1201S.getFileName());
  delay(3000);
  //Play the file No.1, the numbers are arranged according to the sequence of the files copied into the U-disk 
  DF1201S.playFileNum(/*File Number = */1);
  //Play the test.mp3 file in test folder 
  //DF1201S.playSpecFile("/test/test.mp3");

  while(1);
  /*Delete the currently-playing file */
  //DF1201S.delCurFile();
}