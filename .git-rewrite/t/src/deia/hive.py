"""
DEIA Hive Management - Multi-Bot Coordination

Provides functionality for launching and joining bot hives.
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sys


# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import bot coordinator
try:
    from deia.cli_utils import get_bot_coordinator_path
    bot_coordinator_module = __import__('bot_coordinator', fromlist=['BotCoordinator'])
    BotCoordinator = bot_coordinator_module.BotCoordinator
except ImportError:
    # Fallback: try to import from installed location
    import importlib.util
    coordinator_path = Path.home() / ".deia" / "bot_coordinator.py"
    if coordinator_path.exists():
        spec = importlib.util.spec_from_file_location("bot_coordinator", coordinator_path)
        bot_coordinator_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bot_coordinator_module)
        BotCoordinator = bot_coordinator_module.BotCoordinator
    else:
        # Mock for testing
        class BotCoordinator:
            @staticmethod
            def generate_instance_id():
                return "test-instance"

            def claim_identity(self, bot_id, instance_id):
                return True

            def get_bot_info(self, bot_id):
                return {"bot_id": bot_id, "role": "Test", "instance_id": "test"}

            def register_bot(self, role, working_dir, handoff_doc=None, instance_id=None):
                return "BOT-00001"


class HiveJoinError(Exception):
    """Raised when joining a hive fails."""
    pass


class HiveLaunchError(Exception):
    """Raised when launching a hive fails."""
    pass


class HiveManager:
    """Manages hive operations - joining and launching."""

    def __init__(self, deia_root: Optional[str] = None):
        """
        Initialize HiveManager.

        Args:
            deia_root: Path to .deia directory. Defaults to current directory's .deia
        """
        if deia_root is None:
            deia_root = os.path.join(os.getcwd(), ".deia")

        self.deia_root = Path(deia_root)
        self.instructions_dir = self.deia_root / "instructions"
        self.reports_dir = self.deia_root / "reports"
        self.handoffs_dir = self.deia_root / "handoffs"

    def load_hive_config(self, config_path: str) -> Dict:
        """
        Load hive configuration from JSON file.

        Args:
            config_path: Path to hive configuration file

        Returns:
            Dictionary containing hive configuration

        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        config_file = Path(config_path)

        if not config_file.exists():
            raise FileNotFoundError(f"Hive config not found: {config_path}")

        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        return config

    def validate_hive_config(self, config: Dict) -> Tuple[bool, List[str]]:
        """
        Validate hive configuration structure.

        Args:
            config: Hive configuration dictionary

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check for required fields
        if 'queen' not in config:
            errors.append("Missing required field: 'queen'")

        if 'drones' not in config:
            errors.append("Missing required field: 'drones'")

        # Validate queen bot_id format
        if 'queen' in config:
            queen_bot_id = config['queen'].get('bot_id')
            if queen_bot_id and not re.match(r'^BOT-\d{5}$', queen_bot_id):
                errors.append(f"Invalid queen bot_id format: {queen_bot_id} (expected BOT-NNNNN)")

        # Validate drone bot_ids
        if 'drones' in config:
            for idx, drone in enumerate(config['drones']):
                drone_bot_id = drone.get('bot_id')
                if drone_bot_id and not re.match(r'^BOT-\d{5}$', drone_bot_id):
                    errors.append(f"Invalid drone[{idx}] bot_id format: {drone_bot_id} (expected BOT-NNNNN)")

        is_valid = len(errors) == 0
        return is_valid, errors

    def join_hive(self, config_path: str, bot_id: Optional[str] = None) -> Dict:
        """
        Join an existing hive as a drone.

        Args:
            config_path: Path to hive configuration file
            bot_id: Specific bot ID to claim (optional, auto-assigns if None)

        Returns:
            Dictionary with join results:
                - success: bool
                - bot_id: str
                - role: str
                - instance_id: str
                - instruction_file: str

        Raises:
            HiveJoinError: If joining fails
        """
        # Load and validate config
        config = self.load_hive_config(config_path)
        is_valid, errors = self.validate_hive_config(config)

        if not is_valid:
            raise HiveJoinError(f"Invalid hive config: {', '.join(errors)}")

        # Initialize bot coordinator
        coordinator = BotCoordinator()

        # Generate instance ID
        instance_id = coordinator.generate_instance_id()

        # Determine which bot to join as
        if bot_id is None:
            # Auto-assign: find first available drone
            available_drones = config.get('drones', [])
            if not available_drones:
                raise HiveJoinError("No drones available in hive config")

            bot_id = available_drones[0]['bot_id']

        # Claim the identity
        success = coordinator.claim_identity(bot_id, instance_id)

        if not success:
            raise HiveJoinError(f"Bot {bot_id} is already claimed by another instance")

        # Get bot info
        bot_info = coordinator.get_bot_info(bot_id)

        # Find role from config
        role = "Unknown"
        for drone in config.get('drones', []):
            if drone['bot_id'] == bot_id:
                role = drone['role']
                break

        instruction_file = self.instructions_dir / f"{bot_id}-instructions.md"

        return {
            'success': True,
            'bot_id': bot_id,
            'role': role,
            'instance_id': instance_id,
            'instruction_file': str(instruction_file)
        }

    def launch_hive(self, config_path: str, become_queen: bool = True) -> Dict:
        """
        Launch a new hive and optionally become the Queen.

        Args:
            config_path: Path to hive configuration file
            become_queen: Whether to register as Queen (default: True)

        Returns:
            Dictionary with launch results:
                - success: bool
                - hive_name: str
                - queen_id: str or None
                - drones_initialized: list of bot_ids

        Raises:
            HiveLaunchError: If launch fails
        """
        # Load and validate config
        config = self.load_hive_config(config_path)
        is_valid, errors = self.validate_hive_config(config)

        if not is_valid:
            raise HiveLaunchError(f"Invalid hive config: {', '.join(errors)}")

        hive_name = config.get('hive_name', 'unnamed-hive')

        # Create directory structure
        self._create_hive_structure()

        # Initialize instruction files for all bots
        drones_initialized = []

        # Create Queen instruction file
        queen_config = config.get('queen', {})
        queen_bot_id = queen_config.get('bot_id', 'BOT-00001')
        self._create_instruction_file(queen_bot_id, queen_config.get('role', 'Queen'), queen_config)

        # Create drone instruction files
        for drone in config.get('drones', []):
            drone_bot_id = drone.get('bot_id')
            drone_role = drone.get('role', 'Drone')
            self._create_instruction_file(drone_bot_id, drone_role, drone)
            drones_initialized.append(drone_bot_id)

        queen_id = None

        # Register as Queen if requested
        if become_queen:
            coordinator = BotCoordinator()
            instance_id = coordinator.generate_instance_id()

            queen_role = queen_config.get('role', 'Queen/Scrum Master')
            working_dir = os.getcwd()

            queen_id = coordinator.register_bot(
                role=queen_role,
                working_dir=working_dir,
                instance_id=instance_id
            )

        return {
            'success': True,
            'hive_name': hive_name,
            'queen_id': queen_id,
            'drones_initialized': drones_initialized
        }

    def _create_hive_structure(self):
        """Create necessary directory structure for hive."""
        self.instructions_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.handoffs_dir.mkdir(parents=True, exist_ok=True)

    def _create_instruction_file(self, bot_id: str, role: str, config: Dict):
        """
        Create instruction file for a bot.

        Args:
            bot_id: Bot ID (e.g., BOT-00001)
            role: Bot role (e.g., Queen, Drone-Testing)
            config: Bot configuration dict
        """
        instruction_file = self.instructions_dir / f"{bot_id}-instructions.md"

        responsibilities = config.get('responsibilities', [])
        responsibilities_text = "\n".join(f"- {r}" for r in responsibilities)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        content = f"""# Instructions for {bot_id} ({role})
**Created:** {timestamp}
**Status:** UNCLAIMED

---

## CLAIMED BY
**Instance ID:** UNCLAIMED
**Claimed at:** Not claimed yet
**Last check-in:** N/A
**Status:** Waiting for claim

---

## Your Identity

You are **{bot_id}**, a {role} in the hive.

**Responsibilities:**
{responsibilities_text}

---

## Getting Started

1. Claim this identity:
   ```bash
   python ~/.deia/bot_coordinator.py claim {bot_id} --instance <your-instance-id>
   ```

2. Update this file with your instance ID

3. Check the hive coordination rules:
   `.deia/hive-coordination-rules.md`

4. Check the backlog for tasks:
   `.deia/backlog.json`

5. Wait for Queen to assign you a task

---

## Current Task

**Status:** STANDBY
**Task:** None assigned yet

---

**End of Instructions**
"""

        with open(instruction_file, 'w', encoding='utf-8') as f:
            f.write(content)
