# Base Character class
class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.max_health = health  

    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(f"{self.name} attacks {opponent.name} for {self.attack_power} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")

    def display_stats(self):
        print(f"{self.name}'s Stats - Health: {self.health}/{self.max_health}, Attack Power: {self.attack_power}")

# Status effects class
class StatusEffect:
    def __init__(self, name, duration, attack_modifier=0, defense_modifier=0, health_modifier=0):
        self.name = name
        self.duration = duration
        self.attack_modifier = attack_modifier
        self.defense_modifier = defense_modifier
        self.health_modifier = health_modifier
    
    def tick(self):
        self.duration -= 1

# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25)
        self.isRaging = False
        self.rageTurnsRemaining = 0
        self.isDisarming = False

    def showAbilities(self):

        choosing = True
        while choosing:
            print("1. Rage - Increase damage by 15 but double damage taken for 3 turns.")
            print("2. Disarm - Deal 5 damage and reduce the enemies damage by 10 for 3 turns.")
            choice = input("Choice: ").strip()
            if choice == "1":
                self.rage()
                choosing = False
            elif choice == "2":
                self.disarm()
                choosing = False
            else:
                print("\nInvalid input. Please select from the available choices.\n")

    def rage(self):
        self.attack_power = 25
        self.attack_power += 15
        self.isRaging = True
        self.rageTurnsRemaining = 3

    def disarm(self):
        self.isDisarming = True

# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)

# Druid class (inherits from Character)
class Druid(Character):
    def __init__(self, name):
        super().__init__(name, health=110, attack_power=30)

# Paladin class (inherits from Character)
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=160, attack_power=20)

# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=175, attack_power=15)
        self.isDisarmed = False
        self.disarmedTurnsRemaining = 0

    def regenerate(self, healAmount=5):
        self.health += healAmount
        print(f"{self.name} regenerates {healAmount} health! Current health: {self.health}")

# ^-^-^-^-^-^-CLASSES GO ABOVE-^-^-^-^-^-^ #

def create_character():
    print("Choose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Druid") 
    print("4. Paladin")  

    class_choice = input("Enter the number of your class choice: ")
    name = input("Enter your character's name: ")

    if class_choice == '1':
        return Warrior(name)
    elif class_choice == '2':
        return Mage(name)
    elif class_choice == '3':
        return Druid(name)
    elif class_choice == '4':
        return Paladin(name)
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Warrior(name)

def battle(player, wizard):
    while wizard.health > 0 and player.health > 0:

        choosing = True
        while choosing:
            print("\n--- Your Turn ---")
            print("1. Attack")
            print("2. Use Special Ability")
            print("3. Heal")
            print("4. View Stats")
            choice = input("Choose an action: ")

            if choice == '1':
                player.attack(wizard)
                choosing = False
            elif choice == '2':
                player.showAbilities()
                choosing = False
            elif choice == '3':
                choosing = False  # Implement heal method
            elif choice == '4':
                player.display_stats()
            else:
                print("Invalid choice. Try again.")

        # Logic for Warriors abilities.
        try:
            # Logic for Warrior Rage ability.
            if player.isRaging == True and player.rageTurnsRemaining == 3:
                wizard.attack_power *= 2
                player.rageTurnsRemaining -= 1
            elif player.isRaging == True and player.rageTurnsRemaining > 0:
                player.rageTurnsRemaining -= 1
            elif player.isRaging == True and player.rageTurnsRemaining == 0:
                player.isRaging = False
                player.attack_power = 25
                wizard.attack_power = 15

            # Logic for Warrior Disarm ability.
            if player.isDisarming == True and wizard.isDisarmed == False:
                wizard.isDisarmed = True
                wizard.disarmedTurnsRemaining = 2
                wizard.attack_power -= 10
                wizard.health -= 5
            elif player.isDisarming == True and wizard.disarmedTurnsRemaining > 0:
                wizard.disarmedTurnsRemaining -= 1
            elif player.isDisarming == True and wizard.disarmedTurnsRemaining == 0:
                wizard.attack_power = 15
                player.isDisarming = False
                wizard.isDisarmed = False
        except:
            continue

        if wizard.health > 0:
            wizard.regenerate()
            wizard.attack(player)

        if player.health <= 0:
            print(f"{player.name} has been defeated!")
            break

    if wizard.health <= 0:
        print(f"The wizard {wizard.name} has been defeated by {player.name}!")

def main():
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)

if __name__ == "__main__":
    main()