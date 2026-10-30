# BMS, charger and charging port

Answers [#19](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/19) for Pack 4. Prices read 29 Oct 2026, CAD unless marked US$.

## What Pack 4 needs

Pack 4 is 12S2P, 24 cells, 44 V nominal, 50.4 V full, 36 V empty.

- **12S Li-ion NMC.** A 13S board sees one group low and balances the wrong way.
- **15 A continuous discharge.** The issue's floor. [#18](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/18) sets the controller to 10 A battery current, so 15 A is 50% headroom.
- **Balancing** on the 13 balance wires.
- **3 A charge max** until the cell capacity is known. That is 0.3C on 10 Ah, 0.6C on 5 Ah.
- **NTC, no charging below 0 °C.** Cold charging plates the anode and kills the cell.
- **Fuse DC rated 60 V or more.** A car blade fuse is 32 V.
- **Charger marked 12S, 50.4 V.** A "48 V" charger is usually 54.6 V for 13S.

## Do not open the pack

Pack 4 is hand-built, wrapped, and carries its own protection board. Cutting the wrap means re-wrapping a live 50.4 V pack for no gain if the board works. Five checks from the outside, lead present, safety glasses:

1. **Labels.** Pack says 48 V, 12S2P, dated. Photograph any board sticker with a model number.
2. **Leads.** Two thick leads to XT90 for riding plus a thin lead to XT60 for charging means the board has a separate charge input. No charge lead means common port, and the socket reaches the main connector through the fuse instead.
3. **Pack voltage.** 40 to 50.4 V on the main lead. Under 40 V, stop and hand it to [#21](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/21).
4. **Charge lead voltage.** Same reading, charge lead to main negative. Zero means the board is asleep, the lead is broken, or nothing is wired to it.
5. **One supervised charge.** 2 A, tapers to near zero at 50.4 V, pack cool, groups within 0.05 V.

Check 5 is the test that counts. A charge that stops at 50.4 V and holds proves the board, a label does not. If the pack has no usable board, replacing it means cutting the pack open, which is #21's work, not this issue's.

## BMS options

| BMS | Price | Current rating | Balancing | Size | Link |
| --- | --- | --- | --- | --- | --- |
| JBD-SP14S004, 7S to 14S auto detect, Bluetooth and UART | CA$49.99, in stock | 30 A continuous, 90 A peak | Passive, 20 to 55 mA, leads included | 63 x 52 x 9 mm | [affordableebikes.ca](https://affordableebikes.ca/products/small-bms) |
| JBD-SP14S004, 50 A version | CA$59.99, in stock | 50 A continuous, 150 A peak | Passive, 20 to 55 mA | larger board | [affordableebikes.ca](https://affordableebikes.ca/products/small-bms) |
| JBD-DB20SA02, 8S to 20S, common port, Bluetooth and UART | US$32 plus shipping and duty | 40 A continuous | Passive, current not listed, temperature limits settable | 100 x 80 x 5 mm | [JBD store](https://jiabaida-bms.com/collections/frontpage), search the model |
| Daly 7S to 24S smart, 60 A, Bluetooth, CAN | CA$129.99, in stock | 60 A continuous | Active, 1 A | 126 x 67 x 14 mm | [affordableebikes.ca](https://affordableebikes.ca/products/smart-bms-daly-7s-24s-60a-lithium-ion-bluetooth-and-high-balance-current) |

- Take the SP14S004 30 A if a board is needed. In stock in Canada, cheapest, 63 x 52 x 9 mm, external NTC, charge temperature limits settable in the app.
- The Daly is a better board and the wrong buy. 1 A of active balancing is for a 100 Ah solar bank, not a 5 to 10 Ah pack charged weekly, and it costs twice the whole port list.
- Direct from China is cheaper per amp, but shipping, 15 to 25 days and duty eat it.
- No fixed 13S board, even at CA$20. JBD's fixed-string line does not offer 12S in Li-ion at all, only 12S LiFePO4.

## Charger

Team's charger first. Free. The label has to say 50.4 V with 12S, or 12S with 44.4 V. A label reading 54.6 V, 13S, or "48 V" with no voltage must not go on Pack 4.

| Charger | Output | Current | Price | Link |
| --- | --- | --- | --- | --- |
| The team's existing charger | check the label | 2 to 5 A expected | already owned | photograph the label for the issue |
| 12S lithium, RCA 8 mm output, other connectors on request | 50.4 V | 3 A | CA$49.99, out of stock 29 Oct | [affordableebikes.ca](https://affordableebikes.ca/products/charger-12s-50-4v-3-amp-lithium-ion) |
| Chi 50.4 V, 5.5 x 2.1 mm barrel stock, custom connector on request | 50.4 V | 4.5 A | US$100 plus shipping and duty | [chibatterysystems.com](https://chibatterysystems.com/products/12s45a) |

- 3 A suits a 2P pack. The Chi only makes sense if the team's unit turns out to be 13S and an order is happening anyway.
- Nothing gets charged until checks 3 to 5 have run, on concrete, with the lead there.

## Charging port

The socket sits at pack voltage whenever the charger is unplugged, on common port and separate port boards both, because the charge MOSFET conducts both ways. So the bike-side contacts have to be recessed.

| Port | Current rating | Contacts | Size | Price | Link |
| --- | --- | --- | --- | --- | --- |
| 3 pin XLR female chassis socket, metal, latch | 16 A per contact on the Neutrik original, copies vary, treat as 10 A | recessed sockets, latches | 24 mm D cutout | CA$5.95 | [Sayal](https://shop.sayal.com/products/gbsa-2262a) |
| 3 pin XLR male inline plug, for the charger lead | 16 A per contact | pins, charger side only | cable end | CA$6.95 | [Sayal](https://shop.sayal.com/products/gbsa-5212h) |
| 5.5 x 2.1 mm DC panel jack | about 5 A | recessed, thin centre pin, wears | 8 mm hole | CA$6.95 for 2 | [Sayal](https://shop.sayal.com/products/gak-2156-2) |

- Take the XLR. Standard e-bike charge plug, three times the charge current even at 10 A, recessed by construction, latches, metal shell screws to the frame.
- The charge cable photographed with Pack 3 ends in a 3 pin XLR plug through a barrel adapter, so keep the adapter on the charger side.
- Polarity, written on both ends: pin 1 positive, pin 2 negative, pin 3 unused. The shell is isolated from the pins.

## Fuse on the charge line

Positive wire only, between the socket and the pack's charge lead, inside the frame. It covers a damaged socket or a chafed wire.

| Part | Rating | Price | Link |
| --- | --- | --- | --- |
| Inline fuse holder, 5 x 20 mm, bayonet | 10 A, 250 V | CA$6.95 | [Sayal](https://shop.sayal.com/products/ftr-5x20-338-1) |
| Ceramic fuse, 5 x 20 mm, 8 A, pack of 5 | 250 V, ceramic | CA$7.95 | [Sayal](https://shop.sayal.com/products/fbe-8a-250-5-yy) |

- Ceramic, not glass. Ceramic is the body type that carries DC ratings: a Schurter SPT 5 x 20 is 250 V AC and 300 V DC, and 5 A suits a 3 A charger. Check the packet of the 8 A local part for a DC voltage, and order the Schurter if it only says AC.
- No auto-parts blade holder. ATO and ATC fuses are 32 V DC, under the pack's 50.4 V, and a DC arc does not self extinguish.

## Wiring

```
charger (50.4 V, 3 A) -> XLR male on the charger lead
                              |
                    XLR female socket in the frame
                              |
                    fuse, positive wire only
                              |
              pack charge lead (XT60) -> BMS charge input
```

Negative runs socket to pack charge lead negative. Nothing grounds to the frame.

## What to buy

Nothing on the BMS side if the five checks pass. If a board is needed, add the SP14S004 at CA$49.99.

| Part | Qty | Price |
| --- | --- | --- |
| XLR female chassis socket | 1 | CA$5.95 |
| XLR male inline plug | 1 | CA$6.95 |
| Inline fuse holder, 5 x 20 mm | 1 | CA$6.95 |
| Ceramic fuses, 5 x 20 mm, 8 A, pack of 5 | 1 | CA$7.95 |
| **Total** | | **CA$27.80 plus tax** |

Inside the $40 to $80 the electrical side has left ([#11](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/11)). The project lead orders.

## Still open

- Charger label photo. The charger decision hangs on it.
- Capacity in Ah. Not on the label, so 3 A stays the limit until #21 identifies the cells.
- Whether the pack's board has an NTC. If not, the cold block needs a board that does, meaning the SP14S004 and a #21 decision on opening the pack.
- Port position, with the mounting work in [#26](https://github.com/Electrium-Mobility/Bakfiets-F26/issues/26).
