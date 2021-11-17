from auto_splitter.coordinates import Coordinates

locations = [
    "Artaria",
    "Cataris",
    "Dairon",
    "Burenia",
    "Ghavoran",
    "Ferenia",
    "Elun",
    "Hanubia",
    "Itorash"
]

upgrades = [
    "Charge Beam",
    "Phantom Cloak",
    "Spider Magnet",
    "Wide Beam",
    "Morph Ball",
    "Varia Suit",
    "Diffusion Beam",
    "Grapple Beam",
    "Bomb",
    "Flash Shift",
    "Speed Booster",
    "Super Missile",
    "Plasma Beam",
    "Ice Missile",
    "Space Jump",
    "Screw Attack",
    "Gravity Suit",
    "Cross Bomb",
    "Storm Missile",
    "Wave Beam",
    "Power Bomb"
]

item_types = [
    "Missile Tank",
    "Missile+ Tank", 
    "Energy Tank"
]

def get_coordinates(x, y, scale):

    item_coords         = Coordinates(410,410,1500,670,x, y, scale)
    location_coords     = Coordinates(656,40,1263,130,x, y, scale)
    menu_coords = [
        Coordinates(392, 462, 1533, 507, x, y, scale),
        Coordinates(392, 605, 1533, 650, x, y, scale),
        Coordinates(392, 749, 1533, 794, x, y, scale)]

    return item_coords, location_coords, menu_coords