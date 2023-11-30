# Alert Distributionm Prototyping 

Codes in this directory prototype Alert Distribuyion
to a lesser rather than greater degree.

As concieved, alert distribution recieves undecorated alerts
from SP and Chilean alerr detection pipleine.  Because the current
baseline inlcudes the very low bandwith Iridium links, these
alerts are as compact as possible.

The design notion is that Alert Distriution operates are a 
deamon,
- Recieves these undecorated alerts.
- Formats alerts for transmission to one or more brokers. 
- Inserts alerts into a catalog.

The level of development here is to:
- Show the FABRIC environment can support this activity.
- Demonstrate an initial publishable alert.
- Prototype what would be recorded in a catalog.
- Get some experience for a basis of esitmate. 
- Prototype a compact form for the undecorated alert.


