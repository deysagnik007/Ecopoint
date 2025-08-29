# recycle_platform.pip
# Integrated CLI-based Community Recycling Platform
from datetime import datetime, timedelta
import random
import math

# ================== In-Memory Databases ==================
scheduled_pickups = []
recycling_log = []
user_points = []
drop_off_points = []

MATERIAL_POINTS = {
    "Plastic": 5,
    "Paper": 3,
    "Glass": 4,
    "Metal": 6,
    "E-waste": 10
}

REWARD_TIERS = {
    500: "🏆 Planet Protector",
    200: "🌍 Green Warrior",
    100: "♻ Recycling Champion",
    50: "🌱 Eco Contributor"
}

# ================== Scheduling Pickups ==================

def schedule_pickup():
    print("\n--- Schedule Your Recycling Pickup ---")
    name = input("Enter your name: ")
    address = input("Enter your address: ")
    phone = input("Enter your phone number: ")
    material = input("Type of recyclable material (Plastic, Paper, etc.): ")

    date = input("Pickup date (YYYY-MM-DD): ")
    time = input("Pickup time (HH:MM): ")

    try:
        pickup_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        if pickup_datetime < datetime.now() + timedelta(minutes=30):
            print("⛔ Pickup must be scheduled at least 30 minutes in advance.")
            return

        pickup_id = f"PU-{random.randint(1000, 9999)}"
        scheduled_pickups.append({
            "id": pickup_id,
            "name": name,
            "material": material,
            "address": address,
            "datetime": pickup_datetime
        })

        # Reward points for scheduling
        user = next((u for u in user_points if u['name'] == name), None)
        if user:
            user['points'] += 5
            user['pickups'] = user.get('pickups', 0) + 1
        else:
            user_points.append({'name': name, 'points': 5, 'pickups': 1})

        recycling_log.append({
            "name": name,
            "material": "Pickup Scheduled",
            "quantity": 0,
            "points": 5,
            "timestamp": datetime.now()
        })

        print(f"\n✅ Pickup scheduled! ID: {pickup_id} on {pickup_datetime.strftime('%Y-%m-%d %H:%M')}")
        print("🎁 You earned +5 pts for scheduling a pickup!")

    except ValueError:
        print("⛔ Invalid date or time format.")

def view_pickups():
    print("\n📦 Scheduled Pickups:")
    if not scheduled_pickups:
        print("No pickups scheduled yet.")
        return
    for p in scheduled_pickups:
        print(f"[{p['id']}] {p['name']} - {p['material']} on {p['datetime'].strftime('%Y-%m-%d %H:%M')} at {p['address']}")

# ================== Logging & Rewards ==================

def log_recycling_menu():
    while True:
        print("\n--- Recycling & Rewards Menu ---")
        print("1. Log Recycling & Earn Points")
        print("2. Check Points Balance")
        print("3. View Log History")
        print("4. Refer a Friend (+10 pts)")
        print("5. Back")
        choice = input("Choose: ")

        if choice == "1":
            log_recycling()
        elif choice == "2":
            check_points_balance()
        elif choice == "3":
            view_log_history()
        elif choice == "4":
            refer_friend()
        elif choice == "5":
            break
        else:
            print("Invalid option.")

def log_recycling():
    print("\n--- Log Recycling & Earn Points ---")
    name = input("Enter your name: ")
    material = input("Material (Plastic, Paper, etc.): ").capitalize()
    if material not in MATERIAL_POINTS:
        print("Invalid material type.")
        return
    try:
        qty = float(input("Quantity (kg): "))
    except ValueError:
        print("Invalid quantity.")
        return

    points = MATERIAL_POINTS[material] * qty
    recycling_log.append({
        "name": name,
        "material": material,
        "quantity": qty,
        "points": points,
        "timestamp": datetime.now()
    })

    found = next((u for u in user_points if u['name'] == name), None)
    if found:
        found['points'] += points
    else:
        user_points.append({'name': name, 'points': points, 'pickups': 0})

    print(f"✅ {points} points earned for {qty}kg of {material}!")

def check_points_balance():
    name = input("Enter your name: ")
    user = next((u for u in user_points if u['name'] == name), None)
    if not user:
        print("No points found for this user.")
        return
    print(f"💰 {name}'s Current Balance: {user['points']} pts")

def view_log_history():
    name = input("Enter your name: ")
    logs = [log for log in recycling_log if log["name"] == name]
    if not logs:
        print("No history found for this user.")
        return
    print(f"\n📜 Recycling History for {name}:")
    for l in logs:
        print(f"- {l['quantity']}kg {l['material']} → {l['points']} pts at {l['timestamp'].strftime('%Y-%m-%d %H:%M')}")

def refer_friend():
    name = input("Your name: ")
    friend = input("Friend's name: ")
    # Add points to the inviter
    user = next((u for u in user_points if u['name'] == name), None)
    if user:
        user["points"] += 10
    else:
        user_points.append({'name': name, 'points': 10, 'pickups': 0})

    print(f"✅ {name} earned +10 pts for referring {friend}!")

# ================== Achievements ==================

def view_achievements():
    name = input("Enter your name: ")
    user = next((u for u in user_points if u['name'] == name), None)
    if not user:
        print("No points found for this user.")
        return
    pts = user["points"]
    pickups = user.get("pickups", 0)

    # Base achievement system
    achievement_list = []
    if pickups >= 1:
        achievement_list.append("📦 First Recycling Pickup")
    if pickups >= 5:
        achievement_list.append("🚛 Recycling Regular (5+ pickups)")
    if pickups >= 10:
        achievement_list.append("🏅 Eco Veteran (10+ pickups)")
    if pts >= 50:
        achievement_list.append("🌱 Earned 50+ Points")
    if pts >= 100:
        achievement_list.append("♻ Recycling Champion")
    if any(log["material"] == "Pickup Scheduled" for log in recycling_log if log["name"] == name):
        achievement_list.append("👥 Invited a Friend")

    print(f"\n🏅 {name}'s Total Points: {pts}")
    print(f"📊 Total Pickups: {pickups}")
    if achievement_list:
        print("\n🎖 Achievements Unlocked:")
        for a in achievement_list:
            print(f"- {a}")
    else:
        print("No achievements yet. Keep recycling!")

# ================== Leaderboard (by Pickups) ==================

def view_leaderboard():
    print("\n🏆 Leaderboard (Most Pickups):")
    sorted_users = sorted(user_points, key=lambda x: x.get('pickups', 0), reverse=True)
    if not sorted_users:
        print("No user data recorded yet.")
        return
    for i, u in enumerate(sorted_users, start=1):
        print(f"{i}. {u['name']} - {u.get('pickups',0)} pickups ({u['points']} pts)")

# ================== Drop-off Points ==================

def add_drop_point():
    print("\n--- Add Drop-off Location ---")
    name = input("Location name: ")
    address = input("Address: ")
    try:
        lat = float(input("Latitude: "))
        lon = float(input("Longitude: "))
    except ValueError:
        print("Invalid coordinates.")
        return
    drop_off_points.append({
        "name": name,
        "address": address,
        "lat": lat,
        "lon": lon
    })
    print("✅ Drop-off point added.")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)*2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)*2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def find_nearby_drops():
    print("\n--- Find Nearby Drop-offs ---")
    try:
        user_lat = float(input("Your latitude: "))
        user_lon = float(input("Your longitude: "))
        radius = float(input("Search radius (km): "))
    except ValueError:
        print("Invalid input.")
        return

    found = False
    for p in drop_off_points:
        dist = haversine(user_lat, user_lon, p["lat"], p["lon"])
        if dist <= radius:
            print(f"\n📍 {p['name']} ({dist:.2f} km)\nAddress: {p['address']}")
            found = True
    if not found:
        print("❌ No locations within range.")

def view_all_drops():
    print("\n📋 All Drop-off Locations:")
    if not drop_off_points:
        print("No drop-off points added yet.")
    for p in drop_off_points:
        print(f"{p['name']} at ({p['lat']}, {p['lon']}) — {p['address']}")

# ================== Submenus ==================

def other_options_menu():
    while True:
        print("\n=== Other Options ===")
        print("1. Recycling & Rewards")
        print("2. View My Achievements")
        print("3. View Leaderboard")
        print("4. Back")
        choice = input("Choose: ")
        if choice == "1": log_recycling_menu()
        elif choice == "2": view_achievements()
        elif choice == "3": view_leaderboard()
        elif choice == "4": break
        else: print("Invalid option.")

def geo_menu():
    while True:
        print("\n=== Drop-off Locations ===")
        print("1. Add Drop-off Location")
        print("2. Find Nearby Drop-off Locations")
        print("3. View All Drop-off Points")
        print("4. Back")
        choice = input("Choose: ")
        if choice == "1": add_drop_point()
        elif choice == "2": find_nearby_drops()
        elif choice == "3": view_all_drops()
        elif choice == "4": break
        else: print("Invalid option.")

# ================== Main Menu ==================

def main():
    while True:
        print("\n=== Community Recycling Platform ===")
        print("1. Schedule a Pickup")
        print("2. View Scheduled Pickups")
        print("3. Other Options")
        print("4. Drop-off Locations")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == "1": schedule_pickup()
        elif choice == "2": view_pickups()
        elif choice == "3": other_options_menu()
        elif choice == "4": geo_menu()
        elif choice == "5":
            print("👋 Goodbye! Keep recycling ♻")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
