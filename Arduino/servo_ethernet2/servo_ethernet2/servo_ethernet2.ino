#include <SPI.h>
#include <Ethernet.h>
#include <Servo.h>
#include <HttpClient.h>

#define BUFSIZe 100

boolean incoming = 0;

// Enter a MAC address and IP address for your controller below.
byte mac[] = { 0x00, 0xAA, 0xBB, 0xCC, 0xDA, 0x02 };
IPAddress ip(192,168,0,25);

// Initialize the Ethernet server library
EthernetServer server(80);
EthernetClient client;
Servo myservo;
int angle = 0;

void setup()
{
  pinMode(2, OUTPUT);

  // start the Ethernet connection and the server:
  Ethernet.begin(mac, ip);
  server.begin();
  Serial.begin(9600);
  myservo.attach(9);
  myservo.write(0);
}

void loop()
{
  
  EthernetClient client2 = server.available();
  if (client2) {
    boolean currentLineIsBlank = true;
    int index = 0;
    int linia = 0;
    char clientline[BUFSIZe];
    for(int i = 0; i<BUFSIZe; i++){
      clientline[i] = ' ';
    }
    Serial.println("połączono");
    while (client2.connected()) {
      if (client2.available()) {
        char c = client2.read();
        
        if (c != '\n' && c != '\r') {
          clientline[index] = c;
          index++;
          if (index >= BUFSIZe)
            index = BUFSIZe -1;

          // continue to read more data!
          continue;
        }else{
          linia++;
          if(strstr(clientline, "angle=") == 0)
            for(int i = 0;i<100;i++)
            clientline[i] = ' ';
            index = 0;
            continue;
            Serial.println(linia);
        }
        
      }
      Serial.println(clientline);
      angle += atol(strstr(clientline, "angle=") + 6);
      if(angle > 180)
        angle = 180;
      if(angle < 0)
        angle = 0;
      myservo.write(angle);
      Serial.println(angle);
      String PostData = "angle=" + String(angle);
      client2.println("HTTP/1.1 200");
      client2.println("Content-Type: application/x-www-form-urlencoded");
      client2.println("Connection: close");  // the connection will be closed after completion of the response
      client2.print("Content-Length: "); 
      client2.println(PostData.length()); 
      client2.println(); 
      client2.print(PostData);
      delay(50);
      //sendData();
      client2.stop();

    }
    // give the web browser time to receive the data
    delay(1);
    // close the connection:
    
  }
  
  
   

  delay(1000);
  
}
