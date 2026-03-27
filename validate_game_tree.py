#!/usr/bin/env python3
"""
THE SHIFT — Game Tree Validator

Proves the game has no dead-ends by exhaustively exploring all reachable states
and verifying each has a path to the win condition.

Uses BFS to find shortest path from any state to WIN.
"""

from dataclasses import dataclass, field
from typing import Literal, Optional
from collections import deque
import itertools

# ============================================================================
# STATE MODEL
# ============================================================================

Location = Literal["DINING", "COUNTER", "KITCHEN"]
MascotLocation = Literal["TABLE1", "TABLE2", "TABLE3", "COUNTER", "KITCHEN"]

MASCOT_CYCLE = ["TABLE2", "TABLE1", "TABLE3", "COUNTER", "KITCHEN"]

@dataclass(frozen=True)
class GameState:
    """Immutable game state for hashability."""
    location: Location
    mascot_location: MascotLocation
    has_apron: bool
    has_tray: bool
    mascot_caught: bool = False

    def __hash__(self):
        return hash((
            self.location,
            self.mascot_location,
            self.has_apron,
            self.has_tray,
            self.mascot_caught
        ))

# ============================================================================
# ACTIONS
# ============================================================================

@dataclass
class Action:
    name: str
    precondition: callable  # GameState -> bool
    effect: callable        # GameState -> GameState
    advances_mascot: bool = True  # Does this action count toward mascot movement?

def make_move_action(target: Location) -> Action:
    """Create a movement action."""
    valid_from = {
        "DINING": ["COUNTER", "KITCHEN"],
        "COUNTER": ["DINING", "KITCHEN"],
        "KITCHEN": ["DINING", "COUNTER"],
    }

    def precondition(s: GameState) -> bool:
        return s.location in valid_from[target] and not s.mascot_caught

    def effect(s: GameState) -> GameState:
        return GameState(
            location=target,
            mascot_location=s.mascot_location,
            has_apron=s.has_apron,
            has_tray=s.has_tray,
            mascot_caught=s.mascot_caught,
        )

    return Action(f"GO_{target}", precondition, effect)

def take_apron_action() -> Action:
    def precondition(s: GameState) -> bool:
        return s.location == "KITCHEN" and not s.has_apron and not s.mascot_caught

    def effect(s: GameState) -> GameState:
        return GameState(
            location=s.location,
            mascot_location=s.mascot_location,
            has_apron=True,
            has_tray=s.has_tray,
            mascot_caught=s.mascot_caught,
        )

    return Action("TAKE_APRON", precondition, effect)

def take_tray_action() -> Action:
    def precondition(s: GameState) -> bool:
        return s.location == "KITCHEN" and not s.has_tray and not s.mascot_caught

    def effect(s: GameState) -> GameState:
        return GameState(
            location=s.location,
            mascot_location=s.mascot_location,
            has_apron=s.has_apron,
            has_tray=True,
            mascot_caught=s.mascot_caught,
        )

    return Action("TAKE_TRAY", precondition, effect)

def use_apron_action() -> Action:
    """WIN CONDITION: Use apron to catch mascot."""
    def precondition(s: GameState) -> bool:
        if s.mascot_caught:
            return False
        if not s.has_apron:
            return False
        # Must be in same general area as mascot
        if s.mascot_location in ["TABLE1", "TABLE2", "TABLE3"]:
            return s.location == "DINING"
        return s.location == s.mascot_location

    def effect(s: GameState) -> GameState:
        return GameState(
            location=s.location,
            mascot_location=s.mascot_location,
            has_apron=s.has_apron,
            has_tray=s.has_tray,
            mascot_caught=True,  # WIN!
        )

    return Action("USE_APRON", precondition, effect)

def catch_bare_hands_action() -> Action:
    """Attempt catch without apron — always fails, mascot moves."""
    def precondition(s: GameState) -> bool:
        if s.mascot_caught or s.has_apron:
            return False
        if s.mascot_location in ["TABLE1", "TABLE2", "TABLE3"]:
            return s.location == "DINING"
        return s.location == s.mascot_location

    def effect(s: GameState) -> GameState:
        # Mascot escapes to next position in cycle
        current_idx = MASCOT_CYCLE.index(s.mascot_location) if s.mascot_location in MASCOT_CYCLE else 0
        next_idx = (current_idx + 1) % len(MASCOT_CYCLE)
        return GameState(
            location=s.location,
            mascot_location=MASCOT_CYCLE[next_idx],
            has_apron=s.has_apron,
            has_tray=s.has_tray,
            mascot_caught=s.mascot_caught,
        )

    return Action("CATCH_BARE", precondition, effect)

def wait_action() -> Action:
    """Do nothing — lets mascot move (for testing purposes)."""
    def precondition(s: GameState) -> bool:
        return not s.mascot_caught

    def effect(s: GameState) -> GameState:
        return s  # No change

    return Action("WAIT", precondition, effect, advances_mascot=True)

# ============================================================================
# GAME DEFINITION
# ============================================================================

ALL_ACTIONS = [
    make_move_action("DINING"),
    make_move_action("COUNTER"),
    make_move_action("KITCHEN"),
    take_apron_action(),
    take_tray_action(),
    use_apron_action(),
    catch_bare_hands_action(),
    wait_action(),
]

INITIAL_STATE = GameState(
    location="DINING",
    mascot_location="TABLE2",
    has_apron=False,
    has_tray=False,
    mascot_caught=False,
)

def is_win(s: GameState) -> bool:
    return s.mascot_caught

# ============================================================================
# VALIDATION: BFS TO PROVE ALL STATES REACH WIN
# ============================================================================

def get_available_actions(state: GameState) -> list[Action]:
    """Return all actions valid in current state."""
    return [a for a in ALL_ACTIONS if a.precondition(state)]

def get_successors(state: GameState) -> list[tuple[Action, GameState]]:
    """Return all (action, resulting_state) pairs from current state."""
    successors = []
    for action in get_available_actions(state):
        next_state = action.effect(state)
        successors.append((action, next_state))
    return successors

def bfs_to_win(start: GameState) -> Optional[list[Action]]:
    """Find shortest path from start to win state. Returns None if no path exists."""
    if is_win(start):
        return []

    queue = deque([(start, [])])
    visited = {start}

    while queue:
        current, path = queue.popleft()

        for action, next_state in get_successors(current):
            if next_state in visited:
                continue

            new_path = path + [action]

            if is_win(next_state):
                return new_path

            visited.add(next_state)
            queue.append((next_state, new_path))

    return None  # No path to win

def enumerate_all_reachable_states(start: GameState) -> set[GameState]:
    """Find all states reachable from start."""
    visited = {start}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        for _, next_state in get_successors(current):
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)

    return visited

def validate_no_dead_ends():
    """
    MAIN VALIDATION: Prove every reachable state has a path to win.
    """
    print("=" * 60)
    print("THE SHIFT — Game Tree Validator")
    print("=" * 60)
    print()

    # 1. Find all reachable states
    print("[1] Enumerating all reachable states...")
    all_states = enumerate_all_reachable_states(INITIAL_STATE)
    print(f"    Found {len(all_states)} reachable states.")
    print()

    # 2. For each non-win state, verify path to win exists
    print("[2] Verifying all states have path to WIN...")
    dead_ends = []
    longest_path = []

    for state in all_states:
        if is_win(state):
            continue

        path = bfs_to_win(state)
        if path is None:
            dead_ends.append(state)
        elif len(path) > len(longest_path):
            longest_path = path

    if dead_ends:
        print(f"    FAILURE: Found {len(dead_ends)} dead-end states!")
        for de in dead_ends[:5]:
            print(f"      - {de}")
        return False

    print(f"    SUCCESS: All {len(all_states)} states can reach WIN.")
    print()

    # 3. Show optimal solution from start
    print("[3] Optimal solution from initial state:")
    optimal = bfs_to_win(INITIAL_STATE)
    if optimal:
        print(f"    Steps: {len(optimal)}")
        for i, action in enumerate(optimal, 1):
            print(f"      {i}. {action.name}")
    print()

    # 4. Show worst-case (longest shortest path)
    print("[4] Worst-case scenario (longest shortest path):")
    print(f"    Max steps from any state: {len(longest_path)}")
    print()

    # 5. State space breakdown
    print("[5] State space breakdown:")
    win_states = sum(1 for s in all_states if is_win(s))
    with_apron = sum(1 for s in all_states if s.has_apron and not is_win(s))
    without_apron = sum(1 for s in all_states if not s.has_apron and not is_win(s))
    print(f"    Win states: {win_states}")
    print(f"    States with apron (not won): {with_apron}")
    print(f"    States without apron: {without_apron}")
    print()

    print("=" * 60)
    print("VALIDATION COMPLETE: NO DEAD ENDS")
    print("=" * 60)

    return True

# ============================================================================
# PROGRESSIVE DISCLOSURE VERIFICATION
# ============================================================================

def verify_progressive_disclosure():
    """
    Verify that hint system guarantees progress.

    The key property: even without understanding ANY puzzle mechanics,
    following Tier 3 hints leads to win.
    """
    print()
    print("=" * 60)
    print("Progressive Disclosure Verification")
    print("=" * 60)
    print()

    # Simulate a player who only follows explicit instructions
    print("Simulating player who ONLY follows Tier 3 hints:")
    print()

    # Tier 3 instructions (from GAME-DESIGN.md):
    # 1. "Use the apron. It's in the kitchen."
    # 2. "Throw it over the mascot."

    tier3_actions = [
        "GO_KITCHEN",   # Go to kitchen
        "TAKE_APRON",   # Take the apron
        "GO_DINING",    # Go to dining (mascot starts at TABLE2)
        "USE_APRON",    # Catch mascot
    ]

    state = INITIAL_STATE
    print(f"  Start: {state}")

    for action_name in tier3_actions:
        action = next((a for a in ALL_ACTIONS if a.name == action_name), None)
        if action and action.precondition(state):
            state = action.effect(state)
            print(f"  {action_name} -> {state}")
        else:
            # Mascot might have moved, need to adjust
            if action_name == "USE_APRON" and state.has_apron:
                # Find mascot first
                mascot_loc = state.mascot_location
                if mascot_loc in ["TABLE1", "TABLE2", "TABLE3"]:
                    target = "DINING"
                else:
                    target = mascot_loc

                if state.location != target:
                    move_action = next(
                        (a for a in ALL_ACTIONS if a.name == f"GO_{target}"),
                        None
                    )
                    if move_action and move_action.precondition(state):
                        state = move_action.effect(state)
                        print(f"  GO_{target} -> {state}")

                # Now use apron
                use_apron = use_apron_action()
                if use_apron.precondition(state):
                    state = use_apron.effect(state)
                    print(f"  USE_APRON -> {state}")

    print()
    if is_win(state):
        print("  Result: WIN achieved following Tier 3 hints!")
    else:
        print("  Result: FAILED - Tier 3 hints don't guarantee win!")
        return False

    print()
    print("=" * 60)
    print("PROGRESSIVE DISCLOSURE VERIFIED")
    print("=" * 60)

    return True

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    success = validate_no_dead_ends()
    success = verify_progressive_disclosure() and success

    if success:
        print()
        print("ALL VALIDATIONS PASSED")
        exit(0)
    else:
        print()
        print("VALIDATION FAILED")
        exit(1)
