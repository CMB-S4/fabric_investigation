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

we are using the pip hop-client package

OUr channel is cmb-s4-fabric-tests.phase-one-testing                                                                                                                    
Before use,                                                                                                                                                            
   - obtain an indentity and scram creential from my.hop.scimma.org                                                                                                    
   - use the "hop auth add" to store the credential                                                                                                                    
   - Ask Don to put you in the right group in scimma or make you a co-admin of the grop.  

To see what you publish,  use this:

`hop subscribe  kafka://kafka.scimma.org/cmb-s4-fabric-tests.phase-one-testing

want  more? : A [Tutorial](https://github.com/scimma/hop-client/wiki/Tutorial%3A-using-hop-client-with-the-SCiMMA-Hopskotch-server).l from SCIMMA is here

If you get errors about certificates
-t  See Don (after he fixed this yet again and remebers how)