"""
Seed database with realistic global data:
- 56 airlines
- 180 airports across 6 continents
- 3 aircraft types with proper seat maps
- 300+ routes (realistic hub-and-spoke + point-to-point)
- Flights for next 14 days on every route

Run: python seed_data.py
"""

from datetime import datetime, timedelta
import random
from app.db.session import SessionLocal
from app.models.user import User
from app.models.airline import Airline
from app.models.airport import Airport
from app.models.aircraft import Aircraft
from app.models.route import Route
from app.models.flight import Flight
from app.core.security import hash_password

# ── AIRLINES (56) ──────────────────────────────────────────────────────────
AIRLINES_DATA = [
    # North America
    ("American Airlines",        "AA",  1.2),
    ("Delta Air Lines",          "DL",  1.15),
    ("United Airlines",          "UA",  1.1),
    ("Southwest Airlines",       "WN",  0.85),
    ("JetBlue Airways",          "B6",  0.95),
    ("Alaska Airlines",          "AS",  1.0),
    ("Spirit Airlines",          "NK",  0.70),
    ("Frontier Airlines",        "F9",  0.72),
    ("Sun Country Airlines",     "SY",  0.80),
    ("Hawaiian Airlines",        "HA",  1.05),
    # Europe
    ("British Airways",          "BA",  1.35),
    ("Lufthansa",                "LH",  1.30),
    ("Air France",               "AF",  1.25),
    ("KLM Royal Dutch",          "KL",  1.20),
    ("Swiss International",      "LX",  1.40),
    ("Austrian Airlines",        "OS",  1.15),
    ("Iberia",                   "IB",  1.10),
    ("Alitalia",                 "AZ",  1.05),
    ("Turkish Airlines",         "TK",  1.10),
    ("Ryanair",                  "FR",  0.65),
    ("EasyJet",                  "U2",  0.70),
    ("Wizz Air",                 "W6",  0.68),
    ("Norwegian Air",            "DY",  0.75),
    ("Vueling",                  "VY",  0.80),
    ("Aer Lingus",               "EI",  0.90),
    # Middle East & Africa
    ("Emirates",                 "EK",  1.50),
    ("Qatar Airways",            "QR",  1.45),
    ("Etihad Airways",           "EY",  1.40),
    ("Fly Dubai",                "FZ",  0.85),
    ("Air Arabia",               "G9",  0.75),
    ("Ethiopian Airlines",       "ET",  1.05),
    ("EgyptAir",                 "MS",  0.90),
    ("South African Airways",    "SA",  1.00),
    ("Kenya Airways",            "KQ",  0.95),
    ("Royal Air Maroc",          "AT",  0.88),
    # Asia Pacific
    ("Singapore Airlines",       "SQ",  1.55),
    ("Cathay Pacific",           "CX",  1.45),
    ("Japan Airlines",           "JL",  1.40),
    ("ANA All Nippon",           "NH",  1.35),
    ("Korean Air",               "KE",  1.30),
    ("Asiana Airlines",          "OZ",  1.20),
    ("Thai Airways",             "TG",  1.15),
    ("Malaysia Airlines",        "MH",  1.10),
    ("Garuda Indonesia",         "GA",  1.05),
    ("Philippine Airlines",      "PR",  1.00),
    ("IndiGo",                   "6E",  0.80),
    ("Air India",                "AI",  0.95),
    ("SpiceJet",                 "SG",  0.72),
    ("Vietjet Air",              "VJ",  0.75),
    ("AirAsia",                  "AK",  0.70),
    # South America & Oceania
    ("LATAM Airlines",           "LA",  1.05),
    ("Avianca",                  "AV",  1.00),
    ("Copa Airlines",            "CM",  1.10),
    ("Aeromexico",               "AM",  1.00),
    ("Qantas",                   "QF",  1.35),
    ("Air New Zealand",          "NZ",  1.30),
]

# ── AIRPORTS (180) ──────────────────────────────────────────────────────────
# (name, city, country, iata, is_hub)
AIRPORTS_DATA = [
    # North America – USA (40)
    ("John F. Kennedy International",        "New York",      "USA", "JFK", True),
    ("Los Angeles International",            "Los Angeles",   "USA", "LAX", True),
    ("O'Hare International",                 "Chicago",       "USA", "ORD", True),
    ("Hartsfield-Jackson Atlanta",           "Atlanta",       "USA", "ATL", True),
    ("Dallas Fort Worth International",      "Dallas",        "USA", "DFW", True),
    ("Denver International",                 "Denver",        "USA", "DEN", True),
    ("San Francisco International",          "San Francisco", "USA", "SFO", True),
    ("Seattle-Tacoma International",         "Seattle",       "USA", "SEA", True),
    ("Miami International",                  "Miami",         "USA", "MIA", True),
    ("Orlando International",                "Orlando",       "USA", "MCO", False),
    ("Boston Logan International",           "Boston",        "USA", "BOS", True),
    ("Washington Dulles International",      "Washington DC", "USA", "IAD", True),
    ("Minneapolis Saint Paul International", "Minneapolis",   "USA", "MSP", False),
    ("Phoenix Sky Harbor International",     "Phoenix",       "USA", "PHX", False),
    ("Detroit Metropolitan",                 "Detroit",       "USA", "DTW", False),
    ("Newark Liberty International",         "Newark",        "USA", "EWR", True),
    ("Charlotte Douglas International",      "Charlotte",     "USA", "CLT", False),
    ("Las Vegas Harry Reid International",   "Las Vegas",     "USA", "LAS", False),
    ("Portland International",               "Portland",      "USA", "PDX", False),
    ("Salt Lake City International",         "Salt Lake City","USA", "SLC", False),
    ("San Diego International",              "San Diego",     "USA", "SAN", False),
    ("Tampa International",                  "Tampa",         "USA", "TPA", False),
    ("Houston George Bush Intercontinental", "Houston",       "USA", "IAH", True),
    ("Baltimore Washington International",   "Baltimore",     "USA", "BWI", False),
    ("Austin Bergstrom International",       "Austin",        "USA", "AUS", False),
    ("Nashville International",              "Nashville",     "USA", "BNA", False),
    ("Raleigh Durham International",         "Raleigh",       "USA", "RDU", False),
    ("Kansas City International",            "Kansas City",   "USA", "MCI", False),
    ("Indianapolis International",           "Indianapolis",  "USA", "IND", False),
    ("Pittsburgh International",             "Pittsburgh",    "USA", "PIT", False),
    ("Honolulu Daniel K. Inouye International","Honolulu",    "USA", "HNL", False),
    ("Cincinnati Northern Kentucky International","Cincinnati","USA","CVG", False),
    ("Cleveland Hopkins International",      "Cleveland",     "USA", "CLE", False),
    ("St. Louis Lambert International",      "St. Louis",     "USA", "STL", False),
    ("Sacramento International",             "Sacramento",    "USA", "SMF", False),
    ("San Jose International",               "San Jose",      "USA", "SJC", False),
    ("Oakland International",                "Oakland",       "USA", "OAK", False),
    ("Tucson International",                 "Tucson",        "USA", "TUS", False),
    ("Albuquerque International Sunport",    "Albuquerque",   "USA", "ABQ", False),
    ("El Paso International",                "El Paso",       "USA", "ELP", False),
    # Canada (5)
    ("Toronto Pearson International",        "Toronto",       "Canada", "YYZ", True),
    ("Vancouver International",              "Vancouver",     "Canada", "YVR", True),
    ("Montreal Trudeau International",       "Montreal",      "Canada", "YUL", False),
    ("Calgary International",               "Calgary",       "Canada", "YYC", False),
    ("Edmonton International",               "Edmonton",      "Canada", "YEG", False),
    # Mexico & Central America (5)
    ("Mexico City Benito Juarez International","Mexico City", "Mexico",     "MEX", True),
    ("Cancun International",                 "Cancun",        "Mexico",     "CUN", False),
    ("Guadalajara Miguel Hidalgo International","Guadalajara","Mexico",     "GDL", False),
    ("El Salvador International",            "San Salvador",  "El Salvador","SAL", False),
    ("Costa Rica Juan Santamaria International","San Jose",   "Costa Rica", "SJO", False),
    # Caribbean & South America (10)
    ("Bogota El Dorado International",       "Bogota",        "Colombia",   "BOG", True),
    ("Sao Paulo Guarulhos International",    "Sao Paulo",     "Brazil",     "GRU", True),
    ("Rio de Janeiro Galeao International",  "Rio de Janeiro","Brazil",     "GIG", False),
    ("Buenos Aires Ezeiza International",    "Buenos Aires",  "Argentina",  "EZE", True),
    ("Lima Jorge Chavez International",      "Lima",          "Peru",       "LIM", False),
    ("Santiago Arturo Merino Benitez",       "Santiago",      "Chile",      "SCL", False),
    ("Caracas Simon Bolivar International",  "Caracas",       "Venezuela",  "CCS", False),
    ("Panama City Tocumen International",    "Panama City",   "Panama",     "PTY", True),
    ("Quito Mariscal Sucre International",   "Quito",         "Ecuador",    "UIO", False),
    ("Havana Jose Marti International",      "Havana",        "Cuba",       "HAV", False),
    # Europe (40)
    ("London Heathrow",                      "London",        "UK",          "LHR", True),
    ("London Gatwick",                       "London",        "UK",          "LGW", False),
    ("Paris Charles de Gaulle",              "Paris",         "France",      "CDG", True),
    ("Paris Orly",                           "Paris",         "France",      "ORY", False),
    ("Frankfurt International",              "Frankfurt",     "Germany",     "FRA", True),
    ("Munich International",                 "Munich",        "Germany",     "MUC", True),
    ("Amsterdam Schiphol",                   "Amsterdam",     "Netherlands", "AMS", True),
    ("Madrid Barajas International",         "Madrid",        "Spain",       "MAD", True),
    ("Barcelona El Prat",                    "Barcelona",     "Spain",       "BCN", False),
    ("Rome Fiumicino",                       "Rome",          "Italy",       "FCO", True),
    ("Milan Malpensa",                       "Milan",         "Italy",       "MXP", False),
    ("Zurich International",                 "Zurich",        "Switzerland", "ZRH", True),
    ("Vienna International",                 "Vienna",        "Austria",     "VIE", True),
    ("Brussels International",              "Brussels",       "Belgium",     "BRU", False),
    ("Copenhagen International",             "Copenhagen",    "Denmark",     "CPH", False),
    ("Stockholm Arlanda",                    "Stockholm",     "Sweden",      "ARN", False),
    ("Oslo Gardermoen",                      "Oslo",          "Norway",      "OSL", False),
    ("Helsinki Vantaa",                      "Helsinki",      "Finland",     "HEL", False),
    ("Warsaw Chopin International",          "Warsaw",        "Poland",      "WAW", False),
    ("Prague Vaclav Havel International",    "Prague",        "Czech Republic","PRG",False),
    ("Budapest Liszt Ferenc International",  "Budapest",      "Hungary",     "BUD", False),
    ("Bucharest Henri Coanda International", "Bucharest",     "Romania",     "OTP", False),
    ("Athens Eleftherios Venizelos",         "Athens",        "Greece",      "ATH", False),
    ("Istanbul Ataturk International",       "Istanbul",      "Turkey",      "IST", True),
    ("Lisbon Humberto Delgado International","Lisbon",        "Portugal",    "LIS", False),
    ("Dublin International",                 "Dublin",        "Ireland",     "DUB", False),
    ("Kyiv Boryspil International",          "Kyiv",          "Ukraine",     "KBP", False),
    ("Moscow Sheremetyevo",                  "Moscow",        "Russia",      "SVO", True),
    ("St. Petersburg Pulkovo",               "St. Petersburg","Russia",      "LED", False),
    ("Geneva International",                 "Geneva",        "Switzerland", "GVA", False),
    ("Nice Cote d'Azur International",       "Nice",          "France",      "NCE", False),
    ("Lyon Saint-Exupery International",     "Lyon",          "France",      "LYS", False),
    ("Dusseldorf International",             "Dusseldorf",    "Germany",     "DUS", False),
    ("Berlin Brandenburg International",    "Berlin",        "Germany",     "BER", False),
    ("Hamburg International",               "Hamburg",       "Germany",     "HAM", False),
    ("Manchester International",             "Manchester",    "UK",          "MAN", False),
    ("Edinburgh International",             "Edinburgh",     "UK",          "EDI", False),
    ("Palma de Mallorca International",      "Palma",         "Spain",       "PMI", False),
    ("Malaga Costa del Sol International",   "Malaga",        "Spain",       "AGP", False),
    ("Catania Fontanarossa International",   "Catania",       "Italy",       "CTA", False),
    # Middle East (10)
    ("Dubai International",                  "Dubai",         "UAE",         "DXB", True),
    ("Abu Dhabi International",              "Abu Dhabi",     "UAE",         "AUH", True),
    ("Doha Hamad International",             "Doha",          "Qatar",       "DOH", True),
    ("Riyadh King Khalid International",     "Riyadh",        "Saudi Arabia","RUH", True),
    ("Jeddah King Abdulaziz International",  "Jeddah",        "Saudi Arabia","JED", False),
    ("Kuwait International",                 "Kuwait City",   "Kuwait",      "KWI", False),
    ("Bahrain International",               "Manama",        "Bahrain",     "BAH", False),
    ("Muscat International",                 "Muscat",        "Oman",        "MCT", False),
    ("Beirut Rafic Hariri International",    "Beirut",        "Lebanon",     "BEY", False),
    ("Amman Queen Alia International",       "Amman",         "Jordan",      "AMM", False),
    # Africa (10)
    ("Johannesburg O.R. Tambo International","Johannesburg",  "South Africa","JNB", True),
    ("Cairo International",                  "Cairo",         "Egypt",       "CAI", True),
    ("Addis Ababa Bole International",       "Addis Ababa",   "Ethiopia",    "ADD", True),
    ("Nairobi Jomo Kenyatta International",  "Nairobi",       "Kenya",       "NBO", False),
    ("Lagos Murtala Muhammed International", "Lagos",         "Nigeria",     "LOS", False),
    ("Casablanca Mohammed V International",  "Casablanca",    "Morocco",     "CMN", False),
    ("Cape Town International",              "Cape Town",     "South Africa","CPT", False),
    ("Accra Kotoka International",           "Accra",         "Ghana",       "ACC", False),
    ("Tunis Carthage International",         "Tunis",         "Tunisia",     "TUN", False),
    ("Dakar Blaise Diagne International",    "Dakar",         "Senegal",     "DSS", False),
    # South Asia (10)
    ("New Delhi Indira Gandhi International","New Delhi",     "India",       "DEL", True),
    ("Mumbai Chhatrapati Shivaji International","Mumbai",     "India",       "BOM", True),
    ("Bangalore Kempegowda International",   "Bangalore",     "India",       "BLR", False),
    ("Chennai International",               "Chennai",       "India",       "MAA", False),
    ("Hyderabad Rajiv Gandhi International", "Hyderabad",     "India",       "HYD", False),
    ("Kolkata Netaji Subhas Chandra Bose",   "Kolkata",       "India",       "CCU", False),
    ("Lahore Allama Iqbal International",    "Lahore",        "Pakistan",    "LHE", False),
    ("Karachi Jinnah International",         "Karachi",       "Pakistan",    "KHI", False),
    ("Dhaka Hazrat Shahjalal International", "Dhaka",         "Bangladesh",  "DAC", False),
    ("Chittagong Shah Amanat International",  "Chittagong",    "Bangladesh",  "CGP", False),
    # East & Southeast Asia (20)
    ("Beijing Capital International",        "Beijing",       "China",       "PEK", True),
    ("Shanghai Pudong International",        "Shanghai",      "China",       "PVG", True),
    ("Guangzhou Baiyun International",       "Guangzhou",     "China",       "CAN", False),
    ("Shenzhen Bao'an International",        "Shenzhen",      "China",       "SZX", False),
    ("Chengdu Tianfu International",         "Chengdu",       "China",       "TFU", False),
    ("Tokyo Narita International",           "Tokyo",         "Japan",       "NRT", True),
    ("Tokyo Haneda International",           "Tokyo",         "Japan",       "HND", True),
    ("Osaka Kansai International",           "Osaka",         "Japan",       "KIX", False),
    ("Seoul Incheon International",          "Seoul",         "South Korea", "ICN", True),
    ("Taipei Taiwan Taoyuan International",  "Taipei",        "Taiwan",      "TPE", False),
    ("Hong Kong International",              "Hong Kong",     "Hong Kong",   "HKG", True),
    ("Singapore Changi International",       "Singapore",     "Singapore",   "SIN", True),
    ("Kuala Lumpur International",           "Kuala Lumpur",  "Malaysia",    "KUL", True),
    ("Bangkok Suvarnabhumi International",   "Bangkok",       "Thailand",    "BKK", True),
    ("Jakarta Soekarno Hatta International", "Jakarta",       "Indonesia",   "CGK", True),
    ("Manila Ninoy Aquino International",    "Manila",        "Philippines", "MNL", False),
    ("Ho Chi Minh City Tan Son Nhat",        "Ho Chi Minh City","Vietnam",   "SGN", False),
    ("Hanoi Noi Bai International",          "Hanoi",         "Vietnam",     "HAN", False),
    ("Yangon International",                 "Yangon",        "Myanmar",     "RGN", False),
    ("Phnom Penh International",             "Phnom Penh",    "Cambodia",    "PNH", False),
    # Oceania (5)
    ("Sydney Kingsford Smith International", "Sydney",        "Australia",   "SYD", True),
    ("Melbourne Tullamarine International",  "Melbourne",     "Australia",   "MEL", True),
    ("Brisbane International",               "Brisbane",      "Australia",   "BNE", False),
    ("Perth International",                  "Perth",         "Australia",   "PER", False),
    ("Auckland International",               "Auckland",      "New Zealand", "AKL", False),
    # Extra airports to reach 180+ ──
    ("Bali Ngurah Rai International",        "Bali",          "Indonesia",   "DPS", False),
    ("Phuket International",                 "Phuket",        "Thailand",    "HKT", False),
    ("Chiang Mai International",             "Chiang Mai",    "Thailand",    "CNX", False),
    ("Fukuoka International",               "Fukuoka",       "Japan",       "FUK", False),
    ("Sapporo New Chitose International",    "Sapporo",       "Japan",       "CTS", False),
    ("Nagoya Chubu Centrair International",  "Nagoya",        "Japan",       "NGO", False),
    ("Busan Gimhae International",           "Busan",         "South Korea", "PUS", False),
    ("Macau International",                  "Macau",         "Macau",       "MFM", False),
    ("Chongqing Jiangbei International",     "Chongqing",     "China",       "CKG", False),
    ("Xi'an Xianyang International",         "Xi'an",         "China",       "XIY", False),
    ("Kathmandu Tribhuvan International",    "Kathmandu",     "Nepal",       "KTM", False),
    ("Islamabad New International",          "Islamabad",     "Pakistan",    "ISB", False),
    ("Colombo Bandaranaike International",   "Colombo",       "Sri Lanka",   "CMB", False),
    ("Male Velana International",            "Male",          "Maldives",    "MLE", False),
    ("Sana'a International",                 "Sana'a",        "Yemen",       "SAH", False),
    ("Tbilisi Shota Rustaveli International","Tbilisi",       "Georgia",     "TBS", False),
    ("Baku Heydar Aliyev International",     "Baku",          "Azerbaijan",  "GYD", False),
    ("Almaty International",                 "Almaty",        "Kazakhstan",  "ALA", False),
    ("Tashkent International",               "Tashkent",      "Uzbekistan",  "TAS", False),
    ("Khartoum International",               "Khartoum",      "Sudan",       "KRT", False),
    ("Dar es Salaam Julius Nyerere International","Dar es Salaam","Tanzania", "DAR", False),
    ("Abidjan Felix Houphouet-Boigny",       "Abidjan",       "Ivory Coast", "ABJ", False),
    ("Maputo International",                 "Maputo",        "Mozambique",  "MPM", False),
    ("Lusaka Kenneth Kaunda International",  "Lusaka",        "Zambia",      "LUN", False),
    ("Harare Robert Mugabe International",   "Harare",        "Zimbabwe",    "HRE", False),
]

# ── AIRCRAFT SEAT MAPS ───────────────────────────────────────────────────────
def make_seat_map_737():
    """Boeing 737-800: 162 seats, 3-3 layout, rows 1-27"""
    rows = []
    for i in range(1, 28):
        rows.append({
            "row_number": i,
            "class": "business" if i <= 4 else "economy",
            "seats": [
                {"number": f"{i}A", "type": "window",  "premium": i <= 4},
                {"number": f"{i}B", "type": "middle",  "premium": False},
                {"number": f"{i}C", "type": "aisle",   "premium": i <= 4},
                {"number": f"{i}D", "type": "aisle",   "premium": i <= 4},
                {"number": f"{i}E", "type": "middle",  "premium": False},
                {"number": f"{i}F", "type": "window",  "premium": i <= 4},
            ]
        })
    return {"layout": "3-3", "rows": rows}

def make_seat_map_a320():
    """Airbus A320: 150 seats, 3-3 layout, rows 1-25"""
    rows = []
    for i in range(1, 26):
        rows.append({
            "row_number": i,
            "class": "business" if i <= 3 else "economy",
            "seats": [
                {"number": f"{i}A", "type": "window",  "premium": i <= 3},
                {"number": f"{i}B", "type": "middle",  "premium": False},
                {"number": f"{i}C", "type": "aisle",   "premium": i <= 3},
                {"number": f"{i}D", "type": "aisle",   "premium": i <= 3},
                {"number": f"{i}E", "type": "middle",  "premium": False},
                {"number": f"{i}F", "type": "window",  "premium": i <= 3},
            ]
        })
    return {"layout": "3-3", "rows": rows}

def make_seat_map_777():
    """Boeing 777-300ER: 396 seats, 3-4-3 layout, rows 1-44"""
    rows = []
    for i in range(1, 45):
        if i <= 6:
            cls = "first"
            seats = [
                {"number": f"{i}A", "type": "window",  "premium": True},
                {"number": f"{i}B", "type": "aisle",   "premium": True},
                {"number": f"{i}C", "type": "aisle",   "premium": True},
                {"number": f"{i}D", "type": "window",  "premium": True},
            ]
        elif i <= 16:
            cls = "business"
            seats = [
                {"number": f"{i}A", "type": "window",  "premium": True},
                {"number": f"{i}B", "type": "middle",  "premium": True},
                {"number": f"{i}C", "type": "aisle",   "premium": True},
                {"number": f"{i}D", "type": "aisle",   "premium": True},
                {"number": f"{i}E", "type": "middle",  "premium": True},
                {"number": f"{i}F", "type": "window",  "premium": True},
            ]
        else:
            cls = "economy"
            seats = [
                {"number": f"{i}A", "type": "window",  "premium": False},
                {"number": f"{i}B", "type": "middle",  "premium": False},
                {"number": f"{i}C", "type": "aisle",   "premium": False},
                {"number": f"{i}D", "type": "aisle",   "premium": False},
                {"number": f"{i}E", "type": "middle",  "premium": False},
                {"number": f"{i}F", "type": "aisle",   "premium": False},
                {"number": f"{i}G", "type": "middle",  "premium": False},
                {"number": f"{i}H", "type": "middle",  "premium": False},
                {"number": f"{i}J", "type": "window",  "premium": False},
            ]
        rows.append({"row_number": i, "class": cls, "seats": seats})
    return {"layout": "3-4-3", "rows": rows}


# ── ROUTES (hub-and-spoke + popular point-to-point) ──────────────────────────
# Routes are defined as (origin_iata, dest_iata, distance_km)
ROUTES_DATA = [
    # ── NORTH AMERICA DOMESTIC ──
    ("JFK", "LAX", 3944), ("LAX", "JFK", 3944),
    ("JFK", "LHR", 5541), ("LHR", "JFK", 5541),
    ("JFK", "CDG", 5836), ("CDG", "JFK", 5836),
    ("JFK", "MIA", 1757), ("MIA", "JFK", 1757),
    ("JFK", "ORD", 1185), ("ORD", "JFK", 1185),
    ("JFK", "BOS", 297),  ("BOS", "JFK", 297),
    ("JFK", "ATL", 1232), ("ATL", "JFK", 1232),
    ("JFK", "DFW", 2303), ("DFW", "JFK", 2303),
    ("JFK", "SFO", 4139), ("SFO", "JFK", 4139),
    ("JFK", "IAD", 361),  ("IAD", "JFK", 361),
    ("LAX", "SFO", 559),  ("SFO", "LAX", 559),
    ("LAX", "SEA", 1535), ("SEA", "LAX", 1535),
    ("LAX", "DEN", 1387), ("DEN", "LAX", 1387),
    ("LAX", "ORD", 2808), ("ORD", "LAX", 2808),
    ("LAX", "MIA", 3757), ("MIA", "LAX", 3757),
    ("LAX", "DFW", 1997), ("DFW", "LAX", 1997),
    ("LAX", "ATL", 3108), ("ATL", "LAX", 3108),
    ("LAX", "PHX", 599),  ("PHX", "LAX", 599),
    ("LAX", "LAS", 435),  ("LAS", "LAX", 435),
    ("ORD", "DFW", 1452), ("DFW", "ORD", 1452),
    ("ORD", "ATL", 975),  ("ATL", "ORD", 975),
    ("ORD", "MIA", 2209), ("MIA", "ORD", 2209),
    ("ORD", "DEN", 1475), ("DEN", "ORD", 1475),
    ("ORD", "SEA", 2784), ("SEA", "ORD", 2784),
    ("ATL", "DFW", 1150), ("DFW", "ATL", 1150),
    ("ATL", "MIA", 1094), ("MIA", "ATL", 1094),
    ("ATL", "BOS", 1507), ("BOS", "ATL", 1507),
    ("ATL", "IAH", 1160), ("IAH", "ATL", 1160),
    ("DFW", "DEN", 1059), ("DEN", "DFW", 1059),
    ("DFW", "IAH", 362),  ("IAH", "DFW", 362),
    ("DFW", "PHX", 1445), ("PHX", "DFW", 1445),
    ("SFO", "SEA", 1094), ("SEA", "SFO", 1094),
    ("SFO", "DEN", 1905), ("DEN", "SFO", 1905),
    ("SFO", "ORD", 2963), ("ORD", "SFO", 2963),
    ("DEN", "SEA", 1635), ("SEA", "DEN", 1635),
    ("DEN", "PHX", 942),  ("PHX", "DEN", 942),
    ("BOS", "IAD", 633),  ("IAD", "BOS", 633),
    ("BOS", "ORD", 1580), ("ORD", "BOS", 1580),
    ("MIA", "IAH", 1554), ("IAH", "MIA", 1554),
    ("MIA", "CUN", 528),  ("CUN", "MIA", 528),
    ("MIA", "BOG", 2587), ("BOG", "MIA", 2587),
    ("MIA", "GRU", 6607), ("GRU", "MIA", 6607),
    ("MIA", "EZE", 7243), ("EZE", "MIA", 7243),
    ("IAH", "MEX", 1085), ("MEX", "IAH", 1085),
    ("IAH", "BOG", 3104), ("BOG", "IAH", 3104),
    ("LAX", "MEX", 2485), ("MEX", "LAX", 2485),
    ("YYZ", "JFK", 569),  ("JFK", "YYZ", 569),
    ("YYZ", "LHR", 5724), ("LHR", "YYZ", 5724),
    ("YYZ", "CDG", 6022), ("CDG", "YYZ", 6022),
    ("YYZ", "YVR", 3362), ("YVR", "YYZ", 3362),
    ("YVR", "SEA", 229),  ("SEA", "YVR", 229),
    ("YVR", "LAX", 1742), ("LAX", "YVR", 1742),
    ("YUL", "YYZ", 542),  ("YYZ", "YUL", 542),
    # ── TRANSATLANTIC ──
    ("LHR", "LAX", 8757), ("LAX", "LHR", 8757),
    ("LHR", "ORD", 6347), ("ORD", "LHR", 6347),
    ("LHR", "ATL", 6997), ("ATL", "LHR", 6997),
    ("LHR", "MIA", 7126), ("MIA", "LHR", 7126),
    ("LHR", "IAD", 5918), ("IAD", "LHR", 5918),
    ("LHR", "BOS", 5264), ("BOS", "LHR", 5264),
    ("CDG", "LAX", 9124), ("LAX", "CDG", 9124),
    ("CDG", "IAD", 6178), ("IAD", "CDG", 6178),
    ("CDG", "BOS", 5523), ("BOS", "CDG", 5523),
    ("FRA", "JFK", 6197), ("JFK", "FRA", 6197),
    ("FRA", "IAD", 6800), ("IAD", "FRA", 6800),
    ("FRA", "ORD", 7587), ("ORD", "FRA", 7587),
    ("AMS", "JFK", 5855), ("JFK", "AMS", 5855),
    ("AMS", "IAD", 6207), ("IAD", "AMS", 6207),
    ("MUC", "JFK", 6452), ("JFK", "MUC", 6452),
    ("MUC", "IAD", 7032), ("IAD", "MUC", 7032),
    ("ZRH", "JFK", 6327), ("JFK", "ZRH", 6327),
    ("MAD", "JFK", 5765), ("JFK", "MAD", 5765),
    ("MAD", "MIA", 7290), ("MIA", "MAD", 7290),
    ("LIS", "JFK", 5448), ("JFK", "LIS", 5448),
    ("DUB", "JFK", 5134), ("JFK", "DUB", 5134),
    ("VIE", "JFK", 6783), ("JFK", "VIE", 6783),
    ("IST", "JFK", 9375), ("JFK", "IST", 9375),
    ("IST", "ORD", 9596), ("ORD", "IST", 9596),
    # ── EUROPE INTRA ──
    ("LHR", "CDG", 340),  ("CDG", "LHR", 340),
    ("LHR", "AMS", 369),  ("AMS", "LHR", 369),
    ("LHR", "FRA", 638),  ("FRA", "LHR", 638),
    ("LHR", "MAD", 1258), ("MAD", "LHR", 1258),
    ("LHR", "FCO", 1433), ("FCO", "LHR", 1433),
    ("LHR", "BCN", 1139), ("BCN", "LHR", 1139),
    ("LHR", "ZRH", 776),  ("ZRH", "LHR", 776),
    ("LHR", "DUB", 449),  ("DUB", "LHR", 449),
    ("LHR", "MUC", 919),  ("MUC", "LHR", 919),
    ("LHR", "ARN", 1446), ("ARN", "LHR", 1446),
    ("CDG", "FRA", 477),  ("FRA", "CDG", 477),
    ("CDG", "AMS", 425),  ("AMS", "CDG", 425),
    ("CDG", "MAD", 1054), ("MAD", "CDG", 1054),
    ("CDG", "FCO", 1107), ("FCO", "CDG", 1107),
    ("CDG", "BCN", 832),  ("BCN", "CDG", 832),
    ("CDG", "IST", 2243), ("IST", "CDG", 2243),
    ("FRA", "AMS", 368),  ("AMS", "FRA", 368),
    ("FRA", "MAD", 1437), ("MAD", "FRA", 1437),
    ("FRA", "FCO", 1048), ("FCO", "FRA", 1048),
    ("FRA", "ZRH", 258),  ("ZRH", "FRA", 258),
    ("FRA", "VIE", 600),  ("VIE", "FRA", 600),
    ("FRA", "IST", 2256), ("IST", "FRA", 2256),
    ("FRA", "ATH", 1806), ("ATH", "FRA", 1806),
    ("AMS", "BCN", 1249), ("BCN", "AMS", 1249),
    ("AMS", "FCO", 1472), ("FCO", "AMS", 1472),
    ("AMS", "VIE", 936),  ("VIE", "AMS", 936),
    ("MAD", "BCN", 483),  ("BCN", "MAD", 483),
    ("MAD", "FCO", 1360), ("FCO", "MAD", 1360),
    ("MAD", "LIS", 624),  ("LIS", "MAD", 624),
    ("FCO", "ATH", 1052), ("ATH", "FCO", 1052),
    ("FCO", "IST", 1374), ("IST", "FCO", 1374),
    ("MUC", "VIE", 326),  ("VIE", "MUC", 326),
    ("MUC", "ZRH", 314),  ("ZRH", "MUC", 314),
    ("MUC", "FCO", 703),  ("FCO", "MUC", 703),
    ("IST", "ATH", 853),  ("ATH", "IST", 853),
    ("IST", "DXB", 2590), ("DXB", "IST", 2590),
    # ── MIDDLE EAST HUB ──
    ("DXB", "LHR", 5490), ("LHR", "DXB", 5490),
    ("DXB", "CDG", 5246), ("CDG", "DXB", 5246),
    ("DXB", "FRA", 4811), ("FRA", "DXB", 4811),
    ("DXB", "JFK", 11041),("JFK", "DXB", 11041),
    ("DXB", "LAX", 13420),("LAX", "DXB", 13420),
    ("DXB", "SIN", 5840), ("SIN", "DXB", 5840),
    ("DXB", "BKK", 4898), ("BKK", "DXB", 4898),
    ("DXB", "KUL", 5534), ("KUL", "DXB", 5534),
    ("DXB", "PEK", 6866), ("PEK", "DXB", 6866),
    ("DXB", "DEL", 2197), ("DEL", "DXB", 2197),
    ("DXB", "BOM", 1920), ("BOM", "DXB", 1920),
    ("DXB", "CGK", 7174), ("CGK", "DXB", 7174),
    ("DXB", "NRT", 7959), ("NRT", "DXB", 7959),
    ("DXB", "SYD", 11822),("SYD", "DXB", 11822),
    ("DXB", "JNB", 6374), ("JNB", "DXB", 6374),
    ("DXB", "ADD", 3229), ("ADD", "DXB", 3229),
    ("DXB", "CAI", 2204), ("CAI", "DXB", 2204),
    ("DOH", "LHR", 5724), ("LHR", "DOH", 5724),
    ("DOH", "JFK", 11136),("JFK", "DOH", 11136),
    ("DOH", "CDG", 5247), ("CDG", "DOH", 5247),
    ("DOH", "SIN", 5892), ("SIN", "DOH", 5892),
    ("DOH", "BKK", 5906), ("BKK", "DOH", 5906),
    ("DOH", "DEL", 2338), ("DEL", "DOH", 2338),
    ("DOH", "BOM", 2122), ("BOM", "DOH", 2122),
    ("AUH", "LHR", 5514), ("LHR", "AUH", 5514),
    ("AUH", "JFK", 11019),("JFK", "AUH", 11019),
    ("AUH", "SIN", 5841), ("SIN", "AUH", 5841),
    # ── ASIA INTRA & LONG HAUL ──
    ("SIN", "LHR", 10841),("LHR", "SIN", 10841),
    ("SIN", "SYD", 6310), ("SYD", "SIN", 6310),
    ("SIN", "NRT", 5361), ("NRT", "SIN", 5361),
    ("SIN", "ICN", 4687), ("ICN", "SIN", 4687),
    ("SIN", "HKG", 2574), ("HKG", "SIN", 2574),
    ("SIN", "PVG", 4059), ("PVG", "SIN", 4059),
    ("SIN", "PEK", 4463), ("PEK", "SIN", 4463),
    ("SIN", "BKK", 1432), ("BKK", "SIN", 1432),
    ("SIN", "KUL", 298),  ("KUL", "SIN", 298),
    ("SIN", "CGK", 898),  ("CGK", "SIN", 898),
    ("SIN", "MNL", 2396), ("MNL", "SIN", 2396),
    ("SIN", "DEL", 4163), ("DEL", "SIN", 4163),
    ("SIN", "BOM", 3951), ("BOM", "SIN", 3951),
    ("NRT", "LAX", 8748), ("LAX", "NRT", 8748),
    ("NRT", "JFK", 10836),("JFK", "NRT", 10836),
    ("NRT", "LHR", 9559), ("LHR", "NRT", 9559),
    ("NRT", "SYD", 7823), ("SYD", "NRT", 7823),
    ("NRT", "ICN", 1156), ("ICN", "NRT", 1156),
    ("NRT", "HKG", 2884), ("HKG", "NRT", 2884),
    ("NRT", "PEK", 2086), ("PEK", "NRT", 2086),
    ("NRT", "PVG", 1760), ("PVG", "NRT", 1760),
    ("NRT", "BKK", 4573), ("BKK", "NRT", 4573),
    ("HND", "ICN", 1161), ("ICN", "HND", 1161),
    ("HND", "PEK", 2091), ("PEK", "HND", 2091),
    ("HND", "HKG", 2897), ("HKG", "HND", 2897),
    ("ICN", "LAX", 9608), ("LAX", "ICN", 9608),
    ("ICN", "JFK", 11085),("JFK", "ICN", 11085),
    ("ICN", "LHR", 8742), ("LHR", "ICN", 8742),
    ("ICN", "SYD", 8326), ("SYD", "ICN", 8326),
    ("ICN", "PVG", 861),  ("PVG", "ICN", 861),
    ("ICN", "PEK", 954),  ("PEK", "ICN", 954),
    ("ICN", "HKG", 2082), ("HKG", "ICN", 2082),
    ("ICN", "BKK", 3700), ("BKK", "ICN", 3700),
    ("HKG", "LHR", 9643), ("LHR", "HKG", 9643),
    ("HKG", "JFK", 12975),("JFK", "HKG", 12975),
    ("HKG", "LAX", 11389),("LAX", "HKG", 11389),
    ("HKG", "SYD", 7372), ("SYD", "HKG", 7372),
    ("HKG", "PVG", 1256), ("PVG", "HKG", 1256),
    ("HKG", "PEK", 1966), ("PEK", "HKG", 1966),
    ("HKG", "BKK", 1712), ("BKK", "HKG", 1712),
    ("HKG", "DEL", 3782), ("DEL", "HKG", 3782),
    ("HKG", "BOM", 3659), ("BOM", "HKG", 3659),
    ("PEK", "LAX", 9783), ("LAX", "PEK", 9783),
    ("PEK", "JFK", 10989),("JFK", "PEK", 10989),
    ("PEK", "LHR", 8154), ("LHR", "PEK", 8154),
    ("PEK", "SYD", 8970), ("SYD", "PEK", 8970),
    ("PVG", "LAX", 9833), ("LAX", "PVG", 9833),
    ("PVG", "JFK", 11158),("JFK", "PVG", 11158),
    ("PVG", "LHR", 9215), ("LHR", "PVG", 9215),
    ("PVG", "SYD", 8744), ("SYD", "PVG", 8744),
    ("BKK", "LHR", 9545), ("LHR", "BKK", 9545),
    ("BKK", "SYD", 7555), ("SYD", "BKK", 7555),
    ("BKK", "DEL", 2866), ("DEL", "BKK", 2866),
    ("KUL", "LHR", 10553),("LHR", "KUL", 10553),
    ("KUL", "SYD", 6630), ("SYD", "KUL", 6630),
    ("KUL", "CGK", 1184), ("CGK", "KUL", 1184),
    ("KUL", "MNL", 2639), ("MNL", "KUL", 2639),
    ("CGK", "SYD", 5524), ("SYD", "CGK", 5524),
    # ── INDIA INTRA & HUB ──
    ("DEL", "BOM", 1152), ("BOM", "DEL", 1152),
    ("DEL", "BLR", 1744), ("BLR", "DEL", 1744),
    ("DEL", "MAA", 1759), ("MAA", "DEL", 1759),
    ("DEL", "CCU", 1305), ("CCU", "DEL", 1305),
    ("DEL", "HYD", 1253), ("HYD", "DEL", 1253),
    ("DEL", "LHR", 6714), ("LHR", "DEL", 6714),
    ("DEL", "CDG", 6604), ("CDG", "DEL", 6604),
    ("DEL", "JFK", 11740),("JFK", "DEL", 11740),
    ("BOM", "LHR", 7193), ("LHR", "BOM", 7193),
    ("BOM", "CDG", 6830), ("CDG", "BOM", 6830),
    ("BOM", "JFK", 12553),("JFK", "BOM", 12553),
    ("BOM", "BLR", 984),  ("BLR", "BOM", 984),
    # ── AFRICA ──
    ("JNB", "LHR", 9067), ("LHR", "JNB", 9067),
    ("JNB", "CDG", 9072), ("CDG", "JNB", 9072),
    ("JNB", "ADD", 3844), ("ADD", "JNB", 3844),
    ("JNB", "NBO", 3482), ("NBO", "JNB", 3482),
    ("JNB", "LOS", 4797), ("LOS", "JNB", 4797),
    ("CAI", "LHR", 3518), ("LHR", "CAI", 3518),
    ("CAI", "CDG", 3210), ("CDG", "CAI", 3210),
    ("CAI", "JFK", 9132), ("JFK", "CAI", 9132),
    ("ADD", "LHR", 6843), ("LHR", "ADD", 6843),
    ("ADD", "NBO", 1160), ("NBO", "ADD", 1160),
    ("NBO", "LHR", 6814), ("LHR", "NBO", 6814),
    # ── SOUTH AMERICA ──
    ("GRU", "LHR", 9500), ("LHR", "GRU", 9500),
    ("GRU", "CDG", 9337), ("CDG", "GRU", 9337),
    ("GRU", "FRA", 9786), ("FRA", "GRU", 9786),
    ("GRU", "EZE", 1977), ("EZE", "GRU", 1977),
    ("GRU", "LIM", 3693), ("LIM", "GRU", 3693),
    ("GRU", "BOG", 4256), ("BOG", "GRU", 4256),
    ("EZE", "LHR", 11097),("LHR", "EZE", 11097),
    ("EZE", "MAD", 10034),("MAD", "EZE", 10034),
    ("EZE", "SCL", 1137), ("SCL", "EZE", 1137),
    ("EZE", "LIM", 3154), ("LIM", "EZE", 3154),
    ("BOG", "MEX", 2974), ("MEX", "BOG", 2974),
    ("BOG", "MAD", 8216), ("MAD", "BOG", 8216),
    ("LIM", "MAD", 10147),("MAD", "LIM", 10147),
    ("LIM", "BOG", 1868), ("BOG", "LIM", 1868),
    ("MEX", "MAD", 9017), ("MAD", "MEX", 9017),
    ("MEX", "GDL", 543),  ("GDL", "MEX", 543),
    ("PTY", "BOG", 723),  ("BOG", "PTY", 723),
    ("PTY", "MEX", 2074), ("MEX", "PTY", 2074),
    # ── OCEANIA ──
    ("SYD", "LHR", 16993),("LHR", "SYD", 16993),
    ("SYD", "LAX", 12051),("LAX", "SYD", 12051),
    ("SYD", "JFK", 16016),("JFK", "SYD", 16016),
    ("SYD", "MEL", 714),  ("MEL", "SYD", 714),
    ("SYD", "BNE", 921),  ("BNE", "SYD", 921),
    ("SYD", "PER", 3290), ("PER", "SYD", 3290),
    ("SYD", "AKL", 2156), ("AKL", "SYD", 2156),
    ("MEL", "LHR", 16892),("LHR", "MEL", 16892),
    ("MEL", "LAX", 12756),("LAX", "MEL", 12756),
    ("MEL", "AKL", 2587), ("AKL", "MEL", 2587),
    ("MEL", "SIN", 6325), ("SIN", "MEL", 6325),
    ("BNE", "LAX", 12449),("LAX", "BNE", 12449),
]

# Remove exact duplicates (routes listed twice in both directions are intended)
# But remove true exact duplicates
def dedupe_routes(routes):
    seen = set()
    result = []
    for r in routes:
        key = (r[0], r[1])
        if key not in seen:
            seen.add(key)
            result.append(r)
    return result

ROUTES_DATA = dedupe_routes(ROUTES_DATA)


def seed_database():
    db = SessionLocal()
    try:
        print("🌱 Starting database seed...")
        print("  Clearing existing data...")

        # Delete in FK-safe order (payments → bookings → flights → routes → aircraft → airports → airlines → users)
        from app.models.payment import Payment
        from app.models.booking import Booking as BookingModel
        db.query(Payment).delete()
        db.query(BookingModel).delete()
        db.query(Flight).delete()
        db.query(Route).delete()
        db.query(Aircraft).delete()
        db.query(Airport).delete()
        db.query(Airline).delete()
        db.query(User).delete()
        db.commit()
        print("  ✓ Cleared existing data")

        # ── Users ──
        print("  Creating users...")
        admin = User(
            name="Admin User", email="admin@aerobook.com",
            username="admin", password_hash=hash_password("Admin@123"),
            is_admin=True
        )
        user1 = User(
            name="John Doe", email="john@example.com",
            username="johndoe", password_hash=hash_password("Test@1234"),
            is_admin=False
        )
        user2 = User(
            name="Jane Smith", email="jane@example.com",
            username="janesmith", password_hash=hash_password("Test@1234"),
            is_admin=False
        )
        db.add_all([admin, user1, user2])
        db.flush()
        print(f"  ✓ Created 3 users")

        # ── Airlines ──
        print("  Creating airlines...")
        airline_objs = {}
        for name, code, factor in AIRLINES_DATA:
            a = Airline(name=name, code=code, price_factor=factor)
            db.add(a)
            airline_objs[code] = a
        db.flush()
        print(f"  ✓ Created {len(AIRLINES_DATA)} airlines")

        # ── Airports ──
        print("  Creating airports...")
        airport_objs = {}
        for name, city, country, iata, is_hub in AIRPORTS_DATA:
            ap = Airport(name=name, city=city, country=country, iata_code=iata)
            db.add(ap)
            airport_objs[iata] = ap
        db.flush()
        print(f"  ✓ Created {len(AIRPORTS_DATA)} airports")

        # ── Aircraft ──
        print("  Creating aircraft...")
        ac_737 = Aircraft(model="Boeing 737-800",    total_capacity=162, seat_map=make_seat_map_737())
        ac_a320 = Aircraft(model="Airbus A320",       total_capacity=150, seat_map=make_seat_map_a320())
        ac_777 = Aircraft(model="Boeing 777-300ER",  total_capacity=396, seat_map=make_seat_map_777())
        db.add_all([ac_737, ac_a320, ac_777])
        db.flush()
        print("  ✓ Created 3 aircraft types")

        # ── Routes ──
        print("  Creating routes...")
        route_objs = {}
        skipped_routes = 0
        for origin_iata, dest_iata, dist in ROUTES_DATA:
            if origin_iata not in airport_objs or dest_iata not in airport_objs:
                skipped_routes += 1
                continue
            r = Route(
                source_airport_id=airport_objs[origin_iata].id,
                destination_airport_id=airport_objs[dest_iata].id,
                distance_km=dist
            )
            db.add(r)
            route_objs[(origin_iata, dest_iata)] = r
        db.flush()
        print(f"  ✓ Created {len(route_objs)} routes (skipped {skipped_routes} with missing airports)")

        # ── Flights ──
        print("  Creating flights (14 days)...")

        # Assign airlines to routes based on region/realism
        # Long haul (>5000km) → wide body 777, medium airline selection
        # Medium haul (1500-5000km) → mix of 737/A320
        # Short haul (<1500km) → 737 or A320

        # Major airline lists by region
        us_carriers     = ["AA", "DL", "UA", "B6", "AS", "WN", "NK"]
        eu_carriers     = ["BA", "LH", "AF", "KL", "LX", "IB", "FR", "U2", "EI", "TK"]
        me_carriers     = ["EK", "QR", "EY", "FZ", "G9"]
        asia_carriers   = ["SQ", "CX", "JL", "NH", "KE", "TG", "MH", "AK", "6E", "AI"]
        long_haul_set   = ["EK", "QR", "EY", "SQ", "CX", "BA", "LH", "AF", "NH", "JL",
                           "AA", "DL", "UA", "QF", "KE", "TK"]

        all_airline_codes = [a[1] for a in AIRLINES_DATA]

        base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        flight_count = 0

        for (origin_iata, dest_iata), route in route_objs.items():
            dist = next((r[2] for r in ROUTES_DATA if r[0] == origin_iata and r[1] == dest_iata), 3000)

            # Choose aircraft by distance
            if dist >= 6000:
                aircraft = ac_777
                base_price_eco = round(random.uniform(550, 1400), 2)
                base_price_bus = round(base_price_eco * random.uniform(2.8, 4.5), 2)
                base_price_fst = round(base_price_eco * random.uniform(5.0, 8.0), 2)
                flight_hours   = dist / 870
            elif dist >= 2000:
                aircraft = ac_737 if random.random() < 0.5 else ac_a320
                base_price_eco = round(random.uniform(180, 550), 2)
                base_price_bus = round(base_price_eco * random.uniform(2.2, 3.5), 2)
                base_price_fst = None
                flight_hours   = dist / 820
            else:
                aircraft = ac_737 if random.random() < 0.6 else ac_a320
                base_price_eco = round(random.uniform(60, 280), 2)
                base_price_bus = round(base_price_eco * random.uniform(1.8, 2.8), 2)
                base_price_fst = None
                flight_hours   = dist / 800

            # Pick 2-3 airlines for this route
            if dist >= 6000:
                pool = long_haul_set
            elif origin_iata in [a[3] for a in AIRPORTS_DATA if a[4] and a[2] == "USA"] or \
                 dest_iata   in [a[3] for a in AIRPORTS_DATA if a[4] and a[2] == "USA"]:
                pool = us_carriers + eu_carriers[:4]
            elif origin_iata in ["LHR","CDG","FRA","AMS","MAD","FCO","ZRH","MUC","VIE"] or \
                 dest_iata   in ["LHR","CDG","FRA","AMS","MAD","FCO","ZRH","MUC","VIE"]:
                pool = eu_carriers
            elif origin_iata in ["DXB","DOH","AUH","RUH","JED"] or \
                 dest_iata   in ["DXB","DOH","AUH","RUH","JED"]:
                pool = me_carriers + ["BA","LH","AF","SQ","AI","EK"]
            elif origin_iata in ["SIN","BKK","KUL","HKG","NRT","ICN","PEK","PVG"] or \
                 dest_iata   in ["SIN","BKK","KUL","HKG","NRT","ICN","PEK","PVG"]:
                pool = asia_carriers + ["BA","LH","EK","QR"]
            else:
                pool = all_airline_codes

            # Ensure pool airlines exist in our db
            pool = [c for c in pool if c in airline_objs]
            if not pool:
                pool = all_airline_codes[:5]

            num_airlines = min(random.randint(2, 3), len(pool))
            chosen_airlines = random.sample(pool, num_airlines)

            # Departure times — 1-3 flights per day per airline
            dep_hours = sorted(random.sample(range(5, 23), min(num_airlines + 1, 4)))

            for day in range(14):
                date = base_date + timedelta(days=day)
                for ai, airline_code in enumerate(chosen_airlines):
                    hour = dep_hours[ai % len(dep_hours)]
                    dep_time = date.replace(hour=hour, minute=random.choice([0, 15, 30, 45]))
                    arr_time = dep_time + timedelta(hours=flight_hours, minutes=random.randint(0, 30))

                    fn = f"{airline_code}{random.randint(100, 9999)}"
                    flight = Flight(
                        flight_number=fn,
                        route_id=route.id,
                        airline_id=airline_objs[airline_code].id,
                        aircraft_id=aircraft.id,
                        departure_time=dep_time,
                        arrival_time=arr_time,
                        base_price_economy=base_price_eco,
                        base_price_business=base_price_bus,
                        base_price_first=base_price_fst,
                    )
                    db.add(flight)
                    flight_count += 1

        db.commit()
        print(f"  ✓ Created {flight_count:,} flights across 14 days")
        print()
        print("✅ Database seeded successfully!")
        print(f"   Airlines : {len(AIRLINES_DATA)}")
        print(f"   Airports : {len(AIRPORTS_DATA)}")
        print(f"   Routes   : {len(route_objs)}")
        print(f"   Flights  : {flight_count:,}")
        print()
        print("Test credentials:")
        print("  Admin : username=admin      password=Admin@123")
        print("  User  : username=johndoe    password=Test@1234")
        print("  User  : username=janesmith  password=Test@1234")

    except Exception as e:
        db.rollback()
        import traceback
        print(f"❌ Error: {e}")
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()