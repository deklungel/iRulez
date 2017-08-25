# Contents
1. [Device](#device)
    1. [Arduino](#arduino)
    2. [Kodi](#kodi)
    3. [Radio](#radio)
2. [Python](#python)
	1. [Core Script](#core-script)
	2. [AutoConfig](#autoconfig)
	3. [DeviceMonitor](#devicemonitor)
	4. [Discovery](#discovery)
	5. [Dummy](#dummy)
	6. [FBL](#fbl)
	7. [Logger](#logger)
	8. [Monitor](#monitor)
	9. [Service](#service)
	10. [Statistics](#statistics)
	11. [Telegram](#telegram)
	12. [Timer](#timer)



# Device
## Arduino

De arduino gaat tijdens het booten eerst achter een IP zoeken via DHCP. Als hij dit gevonden heeft gaat hij via de bonjour service het ip van de MQTT server zoeken. Wanneer hij ook dit heeft gaat hij zijn MAC + IP als topic uitsturen. Hierop ontvangt hij van de autoconfig module zijn hostname. Hij gaat ook zijn type + versie van de software die er op draait uitsturen.

Nadat hij zijn hostname gekregen heeft gaat hij luistern naar hostname/relais/actions. Als dit een H is wordt een uitgang hoog gebracht met een L laag. Hij gaat nadat hij een uitgang hoog of laag brengt ook een status bericht uitsturen hostname/relais/status.  Voor dimmers wordt er een waarde doorgestuurd tussen 0 en 100. Dit is de PWM waarde die de arduino op zijn eerste 10 interface kan zetten. Ook hier wordt een status met de laatste waarde teruggestuurd.

Ondertussen stuurt hij ook een keepalive uit.

## Kodi

Kodi werkt momenteel via een MQTT adapter. Deze plugin maakt een MQTT connectie en luistert op bepaalde topics. Via de website kan er zo content afgespeeld worden, muziek luider/ stiller gezet worden,…. Kodi kan ook bediend worden met een fysieke drukknop via het corescript.

De plugin stuurt ook een progressie van wat er aan het afspelen is. Nadeel van deze module is dat er handmatig instellingen aangepast moeten worden in de plugin  not plug and play

## Radio

# Python
## Core Script

- Toggle
- ON (publish H after defined period)
- OFF (publish L after defined period)
- Mail (send mail when button pushed)

Delay (delay all the programmed actions)
Button First Action (A button can have two actions, an immediat action when the button is pressed and released, and a second action when the button is pressed for a predefined time)

The first number now defines when the action should occur:

            0: perform action after release

            1: perform action immediately

            2: send a command for the dimmer

            3: wait a moment for a second action

Wait (For motion detection, if there is motion detected, the relais stays high for some time, if within this time, there is again motion detected, the timer is reset. The Wait option allows to give some time to consider the motion detector as invalid.)

Condition OR (The status of a relay, (new topic  time) or SUN down can be used, a status can be inverted)

Condition AND

End (Actions and conditions can be concatenated, so a relay can have multiple actions depending on the condition)

ToDo → option to break out of concatenated actions and conditions → check Laurent

Dimmer (Value can be shosen between -1 and 255/100, -1 stands for current value, dimmer speed represends the time needed to go to 255. If the dimmer option is present as first action, again a value of -1 and 255 can be given, and a dimmer speed. This time it will be used to toggle) Dimmer directions is stored in script

Relay as Master ( the first relay defined will count as master)

Kodi can be activated with a button:

Play [Volume] else current Volume

Play Toggle [Volume] (if something is playing stop else start)

Stop

Resume

new topic telegram

Beschikbaretags

#R = relay

#M = mail

#On = On

#Off = Off

#D = Delay

#SD = Sun Down

#CO = Condition Or

#CA = Condition And

#E = End

#TE = The End -&gt; niet nodig

#T = Toggle

#W = Wait till button released (for motion detection)

#FBLWR -&gt; FBL with feedback relais

#FBL = Place before R -&gt; Controls a FeedBackLight for the given Button ex. `"1|W|1800|FBL|0|1|R|2|15|Off|300|E"`

#RFBL = Place before R -&gt; Controls a FeedBackLight for the given Button ex. `"1|W|1800|FBL|0|1|R|2|15|Off|300|E"` returns the opposite/Reverse as FBL

#BTF = ButtonTimer perform action after a certain button hold time ex. `"3|2|R|0|1|T|E|BTF|R|0;0|1;2|Off|0|E"` BTF -&gt; ButtonTimerFirst action / ButtonTimerSecond action after a hold time of 2 sec

#BD = ButtonDimmer `"3|2|BD|-1|10000|0|1|E|R|0;0|1;2|Off|0|E|BTF|R|0;0|1;2|BD|75|10000|0|3|E"` -&gt; -1 use previous vallue, value between 0 and 100 filed in below 127 go up oterhwise go down, next value speed in milliseconds to have full value

First place of action string MUST be a number :

            0: perform action after release

            1: perform action immediately

            2: send a command for the dimmer

            3: wait a moment for a second action

**Voorbeeld1:**

`1|W|1800|FBL|0;0|1;0|R|1;2|3;15|M|testmail@gmail.com|OFF|60|CO|R|0;0|2;!3|SD|E|R|2;2|13;14|ON|60|CA|0;0|2;3|E`

Deze string zal volgende doen:

Bij indrukken (bewegingsmelder) onmiddellijk schakelen

De W geeft aan dat de ingang hoog mag blijven maar na 1800sec hoog zal de bewegingsmelder als ongeldig gezien worden en gaat het core script de ingang als terug laag beschouwen.

FBL betekent dat er naar de website en in dit geval ook naar Arduino0/Relais1 en Arduino0/Relais0 een signaal wordt gestuurd indien minstens één van de volgende Relais&#39; hoog is

Indien de voorwaarde in deze sectie (alles voor de E) is voldaan zullen volgende relais&#39; geschakeld worden:
Arduino1/Relais3
Arduino2/Relais15

Mail wordt meegestuurd indien voorwaarde in deze sectie is voldaan.

OFF na 60 seconden. Na 60 seconden zal het licht uitgaan.
Indien er ipv FBL, CFBL had gestaan was het terugkoppellampje aangegaan wanneer het licht uit was. Immers is de voorwaarde pas voldaan wanneer de lamp OFF is. Lichten kan je uiteraard ook onmiddellijk uitschakelen door OFF|0 te zetten.

CO, Condition On, gaat volgende waarden nakijken en indien één hiervan voldoet worden voorgaande acties uitgevoerd:
Arduino0/Relais2 mag hoog zijn
Arduino0/Relais3 mag laag zijn
Zon mag onder zijn

E volgende sectie begint vanaf hier

Relais13 &amp; 14 van Arduino2 zullen geschakeld worden indien de voorwaarde in de conditie voldaan is.

ON na 60 seconden, wanneer dit commando uitgevoerd wordt zal het licht na 60 seconden uitgeschakeld worden. Lichten die reeds aan waren gaan uit en zullen pas na 60 seconden terug aangaan. Zonder bijkomende interactie zullen ze aanblijven.

CA betekent dat  Arduino0/Relais2 EN Arduino0/Relais3 moeten hoog zijn.

**Voorbeeld2:**

`3|_2_|BD|-1|10000|0|1|E|R|0;0;0;0|2;3;4;5|T|E|BTF|R|0;0|1;2|BD|75|10000|0;0|3;4|T|E`

3 Vooraan betekent dat er _2_ seconden gewacht wordt. Indien de schakelaar niet langer dan _2_ seconden wordt ingedrukt dan wordt BTF(ButtonFirstAction) uitgevoerd. Indien de schakelaar wel langer dan 2 seconden ingeduwd wordt, wordt alles voor BTF inclusief de verschillende secties, uitgevoerd.

Relais 1 &amp; 2 van Arduino0 zullen getoggled worden. Dit betekent, indien het licht uit was, zal het aangaan en omgekeerd. Om te vermijden dat sommige lichten in dit geval aangaan en andere uit, geldt de eerste relais, in dit geval Arduino0/Relais1 als Master.

Dat betekent dat indien relais1 hoog was, relais2 ongeacht de status mee laag zal gaan.

BD (ButtonDimmer):

eerste waarde : lichtsterkte (in dit geval 75, had ook -1 kunnen zijn wat staat voor de actuele waarde)

tweede waarde : Snelheid waarmee het licht van 0 tot 100 gaat (in dit geval 10seconden)

derde waarde : de arduino&#39;s

vierde waarde : de relias&#39;

BD zal in dit geval mee toggle&#39;n. Indien op het einde OFF|10, dan had de dimmer naar 75 gegaan om na 10 seconden terug uit te gaan.

BD zie voorgaande

Anders dan in voorgaande kijkt deze functie niet naar de T(oggle)

Deze functie zal altijd op dezelfde manier werken.

Vanaf 2seconden zal het licht aangaan indien het uit was en blijven hangen op een bepaalde lichtsterkte indien je de schakelaar lost.

Wanneer je nogmaals duwt zal het licht uitdoven tot je de schakelaar last.

Arduino0/Relais2 is in dit geval de master.

**Voorbeeld3:**

`0|FBL|1|7|R|2;3;3;3;3;3;3;3;2;2;2;2;2;2;0;2;2;2;2;2;2;0;0;0;0;0;0|7;6;5;4;3;2;1;0;14;13;12;10;9;8;0;6;5;4;3;2;0;7;5;4;3;2;1|Off|0|D|15|`

Bovenstaande is een typische alles uit configuratie.

Wanneer de schakelaar gelost is heb je 15 seconden voor alle lichten uitgaan.



## AutoConfig

Autoconfig ga na opstarten een lijst uitsturen van alle radio zenders  radiolist  + de hostname voor alle devices   MAC/hostname

Wanneer deze module het bericht MAC/ip/xxxxxxxxx ontvangt gaat het kijken welk arduino nummer hiermee overeen stemt. En de hostname uitsturen MAC/hostname .

Wanneer deze module het bericht MAC/ lastWill /xxxxxxxxx ontvangt gaat het de relais status in de database op OFF zetten, hierna de feedbacklight module requesten om opnieuw de feedback lights te bekijken.  Het stuurt ook een melding naar de telegram module  Telegram/Message/&quot; [ALERT] - Device   with MAC: xxxx DOWN!&quot;

## DeviceMonitor

Deze module is gebouwt wanneer er met een borderMQTT gewerkt wordt. Deze borderMQTT staat in de DMZ en heeft een username en password.

Wanneer de deviceMonitor opstart gaat het lijst met owntrackIDs uitsturen waarop de BorderMQTT mag subscriben.

Wanneer het een /event/ van de BorderGateway binnen krijgt gaat hij de database updaten zodat we weten als een gebruiker binnen of buiten een bepaalde zone is. Hij gaat ook kijken welke acties verbonden zijn aan het event en deze uitvoeren.

Wanneer hij een gateway/getList binnen krijgt gaat hij de lijst met owntrack id&#39;s nog een uitsturen naar de borderMQTT

## Discovery

Deze module verzorgd de bonjour service. Deze stuurt \_irulez.\_tcp met het IP adres van de MQTT server.

## Dummy

De Dummer is gemaakt om in een test omgeving scripts te testen. De Dummy reageert exact zoals alle arduino&#39;s zouden reageren die geconfigureerd zijn.

## FBL

FBL gaat de status messages van de arduinos volgen en deze status in de database wegschrijven. Hierna gaat het FBL script een controle doen van alle geconfigureerde FBL en de juist status van het FBL uitsturen. Dit wordt dan op de webinterface correct weergeven. Deze module gaat ook de relais hoog of laag brengen indien er een fysieke FBL geconfigureerd is.

ER zijn 4 verschillende FBL modus:

Feedback Light : is HIGH als er minimaal 1 relais hoog is

Reverse Feedback Light: is HIGH als er minimaal 1 relais laag is

Condition Feedback Light: is HIGH als alle relais aan hun voorwaarde voldoen (Toggle  High, On  High, Off  Low)

Reverse Condition Feedback Light: NIET GEIMPLEMENTEERD maar was de bedoeling is LOW als alle relais aan hun voorwaarde voldoen (Toggle  High, On  High, Off  Low)

## Logger

De logger volgt alle MQTT topics en schrijft de topic met Payload weg in een file. Wordt enkel gebruikt om te debuggen

## Monitor

Monitor gaat het IP, type van de devices + versie van de software in de database zetten als ze het na booten uitsturen

Het gaat ook een hardbeat + ping van de devices bijhouden.

## Service

We hebben gemerkt dat de mqtt service kan crashen. Dit script checkt constant de MQTT poort. Als deze down is herstart het script de MQTT service. Het script stuurt dan ook een telegram notificatie

## Statistics

Deze module houd in de database bij wanneer een licht aan en uit gegaan is. Elke dag krijgt het van de timer module ook het bericht om een cleanup van de database te doen. Hier worden alle geven van meer dan 1j verwijderd.

## Telegram

De Telegram module gaat een melding sturen naar uw gsm indien een relais voor een ingestelde tijd aan is. U kan dan kiezen om het licht uit te doen, melding te snoozen of melding te negeren. U kan ook zelf door /status te sturen een overzicht krijgen van alle lichten die aan zijn en ze in 1 keer uit doen.

Telegram kan ook een melding uitsturen wanneer er een probleem is door te publishen in Telegram/Message

## Timer

De timer module kan op een ingestelde tijd een vbutton toggelen. Dit kan op een bepaald tijstip zijn, met zonsondergang (+/- #minuten), zonsopkomst  (+/- #minuten), of een random tijdstip tussen 2tijdstippen. Dit kan ingesteld worden voor elke dag van de week afzonderlijk. Om 12u gaat de timer module resetten zodat het de nieuwe tijd van zonsopgang en zonsondergang kan bereken. Deze module stuurt ook een cleanup naar de statistieken module.
