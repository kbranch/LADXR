from assembler import ASM
from roomEditor import RoomEditor


def updateWitch(rom):
    # Add a heartpiece at the toadstool, the item patches turn this into a 1 time toadstool item
    # Or depending on flags, in something else.
    re = RoomEditor(rom, 0x050)
    re.addEntity(2, 3, 0x35)
    re.store(rom)

    # Change what happens when you trade the toadstool with the witch
    #  Note that the 2nd byte of this code gets patched with the item to give from the witch.
    rom.patch(0x05, 0x08D4, 0x08F0, ASM("""
        ld  e, $09 ; load the item to give the first time

        ; Get the room flags and mark the witch as done.
        ld  hl, $DAA2
        ld  a, [hl]
        and $30
        set 4, [hl]
        set 5, [hl]
        jr  z, skip
        ld  e, $09 ; give powder every time after the first time.
skip:
        ld  a, e
        ldh [hActiveEntitySpriteVariant], a
        ld  a, $02
        rst 8
        ld  a, $03
        rst 8
    """), fill_nop=True)

    # Patch the toadstool to unload when you haven't delivered something to the witch yet.
    rom.patch(0x03, 0x1D4B, ASM("""
        ld   hl, wHasToadstool
        ld   a, [wMagicPowderCount]
        or   [hl]
        jp   nz, UnloadEntity
    """), ASM("""
        ld   a, [$DAA2]
        and  $20
        jp   z, UnloadEntity
    """), fill_nop=True)

    # Patch what happens when we pickup the toadstool, call our chest code to give a toadstool.
    rom.patch(0x03, 0x1D6F, 0x1D7D, ASM("""
        ld   a, $50
        ldh  [hActiveEntitySpriteVariant], a
        ld  a, $02 ; give item
        rst 8

        ld   hl, $DAA2
        res  5, [hl]
    """), fill_nop=True)

def witchIsPatched(rom):
    return sum(rom.banks[0x05][0x08D4:0x08F0]) != 0x0DC2
