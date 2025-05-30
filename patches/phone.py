from assembler import ASM


def patchPhone(rom):
    rom.texts[0x141] = b""
    rom.texts[0x142] = b""
    rom.texts[0x143] = b""
    rom.texts[0x144] = b""
    rom.texts[0x145] = b""
    rom.texts[0x146] = b""
    rom.texts[0x147] = b""
    rom.texts[0x148] = b""
    rom.texts[0x149] = b""
    rom.texts[0x14A] = b""
    rom.texts[0x14B] = b""
    rom.texts[0x14C] = b""
    rom.texts[0x14D] = b""
    rom.texts[0x14E] = b""
    rom.texts[0x14F] = b""
    rom.texts[0x16E] = b""
    rom.texts[0x1FD] = b""
    rom.texts[0x228] = b""
    rom.texts[0x229] = b""
    rom.texts[0x22A] = b""
    rom.texts[0x240] = b""
    rom.texts[0x241] = b""
    rom.texts[0x242] = b""
    rom.texts[0x243] = b""
    rom.texts[0x244] = b""
    rom.texts[0x245] = b""
    rom.texts[0x247] = b""
    rom.texts[0x248] = b""
    rom.patch(0x06, 0x2A7C, 0x2BBC, ASM("""
        ld   a, [wTunicType]
        call SetEntitySpriteVariant

        ldh  a, [hActiveEntityVisualPosY]
        sub  $05
        ldh  [hActiveEntityVisualPosY], a
        ld   de, TelephoneSpriteVariants
        call RenderActiveEntitySpritesPair
        call ReturnIfNonInteractive_06
        call CheckLinkInteractionWithEntity_06
        ret  nc
    
        ; We use $DB6D to store which tunics we have. This is normally the Dungeon9 instrument, which does not exist.
        ld  a, [wTunicType]
        ld  hl, wCollectedTunics
        inc a

        cp  $01
        jr  nz, notTunic1
        bit 0, [HL]
        jr  nz, notTunic1
        inc a
notTunic1: 

        cp  $02
        jr  nz, notTunic2
        bit 1, [HL]
        jr  nz, notTunic2
        inc a
notTunic2: 

        cp  $03
        jr  nz, noWrap
        xor a
noWrap:

        ld  [wTunicType], a
        ret
TelephoneSpriteVariants:
        db $50, $00, $52, $00
        db $50, $02, $52, $02
        db $50, $03, $52, $03
    """, 0x6A7C), fill_nop=True)
