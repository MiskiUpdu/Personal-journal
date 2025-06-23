import json
import os
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

class JournalEntry:
    def __init__(self, title, mood, content, forget):
        self.title = title
        self.mood = mood if mood else "mixed"
        self.content = content
        self.forget = forget 
        self.date = datetime.now().strftime("%Y-%m-%d %I:%M %p")  

    def to_dict(self):
        return {
            "title": self.title,
            "mood": self.mood,
            "content": self.content,
            "forget": self.forget,
            "date": self.date
        }

    def display(self):
        print(Fore.CYAN + f"\n{self.title} ({self.date})")
        print(f"Mood: {self.mood}")
        print(f"Thoughts: {self.content}")
        print(f"Forgettable: {self.forget}\n")

class JournalManager:
    def __init__(self):
        self.entries = []
        self.file_name = "journal_entries.json"
        self.load_entries()

    def load_entries(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                    data = json.load(file)
                    for entry_data in data:
                        entry = JournalEntry(
                            entry_data["title"],
                            entry_data["mood"],
                            entry_data["content"],
                            entry_data.get("forget", "")
                        )
                        entry.date = entry_data["date"]
                        self.entries.append(entry)
               
    def save_entries(self):
        with open(self.file_name, "w") as file:
            json.dump([entry.to_dict() for entry in self.entries], file, indent=4)

    def write_entry(self):
        print(Fore.YELLOW + "\n Let's write something new")
        title = input("Title: ") 
        mood = input("How are you feeling today? ")
        content = input("What is on your mind right now?\n> ")
        forget = input("Anything you would like to forget today?\n> ")

        entry = JournalEntry(title, mood, content, forget)
        self.entries.append(entry)
        self.save_entries()
        print(Fore.GREEN + "\n✅ Entry saved! Come back anytime.")

    def view_entries(self):
        print(Fore.MAGENTA + "\nYour Journal Entries:")
        if not self.entries:
            print("You haven't written anything yet. Today is a pretty good day to start")
        else:
            for entry in self.entries:
                entry.display()

    def search_by_mood(self):
        mood_to_search = input("\n What mood would you like to search?:  ").strip()
        if not mood_to_search:
            print("Please enter a valid mood.")
            return
        found = False
        for entry in self.entries:
            if entry.mood.lower() == mood_to_search.lower():
                entry.display()
                found = True
        if not found:
            print("No entries matched that mood Try again later.")

    def run(self):
        while True:
            print(Fore.BLUE + "\nWelcome to thee Personal Journal")
            print("1. Write a new journal entry")
            print("2. View all entries")
            print("3. Search entries by mood")
            print("4. Exit")

            choice = input("Choose (1-4): ")

            if choice == "1":
                self.write_entry()
            elif choice == "2":
                self.view_entries()
            elif choice == "3":
                self.search_by_mood()
            elif choice == "4":
                print(Fore.YELLOW + "\n Take care ooo See you next time")
                break
            else:
                print(Fore.RED + "Invalid option. please choose between 1 and 4.")

if __name__ == "__main__":
    journal_app = JournalManager()
    journal_app.run()
