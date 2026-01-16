#!/usr/bin/env python3
"""
Monster Hunter World Quest Generator
Generates custom quest files for the PermanentEventQuest Mod
"""

import json
import random
import argparse
import os
from datetime import datetime
from pathlib import Path


class QuestGenerator:
    """Generates custom quests for Monster Hunter World"""
    
    def __init__(self, data_dir="data"):
        """Initialize the generator with game data"""
        self.data_dir = Path(data_dir)
        self.monsters = self._load_json("monsters.json")["monsters"]
        self.maps = self._load_json("maps.json")["maps"]
        self.items = self._load_json("items.json")["items"]
    
    def _load_json(self, filename):
        """Load JSON data file"""
        filepath = self.data_dir / filename
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def generate_quest(self, title=None, description=None, monster_count=1, 
                      difficulty=None, map_name=None, reward_count=3):
        """Generate a custom quest
        
        Args:
            title: Quest title (optional, will generate if not provided)
            description: Quest description (optional)
            monster_count: Number of monsters in quest (1-3)
            difficulty: Quest difficulty/star rating (1-9, optional)
            map_name: Map name (optional, random if not provided)
            reward_count: Number of reward items (1-10)
            
        Returns:
            dict: Generated quest data
        """
        # Select monsters
        selected_monsters = self._select_monsters(monster_count)
        
        # Determine difficulty if not provided
        if difficulty is None:
            difficulty = max(m["threat_level"] for m in selected_monsters)
        
        # Select map
        if map_name:
            quest_map = next((m for m in self.maps if m["name"].lower() == map_name.lower()), None)
            if not quest_map:
                quest_map = random.choice(self.maps)
        else:
            quest_map = random.choice(self.maps)
        
        # Generate title if not provided
        if not title:
            if len(selected_monsters) == 1:
                title = f"Hunt: {selected_monsters[0]['name']}"
            else:
                title = f"Multi-Monster Hunt"
        
        # Generate description if not provided
        if not description:
            monster_names = ", ".join(m["name"] for m in selected_monsters)
            description = f"Hunt the following monsters in {quest_map['name']}: {monster_names}"
        
        # Generate rewards
        rewards = self._generate_rewards(difficulty, reward_count)
        
        # Create quest structure
        quest = {
            "quest_info": {
                "title": title,
                "description": description,
                "difficulty": difficulty,
                "map": quest_map["name"],
                "map_id": quest_map["id"],
                "time_limit": 50,  # minutes
                "zenny_reward": difficulty * 1000 + random.randint(500, 2000),
                "hrp_reward": difficulty * 100 + random.randint(50, 200)
            },
            "monsters": [
                {
                    "monster_id": m["id"],
                    "name": m["name"],
                    "type": m["type"],
                    "is_target": True,
                    "initial_area": random.randint(1, quest_map["areas"])
                }
                for m in selected_monsters
            ],
            "rewards": rewards,
            "conditions": {
                "objective_type": "hunt",
                "target_count": len(selected_monsters),
                "failure_conditions": ["time_up", "cart_3_times"]
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator_version": "1.0.0"
            }
        }
        
        return quest
    
    def _select_monsters(self, count):
        """Select random monsters for the quest"""
        count = max(1, min(count, 3))  # Limit to 1-3 monsters
        return random.sample(self.monsters, count)
    
    def _generate_rewards(self, difficulty, count):
        """Generate quest rewards based on difficulty"""
        count = max(1, min(count, 10))
        
        # Filter items by appropriate rarity for difficulty
        max_rarity = min(difficulty + 2, 7)
        suitable_items = [i for i in self.items if i["rarity"] <= max_rarity]
        
        rewards = []
        for item in random.sample(suitable_items, min(count, len(suitable_items))):
            # Higher difficulty = better drop rates
            base_probability = 0.1 + (difficulty * 0.05)
            quantity = random.randint(1, 3) if item["rarity"] <= 3 else 1
            
            rewards.append({
                "item_id": item["id"],
                "item_name": item["name"],
                "quantity": quantity,
                "probability": min(base_probability, 0.85),
                "rarity": item["rarity"]
            })
        
        return rewards
    
    def save_quest(self, quest, output_dir="output", filename=None):
        """Save quest to JSON file
        
        Args:
            quest: Quest data dictionary
            output_dir: Output directory path
            filename: Output filename (optional, will generate if not provided)
            
        Returns:
            str: Path to saved file
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if not filename:
            # Generate filename from quest title
            safe_title = "".join(c if c.isalnum() or c in (' ', '_') else '_' 
                                for c in quest["quest_info"]["title"])
            safe_title = safe_title.replace(' ', '_').lower()
            filename = f"{safe_title}.quest.json"
        
        filepath = output_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(quest, f, indent=2)
        
        return str(filepath)


def interactive_mode(generator):
    """Run the generator in interactive mode"""
    print("\n=== Monster Hunter World Quest Generator ===\n")
    
    # Get quest title
    title = input("Quest Title (press Enter for auto-generated): ").strip()
    if not title:
        title = None
    
    # Get description
    description = input("Quest Description (press Enter for auto-generated): ").strip()
    if not description:
        description = None
    
    # Get monster count
    while True:
        try:
            monster_count = input("Number of monsters (1-3, default 1): ").strip()
            monster_count = int(monster_count) if monster_count else 1
            if 1 <= monster_count <= 3:
                break
            print("Please enter a number between 1 and 3")
        except ValueError:
            print("Please enter a valid number")
    
    # Get difficulty
    while True:
        try:
            difficulty = input("Difficulty level (1-9, press Enter for auto): ").strip()
            difficulty = int(difficulty) if difficulty else None
            if difficulty is None or 1 <= difficulty <= 9:
                break
            print("Please enter a number between 1 and 9")
        except ValueError:
            print("Please enter a valid number")
    
    # Get map
    print("\nAvailable maps:")
    for map_data in generator.maps:
        print(f"  - {map_data['name']}")
    map_name = input("Map name (press Enter for random): ").strip()
    if not map_name:
        map_name = None
    
    # Get reward count
    while True:
        try:
            reward_count = input("Number of reward items (1-10, default 3): ").strip()
            reward_count = int(reward_count) if reward_count else 3
            if 1 <= reward_count <= 10:
                break
            print("Please enter a number between 1 and 10")
        except ValueError:
            print("Please enter a valid number")
    
    # Generate quest
    print("\nGenerating quest...")
    quest = generator.generate_quest(
        title=title,
        description=description,
        monster_count=monster_count,
        difficulty=difficulty,
        map_name=map_name,
        reward_count=reward_count
    )
    
    # Display quest summary
    print("\n=== Generated Quest ===")
    print(f"Title: {quest['quest_info']['title']}")
    print(f"Description: {quest['quest_info']['description']}")
    print(f"Difficulty: {quest['quest_info']['difficulty']} stars")
    print(f"Map: {quest['quest_info']['map']}")
    print(f"Monsters: {', '.join(m['name'] for m in quest['monsters'])}")
    print(f"Rewards: {len(quest['rewards'])} items")
    
    # Save quest
    save = input("\nSave quest? (y/n): ").strip().lower()
    if save == 'y':
        filepath = generator.save_quest(quest)
        print(f"\nQuest saved to: {filepath}")
        return filepath
    else:
        print("\nQuest not saved.")
        return None


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate custom quests for Monster Hunter World PermanentEventQuest Mod"
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '-t', '--title',
        type=str,
        help='Quest title'
    )
    
    parser.add_argument(
        '-d', '--description',
        type=str,
        help='Quest description'
    )
    
    parser.add_argument(
        '-m', '--monsters',
        type=int,
        default=1,
        help='Number of monsters (1-3, default: 1)'
    )
    
    parser.add_argument(
        '--difficulty',
        type=int,
        help='Difficulty level (1-9)'
    )
    
    parser.add_argument(
        '--map',
        type=str,
        help='Map name'
    )
    
    parser.add_argument(
        '-r', '--rewards',
        type=int,
        default=3,
        help='Number of reward items (1-10, default: 3)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='data',
        help='Data directory path (default: data)'
    )
    
    parser.add_argument(
        '-n', '--count',
        type=int,
        default=1,
        help='Number of quests to generate (default: 1)'
    )
    
    args = parser.parse_args()
    
    # Initialize generator
    try:
        generator = QuestGenerator(data_dir=args.data_dir)
    except FileNotFoundError as e:
        print(f"Error: Could not find data files. Make sure data directory exists.")
        print(f"Details: {e}")
        return 1
    
    # Run in interactive mode if requested
    if args.interactive:
        interactive_mode(generator)
        return 0
    
    # Generate quests
    print(f"Generating {args.count} quest(s)...")
    
    for i in range(args.count):
        quest = generator.generate_quest(
            title=args.title,
            description=args.description,
            monster_count=args.monsters,
            difficulty=args.difficulty,
            map_name=args.map,
            reward_count=args.rewards
        )
        
        filepath = generator.save_quest(quest, output_dir=args.output)
        print(f"Generated quest {i+1}/{args.count}: {filepath}")
        
        # Show summary
        print(f"  Title: {quest['quest_info']['title']}")
        print(f"  Monsters: {', '.join(m['name'] for m in quest['monsters'])}")
        print(f"  Difficulty: {quest['quest_info']['difficulty']} stars")
        print()
    
    print("Done!")
    return 0


if __name__ == "__main__":
    exit(main())
