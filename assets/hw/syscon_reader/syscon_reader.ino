// Syscon glitcher (reader) by DarkNESmonk (https://t.me/darknesmonk)
// For A0X-C0LX only (Renesas RL78/G13)

#define ledPin          13      // LED

#define reset_pin       2       // D2 
#define glitch_pin      4       // D4 PIN = PORTD B11101111 ( faster method )
#define VDD_OFF         PORTD = PORTD & B11101111
#define VDD_ON          PORTD = PORTD | B00010000

#define TX              1       // D1
#define RX              0       // D0

#define OCD_CONNECT_CMD 0x91
#define OCD_READ_CMD    0x92
#define OCD_WRITE_CMD   0x93
#define OCD_EXEC_CMD    0x94
#define BAUD_SET_CMD    0x9a

#define SOH             1
#define STX             2
#define ETX             3

#define CHKS 1
#define CHKS_A 2
#define CHKS_OCD 3
#define FSL_ERR_PROTECTION   0x10

struct ST_FRAME {
  byte stx;
  byte LEN;
  byte DATA1;
  byte SUM;
  byte etx;
};

uint8_t shellcode[] = {
  0xe0, 0x07, 0x26,
  0x41, 0x00, 0x34, 0x00, 0x00, 0x00, 0x11, 0x89, 0xFC, 0xA1, 0xFF, 0x0E, 0xA5, 0x15, 0x44,
  0x00, 0x00, 0xDF, 0xF3, 0xEF, 0x04, 0x55, 0x00, 0x00, 0x00, 0x8E, 0xFD, 0x81, 0x5C, 0x0F,
  0x9E, 0xFD, 0x71, 0x00, 0x90, 0x00, 0xEF, 0xE0
};

uint8_t csum = 0;
bool ledState = 0;

void w(char b)
{
  csum += b;
  Serial.write(b);
  delayMicroseconds(100);
}

char gsum(char t)
{
  if (t == CHKS) csum = 0;
  if (t == CHKS_A) { csum ^= 0xff; csum += 1; }
  if (t == CHKS_OCD) csum -= 1;
  return csum;
}

void setup(void)
{
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  pinMode(reset_pin, OUTPUT);
  pinMode(glitch_pin, OUTPUT);
  pinMode(TX, OUTPUT);
  pinMode(RX, INPUT);
  digitalWrite(reset_pin, LOW);
  digitalWrite(TX, LOW);
  digitalWrite(RX, LOW);
  digitalWrite(glitch_pin, HIGH);
}

void loop(void)
{

  while (1)
  {
    int random_pos, random_delay;
    ST_FRAME STF1 = {0};
    
    byte a;
    random_pos = random(2000, 8000);
    random_delay = random(1, 8);
    
    digitalWrite(reset_pin, LOW);
    delayMicroseconds(40);
    Serial.end();
    delay(5);
    
    digitalWrite(reset_pin, HIGH);
    delay(5);
    
    Serial.begin(115200);
    Serial.setTimeout(100);
    delay(1);
    
    w(0xc5);
    w(SOH);
    gsum(CHKS);
    w(0x03);
    w(BAUD_SET_CMD);
    w(0x00);
    w(0x14);
    w(gsum(CHKS_A));
    
    while (Serial.available() > 0) Serial.read()
    w(ETX);
    
    Serial.read();
    Serial.readBytes((byte *)&STF1, sizeof(ST_FRAME));
    
    if (STF1.DATA1 != 0x06 && STF1.DATA1 != FSL_ERR_PROTECTION ) {
      w(0xEE);
      break;
    }
    
    if (STF1.DATA1 == FSL_ERR_PROTECTION) {
      
      delayMicroseconds(random_pos);
      VDD_OFF;
      
      delayMicroseconds(random_delay);
      VDD_ON;
      
      int counter = 0;
      
      while (Serial.available() > 0) Serial.read()
      
      while ( ++counter < 1000)
      {
        if (Serial.available() > 0)
        {
          a = Serial.read();
          if (a == STX) break; // wait STX response
        }
        delayMicroseconds(5);
      }
      if (counter >= 1000) {
        continue;
      }
    }
    delay(5);
    w(OCD_CONNECT_CMD);
    delay(1);

    gsum(CHKS);
    w(':');
    w('N');
    w('o');
    w('t');
    w(':');
    w('U');
    w('s');
    w('e');
    w('d');
    w(':');
    w(gsum(CHKS_OCD));

    delay(1);
    w(OCD_WRITE_CMD);
    delay(1);

    for (int s = 0; s < sizeof(shellcode); s++) w(shellcode[s]);

    delay(1);

    Serial.write(OCD_EXEC_CMD); // EXEC without delay
    pinMode(TX, INPUT);
    Serial.end();
    break;
  }

  while (1)
  {
    digitalWrite(ledPin, ledState); // blinking LED :)
    ledState ^= 1;
    delay(500);
  }
}
