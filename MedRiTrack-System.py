from datetime import datetime

print(" 💊  Welcome to MedRiTrack: Medicine Reminder Tracker System")
print("---------------------------------------------------------------")

# Basic input validator
def get_nonempty_input(message):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("⚠️  Input cannot be blank.")

# Reads one or more time values
def get_time_list():
    while True:
        raw_times = input("⏰ Time(s) (e.g., 08:00 AM or 08:00 AM, 08:00 PM): ").upper()
        try:
            return [
                datetime.strptime(t.strip(), "%I:%M %p").time()
                for t in raw_times.split(",")
            ]
        except:
            print("⚠️  Invalid time format.")

# Reads end date
def get_date():
    while True:
        raw_date = input("📅 End date (MM-DD-YYYY): ")
        try:
            return datetime.strptime(raw_date, "%m-%d-%Y").date()
        except:
            print("⚠️  Invalid date format.")

# Creates one medicine record
def add_medicine():
    name = get_nonempty_input("💊 Medicine Name: ").title()
    dose = get_nonempty_input("💧 Dosage: ")
    days = get_nonempty_input("🗓️ Days (Mon,Wed,Fri or Everyday): ").lower()
    times = get_time_list()
    end_date = get_date()

    return {
        "name": name,
        "dose": dose,
        "days": days,
        "times": times,
        "end": end_date,
        "taken": 0,
        "missed": 0,
        "status": "Not yet time"
    }

# Start program
user_name = get_nonempty_input("Please enter your name: ").title()
print(f"\nHello {user_name}. Let's set up your medicine reminders.\n")

medicine_list = []

# Add initial medicines
medicine_count = int(get_nonempty_input("➕ How many medicines to add? "))
for _ in range(medicine_count):
    print("\n📝 Medicine details:")
    medicine_list.append(add_medicine())

# For converting Mon/Tue/Wed to Monday/Tuesday/Wednesday
day_map = {
    "mon": "monday", "tue": "tuesday", "wed": "wednesday",
    "thu": "thursday", "fri": "friday", "sat": "saturday", "sun": "sunday"}

print(f"\nAll medicines recorded successfully, {user_name}! 🎉")

# Main loop
while True:
    print("\n-----------------------------------------------------------------------")
    command = input("⌨️ Enter 'MM-DD-YYYY HH:MM AM/PM', or 'add', or 'exit': ").lower()

    # Exit and print final summary
    if command == "exit":
        print(f"\n👋 Goodbye {user_name}.")

        total_taken = sum(m["taken"] for m in medicine_list)
        total_missed = sum(m["missed"] for m in medicine_list)

        print("\n======================  MEDICATION SUMMARY REPORT  ======================\n")
        for m in medicine_list:
            times = ", ".join(t.strftime("%I:%M %p") for t in m["times"])
            print("-------------------------------------------------------------------------------")
            print(f"💊 Medicine: {m['name']}")
            print(f"💧 Dosage: {m['dose']}")
            print(f"🗓️ Days: {m['days']}")
            print(f"⏰ Time Schedule: {times}")
            print(f"📅 End Date: {m['end']}")
            print(f"✅ Taken: {m['taken']}   |    ❌ Missed: {m['missed']}")
            print(f"📌 Status: {m['status']}")
        print("\n===============================================================================")
        print(f"TOTAL TAKEN: {total_taken}   |    TOTAL MISSED: {total_missed}")
        print("Thank you for using MediTrack. 🙏")
        print("===============================================================================\n")
        break

    # Add new medicine anytime
    if command == "add":
        print("\n➕  New medicine:")
        medicine_list.append(add_medicine())
        continue

    # Validate date and time
    try:
        current_datetime = datetime.strptime(command, "%m-%d-%Y %I:%M %p")
    except:
        print("⚠️ Invalid format.")
        continue

    today_day = current_datetime.strftime("%A").lower()
    current_time = current_datetime.time()

    print(f"\n=============== 📋 Medicine Report for {user_name} ===============")

    for med in medicine_list:

        # Prepare schedule days
        if "every" in med["days"]:
            schedule_days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
        else:
            schedule_days = []
            for d in med["days"].split(","):
                key = d.strip()[:3]
                if key in day_map:
                    schedule_days.append(day_map[key])

        # Expired
        if current_datetime.date() > med["end"]:
            med["status"] = "Expired"
            print(f"⌛️  {med['name']} is past its end date.")
            continue

        # Not scheduled today
        if today_day not in schedule_days:
            med["status"] = "Not sched today"
            print(f"📌  {med['name']} is not scheduled today.")
            continue

        # Determine status based on time
        upcoming = False
        exact = False
        late = False

        for t in med["times"]:
            if current_time < t:
                upcoming = True
            elif current_time == t:
                exact = True
            elif current_time > t:
                late = True

        # Before time
        if upcoming and not exact and not late:
            med["status"] = "Not yet time"
            print(f"⏳ Not yet time for {med['name']} ({med['dose']}).")

        # On exact time
        elif exact:
            print(f"\n🔔 Reminder: Time to take {med['name']} ({med['dose']}).")
            response = input("Did you take it? (yes/no): ").lower()
            if response == "yes":
                med["taken"] += 1
                med["status"] = "Taken"
                print("✅ Recorded as taken.")
            else:
                med["missed"] += 1
                med["status"] = "Missed"
                print("❌ Recorded as missed.")

        # Late or missed
        elif late and med["status"] not in ["Taken", "Missed"]:
            med["missed"] += 1
            med["status"] = "Missed"
            print(f"⚠️ You missed the schedule for {med['name']} earlier.")

        # Display record
        times = ", ".join(t.strftime("%I:%M %p") for t in med["times"])
        print("\n+------------------------------------- MEDICINE RECORD -------------------------------------+")
        print(
            f"💊 Medicine: {med['name']} | 💧 Dose: {med['dose']} | 🗓️ Days: {med['days']} | "
            f"⏰ Time: {times} | 📅 End Date: {med['end']} | 📌 Status: {med['status']} | "
            f"✅ Taken: {med['taken']} | ❌ Missed: {med['missed']}")

    print("\nYou may enter another date, add medicine, or exit.")