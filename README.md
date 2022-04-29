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