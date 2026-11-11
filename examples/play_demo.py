from termpet.feed import feed
from termpet.pet import Pet
from termpet.play import play
from termpet.render import render
from termpet.sleep import sleep
from termpet.status import status
from termpet.storage import load, save
from termpet.tick import tick

def main():
    while True:
        try:
            name = input("Pet name: ").strip()
            species = input("Species: ").strip()
            pet = Pet(name, species)
            break
        except ValueError as error:
            print(error)

    while True:
        print(render(pet))
        action = input("feed / sleep / play / wait / status / save / load / quit: ")
        action = action.strip().lower()

        try:
            if action == "quit":
                break
            elif action == "feed":
                feed(pet, input("Food: "))
            elif action == "sleep":
                sleep(pet, float(input("Hours: ")))
            elif action == "play":
                game = input("Game: ")
                minutes = int(input("Minutes: "))
                play(pet, game, minutes)
            elif action == "wait":
                tick(pet, int(input("Hours: ")))
            elif action == "status":
                print(status(pet))
            elif action == "save":
                save(pet, input("Save to file: "))
            elif action == "load":
                pet = load(input("Load from file: "))
            else:
                print("Choose an action from the menu.")
        except (ValueError, OSError) as error:
            print(error)


if __name__ == "__main__":
    main()
