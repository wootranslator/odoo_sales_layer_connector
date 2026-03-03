const questions = [
    // --- CATEGORY: Traffic Laws ---
    {
        id: 1, category: "traffic-laws",
        question: "When approaching an intersection with a flashing red light, what should you do?",
        options: ["Stop completely, then proceed only when safe.", "Slow down and proceed with caution.", "Keep going at the same speed if there is no cross traffic.", "Stop only if there are other vehicles present."],
        answer: 0, explanation: "A flashing red light has the same meaning as a stop sign. You must come to a complete stop."
    },
    {
        id: 2, category: "traffic-laws",
        question: "A solid yellow line in the center of the road means:",
        options: ["You can overtake if safe.", "Do not cross or overtake.", "Keep left at all times.", "Caution: road works ahead."],
        answer: 1, explanation: "Solid lines indicate that crossing the line to overtake or change lanes is prohibited."
    },
    {
        id: 3, category: "traffic-laws",
        question: "What is the minimum age to apply for a temporary car driving license in Thailand?",
        options: ["16 years old", "17 years old", "18 years old", "20 years old"],
        answer: 2, explanation: "The minimum age for a car driving license in Thailand is 18."
    },
    {
        id: 4, category: "traffic-laws",
        question: "How long is a temporary driving license valid for in Thailand?",
        options: ["1 year", "2 years", "5 years", "Permanent"],
        answer: 1, explanation: "Temporary driving licenses are valid for 2 years initially."
    },
    {
        id: 5, category: "traffic-laws",
        question: "When turning left at a red light where a 'Turn Left on Red' sign is present, you must:",
        options: ["Turn immediately without stopping.", "Stop and wait for the green light.", "Stop, yield to traffic and pedestrians, then turn when safe.", "Only turn if there are no other cars."],
        answer: 2, explanation: "You must stop first and ensure the way is clear before turning left on red."
    },
    {
        id: 6, category: "traffic-laws",
        question: "What does a red and white marker on the edge of the curb mean?",
        options: ["Parking allowed for short periods only.", "No stopping and no parking for all vehicles.", "Bus stop only.", "Taxi stand only."],
        answer: 1, explanation: "Red and white stripes on the curb mean 'No Stopping' and 'No Parking' at any time."
    },
    {
        id: 7, category: "traffic-laws",
        question: "What does 'Yellow and White' markings on the curb mean?",
        options: ["No stopping", "Short-term parking or loading/unloading area", "Parking for motorcycles only", "Bus lane only"],
        answer: 1, explanation: "Yellow and white stripes mean you can stop briefly for loading but no long-term parking."
    },
    {
        id: 8, category: "traffic-laws",
        question: "How many days must you notify the DLT after changing your vehicle's color?",
        options: ["3 days", "7 days", "15 days", "30 days"],
        answer: 1, explanation: "You must notify the DLT within 7 days of changing the vehicle's color."
    },
    {
        id: 9, category: "traffic-laws",
        question: "When should you use your turn signals?",
        options: ["Only at night", "At least 30 meters before turning or changing lanes", "Only when there are other cars behind you", "Exactly when you start turning"],
        answer: 1, explanation: "Signaling early (at least 30m) gives other drivers enough time to react."
    },
    {
        id: 10, category: "traffic-laws",
        question: "Driving with an expired license is punishable by:",
        options: ["No fine", "A fine not exceeding 2,000 Baht", "Confiscation of the vehicle", "A warning only"],
        answer: 1, explanation: "Driving with an expired license is subject to fines."
    },
    {
        id: 11, category: "traffic-laws",
        question: "At an intersection without signs or lights, which vehicle has priority?",
        options: ["The vehicle on the left", "The vehicle on the right", "The faster vehicle", "The larger vehicle"],
        answer: 1, explanation: "In Thailand, at an uncontrolled intersection, you generally yield to the vehicle coming from your right."
    },
    {
        id: 12, category: "traffic-laws",
        question: "What is the legal blood alcohol limit for drivers over 20 years old with a full license?",
        options: ["0.2 mg%", "0.5 mg% (50mg/100ml)", "0.8 mg%", "1.0 mg%"],
        answer: 1, explanation: "The common limit is 50mg of alcohol per 100ml of blood (0.5 mg%)."
    },
    {
        id: 13, category: "traffic-laws",
        question: "How many meters must you park away from a fire hydrant?",
        options: ["1 meter", "3 meters", "5 meters", "10 meters"],
        answer: 1, explanation: "You must not park within 3 meters of a fire hydrant."
    },
    {
        id: 14, category: "traffic-laws",
        question: "What is the maximum distance allowed for a vehicle to be parked from the curb?",
        options: ["10 cm", "25 cm", "50 cm", "1 meter"],
        answer: 1, explanation: "A vehicle must be parked parallel to and no more than 25 cm from the curb."
    },
    {
        id: 15, category: "traffic-laws",
        question: "How far from a railway crossing must you stop your vehicle when a train is approaching?",
        options: ["2 meters", "3 meters", "5 meters", "10 meters"],
        answer: 2, explanation: "You must stop at least 5 meters away from the railway tracks."
    },

    // --- CATEGORY: Traffic Signs ---
    {
        id: 16, category: "traffic-signs",
        question: "A blue circular sign with a white arrow pointing straight ahead means:",
        options: ["One-way road ahead.", "Go straight only.", "Keep right.", "U-turn allowed ahead."],
        answer: 1, explanation: "Blue circular signs are mandatory. An arrow pointing straight means you must go straight only."
    },
    {
        id: 17, category: "traffic-signs",
        question: "What does an inverted triangle sign with a red border mean?",
        options: ["Stop", "Give Way (Yield)", "No Entry", "Danger Ahead"],
        answer: 1, explanation: "The inverted triangle is the sign for 'Give Way'."
    },
    {
        id: 18, category: "traffic-signs",
        question: "A yellow diamond-shaped sign with a black symbol is a:",
        options: ["Regulatory sign", "Warning sign", "Information sign", "Mandatory sign"],
        answer: 1, explanation: "Yellow diamond signs are warning signs."
    },
    {
        id: 19, category: "traffic-signs",
        question: "A red circular sign with a white horizontal bar in the middle means:",
        options: ["No Parking", "No Entry", "One-way road", "End of all restrictions"],
        answer: 1, explanation: "This is the 'No Entry' sign."
    },
    {
        id: 20, category: "traffic-signs",
        question: "What does a sign showing a horn with a red diagonal line mean?",
        options: ["No loud music", "Sound horn allowed", "No use of horn (Silence zone)", "Area for testing horns"],
        answer: 2, explanation: "This sign prohibits the use of horns."
    },
    {
        id: 21, category: "traffic-signs",
        question: "A blue square sign with a white 'P' indicates:",
        options: ["Police station", "Parking area", "Pedestrian crossing", "Petrol station"],
        answer: 1, explanation: "Blue square 'P' signs indicate parking areas."
    },
    {
        id: 22, category: "traffic-signs",
        question: "Which sign indicates a U-Turn is allowed?",
        options: ["Red circle with U-arrow and red line", "Blue circle with white U-arrow", "Yellow diamond with black U-arrow", "Green square with white U-arrow"],
        answer: 1, explanation: "Common mandatory U-Turn signs are blue with white arrows."
    },
    {
        id: 23, category: "traffic-signs",
        question: "A sign with a number like '60' inside a red circle means:",
        options: ["Minimum speed 60", "Maximum speed 60", "Recommended speed 60", "Distance to next town is 60km"],
        answer: 1, explanation: "Numbers inside red circles indicate the maximum speed limit."
    },
    {
        id: 24, category: "traffic-signs",
        question: "A sign showing two cars with a red circle and a diagonal line means:",
        options: ["No Entry for cars", "No Overtaking", "Two-way traffic", "Bridge ahead"],
        answer: 1, explanation: "This sign indicates that overtaking is prohibited."
    },
    {
        id: 25, category: "traffic-signs",
        question: "What does a blue circular sign with a white bicycle mean?",
        options: ["Warning: Bicycles ahead", "Bicycles only (Mandatory lane)", "No bicycles allowed", "Parking for bicycles"],
        answer: 1, explanation: "Blue circular signs mean it is a mandatory lane for the vehicle shown."
    },

    // --- CATEGORY: Safe Driving ---
    {
        id: 26, category: "safe-driving",
        question: "What is the maximum speed limit for a passenger car on a highway (Motorway) in Thailand?",
        options: ["90 km/h", "100 km/h", "120 km/h", "80 km/h"],
        answer: 2, explanation: "On major motorways, the speed limit is 120 km/h."
    },
    {
        id: 27, category: "safe-driving",
        question: "When driving in heavy rain and visibility is low, you should:",
        options: ["Turn on your high beams.", "Turn on your hazard lights while driving.", "Turn on your headlights and slow down.", "Speed up to get out of the rain quickly."],
        answer: 2, explanation: "Use regular headlights and increase following distance in low visibility."
    },
    {
        id: 28, category: "safe-driving",
        question: "What is the safest following distance from the vehicle in front?",
        options: ["5 meters", "1 car length", "A distance that allows you to stop safely", "Exactly 50 meters"],
        answer: 2, explanation: "Maintain a distance that allows safe stopping if the front car brakes suddenly."
    },
    {
        id: 29, category: "safe-driving",
        question: "When approaching a pedestrian crossing, you should:",
        options: ["Speed up to pass before pedestrians start crossing.", "Slow down and prepare to stop.", "Honk the horn to warn pedestrians.", "Stop only if a police officer is present."],
        answer: 1, explanation: "Drivers must yield to pedestrians at zebra crossings."
    },
    {
        id: 30, category: "safe-driving",
        question: "If you feel sleepy while driving long distance, you should:",
        options: ["Drink energy drinks", "Turn up the music", "Stop and take a short nap", "Drive faster"],
        answer: 2, explanation: "Stop at a safe place and rest if you are sleepy."
    },
    {
        id: 31, category: "safe-driving",
        question: "When an emergency vehicle with sirens is behind you, you should:",
        options: ["Keep driving at your speed", "Follow the ambulance", "Pull over to the left to give way", "Speed up"],
        answer: 2, explanation: "Yield and pull over for emergency vehicles."
    },
    {
        id: 32, category: "safe-driving",
        question: "When driving at night, when should you switch from high beams to low beams?",
        options: ["When it's raining", "When approaching another vehicle or following one", "When driving through a tunnel", "Never"],
        answer: 1, explanation: "Switch to low beams to avoid blinding other drivers."
    },
    {
        id: 33, category: "safe-driving",
        question: "What is the safest way to enter a main road from a side road?",
        options: ["Speed up quickly", "Stop and yield to all vehicles on the main road", "Honk before entering", "Merge without looking"],
        answer: 1, explanation: "Always yield to traffic on the main road before entering."
    },
    {
        id: 34, category: "safe-driving",
        question: "At a roundabout, who has the right of way in Thailand?",
        options: ["Vehicles entering the roundabout", "Vehicles already in the roundabout (from the right)", "The largest vehicle", "The vehicle going straight"],
        answer: 1, explanation: "Vehicles already in the roundabout coming from the right have the right of way."
    },
    {
        id: 35, category: "safe-driving",
        question: "When should you use hazard lights (double blinkers)?",
        options: ["When parking illegally", "Only when your vehicle is broken down or in an emergency", "When driving through an intersection", "When it is raining heavily"],
        answer: 1, explanation: "Hazard lights are for emergencies or when your car is a hazard; not for raining or parking."
    },

    // --- CATEGORY: Maintenance ---
    {
        id: 36, category: "maintenance",
        question: "When should you check your tire pressure?",
        options: ["Only when flat", "Once every year", "Regularly (monthly) when cold", "Only before long trips"],
        answer: 2, explanation: "Check tire pressure at least once a month when cold."
    },
    {
        id: 37, category: "maintenance",
        question: "If your engine overheats while driving, you should:",
        options: ["Pour cold water on it", "Pull over and turn off the engine", "Keep driving slowly", "Remove radiator cap immediately"],
        answer: 1, explanation: "Stop safely and let it cool. Do not open the cap while hot."
    },
    {
        id: 38, category: "maintenance",
        question: "What does it mean if the oil pressure warning light comes on?",
        options: ["Oil is fine", "Oil level or pressure is too low", "Time for a car wash", "Engine is too cold"],
        answer: 1, explanation: "Stop the engine immediately and check oil levels if this light appears."
    },
    {
        id: 39, category: "maintenance",
        question: "How often should you check the engine oil level?",
        options: ["Every 10,000 km", "Once a year", "At least once a week or before long trips", "Only when the car makes noise"],
        answer: 2, explanation: "Frequent oil checks (weekly/bi-weekly) ensure engine health."
    },
    {
        id: 40, category: "maintenance",
        question: "What should you check if your car's steering wheel vibrates at high speeds?",
        options: ["Brake fluid", "Tire balance and alignment", "Battery water", "Wiper blades"],
        answer: 1, explanation: "Vibration is often caused by unbalanced tires or poor alignment."
    },
    {
        id: 41, category: "maintenance",
        question: "If your brakes feel 'spongy' or soft when pressed, what is the likely cause?",
        options: ["New brake pads", "Air in the brake lines or low brake fluid", "Cold weather", "Driving too fast"],
        answer: 1, explanation: "Spongy brakes indicate a leak or air in the hydraulic system."
    },
    {
        id: 42, category: "maintenance",
        question: "What color should the engine coolant usually be?",
        options: ["Black", "Clear like water", "Bright green, pink, or orange", "Dark brown"],
        answer: 2, explanation: "Coolant contains additives giving it distinct colors (green/pink/orange)."
    },

    // --- CATEGORY: Etiquette & Situations ---
    {
        id: 43, category: "traffic-laws",
        question: "What should you do if your license is lost or damaged?",
        options: ["Keep driving anyway", "Apply for a replacement within 15 days", "Wait for the next renewal", "Report to the police only"],
        answer: 1, explanation: "You must apply for a replacement at the DLT within 15 days."
    },
    {
        id: 44, category: "safe-driving",
        question: "When driving down a steep hill, you should:",
        options: ["Put the car in neutral", "Use a lower gear (Engine braking)", "Keep your foot on the brake the whole time", "Turn off the engine"],
        answer: 1, explanation: "Using a lower gear helps control speed without overheating the brakes."
    },
    {
        id: 45, category: "safe-driving",
        question: "If your car skids on a wet road, you should:",
        options: ["Brake hard", "Steer into the direction of the skid", "Turn the steering wheel the opposite way", "Accelerate"],
        answer: 1, explanation: "Removing your foot from the gas and steering into the skid helps regain control."
    },
    {
        id: 46, category: "traffic-laws",
        question: "How many people are allowed to sit in the front seat of a standard passenger car?",
        options: ["1 person", "2 people (including driver)", "3 people", "As many as fit"],
        answer: 1, explanation: "Standard cars allow only the driver and one passenger in the front seat."
    },
    {
        id: 47, category: "traffic-laws",
        question: "What is the maximum noise level allowed for a vehicle's exhaust in Thailand?",
        options: ["80 decibels", "95 decibels", "110 decibels", "120 decibels"],
        answer: 1, explanation: "The legal limit for exhaust noise is typically around 95 decibels."
    },
    {
        id: 48, category: "traffic-signs",
        question: "A sign showing a red circle with a truck and a red diagonal line means:",
        options: ["Trucks only", "Parking for trucks", "Trucks prohibited", "Truck washing area"],
        answer: 2, explanation: "This sign prohibits trucks from entering the road."
    },
    {
        id: 49, category: "safe-driving",
        question: "When stopping your car, how far must your left tires be from the curb?",
        options: ["0 cm", "Not more than 25 cm", "Not more than 50 cm", "Exactly 10 cm"],
        answer: 1, explanation: "You must stop parallel to and within 25 cm of the curb."
    },
    {
        id: 50, category: "traffic-laws",
        question: "A person with a temporary license who commits a traffic violation may:",
        options: ["Pay no fine", "Have their license revoked or extended", "Be banned for life", "Receive a new license immediately"],
        answer: 1, explanation: "Violations can affect the conversion of a temporary license to a permanent one."
    }
];

// Export to pool
window.questionsData = questions;
console.log("Loaded " + window.questionsData.length + " questions.");
