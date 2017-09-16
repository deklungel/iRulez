
#define USEDPINS_PORTB 0xE0 //b1110 0000
#define USEDPINS_PORTD 0x0C //b0000 1100
#define USEDPINS_PORTE 0x38 //b0011 1000
#define USEDPINS_PORTH 0x7B //b0111 1011
#define USEDPINS_PORTJ 0x03 //b0000 0011

//Dit ter info
/*#define INPUTMASK_PORTB 0xE000
  #define INPUTMASK_PORTD 0x0003
  #define INPUTMASK_PORTE 0x01C0
  #define INPUTMASK_PORTH 0x1E0C
  #define INPUTMASK_PORTJ 0x0030*/

int INPUT_COMMAND_PORTB = 0x00;
int INPUT_COMMAND_PORTD = 0x00;
int INPUT_COMMAND_PORTE = 0x00;
int INPUT_COMMAND_PORTH = 0x00;
int INPUT_COMMAND_PORTJ = 0x00;

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
    print_binary(number,16);
    printStatusPorts();
    Serial.println(F("------------------------------------------"));
    double timeOne = micros();
    verwerkInput(number);
    double timeTwo = micros();
    double duration = timeTwo - timeOne;   
    printStatusPorts();
    Serial.print(F("Tijd nodig om ALLE uitgangen te updaten[Microseconden]: "));
    Serial.println(duration); 
    Serial.println(F("__________________________________________"));
    endMessage = false;
    beginMessage = false;
    x = 0;    
    memset(inData, 0, sizeof(inData));
  }
}

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
  DDRB = USEDPINS_PORTB;
  DDRD = USEDPINS_PORTD;
  DDRE = USEDPINS_PORTE;
  DDRH = USEDPINS_PORTH;
  DDRJ = USEDPINS_PORTJ;

  //HIER HETZELFDE DOEN VOOR DE INGANGEN
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

void printStatusPorts() {
  Serial.print("PORTB: ");
  Serial.print(PORTB, HEX);
  Serial.print("=>");
  Serial.println(PORTB, BIN);

  Serial.print("PORTD: ");
  Serial.print(PORTD, HEX);
  Serial.print("=>");
  Serial.println(PORTD, BIN);

  Serial.print("PORTE: ");
  Serial.print(PORTE, HEX);
  Serial.print("=>");
  Serial.println(PORTE, BIN);

  Serial.print("PORTH: ");
  Serial.print(PORTH, HEX);
  Serial.print("=>");
  Serial.println(PORTH, BIN);

  Serial.print("PORTJ: ");
  Serial.print(PORTJ, HEX);
  Serial.print("=>");
  Serial.println(PORTJ, BIN);
}

void printInfoPoorten(){
 Serial.print(F("Uitgang:        "));
 Serial.println(F("0  1   2   3   4  5   6  7  8  9  10  11  12  13  14  15"));
 Serial.print(F("Port# arduino:  "));
 Serial.println(F("13 12  11  9   8  7   6  5  3  2  14  15  16  17  18  19"));
 Serial.print(F("Port.BIT:       "));
 Serial.println(F("B7 B6  B5  H6  H5 H4  H3 E3 E5 E4 J1  J0  H1  H0  D3  D2"));

 Serial.println(F("Je kan nu een de uitgangen sturen door tussen [] een HEX-waarde mee te geven."));
 Serial.println(F("Bv: [FFFF] => alles aan | [0000] => alles uit | [1800] => uitgagen 3&4 aan, de rest uit"));
  }
