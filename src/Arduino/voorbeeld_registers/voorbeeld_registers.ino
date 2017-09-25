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

char inData[25];
int x = 0;
bool endMessage = false;
bool beginMessage = false;

void setup() {
  Serial.begin(115200);
  delay(2000);
  setRegisterDirection();
  printInfoPoorten();
}

void loop() {
  while (Serial.available() && endMessage == false) {

    if (Serial.peek() == '[') {
      beginMessage = true;
      Serial.read();
    }

    else {
      if (beginMessage == true) {
        if (Serial.peek() == ']') {
          endMessage = true;
        }
        else {
          inData[x] = Serial.read();
          x++;
        }
      }
      else {
        Serial.read();
      }
    }
  }

  if (endMessage == true) {
    Serial.print(F("Ontvangen commando: 0x"));
    String ontvangenData = String(inData);
    Serial.println(ontvangenData);
    unsigned int number = hex2int(inData);
    Serial.print(F("Onvangen data in binair: "));
    print_binary(number, 16);
    Serial.println(F("------------------------------------------"));
    double timeOne = micros();
    verwerkInput(number);
    double timeTwo = micros();
    double duration = timeTwo - timeOne;
    printStatusPorts();
    readStatusOutputPorts();
    Serial.print(F("Tijd nodig om ALLE uitgangen te updaten[Microseconden]: "));
    Serial.println(duration);
    Serial.println(F("__________________________________________"));
    endMessage = false;
    beginMessage = false;
    x = 0;
    memset(inData, 0, sizeof(inData));
  }

  leesStatusIngangen();
}

//Deze functie is enkel voor het printen van binaire waarden.
//voorbeeld: 0000_1111_0000_0000
void print_binary(int v, int num_places)
{
  int mask = 0, n;
  for (n = 1; n <= num_places; n++)
  {
    mask = (mask << 1) | 0x0001;
  }
  v = v & mask;  // truncate v to specified number of places
  while (num_places)
  {
    if (v & (0x0001 << num_places - 1))
    {
      Serial.print("1");
    }
    else
    {
      Serial.print("0");
    }
    --num_places;
    if (((num_places % 4) == 0) && (num_places != 0))
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
    else if (byte >= 'a' && byte <= 'f') byte = byte - 'a' + 10;
    else if (byte >= 'A' && byte <= 'F') byte = byte - 'A' + 10;
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
  //Outputs, Direction Register moet 1 zijn om uitgang te zijn
  DDRB = USEDPINS_PORTB;
  DDRD = USEDPINS_PORTD;
  DDRE = USEDPINS_PORTE;
  DDRH = USEDPINS_PORTH;
  DDRJ = USEDPINS_PORTJ;

  //Inputs, Direction Register moet 0 zijn om ingang te zijn.
  DDRF = ~USEDPINS_PORTF;
  DDRL = ~USEDPINS_PORTL;
  DDRG = ~USEDPINS_PORTG;
  DDRD = ~USEDPINS_PORTD_; // Deze moet eigenlijk niet omdat DDRD bij de uitgangen al werd juist gezet.

}

//Deze functie gaat een register updaten met de waarden in NEWVALUE.
//mask is afhankelijk van het register dat geupdate moet worden.
//Enkel de bits die effectief gebruikt worden als uitgang zullen aangepast worden, ander worden genegeerd.
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


//Deze functie gaat de poorten (registers) lezen en serieel terugsturen.
//Nu in binair maar kan ook in HEX.
void readStatusOutputPorts() {
  unsigned int partB = (PORTB & USEDPINS_PORTB) << 8;
  unsigned int partD = (PORTD & USEDPINS_PORTD) >> 2;
  unsigned int partE1 = (PORTE & 0x08) << 5;
  unsigned int partE2 = (PORTE & 0x30) << 2;
  unsigned int partH1 = (PORTH & 0x78) << 6;
  unsigned int partH2 = (PORTH & 0x03) << 2;
  unsigned int partJ = (PORTJ & USEDPINS_PORTJ) << 4;

  FEEDBACK_STATUS_PORT = 0x0000;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT | partB;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT | partD;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT | partE1;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT | partE2;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT | partH1;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT | partH2;
  FEEDBACK_STATUS_PORT = FEEDBACK_STATUS_PORT | partJ;

  Serial.print(F("Status van de poorten na aanpssen van registers[BIN]: "));
  print_binary(FEEDBACK_STATUS_PORT, 16);
  Serial.print(F("Status van de poorten na aanpssen van registers [HEX]: 0x"));
  Serial.println(FEEDBACK_STATUS_PORT, HEX);

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
    Serial.print("Status van de ingangen: 0x");
    Serial.println(temp_INPUT_STATUS, HEX);
    Serial.print("Status van de ingangen in binair: ");
    print_binary(temp_INPUT_STATUS, 16);
    INPUT_STATUS_PORT = temp_INPUT_STATUS;

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

//Print de mapping van de poorten
void printInfoPoorten() {
  Serial.print(F("Uitgang:        "));
  Serial.println(F("0  1   2   3   4  5   6  7  8  9  10  11  12  13  14  15"));
  Serial.print(F("Port# arduino:  "));
  Serial.println(F("13 12  11  9   8  7   6  5  3  2  14  15  16  17  18  19"));
  Serial.print(F("Port.BIT:       "));
  Serial.println(F("B7 B6  B5  H6  H5 H4  H3 E3 E5 E4 J1  J0  H1  H0  D3  D2"));

  Serial.println(F("Je kan nu een de uitgangen sturen door tussen [] een HEX-waarde mee te geven."));
  Serial.println(F("Bv: [FFFF] => alles aan | [0000] => alles uit | [1800] => uitgagen 3&4 aan, de rest uit"));
}
