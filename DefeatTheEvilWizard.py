# Base Character class
class Character:
    def __init__(self, name, health, attack_power, defense=0):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.max_health = health
        self.status_effects = []

    def attack(self, opponent):
        self.damage_dealt = self.get_attack_power() - opponent.get_defense()
        if self.damage_dealt < 0:
            self.damage_dealt = 0
        opponent.health -= self.damage_dealt
        print(f"{self.name} attacks {opponent.name} for {self.damage_dealt} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")

    def display_stats(self):
        print(f"{self.name}'s Stats - Health: {self.get_health()}/{self.max_health}, Attack Power: {self.get_attack_power()}")

    def add_status_effect(self, status_effect):
        self.status_effects.append(status_effect)

    def tick_status_effects(self):
        for effect in self.status_effects:
            effect.tick()
            if effect.duration <= 0:
                self.status_effects.remove(effect)

    def get_attack_power(self):
        self.total_attack = self.attack_power

        for effect in self.status_effects:
            if effect.stat == "attack":
                self.total_attack += effect.status_modifier
        
        return self.total_attack

    def get_defense(self):
        self.total_defense = self.defense

        for effect in self.status_effects:
            if effect.stat == "defense":
                self.total_defense += effect.status_modifier

        return self.total_defense
    
    def get_health(self):
        self.total_health = self.health

        for effect in self.status_effects:
            if effect.stat == "health":
                self.total_health += effect.status_modifier

        return self.total_health
    
# Status effects class
class StatusEffect:
    def __init__(self, name, stat, duration, status_modifier=0):
        self.name = name
        self.stat = stat
        self.duration = duration
        self.status_modifier = status_modifier

    def tick(self):
        self.duration -= 1

# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25, defense=10)

    def showAbilities(self):
        self.choosing = True
        while self.choosing:
            print("1. Rage - Increase damage by 15 but reduce defense to 0 for 3 turns.")
            print("2. Disarm - Deal 5 damage and reduce the enemies damage by 10 for 3 turns.")
            choice = input("Choice: ").strip()
            if choice == "1":
                self.rage()
                self.choosing = False
            elif choice == "2":
                self.disarm()
                self.choosing = False
            else:
                print("\nInvalid input. Please select from the available choices.\n")

    def rage(self):
        self.add_status_effect(StatusEffect("Rage", "attack", duration=3, status_modifier=15))
        self.add_status_effect(StatusEffect("Rage", "defense", duration=3, status_modifier=-self.get_defense()))

    def disarm(self, opponent):
        opponent.add_status_effect(StatusEffect("Disarm", "attack", duration=3, status_modifier=-10))

# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)

# Druid class (inherits from Character)
class Druid(Character):
    def __init__(self, name):
        super().__init__(name, health=110, attack_power=30, defense=5)

# Paladin class (inherits from Character)
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=160, attack_power=20, defense=15)

# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=175, attack_power=25)
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

        if wizard.health > 0:
            wizard.regenerate()
            wizard.attack(player)

        if player.health <= 0:
            print(f"{player.name} has been defeated!")
            break

        player.tick_status_effects()
        wizard.tick_status_effects()

    if wizard.health <= 0:
        print(f"The wizard {wizard.name} has been defeated by {player.name}!")
    

def main():
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)

if __name__ == "__main__":
    main()