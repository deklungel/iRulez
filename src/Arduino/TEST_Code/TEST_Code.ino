
//////////////////////////////////////////
//        iRulez Home Automation        //
//        Version 15.1 2017/09/14       //
//             www.iRulez.be            //
//////////////////////////////////////////

#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
#include <EthernetBonjour.h>
#include <Wire.h>
#include <string.h>
#include <ctype.h>
#include <avr/wdt.h>

//Outputs
#define USEDPINS_PORTB 0xE0 //b1110 0000
#define USEDPINS_PORTD 0x0C //b0000 1100
#define USEDPINS_PORTE 0x38 //b0011 1000
#define USEDPINS_PORTH 0x7B //b0111 1011
#define USEDPINS_PORTJ 0x03 //b0000 0011

//Inputs
#define USEDPINS_PORTF 0xFF //b1111 1111
#define USEDPINS_PORTL 0xC7 //b1100 0111
#define USEDPINS_PORTG 0x03 //b0000 0011
#define USEDPINS_PORTD_ 0x80 //b1000 0000

# define aantalSamples 6

/* Variables to change */
String Version = "15.2";
String ReleaseDate = "2017/09/19";
String Model = "iRulezIO16";
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xE9};
char iRulez[] = "irulez";
char MqttUsername[] = "iRulezMqtt";
char MqttPassword[] = "iRulez4MQTT";
/* Variables to change */
String MAC_String = "";
byte ColorArray[3] = {A8, A9, A10};
int button3change = 0;
int ConnectedToServer = 0;
bool bonjour = false;
bool setupClient = true;
int buttonState = 0;
int ButtonChange[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int ButtonLowTimer[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int ButtonHighTimer[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int ButtonLowTimer2[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int ButtonHighTimer2[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
byte Input_array[16] = {A0, A1, A2, A3, A4, A5, A6, A7, 48, 46, 44, 42, 49, 47, 45, 43};
byte ByteOn[] = {"H"};
byte ByteOff[] = {"L"};
byte lengthByte = 1;
byte retain = 1;
char charString[64];
int relaisNumberInt = 0;
int newPin = 0;
int LowTime1 = 150;
int LowTime2 = 50;
char message_buff[100];
char buffer[10];
String BoardName;
bool check_Subscribe = true;

byte INPUT_1[aantalSamples];
byte INPUT_2[aantalSamples];
byte INPUT_3[aantalSamples];
byte INPUT_4[aantalSamples];
byte INPUT_5[aantalSamples];
byte INPUT_6[aantalSamples];
byte INPUT_7[aantalSamples];
byte INPUT_8[aantalSamples];
byte INPUT_9[aantalSamples];
byte INPUT_10[aantalSamples];
byte INPUT_11[aantalSamples];
byte INPUT_12[aantalSamples];
byte INPUT_13[aantalSamples];
byte INPUT_14[aantalSamples];
byte INPUT_15[aantalSamples];
byte INPUT_16[aantalSamples];

int index = 0;

unsigned int temp_INPUT_STATUS = 0x0000;

int INPUT_COMMAND_PORTB = 0x00;
int INPUT_COMMAND_PORTD = 0x00;
int INPUT_COMMAND_PORTE = 0x00;
int INPUT_COMMAND_PORTH = 0x00;
int INPUT_COMMAND_PORTJ = 0x00;


unsigned int FEEDBACK_STATUS_PORT = 0x0000;
unsigned int INPUT_STATUS_PORT = 0x0000;

byte MQTTip[4];
byte ipAddr[4] = {0,0,0,0};
int resetCounter = 0;
int firstResetCounter = 0;
int redPin = 22;
int greenPin = 23;
int bluePin = 24;
EthernetClient ethClient;
PubSubClient client;

const char* ip_to_str(const uint8_t*);
void serviceFound(const char* type, MDNSServiceProtocol proto,
                  const char* name, const byte ipAddr[4], unsigned short port,
                  const char* txtContent);


void setup()
{
  wdt_enable(WDTO_8S);
  MAC_String = mac2String(mac);
  Serial.begin(9600);
  Serial.println("===============================================");
  Serial.println("======       iRulez Home Automation      ======");
  Serial.print("=========   Version ");
  Serial.print(Version);
  Serial.print(" ");
  Serial.print(ReleaseDate);
  Serial.println("   =========");
  Serial.println("==============   www.iRulez.be  ===============");
  Serial.println("===============================================");
  Serial.println(" ");
  Serial.print(" MAC address ");
  Serial.print(MAC_String);
  Serial.println(" ");
  pinMode(10, OUTPUT);
  pinMode(4, OUTPUT);
  for (int thisPin = 0; thisPin <= 2; thisPin++) {
    pinMode(ColorArray[thisPin], OUTPUT);
    Serial.println(" Initialize color output");
  }
  setColor("yellow");
  
  // start the Ethernet connection:
  wdt_reset();
  Serial.println("Trying to get an IP address using DHCP");
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // no point in carrying on, so do nothing forevermore:
    for (;;)
      setColor("red");
  }
  setColor("green");
//  digitalWrite(10, HIGH);
//  digitalWrite(4, HIGH);

  // Initialize the Bonjour/MDNS library. You can now reach or ping this
  // Arduino via the host name "arduino.local", provided that your operating
  // system is Bonjour-enabled (such as MacOS X).
  // Always call this before any other method!
  EthernetBonjour.begin("MAC_String");

  // We specify the function that the Bonjour library will call when it
  // discovers a service instance. In this case, we will call the function
  // named "serviceFound".
  EthernetBonjour.setServiceFoundCallback(serviceFound);


  Serial.println("Initializing all in and outputs");
  
  
  setRegisterDirection();
   
 
  
}

void loop()
{
  char charBoardName[64];
  char CharServiceName[256];
  String serviceName = "_irulez\0";
  serviceName.toCharArray(CharServiceName, serviceName.length() + 1);
  if (!EthernetBonjour.isDiscoveringService()) {
    Serial.print("Discovering services of type '");
    Serial.print(serviceName);
    Serial.println("' via Multi-Cast DNS (Bonjour)...");

    EthernetBonjour.startDiscoveringService(CharServiceName, MDNSServiceTCP, 0);
  }

  if (bonjour == true) {
    if (firstResetCounter == 0)
    {
      firstResetCounter = 1;
      resetCounter = 0;
      wdt_reset();
    }
    if(setupClient == true){
      //override MQTTip
      byte OverrideMQTTip[] = { 10, 0, 50, 50 };
      client = PubSubClient (OverrideMQTTip, 1883, callback, ethClient);
      //client = PubSubClient (MQTTip, 1883, callback, ethClient);
      setupClient = false;
    }
    if (!client.connected())
    {
      check_Subscribe = true;
      setColor("green");
      delay(750);
      setColor("blue");
      delay(750);
      setColor("red");
      delay(750);
       if (resetCounter < 7)
      {
        Serial.println("do reset1");
        wdt_reset();
        resetCounter = resetCounter + 1;
      }
      Serial.println("Connecting to server");
      MAC_String.toCharArray(charBoardName, 63);

      String WillTopic = MAC_String + "/lastWill";
      char charWillTopic[WillTopic.length() + 1];
      WillTopic.toCharArray(charWillTopic, WillTopic.length() + 1);

      client.connect(charBoardName, MqttUsername, MqttPassword, charWillTopic , 0 , 0, "D");
      ConnectedToServer = 0;
      delay(2000);
      if (resetCounter < 7)
      {
        Serial.println("do reset2");
        wdt_reset();
        resetCounter = resetCounter + 1;
      }
    }
    else {
      if (ConnectedToServer == 0)
      {
        wdt_reset();
        resetCounter = 0;
        firstResetCounter = 0;
        setColor("blue");
        ConnectedToServer = 1;
        Serial.println("Connected to server");
        String MAC_Alive = MAC_String + "/alive";
        char charAlive[MAC_Alive.length() + 1];
        MAC_Alive.toCharArray(charAlive, MAC_Alive.length() + 1);
        String IP = DisplayAddress(Ethernet.localIP());
        char charIP[IP.length() + 1];
        String MAC_StringIP = MAC_String + "/ip";
        String MAC_Hostname = MAC_String + "/hostname";
        String MAC_Model = MAC_String + "/type";
        String MAC_Version = MAC_String + "/version";
        char charModel[Model.length() + 1];
        char charVersion[Version.length() + 1];
        char charMAC_Hostname[MAC_Hostname.length() + 1];
        char charMAC_Model[MAC_Model.length() + 1];
        char charMAC_IP[MAC_StringIP.length() + 1];
        char charMAC_Version[MAC_Version.length() + 1];
        IP.toCharArray(charIP, IP.length() + 1);
        Model.toCharArray(charModel, Model.length() + 1);
        Version.toCharArray(charVersion, Version.length() + 1);
        MAC_StringIP.toCharArray(charMAC_IP, MAC_StringIP.length() + 1);
        MAC_Hostname.toCharArray(charMAC_Hostname, MAC_Hostname.length() + 1);
        MAC_Model.toCharArray(charMAC_Model, MAC_Model.length() + 1);
        MAC_Version.toCharArray(charMAC_Version, MAC_Version.length() + 1);
        client.publish(charMAC_IP, charIP);
        client.subscribe(charMAC_Hostname);
        client.publish(charAlive, "H");
        client.publish(charMAC_Model, charModel);
        client.publish(charMAC_Version, charVersion);

        //to be delete when going live"
        char charBoardName[64];
        BoardName = "DEMO";
        (Model + "/" + BoardName + "/action").toCharArray(charBoardName, 63);
        client.subscribe(charBoardName);
        check_Subscribe = false;
      }
      client.loop();
      wdt_reset();
      resetCounter = 0;
      firstResetCounter = 0;

      leesStatusIngangen();
    }
  }
  else {
    delay(2000);
    Serial.println("Searching...)");
    EthernetBonjour.run();
    if (resetCounter < 7)
    {
     wdt_reset();
     resetCounter = resetCounter + 1;
    }
  }
}


void callback(char* topic, byte* payload, unsigned int lengthpayload) {
  int i = 0;
  char charBoardName[64];


  //Serial.println("Message arrived:  topic: " + String(topic));
  //Serial.println("Length: " + String(length,DEC));

  // create character buffer with ending null terminator (string)
  for (i = 0; i < lengthpayload; i++) {
    message_buff[i] = payload[i];
  }
  message_buff[i] = '\0';

  String payloadString = String(message_buff);
  String topicString = String(topic);

  Serial.println("Message Toppic arrived: " + topicString);
  Serial.println("Message Payload arrived: " + payloadString);
  if (topicString == Model + "/" + BoardName + "/action"){
    //String Status = processHEX(payloadString);

    unsigned int number = hex2int(message_buff);
    Serial.print(F("Onvangen data in binair: "));
    print_binary(number,16);
    Serial.println(F("------------------------------------------"));
    double timeOne = micros();
    verwerkInput(number);
    double timeTwo = micros();
    double duration = timeTwo - timeOne;   
    printStatusPorts();
    String Status = readStatusPorts();
    Serial.print(F("Tijd nodig om ALLE uitgangen te updaten[Microseconden]: "));
    Serial.println(duration); 
    Serial.println(F("__________________________________________"));
    memset(message_buff, 0, sizeof(message_buff));

    
    
    (Model + "/" + BoardName + "/status").toCharArray(charBoardName, 63);
    char charStatus[Status.length() + 1];
    Status.toCharArray(charStatus, Status.length() + 1);
    client.publish(charBoardName,charStatus ,retain); 
    
  }
  else if (topicString == MAC_String + "/hostname")
  {
    String MAC_Alive = MAC_String + "/alive";
    char charAlive[MAC_Alive.length() + 1];
    MAC_Alive.toCharArray(charAlive, MAC_Alive.length() + 1);
    client.publish(charAlive, "H");
    if (check_Subscribe == true)
    {
      payloadString.toLowerCase();
      BoardName = payloadString;
      (Model + "/" + BoardName + "/action").toCharArray(charBoardName, 63);
      client.subscribe(charBoardName);
      check_Subscribe = false;
    }
  }


}
String DisplayAddress(IPAddress address)
{
  return String(address[0]) + "." +
         String(address[1]) + "." +
         String(address[2]) + "." +
         String(address[3]);
}

void setColor(String myColor)
{
  if (myColor == "red") {
    digitalWrite(ColorArray[0], HIGH);
    digitalWrite(ColorArray[1], LOW);
    digitalWrite(ColorArray[2], LOW);
  }
  if (myColor == "green") {
    digitalWrite(ColorArray[0], LOW);
    digitalWrite(ColorArray[1], HIGH);
    digitalWrite(ColorArray[2], LOW);
  }
  if (myColor == "blue") {
    digitalWrite(ColorArray[0], LOW);
    digitalWrite(ColorArray[1], LOW);
    digitalWrite(ColorArray[2], HIGH);
  }
  if (myColor == "yellow") {
    digitalWrite(ColorArray[0], HIGH);
    digitalWrite(ColorArray[1], HIGH);
    digitalWrite(ColorArray[2], LOW);
  }
  if (myColor == "aqua") {
    digitalWrite(ColorArray[0], LOW);
    digitalWrite(ColorArray[1], HIGH);
    digitalWrite(ColorArray[2], HIGH);
  }
  if (myColor == "white") {
    digitalWrite(ColorArray[0], HIGH);
    digitalWrite(ColorArray[1], HIGH);
    digitalWrite(ColorArray[2], HIGH);
  }
  if (myColor == "off") {
    digitalWrite(ColorArray[0], LOW);
    digitalWrite(ColorArray[1], LOW);
    digitalWrite(ColorArray[2], LOW);
  }
}
String mac2String(byte ar[]) {
  String s;
  for (byte i = 0; i < 6; ++i)
  {
    char buf[3];
    sprintf(buf, "%02X", ar[i]);
    s += buf;
  }
  return s;
}
void serviceFound(const char* type, MDNSServiceProtocol proto,
                  const char* name, const byte ipAddr[4],
                  unsigned short poort,
                  const char* txtContent)
{
  if (NULL == name) {
    Serial.print("Finished discovering services of type ");
    Serial.println(type);
  } else {
    Serial.print("Found: ");
    Serial.println(name);

    parseBytes(name, '.', MQTTip, 4, 10);

    // Check out http://www.zeroconf.org/Rendezvous/txtrecords.html for a
    // primer on the structure of TXT records. Note that the Bonjour
    // library will always return the txt content as a zero-terminated
    // string, even if the specification does not require this.
   
    if(MQTTip[0] != 0){
       bonjour = true;
    }
   
  }
}

// This is just a little utility function to format an IP address as a string.
const char* ip_to_str(const uint8_t* ipAddr)
{
  static char buf[16];
  sprintf(buf, "%d.%d.%d.%d\0", ipAddr[0], ipAddr[1], ipAddr[2], ipAddr[3]);
  return buf;
}
void parseBytes(const char* str, char sep, byte* bytes, int maxBytes, int base) {
    for (int i = 0; i < maxBytes; i++) {
        bytes[i] = strtoul(str, NULL, base);  // Convert byte
        str = strchr(str, sep);               // Find next separator
        if (str == NULL || *str == '\0') {
            break;                            // No more separators, exit
        }
        str++;                                // Point to next character after separator
    }
}


//Deze functie is enkel voor het printen van binaire waarden.
//voorbeeld: 0000_1111_0000_0000
void print_binary(int v, int num_places)
{
    int mask=0, n;
    for (n=1; n<=num_places; n++)
    {
        mask = (mask << 1) | 0x0001;
    }
    v = v & mask;  // truncate v to specified number of places
    while(num_places)
    {
        if (v & (0x0001 << num_places-1))
        {
             Serial.print("1");
        }
        else
        {
             Serial.print("0");
        }
        --num_places;
        if(((num_places%4) == 0) && (num_places != 0))
        {
            Serial.print("_");
        }
    }
    Serial.println("");
}

//Omvormen van string naar HEX
unsigned int hex2int(char *hex) {
    unsigned int val = 0;
    while (*hex) {
        // get current character then increment
        uint8_t byte = *hex++; 
        // transform hex character to the 4bit equivalent number, using the ascii table indexes
        if (byte >= '0' && byte <= '9') byte = byte - '0';
        else if (byte >= 'a' && byte <='f') byte = byte - 'a' + 10;
        else if (byte >= 'A' && byte <='F') byte = byte - 'A' + 10;    
        // shift 4 to make space for new digit, and add the 4 bits of the new digit 
        val = (val << 4) | (byte & 0xF);
    }
    return val;
}

void verwerkInput(int input) {

  int PARSE_INPUT_PORTB = (extractBitsBetween(13, 15, input) << 5);
  int deelH1 =  (extractBitsBetween(9, 12, input) << 3);
  int deelE1 =  (extractBitsBetween(8, 8, input) << 3);
  int deelE2 =  (extractBitsBetween(6, 7, input) << 4);
  int PARSE_INPUT_PORTJ =  (extractBitsBetween(4, 5, input));
  int deelH2 =  (extractBitsBetween(2, 3, input));
  int PARSE_INPUT_PORTD =  (extractBitsBetween(0, 1, input) << 2);

  int PARSE_INPUT_PORTH = deelH1 | deelH2;
  int PARSE_INPUT_PORTE = deelE1 | deelE2;

  updateRegisterX('B', PARSE_INPUT_PORTB);
  updateRegisterX('D', PARSE_INPUT_PORTD);
  updateRegisterX('E', PARSE_INPUT_PORTE);
  updateRegisterX('H', PARSE_INPUT_PORTH);
  updateRegisterX('J', PARSE_INPUT_PORTJ);
}

int extractBitsBetween(int lsb, int msb, int DATA) {
  return  (DATA >> lsb) & ~(~0 << (msb - lsb + 1));
}


void setRegisterDirection() {
  DDRB = DDRB | USEDPINS_PORTB;
  DDRD = DDRD | USEDPINS_PORTD;
  DDRE = DDRE | USEDPINS_PORTE;
  DDRH = DDRH | USEDPINS_PORTH;
  DDRJ = DDRJ | USEDPINS_PORTJ;

   //Inputs, Direction Register moet 0 zijn om ingang te zijn.
  DDRF = DDRF | ~USEDPINS_PORTF;
  DDRL = DDRL | ~USEDPINS_PORTL;
  DDRG = DDRG | ~USEDPINS_PORTG;
  DDRD = DDRD | ~USEDPINS_PORTD_; // Deze moet eigenlijk niet omdat DDRD bij de uitgangen al werd juist gezet.
  
}

void updateRegisterX(char PORT, int NEWVALUE) {
  switch (PORT) {
    case 'B':
      PORTB = (PORTB & ~USEDPINS_PORTB) | (NEWVALUE & USEDPINS_PORTB);
      break;
    case 'D':
      PORTD = (PORTD & ~USEDPINS_PORTD) | (NEWVALUE & USEDPINS_PORTD);
      break;
    case 'E':
      PORTE = (PORTE & ~USEDPINS_PORTE) | (NEWVALUE & USEDPINS_PORTE);
      break;
    case 'H':
      PORTH = (PORTH & ~USEDPINS_PORTH) | (NEWVALUE & USEDPINS_PORTH);
      break;
    case 'J':
      PORTJ = (PORTJ & ~USEDPINS_PORTH) | (NEWVALUE & USEDPINS_PORTH);
      break;
    default:
      ;
  }
}
 //Dit is gewoon om de status van de poorten te printen in de seriële console.
 //DEBUG, Niet nodig in finale code
void printStatusPorts() {
  Serial.print("PORTB: 0x");
  Serial.print(PORTB, HEX);
  Serial.print("=>");
  Serial.println(PORTB, BIN);

  Serial.print("PORTD: 0x");
  Serial.print(PORTD, HEX);
  Serial.print("=>");
  Serial.println(PORTD, BIN);

  Serial.print("PORTE: 0x");
  Serial.print(PORTE, HEX);
  Serial.print("=>");
  Serial.println(PORTE, BIN);

  Serial.print("PORTH: 0x");
  Serial.print(PORTH, HEX);
  Serial.print("=>");
  Serial.println(PORTH, BIN);

  Serial.print("PORTJ: 0x");
  Serial.print(PORTJ, HEX);
  Serial.print("=>");
  Serial.println(PORTJ, BIN);

  
}

//Deze functie gaat de poorten (registers) lezen en serieel terugsturen.
//Nu in binair maar kan ook in HEX.
String readStatusPorts(){
  
  unsigned int partB = (PORTB & USEDPINS_PORTB)<<8;
  unsigned int partD = (PORTD & USEDPINS_PORTD)>>2;
  unsigned int partE1 = (PORTE & 0x08)<<5;
  unsigned int partE2 = (PORTE & 0x30)<<2;
  unsigned int partH1 = (PORTH & 0x78)<<6;
  unsigned int partH2 = (PORTH & 0x03)<<2;
  unsigned int partJ = (PORTJ & USEDPINS_PORTJ)<<4;
  
  FEEDBACK_STATUS_PORT=0x0000;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT|partB;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT|partD;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT|partE1;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT|partE2;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT|partH1;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT|partH2;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT|partJ;
  
  Serial.print(F("Status van de poorten na aanpssen van registers[BIN]: "));
  print_binary(FEEDBACK_STATUS_PORT,16);
  Serial.print(F("Status van de poorten na aanpssen van registers [HEX]: 0x"));
  Serial.println(FEEDBACK_STATUS_PORT,HEX);
  return String(FEEDBACK_STATUS_PORT,HEX);
  
}

void leesStatusIngangen() {
  float temp1 = micros();
  temp_INPUT_STATUS = 0x0000;

  INPUT_1[index] = (PINF & 0x01);
  INPUT_2[index] = (PINF & 0x02);
  INPUT_3[index] = (PINF & 0x04);
  INPUT_4[index] = (PINF & 0x08);

  INPUT_5[index] = (PINF & 0x10);
  INPUT_6[index] = (PINF & 0x20);
  INPUT_7[index] = (PINF & 0x40);
  INPUT_8[index] = (PINF & 0x80);

  INPUT_9[index] = (PINL & 0x02);
  INPUT_10[index] = (PING & 0x02);
  INPUT_11[index] = (PING & 0x01);
  INPUT_12[index] = (PINL & 0x80);

  INPUT_13[index] = (PINL & 0x01);
  INPUT_14[index] = (PINL & 0x04);
  INPUT_15[index] = (PIND & 0x80);
  INPUT_16[index] = (PINL & 0x40);

  if (checkElementsArray(INPUT_1)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_1[index] << 15);
  } if (checkElementsArray(INPUT_2)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_2[index] << 13);
  } if (checkElementsArray(INPUT_3)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_3[index] << 11);
  } if (checkElementsArray(INPUT_4)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_4[index] << 9);
  }

  if (checkElementsArray(INPUT_5)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_5[index] << 7);
  } if (checkElementsArray(INPUT_6)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_6[index] << 5);
  } if (checkElementsArray(INPUT_7)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_7[index] << 3);
  } if (checkElementsArray(INPUT_8)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_8[index] << 1);
  }

  if (checkElementsArray(INPUT_9)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_9[index] << 6);
  } if (checkElementsArray(INPUT_10)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_10[index] << 5);
  } if (checkElementsArray(INPUT_11)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_11[index] << 5);
  } if (checkElementsArray(INPUT_12)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_12[index] >> 3);
  }

  if (checkElementsArray(INPUT_13)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_13[index] << 3);
  } if (checkElementsArray(INPUT_14)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_14[index]);
  } if (checkElementsArray(INPUT_15)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_15[index] >> 6);
  } if (checkElementsArray(INPUT_16)) {
    temp_INPUT_STATUS = temp_INPUT_STATUS | (INPUT_16[index] >> 6);
  }

  //-----Index verhogen, indien aan de laatste terug naat nul.
  if (index == (aantalSamples - 1)) {
    index = 0;
  }
  else {
    index++;
  }
  float temp2 = micros();
  //---------------Einde index verhogen----------------------
  float x = temp2 - temp1;


  if (temp_INPUT_STATUS != INPUT_STATUS_PORT) {
    char charBoardName[64];
    Serial.print("Status van de ingangen: 0x");
    Serial.println(temp_INPUT_STATUS, HEX);
    Serial.print("Status van de ingangen in binair: ");
    print_binary(temp_INPUT_STATUS, 16);
    INPUT_STATUS_PORT = temp_INPUT_STATUS;

    String str_INPUT_STATUS_PORT = String(INPUT_STATUS_PORT,HEX);
    (Model + "/" + BoardName + "/button").toCharArray(charBoardName, 63);
    char charINPUT_STATUS_PORT[str_INPUT_STATUS_PORT.length() + 1];
    str_INPUT_STATUS_PORT.toCharArray(charINPUT_STATUS_PORT, str_INPUT_STATUS_PORT.length() + 1);
    client.publish(charBoardName,charINPUT_STATUS_PORT ,retain); 

    //For debug only
    Serial.print("tijd voor berekenen: ");
    Serial.println(x);
  }
}

//Functie gaat kijken of alle elementen dezelfde zijn. Indien dit is krijgen we True anders False.
bool checkElementsArray(byte temp[aantalSamples]) {
  for (int i = 1; i < aantalSamples; i++) {
    if (temp[i] != temp[0]) {
      return false;
    }
  }
  return true;
}


  
//Print de mapping van de poorten
void printInfoPoorten(){
 Serial.print(F("Uitgang:        "));
 Serial.println(F("0  1   2   3   4  5   6  7  8  9  10  11  12  13  14  15"));
 Serial.print(F("Port# arduino:  "));
 Serial.println(F("13 12  11  9   8  7   6  5  3  2  14  15  16  17  18  19"));
 Serial.print(F("Port.BIT:       "));
 Serial.println(F("B7 B6  B5  H6  H5 H4  H3 E3 E5 E4 J1  J0  H1  H0  D3  D2"));
}

