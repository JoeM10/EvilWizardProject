import random

# Base Character class
class Character:
    def __init__(self, name, health, attack_power, defense=0):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.max_health = health
        self.status_effects = []
        self.active_effect_names = []

    def attack(self, opponent, set_fixed_damage=0):
        # Use set_fixed_damage to deal a specific amount of damage regarless of effects and modifiers.
        if set_fixed_damage != 0:
            opponent.health -= set_fixed_damage
            print(f"{self.name} attacks {opponent.name} for {set_fixed_damage} damage!")
        else:
            self.randomize_damage = random.randint(self.get_attack_power() - 10, self.get_attack_power())
            self.damage_dealt = self.randomize_damage - opponent.get_defense()
            if self.damage_dealt < 0:
                self.damage_dealt = 0
            opponent.health -= self.damage_dealt
            print(f"{self.name} attacks {opponent.name} for {self.damage_dealt} damage!")
            if opponent.health <= 0:
                print(f"{opponent.name} has been defeated!")

    def display_stats(self):
        print(f"\n- {self.name}'s Stats -")
        print(f"Health: {self.get_health()}/{self.max_health}")
        print(f"Attack Power: {self.get_attack_power()}")
        print(f"Defense: {self.get_defense()}")
        print(f"Active Effects: {self.active_effect_names}")

    def heal(self, amount):
        newTotal = self.health + amount
        if newTotal > self.max_health:
            self.health = self.max_health
        else:
            self.health = newTotal

    # Use the class StatusEffect to add a status to an entity.
    def add_status_effect(self, status_effect):
        self.status_effects.append(status_effect)
        self.active_effect_names.append(status_effect.name)

    # Manages the tick durations and removes expired effects.
    def tick_status_effects(self):
        for effect in self.status_effects:
            if effect.stat == "dot":
                self.heal -= effect.status_modifier
            elif effect.stat == "hot":
                self.heal(effect.status_modifier)
            effect.tick()
            if effect.duration <= 0:
                self.status_effects.remove(effect)
                self.active_effect_names.remove(effect.name)

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

    def showAbilities(self, opponent):
        self.choosing = True
        while self.choosing:
            print("\n1. Rage - Increase damage by 15 but reduce defense to 0 for 3 turns.")
            print("\n2. Disarm - Deal 5 damage and reduce the enemies damage by 10 for 3 turns.")
            print("\n3. Return.\n")
            self.choice = input("Choice: ").strip()
            if self.choice == "1":
                self.rage()
                self.choosing = False
                return True
            elif self.choice == "2":
                self.disarm(opponent)
                self.choosing = False
                return True
            elif self.choice == "3":
                return False
            else:
                print("\nInvalid input. Please select from the available choices.\n")

# Warrior Abilities.
    def rage(self):
        self.add_status_effect(StatusEffect("Rage Damage up!", "attack", duration=3, status_modifier=15))
        self.add_status_effect(StatusEffect("Rage Defense down!", "defense", duration=3, status_modifier=-self.get_defense()))

    def disarm(self, opponent):
        opponent.add_status_effect(StatusEffect("Disarm", "attack", duration=3, status_modifier=-10))
        self.attack(opponent, 5)

# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)

    def showAbilities(self, opponent):
        self.choosing = True
        while self.choosing:
            print("\n1. Fireball - A powerful spell that deals 70 damage but can only be used 1 time every 4 turns.")
            print("\n2. Mage Armor - Increase defense by 10 for 3 turns.")
            print("\n3. Return.\n")
            self.choice = input("Choice: ").strip()
            if self.choice == "1":
                if "Used Fireball" in self.active_effect_names:
                    for effect in self.status_effects:
                        if effect.name == "Used Fireball":
                            print(f"\nYou cannot use Fireball for another {effect.duration} turns.\n")
                            return False
                else:
                    self.fireball(opponent)
                    self.choosing = False
                    return True
            elif self.choice == "2":
                self.mage_armor()
                return True
            elif self.choice == "3":
                return False
            else:
                print("\nInvalid input. Please select from the available choices.\n")

# Mage Abilities
    def fireball(self, opponent):
        self.attack(opponent, 70)
        self.add_status_effect(StatusEffect("Fireball on cooldown", "attack", 4, 0))

    def mage_armor(self):
        self.add_status_effect(StatusEffect("Mage Armor", "defense", 3, 10))

# Druid class (inherits from Character)
class Druid(Character):
    def __init__(self, name):
        super().__init__(name, health=110, attack_power=30, defense=5)

    def showAbilities(self, opponent):
        self.choosing = True
        while self.choosing:
            print("\n1. Entangle - Wrap spiked vines around the enemy, dealing 10 damage every turn for 3 turns.\n")
            print("\n2. Rejuvenate - Heal for 10 health, and an extra 10 health every turn for 3 turns.")
            print("\n3. Return.\n")
            self.choice = input("Choice: ").strip()
            if self.choice == "1":
                self.entangle(opponent)
                return True
            elif self.choice == "2":
                self.rejuvenate()
                return True
            elif self.choice == "3":
                return False
            else:
                print("\nInvalid input. Please select from the available choices.\n")

    # Druid abilities.
    def entangle(self, opponent):
        opponent.add_status_effect(StatusEffect("Entangled", "dot", 3, 10))
        
    def rejuvenate(self):
        self.add_status_effect(StatusEffect("Rejuvenate", "hot", 3, 10))

# Paladin class (inherits from Character)
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=160, attack_power=15, defense=10)

    def showAbilities(self, opponent):
        self.choosing = True
        while self.choosing:
            print("\n1. Law of Equality - Deal 20 damage and heal 20 health. Can only be used every 4 turns.")
            print("\n2. Hammer of Justice - Throw a hammer that deals 30 damage. Can only be used every 2 turns.")
            print("\n3. Return.\n")
            self.choice = input("Choice: ").strip()
            if self.choice == "1":
                if "Law of Equality Cooldown" in self.active_effect_names:
                    for effect in self.status_effects:
                        if effect.name == "Law of Equality Cooldown":
                            print(f"\nYou have achieved Equilibrium too recently. Turns remaining {effect.duration}.")
                            return False
                else:
                    self.law_of_equality(opponent)
                    self.choosing = False
                    return True
            elif self.choice == "2":
                if "Hammer of Justice Cooldown" in self.active_effect_names:
                    for effect in self.status_effects:
                        if effect.name == "Hammer of Justice Cooldown":
                            print(f"\nHamme of Justice is on cooldown. Turns remaining {effect.duration}.")
                            return False
                else:
                    self.hammer_of_justice(opponent)
                    return True
            elif self.choice == "3":
                return False
            else:
                print("\nInvalid input. Please select from the available choices.\n")

    # Paladin abilities.
    # Law of Equality - Deal 20 damage and heal 20 health. Can only be used every 4 turns.
    def law_of_equality(self, opponent):
        self.add_status_effect(StatusEffect("Law of Equality Cooldown", "health", 4, 0))
        self.attack(opponent, 20)
        self.heal(20)

    # Hammer of Justice - Throw a hammer that deals 30 damage. Can only be used every 2 turns.
    def hammer_of_justice(self, opponent):
        self.add_status_effect(StatusEffect("Hammer of Justice Cooldown", "attack", 2, 0))
        self.attack(opponent, 30)

# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=175, attack_power=25)
        self.isDisarmed = False
        self.disarmedTurnsRemaining = 0

    def regenerate(self, healAmount=5):
        self.heal(5)
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
            print(f"1. Attack - {player.get_attack_power()} damage")
            print("2. Use Special Ability")
            print("3. Heal - Heal for 15 health")
            print("4. View Stats")
            choice = input("Choose an action: ")

            if choice == '1':
                player.attack(wizard)
                choosing = False
            elif choice == '2':
                if player.showAbilities(wizard):
                    choosing = False
                else:
                    continue
            elif choice == '3':
                player.heal(15)
                choosing = False
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