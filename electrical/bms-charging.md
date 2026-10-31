# BMS, charger and charging port

Pack 4's BMS and charger are settled. What is left from [#19](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/19) is the charging socket. Prices read 29 Oct 2026, CAD unless marked US$.

## Where Pack 4 stands

- Ayaan checked the pack on 30 Oct: it works, it has a BMS built in, and the charger works with it ([#21](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/21), closed).
- The main leads were resoldered to an XT60H-F on 29 Oct.
- The charge lead is probably the small yellow XT30-style plug, but nobody has confirmed which lead it is yet.
- Ling said the pack does not need a fuse.
- Left to do: mount the XLR socket, and run two wires from it to the charge lead.

## BMS

Nothing to buy. The pack's own board protects and balances it.

If it ever needs replacing, it has to be 12S Li-ion NMC with balancing, 15 A or more continuous, and a temperature sensor that blocks charging below 0 °C. [#18](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/18) holds the controller at 10 A battery current, so 15 A is 50% headroom.

| BMS | Price | Current rating | Balancing | Size | Link |
| --- | --- | --- | --- | --- | --- |
| JBD-SP14S004, 7S to 14S auto detect, Bluetooth and UART | CA$49.99, in stock | 30 A continuous, 90 A peak | Passive, 20 to 55 mA, leads included | 63 x 52 x 9 mm | [affordableebikes.ca](https://affordableebikes.ca/products/small-bms) |
| JBD-SP14S004, 50 A version | CA$59.99, in stock | 50 A continuous, 150 A peak | Passive, 20 to 55 mA | larger board | [affordableebikes.ca](https://affordableebikes.ca/products/small-bms) |
| JBD-DB20SA02, 8S to 20S, common port, Bluetooth and UART | US$32 plus shipping and duty | 40 A continuous | Passive, current not listed, temperature limits settable | 100 x 80 x 5 mm | [JBD store](https://jiabaida-bms.com/collections/frontpage), search the model |
| Daly 7S to 24S smart, 60 A, Bluetooth, CAN | CA$129.99, in stock | 60 A continuous | Active, 1 A | 126 x 67 x 14 mm | [affordableebikes.ca](https://affordableebikes.ca/products/smart-bms-daly-7s-24s-60a-lithium-ion-bluetooth-and-high-balance-current) |

- Take the SP14S004 30 A if a board is ever needed. In stock in Canada, cheapest, 63 x 52 x 9 mm, external NTC, charge temperature limits settable in the app.
- The Daly is a better board and the wrong buy. 1 A of active balancing is for a 100 Ah solar bank, not a 5 to 10 Ah pack charged weekly, at three times the price.
- No fixed 13S board, even at CA$20. JBD's fixed-string line does not offer 12S in Li-ion at all, only 12S LiFePO4.

## Charger

Works with the pack. Keep it.

If it ever needs replacing, the label has to read 50.4 V with 12S, or 12S with 44.4 V. A reading of 54.6 V, 13S, or "48 V" with no voltage is a 13S unit and must not go on this pack.

| Charger | Output | Current | Price | Link |
| --- | --- | --- | --- | --- |
| 12S lithium, RCA 8 mm output, other connectors on request | 50.4 V | 3 A | CA$49.99, out of stock 29 Oct | [affordableebikes.ca](https://affordableebikes.ca/products/charger-12s-50-4v-3-amp-lithium-ion) |
| Chi 50.4 V, 5.5 x 2.1 mm barrel stock, custom connector on request | 50.4 V | 4.5 A | US$100 plus shipping and duty | [chibatterysystems.com](https://chibatterysystems.com/products/12s45a) |

- 3 A suits a 2P pack. The Chi only makes sense if an order is happening anyway.

## XLR charging socket

The socket sits at pack voltage whenever the charger is unplugged, so the bike-side contacts have to be recessed.

| Port | Current rating | Contacts | Size | Price | Link |
| --- | --- | --- | --- | --- | --- |
| 3 pin XLR female chassis socket, metal, latch | 16 A per contact on the Neutrik original, copies vary, treat as 10 A | recessed sockets, latches | 24 mm D cutout | CA$5.95 | [Sayal](https://shop.sayal.com/products/gbsa-2262a) |
| 3 pin XLR male inline plug, for the charger lead | 16 A per contact | pins, charger side only | cable end | CA$6.95 | [Sayal](https://shop.sayal.com/products/gbsa-5212h) |
| 5.5 x 2.1 mm DC panel jack | about 5 A | recessed, thin centre pin, wears | 8 mm hole | CA$6.95 for 2 | [Sayal](https://shop.sayal.com/products/gak-2156-2) |

- Two parts to buy: the socket at CA$5.95 and the male plug at CA$6.95. The project lead orders.
- The XLR is the standard e-bike charge plug. Three times the charge current even at 10 A, recessed by construction, latches, metal shell screws to the frame.
- The charge cable photographed with Pack 3 ends in a 3 pin XLR plug through a barrel adapter, so keep the adapter on the charger side.
- Polarity, written on both ends: pin 1 positive, pin 2 negative, pin 3 unused. The shell is isolated from the pins.
- No fuse on this line, Ling's call via #21. #19 step 5 asked for one, so this is a deliberate exception, not an oversight.
- Socket position waits on the mounting work in [#26](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/26). It needs to clear the cargo box and the steering.

```
charger (50.4 V) -> XLR male on the charger lead
                        |
              XLR female socket in the frame
                        |
              pack charge lead (XT30 or whatever it turns out to be)
```

Negative runs socket to charge lead negative. Nothing grounds to the frame.

## Still open

- Which of Pack 4's leads is the charge lead, and what plug it uses.
- Socket position on the frame, with #26.
