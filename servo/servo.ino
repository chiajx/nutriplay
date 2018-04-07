#include <Servo.h>;

const int buttonPin = 8; // button pin
const int servoPin = 3; // servo pin
int counter = 0; // variable to store counter, set to zero
int buttonState;
int prevButtonState = 0; 
int initialAngle = 0;
int angleToGetTo = 79;
int delayV=30;

Servo servo;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP); // set push button pin to be an input
  servo.attach(servoPin);
  servo.write(angleToGetTo);

}

void loop() {

  buttonState = digitalRead(buttonPin);

  // new code
  if (buttonState == LOW && prevButtonState == 0) // button is pressed in
    
    for (int i=initialAngle; i < angleToGetTo; i++) {
      servo.write(i);
      delay(delayV);

      prevButtonState = 1;
    }

  else if (buttonState == HIGH && prevButtonState == 1) {
    for (int i=angleToGetTo; i> initialAngle; i--){
     servo.write(i);
     delay(delayV);

     prevButtonState = 0;
    }
  }



//  if (buttonState == LOW && prevButtonState == 1) 
//  {
//    for(int i=0; i<angleToGetTo; i++){
//      servo.write (i);
//      delay(delayV);
//      //Serial.print(i);
//    }

//  }
//  else{
//    servo.write(0);
//    //for (int i=angleToGetTo; i>0; i--){
//     //servo.write(i);
//     //delay(delayV);
//    //}
//  }
   
   Serial.println(buttonState);
   
}
