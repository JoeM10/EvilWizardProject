# Defeat the Evil Wizard

## Description

**Defeat the Evil Wizard** is a Python turn-based battle game where the player chooses a character class and fights against an Evil Wizard.

The game uses object-oriented programming with classes, inheritance, special abilities, healing, randomized damage, and status effects.

## How to Run

Run the game from the terminal:

```bash
python DefeatTheEvilWizard.py
```

Or, depending on your system:

```bash
python3 DefeatTheEvilWizard.py
```

## How to Play

At the start of the game, choose one of four character classes:

1. Warrior
2. Mage
3. Druid
4. Paladin

Each turn, the player can:

1. Attack
2. Use a special ability
3. Heal
4. View stats

After the player takes an action, the Evil Wizard regenerates health and attacks.

The game ends when either the player or the Evil Wizard reaches 0 health.

## Character Classes

### Warrior

A strong melee fighter with high health and defense.

**Abilities:**

- **Rage**: Increases attack power but lowers defense temporarily.
- **Disarm**: Deals damage and lowers the enemy's attack power.

### Mage

A powerful spellcaster with high attack power but lower health.

**Abilities:**

- **Fireball**: Deals heavy damage with a cooldown.
- **Mage Armor**: Temporarily increases defense.

### Druid

A balanced character with healing and damage-over-time abilities.

**Abilities:**

- **Entangle**: Deals damage over time.
- **Rejuvenate**: Heals over time.

### Paladin

A defensive character with high health, healing, and reliable ability damage.

**Abilities:**

- **Law of Equality**: Deals damage and heals the player.
- **Hammer of Justice**: Deals direct damage with a cooldown.

## Evil Wizard

The Evil Wizard is the enemy. After each player turn, the wizard:

- Regenerates health
- Attacks the player

## Features

- Four playable character classes
- Two special abilities per class
- Randomized attack damage
- Healing system with max-health limit
- Status effects and cooldowns
- Turn-based combat
- Victory and defeat messages

## Python Concepts Used

- Classes and objects
- Inheritance
- Methods
- Loops
- Conditional statements
- User input
- Random number generation

## Author

Created by Joseph McDaniel
Github: https://github.com/JoeM10/