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
   - use the "hop auth add" to store the credential (Leave hostname blank)
   - Ask Don to authorize you to acess the cmb-s4-fabric-tests.phase-one-testing topic.
   - arrange for outbound (kafka) port 9092 to be open 

scimma_utils
============

The scimma_utils packages included here further wraps the pbulish and subscribe subfunctions in hop.



More about hop
=============
Tutorial is [here](https://github.com/scimma/hop-client/wiki/Tutorial%3A-using-hop-client-with-the-SCiMMA-Hopskotch-server).
Shell Command documentation is [here](https://hop-client.readthedocs.io/en/latest/user/commands.html).

If you get errors about certificates
====================================
your OS may be supplying a version of openssl with a bug in it.
A work around is:
- $hop auth locate
- cat the file gven by hop auth locate
- edit the file pointed to by ssl_ca_location
- find the DST Root CA X3, in that file delete/cut that certificate out of it,

'