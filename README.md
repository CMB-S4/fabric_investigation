# fabric_investigation
This repository is for code related to the investigation of FABRIC as a type  of resource useful to CMB-S4.
More information for FABRIC is at [FABRIC](https://fabric-testbed.net).

A full investigation would have prompt map making and transient processing occur in a fabric-like
infrastructure.

Phase one 
=========

The Phase One project is to mock up transient processing for the CMB-S4 DC1 within Fabric. The minimal intergration
planned for evaluation is to attempt::

- Dynamically provision FABRIC Resources
- Ingest the maps needed for transient processing, thought to be 30 "per observations maps"
- Run transient detection codes.
- Emit transients to an endpoint representing "the transient community" 
- Tear Down FABRIC resources.

and write up results.

Notes on SCIMMA HOP usage 
==========================

We are using the hop-client package available from pip.

In the scimma hopskotch instance, The phase one channel is
`cmb-s4-fabric-tests.phase-one-testing`

Before use,                                                                                                                                                            
   - obtain an identity and SCRAM credential from my.hop.scimma.org                                                                                                   
   - use the "hop auth add" to store the credential                                                                                                                    
   - Ask Don to authorize you to acess the cmb-s4-fabric-tests.phase-one-testing topic. 

To see what you publish,  use this:

`hop subscribe  kafka://kafka.scimma.org/cmb-s4-fabric-tests.phase-one-testing`

want  more? : A [Tutorial](https://github.com/scimma/hop-client/wiki/Tutorial%3A-using-hop-client-with-the-SCiMMA-Hopskotch-server).l from SCIMMA is here

If you get errors about certificates See the following
'You can just open the certificate archive with a text editor; mine is located at ${VIRTUAL_ENV}/lib/python3.7/site-packages/certifi/cacert.pem


10:21
Once you have it open, you can just search for DST Root CA X3, delete/cut that certificate out of it, save, and see if things get any better?

Donald Petravick  10:22 AM
ok what am I lookign for
DST?

Chris Weaver  10:23 AM
DST Root CA X3
'