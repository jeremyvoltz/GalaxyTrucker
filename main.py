from ship import *
import csv

centers = ["tile_61.jpg", "tile_62.jpg", 
    "tile_63.jpg", "tile_64.jpg"]

tiles = [CrewTile([2,1,0,1], "tile_07.jpg"),
    CrewTile([2,1,2,2], "tile_08.jpg"),
    CrewTile([0,0,1,3], "tile_09.jpg"),
    CrewTile([0,1,0,3], "tile_10.jpg"),
    CargoTile([0,0,0,3], 2, "tile_28.jpg"),
    CargoTile([0,1,0,3], 2, "tile_30.jpg"),
    Tile([1,3,0,3], "tile_31.jpg"),
    Tile([1,3,1,3], "tile_32.jpg"),
    Tile([1,3,2,3], "tile_33.jpg"),
    Tile([2,3,0,3], "tile_34.jpg"),
    Tile([1,3,0,3], "tile_31.jpg"),
    CargoTile([0,1,0,2], 3, "tile_52.jpg"),
    EngineTile([0,3,0,0], "tile_58.jpg"),
    EngineTile([1,0,0,0], "tile_60.jpg"),
    EngineTile([1,1,0,0], "tile_67.jpg"),
    EngineTile([2,0,0,0], "tile_68.jpg"),
    EngineTile([2,0,0,0], "tile_69.jpg"),
    EngineTile([0,2,3,0], "tile_70.jpg"),
    EngineTile([3,2,0,0], "tile_71.jpg"),
    EngineTile([0,3,0,2], "tile_72.jpg"),
    EngineTile([3,0,0,1], "tile_73.jpg"),
    EngineTile([1,2,0,2], "tile_74.jpg"),
    EngineTile([2,0,0,2], "tile_75.jpg"),
    EngineTile([3,1,0,2], "tile_76.jpg"),
    LaserTile([0,0,1,0], "tile_100.jpg"),
    LaserTile([0,0,1,0], "tile_101.jpg"),
    LaserTile([0,0,2,0], "tile_102.jpg"),
    LaserTile([0,0,2,3], "tile_103.jpg"),
    LaserTile([0,1,0,3], "tile_104.jpg"),
    LaserTile([0,1,2,0], "tile_110.jpg"),
    LaserTile([0,3,0,0], "tile_113.jpg")]

