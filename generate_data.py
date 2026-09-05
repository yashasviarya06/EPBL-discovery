import pandas as pd
import random
import os
data = []

random.seed(42)

# ============================================================
# CONFIGURATION
# ============================================================

RECORDS_PER_STATE = 2000

STATES = {
    "Maharashtra": [
        "Mumbai",
        "Pune",
        "Thane",
        "Nashik",
        "Nagpur",
        "Navi Mumbai",
        "Kolhapur",
        "Chhatrapati Sambhajinagar",
        "Lonavala",
        "Alibaug"
    ],

    "Karnataka": [
        "Bengaluru",
        "Mysuru",
        "Mangaluru",
        "Udupi",
        "Hubballi",
        "Belagavi",
        "Coorg",
        "Tumakuru",
        "Manipal",
        "Hassan"
    ],

    "Goa": [
        "Panaji",
        "Margao",
        "Vasco da Gama",
        "Mapusa",
        "Calangute",
        "Candolim",
        "Baga",
        "Anjuna",
        "Ponda",
        "Morjim"
    ]
}


# ============================================================
# OPPORTUNITY DATA
# ============================================================

OPPORTUNITY_TEMPLATES = {

"Residential": [

"A RERA-registered residential development comprising {units} apartments has been announced in {city}.",

"Planning authorities have approved a {units}-unit housing project near {city}.",

"A developer has acquired land for a large residential township in {city}.",

"Construction is expected to begin on a new gated community containing approximately {units} homes near {city}.",

"A mixed-use residential development with {units} apartments is planned on the outskirts of {city}.",

"A new housing project targeting more than {people} residents has received preliminary approval in {city}.",

"A real estate developer has announced a large apartment project in {city} with multiple residential towers.",

"A proposed residential township near {city} will include apartments, community facilities and landscaped areas.",

"A major housing project in {city} has entered the construction approval stage.",

"A large residential complex with common amenities is under development near {city}."

],

"Hospitality": [

"A new {rooms}-room hotel project has been announced in {city}.",

"A luxury resort with approximately {rooms} rooms is proposed near {city}.",

"Construction approval has been granted for a large tourism resort in {city}.",

"A hospitality developer is planning a new property with guest accommodation and recreational facilities near {city}.",

"A beach resort project with {rooms} guest rooms is proposed in {city}.",

"A new business hotel is planned near the commercial district of {city}.",

"A tourism company has acquired land for a resort development near {city}.",

"A large eco-resort project is being evaluated near {city}.",

"A hotel expansion will add more than {rooms} rooms and new guest facilities in {city}.",

"A new hospitality complex with restaurants, accommodation and recreational facilities is planned near {city}."

],

"Healthcare": [

"A new multi-specialty hospital campus is being developed in {city}.",

"A healthcare company has announced a major hospital project near {city}.",

"Planning authorities have approved a new medical campus in {city}.",

"A hospital expansion project will add new patient accommodation and treatment facilities in {city}.",

"A private healthcare group is acquiring land for a new hospital near {city}.",

"A large medical facility with residential accommodation for staff is proposed in {city}.",

"A new healthcare campus is expected to serve thousands of patients in the {city} region.",

"A specialty hospital and associated facilities are planned near {city}.",

"A medical institution has announced construction of a new healthcare complex in {city}.",

"A hospital developer has received approval for a new multi-building medical campus in {city}."

],

"Education": [

"A new university campus with student accommodation is planned near {city}.",

"A private university has announced a residential campus project in {city}.",

"A large educational institution is developing a campus with hostels and dining facilities near {city}.",

"Planning authorities have approved a new college campus in {city}.",

"A university expansion will include new student residences and academic buildings in {city}.",

"A boarding school campus with residential facilities is proposed near {city}.",

"A new higher-education campus is being developed on the outskirts of {city}.",

"An educational trust has acquired land for a large institutional campus near {city}.",

"A new university development will accommodate several thousand students in {city}.",

"A residential educational campus with hostels and common facilities is planned near {city}."

],

"Industrial": [

"A new industrial park is being developed near {city}.",

"An industrial estate with multiple manufacturing units has been approved near {city}.",

"A manufacturing complex is planned on the outskirts of {city}.",

"A major industrial company has announced a new production facility near {city}.",

"Construction approval has been granted for an industrial development in {city}.",

"A large manufacturing campus with employee facilities is proposed near {city}.",

"An industrial developer has acquired land for a multi-unit industrial park near {city}.",

"A new production facility is expected to begin construction in the {city} region.",

"Several manufacturing units are expected to operate from a new industrial zone near {city}.",

"A large industrial expansion project has been announced near {city}."

],

"Logistics": [

"A logistics park with multiple warehouses is planned near {city}.",

"A large warehousing and distribution centre is proposed near {city}.",

"A logistics company has acquired land for a new distribution hub near {city}.",

"A multi-building logistics park is being developed on the outskirts of {city}.",

"A new supply-chain facility with employee amenities is planned near {city}.",

"A warehouse complex covering a large industrial area is proposed near {city}.",

"A major e-commerce logistics hub is being developed near {city}.",

"A freight and warehousing facility has received development approval near {city}.",

"A distribution centre with multiple operational buildings is planned in {city}.",

"A logistics developer has announced a new large-scale warehouse campus near {city}."

],

"Commercial": [

"A large commercial complex is planned in {city}.",

"A mixed-use development containing offices, retail space and public facilities is proposed near {city}.",

"A new business park with multiple commercial buildings is being developed in {city}.",

"A major commercial township has received development approval in {city}.",

"A large shopping and commercial complex is proposed near {city}.",

"A developer has announced a multi-building commercial project in {city}.",

"A new corporate campus with multiple buildings is planned near {city}.",

"Construction is expected to begin on a large commercial development in {city}.",

"A mixed-use property development with offices and retail facilities is planned in {city}.",

"A large business district expansion has been announced near {city}."

],

"Institutional": [

"A large institutional campus is planned near {city}.",

"A public-sector organization has announced development of a new campus in {city}.",

"A training and residential facility is proposed near {city}.",

"A research institution is developing a new campus in {city}.",

"A large institutional complex with accommodation facilities is planned near {city}.",

"A government-supported campus project has received approval in {city}.",

"A new administrative and residential campus is proposed near {city}.",

"A large training centre with residential accommodation is planned in {city}.",

"A research and development campus is being developed near {city}.",

"An institutional development with multiple buildings has been approved near {city}."

],

"Tourism": [

"A major tourism infrastructure project is proposed near {city}.",

"A tourism developer has announced a large visitor accommodation project near {city}.",

"A new destination tourism complex is being planned in {city}.",

"Authorities have approved a tourism development project near {city}.",

"A large visitor facility with accommodation and recreational infrastructure is proposed near {city}.",

"A tourism company is planning a new destination project near {city}.",

"A new eco-tourism development is being evaluated near {city}.",

"A tourism infrastructure expansion is planned in the {city} region.",

"A destination resort and visitor centre is proposed near {city}.",

"A major tourism investment has been announced near {city}."

],

"Senior Living": [

"A new senior living community with residential facilities is planned near {city}.",

"A retirement community with healthcare and accommodation facilities is proposed in {city}.",

"A developer has announced a large assisted-living project near {city}.",

"A senior residential campus with common facilities is being developed near {city}.",

"A retirement housing development has received approval in {city}."

]
}


# ============================================================
# NOISE DATA
# ============================================================

NOISE_TEMPLATES = {

"Technology": [

"A software company has opened a new technology office in {city}.",

"An IT company announced plans to increase its workforce in {city}.",

"A technology startup has launched a new software product from {city}.",

"A technology firm has expanded its office operations in {city}.",

"A software company announced a new digital platform in {city}.",

"A technology company is recruiting engineers for its {city} office.",

"A startup has raised funding to expand its technology operations in {city}.",

"An IT services company has opened a new corporate office in {city}."

],

"Retail": [

"A fashion retailer has opened a new store in {city}.",

"A supermarket chain has launched a retail outlet in {city}.",

"A consumer electronics company has opened a showroom in {city}.",

"A footwear brand has expanded its retail presence in {city}.",

"A national retail company has announced a new store in {city}.",

"A lifestyle brand has opened its latest outlet in {city}.",

"A grocery chain has expanded operations in {city}.",

"A clothing company has announced a new retail location in {city}."

],

"Finance": [

"A bank has opened a new branch in {city}.",

"A financial services company has expanded its operations in {city}.",

"A fintech company has launched a new service in {city}.",

"An insurance company has opened a new office in {city}.",

"A financial institution has increased its workforce in {city}.",

"A banking company has announced expansion of its branch network in {city}.",

"A lending platform has launched services in {city}.",

"A financial company has moved into a larger office in {city}."

],

"Corporate": [

"A consulting company has expanded its office space in {city}.",

"A professional services firm has opened a new office in {city}.",

"A corporate services company has increased its workforce in {city}.",

"A management consulting company has announced expansion in {city}.",

"A legal services company has opened a new office in {city}.",

"A recruitment company has expanded its operations in {city}.",

"A business services firm has announced hiring in {city}.",

"A corporate advisory company has increased its presence in {city}."

],

"Transport": [

"An airline has announced additional flights from {city}.",

"A bus operator has introduced a new route connecting {city}.",

"A logistics company has expanded its delivery network in {city}.",

"A transportation company has increased its fleet operations in {city}.",

"A railway service has announced schedule changes affecting {city}.",

"A ride-sharing company has expanded services in {city}.",

"A courier company has launched a new service in {city}.",

"A transport operator has announced new routes from {city}."

],

"Entertainment": [

"A cinema chain has announced a new screen in {city}.",

"A music festival will take place in {city}.",

"An entertainment company has launched a new venue in {city}.",

"A gaming centre has opened in {city}.",

"A theatre company has announced a performance in {city}.",

"A streaming company has announced an event in {city}.",

"A recreational venue has opened in {city}.",

"An entertainment brand has expanded its operations in {city}."

],

"Small Business": [

"A local bakery has opened a new outlet in {city}.",

"A restaurant has launched a new location in {city}.",

"A small clothing shop has opened in {city}.",

"A local café has expanded its operations in {city}.",

"A neighbourhood pharmacy has opened a new branch in {city}.",

"A small fitness studio has opened in {city}.",

"A local electronics shop has expanded in {city}.",

"A convenience store has opened a new location in {city}."

],

"Events": [

"A business conference will be held in {city}.",

"A cultural festival is scheduled to take place in {city}.",

"A technology conference will attract visitors to {city}.",

"A sports event is planned in {city}.",

"A trade exhibition will be held in {city}.",

"A music event has been announced in {city}.",

"A public seminar is scheduled in {city}.",

"A business networking event will take place in {city}."

],

"Employment": [

"A company has announced hiring for its {city} operations.",

"A technology firm plans to recruit additional employees in {city}.",

"A corporate employer has announced new vacancies in {city}.",

"A business process outsourcing company is hiring in {city}.",

"A retail company plans to recruit staff in {city}.",

"A financial company has announced recruitment in {city}.",

"A startup is hiring employees for its {city} office.",

"A consulting company has announced recruitment in {city}."
]
}


# ============================================================
# ADD RANDOM CONTEXT
# ============================================================

OPPORTUNITY_CONTEXT = [

"following regulatory approval",

"after receiving preliminary clearance",

"as part of a planned expansion",

"following the acquisition of land",

"after receiving development permission",

"as part of a major private investment",

"following a new project announcement",

"after planning authority approval",

"as part of regional infrastructure development",

"following an investment proposal"
]


NOISE_CONTEXT = [

"according to the company announcement",

"as part of its business expansion",

"following a corporate announcement",

"according to local reports",

"as part of its regional growth strategy",

"following a recent launch",

"as part of its operational expansion",

"according to the company",

"following the latest business update",

"as part of its market expansion"
]


# ============================================================
# GENERATE OPPORTUNITIES
# ============================================================

def generate_opportunity(state):

    city = random.choice(STATES[state])

    signal_type = random.choice(
        list(OPPORTUNITY_TEMPLATES.keys())
    )

    template = random.choice(
        OPPORTUNITY_TEMPLATES[signal_type]
    )

    text = template.format(
        city=city,
        units=random.choice([
            150, 250, 300, 400, 500,
            600, 750, 900, 1200,
            1500, 2000, 2500
        ]),
        people=random.choice([
            500, 800, 1200, 1800,
            2500, 3500, 5000,
            7000, 10000
        ]),
        rooms=random.choice([
            80, 100, 120, 150,
            200, 250, 300,
            400, 500, 750
        ])
    )

    # Sometimes add project context
    if random.random() < 0.65:
        text += " " + random.choice(OPPORTUNITY_CONTEXT) + "."

    return [
        state,
        city,
        signal_type,
        text,
        1
    ]


# ============================================================
# GENERATE NOISE
# ============================================================

def generate_noise(state):

    city = random.choice(STATES[state])

    signal_type = random.choice(
        list(NOISE_TEMPLATES.keys())
    )

    template = random.choice(
        NOISE_TEMPLATES[signal_type]
    )

    text = template.format(city=city)

    if random.random() < 0.65:
        text += " " + random.choice(NOISE_CONTEXT) + "."

    return [
        state,
        city,
        signal_type,
        text,
        0
    ]


# ============================================================
# CREATE DATA
# ============================================================

for state in STATES:

    opportunity_count = RECORDS_PER_STATE // 2
    noise_count = RECORDS_PER_STATE // 2

    for _ in range(opportunity_count):
        data.append(
            generate_opportunity(state)
        )

    for _ in range(noise_count):
        data.append(
            generate_noise(state)
        )


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(
    data,
    columns=[
        "state",
        "city",
        "signal_type",
        "signal_text",
        "label"
    ]
)


# ============================================================
# SHUFFLE
# ============================================================

df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


# ============================================================
# REMOVE DUPLICATES
# ============================================================

df = df.drop_duplicates(
    subset=["signal_text"]
).reset_index(drop=True)


# ============================================================
# SAVE
# ============================================================

os.makedirs("data", exist_ok=True)

file_path = "data/opportunity_signals.csv"

df.to_csv(
    file_path,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\n============================================")
print("EPBL LEAD DISCOVERY DATASET")
print("============================================")

print(f"\nTotal records: {len(df)}")

print("\nState distribution:")
print(df["state"].value_counts())

print("\nLabel distribution:")
print(df["label"].value_counts())

print("\nSignal type distribution:")
print(df["signal_type"].value_counts())

print("\nSample records:")
print(
    df[
        [
            "state",
            "city",
            "signal_type",
            "signal_text",
            "label"
        ]
    ].head(10).to_string(index=False)
)

print("\n============================================")
print(f"Saved to: {file_path}")
print("============================================")