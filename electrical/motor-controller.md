# Motor Controller Research
This page reports information on the motor controller used in bakfiets 2026.

Related task: [Issue #38](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/38)

## Firmware, Hardware and UUID
Firmware Version: 7.00

Hardware Name: 60

Hardware UUID: 48 00 18 00 10 36 31 57 4C 39 43 53

## Current limits
Motor Current Max: 70.89A

Battery Current Max: 99.00A

Battery Voltage Cutoff Start: 40.8V

Battery Voltage Cutoff End: 36.0V

## Hardware Information
Manufacturer: Flipsky

Model: Mini FSESC v6.7 Pro

Maximum Input Voltage: 14V-60V

Continuous Motor Current: 70A

Peak Motor Current: 200A

Issue #38 requires a maximum input voltage of 60V or more and a motor current around 40A. The published voltage meets the requirement with a max of 60V but Flipsky notes that voltage spikes must not exceed that value. The published continuous motor current is 70A which is sufficient.
