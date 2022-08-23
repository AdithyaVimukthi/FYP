#include <Servo.h>

Servo servo_elbow;
Servo servo_shoulder;

String cmd;

void setup() {
  servo_elbow.attach(9);
  servo_shoulder.attach(10);
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  while (Serial.available() == 0) {
  }

  cmd = Serial.readStringUntil('\r');

  int index = cmd.indexOf('_');
  int len = cmd.length();

  String angle_elbow = cmd.substring(0, index);
  String angle_shoulder = cmd.substring(index + 1, len);

  servo_elbow.write(angle_elbow.toInt());
  servo_shoulder.write(angle_shoulder.toInt());

  Serial.print(angle_elbow.toInt());
  Serial.print("\t");
  Serial.print(angle_shoulder.toInt());
  Serial.print('\n');
  /*if (cmd == "ON") {
    digitalWrite(LED_BUILTIN, HIGH);
    }
    if (cmd == "OFF") {
    digitalWrite(LED_BUILTIN, LOW);
    }*/
}
