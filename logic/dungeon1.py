from .requirements import *
from .location import Location
from locations.all import *


class Dungeon1:
    def __init__(self, options, world_setup, r):
        entrance = Location("D1 Entrance", dungeon=1)
        entrance.add(DungeonChest(0x113), DungeonChest(0x115), DungeonChest(0x10E))
        Location(dungeon=1).add(DroppedKey(0x116)).connect(entrance, OR(r.enemy_requirements["HARDHAT_BEETLE"], r.push_hardhat), id="b9") # hardhat beetles (can kill with bomb)
        Location(dungeon=1).add(DungeonChest(0x10D)).connect(entrance, OR(r.enemy_requirements["MINI_MOLDORM"], SHIELD), id="ba") # moldorm spawn chest
        stalfos_keese_room = Location(dungeon=1).add(DungeonChest(0x114)).connect(entrance, AND(OR(r.enemy_requirements["STALFOS_EVASIVE"], SHIELD), r.enemy_requirements["KEESE"]), id="bb") # 2 stalfos 2 keese room
        Location(dungeon=1).add(DungeonChest(0x10C)).connect(entrance, BOMB, id="bc") # hidden seashell room
        dungeon1_upper_left = Location("D1 Upper Left", dungeon=1).connect(entrance, FOUND(KEY1, 3), id="bd")
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=1).add(OwlStatue(0x103), OwlStatue(0x104)).connect(dungeon1_upper_left, STONE_BEAK1, id="be")
        feather_chest = Location(dungeon=1).add(DungeonChest(0x11D)).connect(dungeon1_upper_left, OR(r.enemy_requirements["SPIKED_BEETLE"], SHIELD), id="bf")  # feather location, behind spike enemies. can shield bump into pit (only shield works)
        boss_key = Location(dungeon=1).add(DungeonChest(0x108)).connect(entrance, AND(FEATHER, FOUND(KEY1, 3)), id="bg") # boss key
        dungeon1_right_side = Location("D1 Right Side", dungeon=1).connect(entrance, FOUND(KEY1, 3), id="bh")
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=1).add(OwlStatue(0x10A)).connect(dungeon1_right_side, STONE_BEAK1, id="bi")
        dungeon1_3_of_a_kind = Location(dungeon=1).add(DungeonChest(0x10A)).connect(dungeon1_right_side, r.enemy_requirements["THREE_OF_A_KIND"], id="bj") # three of a kind, shield stops the suit from changing
        dungeon1_miniboss_room = Location("D1 Miniboss Room", dungeon=1).connect(dungeon1_right_side, FEATHER, id="bk")
        dungeon1_miniboss = Location("D1 After Miniboss", dungeon=1).connect(dungeon1_miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[0]], id="bl")
        dungeon1_boss_room = Location("D1 Boss Room", dungeon=1).connect(dungeon1_miniboss, NIGHTMARE_KEY1, id="bm")
        boss = Location(dungeon=1).add(HeartContainer(0x106), Instrument(0x102)).connect(dungeon1_boss_room, r.boss_requirements[world_setup.boss_mapping[0]], id="bn")

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            stalfos_keese_room.connect(entrance, r.enemy_requirements["KEESE"], id="bo") # stalfos jump away when you press a button.

        if options.logic == 'glitched' or options.logic == 'hell':
            boss_key.connect(entrance, r.super_jump_feather, id="bq")  # super jump
            dungeon1_miniboss_room.connect(dungeon1_right_side, OR(r.damage_boost, r.pit_buffer_itemless), id="br") # damage boost or buffer pause over the pit to cross or mushroom
        
        if options.logic == 'hell':
            feather_chest.connect(dungeon1_upper_left, SWORD, id="bs")  # keep slashing the spiked beetles until they keep moving 1 pixel close towards you and the pit, to get them to fall
            boss_key.connect(entrance, AND(r.damage_boost, FOUND(KEY1,3)), id="bt") # damage boost off the hardhat to cross the pit
            
        self.entrance = entrance
        self.final_room = boss


class NoDungeon1:
    def __init__(self, options, world_setup, r):
        entrance = Location("D1 Entrance", dungeon=1)
        Location(dungeon=1).add(HeartContainer(0x106), Instrument(0x102)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[0]])
        self.entrance = entrance
