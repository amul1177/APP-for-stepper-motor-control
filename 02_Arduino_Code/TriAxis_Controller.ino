#include <WiFi.h>
#include <BluetoothSerial.h>
#include <AccelStepper.h>
#include <ArduinoJson.h>

// Motor pin definitions
#define X_STEP_PIN 2
#define X_DIR_PIN 3
#define Y_STEP_PIN 4
#define Y_DIR_PIN 5
#define Z_STEP_PIN 6
#define Z_DIR_PIN 7
#define ENABLE_PIN 8

// Emergency stop and limit switches
#define EMERGENCY_STOP_PIN 9
#define X_LIMIT_PIN 10
#define Y_LIMIT_PIN 11
#define Z_LIMIT_PIN 12

// Status LED
#define STATUS_LED_PIN 13

// WiFi credentials
const char* ssid = "TriAxis_Controller";
const char* password = "APEX2024";

// Create stepper motor objects
AccelStepper stepperX(AccelStepper::DRIVER, X_STEP_PIN, X_DIR_PIN);
AccelStepper stepperY(AccelStepper::DRIVER, Y_STEP_PIN, Y_DIR_PIN);
AccelStepper stepperZ(AccelStepper::DRIVER, Z_STEP_PIN, Z_DIR_PIN);

// Bluetooth and WiFi objects
BluetoothSerial SerialBT;
WiFiServer server(80);

// System variables
bool emergencyStop = false;
bool bluetoothMode = true;
long motorPositions[3] = {0, 0, 0}; // X, Y, Z positions
int motorSpeeds[3] = {1000, 1000, 1000}; // Default speeds
bool motorsEnabled = false;

void setup() {
  Serial.begin(115200);
  
  // Initialize pins
  pinMode(ENABLE_PIN, OUTPUT);
  pinMode(EMERGENCY_STOP_PIN, INPUT_PULLUP);
  pinMode(X_LIMIT_PIN, INPUT_PULLUP);
  pinMode(Y_LIMIT_PIN, INPUT_PULLUP);
  pinMode(Z_LIMIT_PIN, INPUT_PULLUP);
  pinMode(STATUS_LED_PIN, OUTPUT);
  
  // Disable motors initially
  digitalWrite(ENABLE_PIN, HIGH);
  digitalWrite(STATUS_LED_PIN, LOW);
  
  // Configure stepper motors
  stepperX.setMaxSpeed(2000);
  stepperX.setAcceleration(1000);
  stepperY.setMaxSpeed(2000);
  stepperY.setAcceleration(1000);
  stepperZ.setMaxSpeed(2000);
  stepperZ.setAcceleration(1000);
  
  // Initialize Bluetooth
  SerialBT.begin("TriAxis_Motor_Hub");
  Serial.println("Bluetooth initialized: TriAxis_Motor_Hub");
  
  // Initialize WiFi Access Point
  WiFi.softAP(ssid, password);
  server.begin();
  Serial.println("WiFi AP started: " + String(ssid));
  Serial.println("IP Address: " + WiFi.softAPIP().toString());
  
  // Startup sequence
  blinkStatusLED(3);
  Serial.println("TriAxis Controller Ready - APEX PRECISION MECHATRONIX");
}

void loop() {
  // Check emergency stop
  if (digitalRead(EMERGENCY_STOP_PIN) == LOW) {
    emergencyStop = true;
    disableMotors();
    Serial.println("EMERGENCY STOP ACTIVATED!");
  }
  
  // Handle Bluetooth communication
  if (SerialBT.available()) {
    String command = SerialBT.readString();
    processCommand(command, "BT");
  }
  
  // Handle WiFi communication
  WiFiClient client = server.available();
  if (client) {
    String request = "";
    while (client.connected() && client.available()) {
      request += client.readString();
    }
    if (request.length() > 0) {
      processCommand(request, "WiFi");
      sendWiFiResponse(client);
    }
    client.stop();
  }
  
  // Run motors if enabled and not in emergency stop
  if (motorsEnabled && !emergencyStop) {
    stepperX.run();
    stepperY.run();
    stepperZ.run();
    digitalWrite(STATUS_LED_PIN, HIGH);
  } else {
    digitalWrite(STATUS_LED_PIN, LOW);
  }
  
  // Check limit switches
  checkLimitSwitches();
  
  delay(1);
}

void processCommand(String command, String source) {
  DynamicJsonDocument doc(1024);
  DeserializationError error = deserializeJson(doc, command);
  
  if (error) {
    Serial.println("JSON parsing failed: " + String(error.c_str()));
    return;
  }
  
  String action = doc["action"];
  
  if (action == "connect") {
    handleConnect(source);
  }
  else if (action == "move") {
    handleMove(doc);
  }
  else if (action == "setSpeed") {
    handleSetSpeed(doc);
  }
  else if (action == "home") {
    handleHome();
  }
  else if (action == "stop") {
    handleStop();
  }
  else if (action == "enable") {
    handleEnable(doc["state"]);
  }
  else if (action == "getStatus") {
    sendStatus(source);
  }
  else if (action == "pattern") {
    handlePattern(doc);
  }
  else if (action == "signature") {
    handleSignature(doc);
  }
}

void handleConnect(String source) {
  DynamicJsonDocument response(512);
  response["status"] = "connected";
  response["device"] = "TriAxis_Motor_Hub";
  response["company"] = "APEX PRECISION MECHATRONIX PVT. LTD.";
  response["version"] = "1.0";
  response["connection"] = source;
  
  String output;
  serializeJson(response, output);
  
  if (source == "BT") {
    SerialBT.println(output);
  }
  Serial.println("Connected via " + source);
}

void handleMove(DynamicJsonDocument& doc) {
  if (emergencyStop) return;
  
  String axis = doc["axis"];
  long steps = doc["steps"];
  int speed = doc["speed"] | 1000;
  
  AccelStepper* motor = getMotor(axis);
  if (motor) {
    motor->setSpeed(speed);
    motor->move(steps);
    
    // Update position tracking
    int axisIndex = getAxisIndex(axis);
    if (axisIndex >= 0) {
      motorPositions[axisIndex] += steps;
    }
    
    Serial.println("Moving " + axis + " axis: " + String(steps) + " steps at " + String(speed) + " RPM");
  }
}

void handleSetSpeed(DynamicJsonDocument& doc) {
  String axis = doc["axis"];
  int speed = doc["speed"];
  
  AccelStepper* motor = getMotor(axis);
  if (motor) {
    motor->setMaxSpeed(speed);
    
    int axisIndex = getAxisIndex(axis);
    if (axisIndex >= 0) {
      motorSpeeds[axisIndex] = speed;
    }
    
    Serial.println("Set " + axis + " speed: " + String(speed));
  }
}

void handleHome() {
  if (emergencyStop) return;
  
  Serial.println("Homing all axes...");
  
  // Move to limit switches
  stepperX.setSpeed(-500);
  stepperY.setSpeed(-500);
  stepperZ.setSpeed(-500);
  
  while (digitalRead(X_LIMIT_PIN) == HIGH || 
         digitalRead(Y_LIMIT_PIN) == HIGH || 
         digitalRead(Z_LIMIT_PIN) == HIGH) {
    
    if (digitalRead(X_LIMIT_PIN) == HIGH) stepperX.runSpeed();
    if (digitalRead(Y_LIMIT_PIN) == HIGH) stepperY.runSpeed();
    if (digitalRead(Z_LIMIT_PIN) == HIGH) stepperZ.runSpeed();
    
    if (digitalRead(EMERGENCY_STOP_PIN) == LOW) break;
  }
  
  // Set current position as zero
  stepperX.setCurrentPosition(0);
  stepperY.setCurrentPosition(0);
  stepperZ.setCurrentPosition(0);
  
  motorPositions[0] = motorPositions[1] = motorPositions[2] = 0;
  
  Serial.println("Homing complete");
}

void handleStop() {
  stepperX.stop();
  stepperY.stop();
  stepperZ.stop();
  Serial.println("All motors stopped");
}

void handleEnable(bool state) {
  motorsEnabled = state;
  digitalWrite(ENABLE_PIN, !state); // Enable pin is active low
  
  if (state && !emergencyStop) {
    Serial.println("Motors enabled");
  } else {
    Serial.println("Motors disabled");
  }
}

void handlePattern(DynamicJsonDocument& doc) {
  if (emergencyStop) return;
  
  String patternType = doc["type"];
  int radius = doc["radius"] | 100;
  int speed = doc["speed"] | 500;
  
  Serial.println("Executing pattern: " + patternType);
  
  if (patternType == "circle") {
    executeCirclePattern(radius, speed);
  }
  else if (patternType == "square") {
    executeSquarePattern(radius, speed);
  }
  else if (patternType == "spiral") {
    executeSpiralPattern(radius, speed);
  }
}

void handleSignature(DynamicJsonDocument& doc) {
  if (emergencyStop) return;
  
  JsonArray points = doc["points"];
  String style = doc["style"] | "normal";
  
  Serial.println("Executing 3D signature in " + style + " style");
  
  for (JsonVariant point : points) {
    float x = point["x"];
    float y = point["y"];
    float z = point["z"] | 0;
    
    // Apply style modifications
    if (style == "embossed") {
      z = (sin(x * 0.1) * 20);
    } else if (style == "calligraphy") {
      z = abs(x - stepperX.currentPosition()) * 0.1;
    }
    
    stepperX.moveTo(x);
    stepperY.moveTo(y);
    stepperZ.moveTo(z);
    
    while (stepperX.isRunning() || stepperY.isRunning() || stepperZ.isRunning()) {
      stepperX.run();
      stepperY.run();
      stepperZ.run();
      if (digitalRead(EMERGENCY_STOP_PIN) == LOW) break;
    }
  }
}

void executeCirclePattern(int radius, int speed) {
  for (int angle = 0; angle < 360; angle += 5) {
    float x = radius * cos(radians(angle));
    float y = radius * sin(radians(angle));
    
    stepperX.moveTo(x);
    stepperY.moveTo(y);
    
    while (stepperX.isRunning() || stepperY.isRunning()) {
      stepperX.run();
      stepperY.run();
      if (digitalRead(EMERGENCY_STOP_PIN) == LOW) return;
    }
  }
}

void executeSquarePattern(int size, int speed) {
  long positions[][2] = {{0,0}, {size,0}, {size,size}, {0,size}, {0,0}};
  
  for (int i = 0; i < 5; i++) {
    stepperX.moveTo(positions[i][0]);
    stepperY.moveTo(positions[i][1]);
    
    while (stepperX.isRunning() || stepperY.isRunning()) {
      stepperX.run();
      stepperY.run();
      if (digitalRead(EMERGENCY_STOP_PIN) == LOW) return;
    }
  }
}

void executeSpiralPattern(int maxRadius, int speed) {
  for (int i = 0; i < 720; i += 5) {
    float radius = (maxRadius * i) / 720.0;
    float x = radius * cos(radians(i));
    float y = radius * sin(radians(i));
    
    stepperX.moveTo(x);
    stepperY.moveTo(y);
    
    while (stepperX.isRunning() || stepperY.isRunning()) {
      stepperX.run();
      stepperY.run();
      if (digitalRead(EMERGENCY_STOP_PIN) == LOW) return;
    }
  }
}

void sendStatus(String source) {
  DynamicJsonDocument status(1024);
  status["motorsEnabled"] = motorsEnabled;
  status["emergencyStop"] = emergencyStop;
  status["positions"]["X"] = stepperX.currentPosition();
  status["positions"]["Y"] = stepperY.currentPosition();
  status["positions"]["Z"] = stepperZ.currentPosition();
  status["speeds"]["X"] = motorSpeeds[0];
  status["speeds"]["Y"] = motorSpeeds[1];
  status["speeds"]["Z"] = motorSpeeds[2];
  status["limits"]["X"] = digitalRead(X_LIMIT_PIN);
  status["limits"]["Y"] = digitalRead(Y_LIMIT_PIN);
  status["limits"]["Z"] = digitalRead(Z_LIMIT_PIN);
  
  String output;
  serializeJson(status, output);
  
  if (source == "BT") {
    SerialBT.println(output);
  }
}

void sendWiFiResponse(WiFiClient& client) {
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: application/json");
  client.println("Access-Control-Allow-Origin: *");
  client.println();
  
  DynamicJsonDocument response(512);
  response["status"] = "ok";
  response["device"] = "TriAxis Controller";
  
  String output;
  serializeJson(response, output);
  client.println(output);
}

AccelStepper* getMotor(String axis) {
  if (axis == "X") return &stepperX;
  if (axis == "Y") return &stepperY;
  if (axis == "Z") return &stepperZ;
  return nullptr;
}

int getAxisIndex(String axis) {
  if (axis == "X") return 0;
  if (axis == "Y") return 1;
  if (axis == "Z") return 2;
  return -1;
}

void checkLimitSwitches() {
  if (digitalRead(X_LIMIT_PIN) == LOW && stepperX.speed() < 0) {
    stepperX.stop();
  }
  if (digitalRead(Y_LIMIT_PIN) == LOW && stepperY.speed() < 0) {
    stepperY.stop();
  }
  if (digitalRead(Z_LIMIT_PIN) == LOW && stepperZ.speed() < 0) {
    stepperZ.stop();
  }
}

void disableMotors() {
  motorsEnabled = false;
  digitalWrite(ENABLE_PIN, HIGH);
  stepperX.stop();
  stepperY.stop();
  stepperZ.stop();
}

void blinkStatusLED(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(STATUS_LED_PIN, HIGH);
    delay(200);
    digitalWrite(STATUS_LED_PIN, LOW);
    delay(200);
  }
}