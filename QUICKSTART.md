# Quick Start Guide

## Generate Your First Quest

### Option 1: Interactive Mode (Recommended for beginners)

```bash
python3 quest_gen.py --interactive
```

Follow the prompts to create your custom quest!

### Option 2: Quick Command

Generate a simple quest with one command:

```bash
python3 quest_gen.py -t "My First Hunt" -m 1 --difficulty 3
```

This creates a quest file in the `output/` directory.

### Option 3: Advanced Quest

Create a multi-monster hunt with custom parameters:

```bash
python3 quest_gen.py \
  -t "Double Dragon Trouble" \
  -d "Face two powerful flying wyverns" \
  -m 2 \
  --difficulty 7 \
  --map "Ancient Forest" \
  -r 5
```

## What's Next?

1. Check the generated `.quest.json` file in the `output/` directory
2. Review the quest structure and customize if needed
3. Copy the file to your Custom Quest Loader mod directory
4. Load up Monster Hunter World and enjoy your custom quest!

## Tips

- Start with difficulty 1-3 for easier quests
- Use difficulty 7-9 for challenging elder dragon hunts
- Multi-monster hunts (2-3 monsters) are significantly harder
- Different maps offer different environments and challenges

## Example Commands

```bash
# Generate 5 random quests
python3 quest_gen.py -n 5

# Create an elder dragon hunt
python3 quest_gen.py -t "Elder Challenge" --difficulty 9

# Arena battle
python3 quest_gen.py -t "Arena Showdown" --map "Arena" --difficulty 6

# Coral Highlands expedition
python3 quest_gen.py -t "Coral Explorer" --map "Coral Highlands" -m 2
```

## Need Help?

Run `python3 quest_gen.py --help` for all available options.
