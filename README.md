# MHW Quest Generator

A Python-based command-line tool for generating custom quests for Monster Hunter World's PermanentEventQuest Mod.

## Features

- 🎮 Generate custom quests with configurable parameters
- 🐉 22 different monsters from Monster Hunter World
- 🗺️ Support for all major maps (Ancient Forest, Wildspire Waste, etc.)
- 💎 Dynamic reward generation based on quest difficulty
- 🎯 Support for single or multi-monster hunts (up to 3 monsters)
- 📝 Interactive mode for easy quest creation
- 🔧 Command-line interface for batch generation and automation

## Installation

1. Clone this repository:
```bash
git clone https://github.com/maxraeche/mhw-quest-gen.git
cd mhw-quest-gen
```

2. Install Python 3.6 or higher (if not already installed)

3. Make the script executable (Linux/Mac):
```bash
chmod +x quest_gen.py
```

## Usage

### Interactive Mode

Run the generator in interactive mode for a guided quest creation experience:

```bash
python3 quest_gen.py --interactive
```

The interactive mode will prompt you for:
- Quest title
- Quest description
- Number of monsters (1-3)
- Difficulty level (1-9)
- Map selection
- Number of reward items

### Command-Line Mode

Generate quests using command-line arguments:

```bash
# Generate a simple single-monster quest
python3 quest_gen.py

# Generate a quest with specific parameters
python3 quest_gen.py -t "Elder Dragon Challenge" -m 1 --difficulty 9 -r 5

# Generate a multi-monster hunt
python3 quest_gen.py -t "Double Trouble" -m 2 --difficulty 7

# Generate on a specific map
python3 quest_gen.py -t "Ancient Forest Expedition" --map "Ancient Forest" --difficulty 3

# Generate multiple quests at once
python3 quest_gen.py -n 5
```

### Command-Line Options

```
-h, --help            Show help message
-i, --interactive     Run in interactive mode
-t, --title          Quest title
-d, --description    Quest description
-m, --monsters       Number of monsters (1-3, default: 1)
--difficulty         Difficulty level (1-9)
--map                Map name (Ancient Forest, Wildspire Waste, etc.)
-r, --rewards        Number of reward items (1-10, default: 3)
-o, --output         Output directory (default: output)
--data-dir           Data directory path (default: data)
-n, --count          Number of quests to generate (default: 1)
```

## Output Format

Generated quests are saved as JSON files with the following structure:

```json
{
  "quest_info": {
    "title": "Quest Title",
    "description": "Quest description",
    "difficulty": 5,
    "map": "Ancient Forest",
    "map_id": 1,
    "time_limit": 50,
    "zenny_reward": 5500,
    "hrp_reward": 600
  },
  "monsters": [
    {
      "monster_id": 17,
      "name": "Nergigante",
      "type": "Elder Dragon",
      "is_target": true,
      "initial_area": 8
    }
  ],
  "rewards": [
    {
      "item_id": 15,
      "item_name": "Wyvern Gem",
      "quantity": 1,
      "probability": 0.35,
      "rarity": 6
    }
  ],
  "conditions": {
    "objective_type": "hunt",
    "target_count": 1,
    "failure_conditions": ["time_up", "cart_3_times"]
  },
  "metadata": {
    "generated_at": "2026-01-16T20:00:00.000000",
    "generator_version": "1.0.0"
  }
}
```

## Examples

Example quests can be found in the `examples/` directory:

- `ancient_forest_expedition.quest.json` - A basic hunt in the Ancient Forest
- `elder_dragon_challenge.quest.json` - A high-difficulty elder dragon hunt

## Available Content

### Monsters

The generator includes 22 monsters spanning all threat levels:
- **Threat Level 1-2**: Great Jagras, Kulu-Ya-Ku, Pukei-Pukei, Barroth, Tobi-Kadachi, Anjanath, etc.
- **Threat Level 3-4**: Rathian, Rathalos, Diablos, Odogaron, Legiana, Bazelgeuse, Kirin
- **Threat Level 5**: Nergigante, Teostra, Kushala Daora, Vaal Hazak, Deviljho

### Maps

- Ancient Forest
- Wildspire Waste
- Coral Highlands
- Rotten Vale
- Elder's Recess
- Arena

### Items

The generator includes various reward items from potions to rare gems, with rarity-based selection based on quest difficulty.

## Integration with PermanentEventQuest Mod

The generated JSON files are designed to work with the Custom Quest Loader mod for Monster Hunter World. To use:

1. Generate your quest using this tool
2. Copy the generated `.quest.json` file to your Custom Quest Loader mod directory
3. Follow the mod's instructions for loading custom quests

**Note**: The exact integration steps may vary depending on the mod version. Refer to the PermanentEventQuest Mod documentation for specific installation instructions.

## Data Files

Quest data is stored in the `data/` directory:
- `monsters.json` - Monster definitions with IDs, names, types, and threat levels
- `maps.json` - Map definitions with IDs, names, and area counts
- `items.json` - Item/reward definitions with IDs, names, and rarity

You can edit these files to customize available content or add new monsters, maps, and items.

## Contributing

Contributions are welcome! Feel free to:
- Add more monsters, maps, or items
- Improve quest generation logic
- Add new features or options
- Fix bugs or improve documentation

## License

This project is provided as-is for use with Monster Hunter World mods. Monster Hunter World and all related content are property of Capcom.

## Acknowledgments

- Inspired by the Monster Hunter World modding community
- Created for use with the PermanentEventQuest and Custom Quest Loader mods
