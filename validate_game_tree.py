#!/usr/bin/env python3
"""
AFTER CLASS — Game Tree Validator

Proves the game has no dead-ends by exhaustively exploring all reachable states
and verifying each has a path to the win condition.

Uses BFS to find shortest path from any state to WIN.

NEW DESIGN (v2):
- APRON at COUNTER, revealed by LOOK
- BOWL in cabinet (KITCHEN), revealed by OPEN CABINET
- Win sequence: USE BOWL (traps) → USE APRON (catches)
- Red herrings: KNIFE, BAG, TREATS (fail gracefully, no softlock)
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
    apron_revealed: bool = False   # LOOK at counter reveals apron
    has_apron: bool = False
    cabinet_opened: bool = False   # OPEN CABINET reveals bowl
    has_bowl: bool = False
    mascot_trapped: bool = False   # BOWL traps mascot
    mascot_caught: bool = False    # WIN state

    def __hash__(self):
        return hash((
            self.location,
            self.mascot_location,
            self.apron_revealed,
            self.has_apron,
            self.cabinet_opened,
            self.has_bowl,
            self.mascot_trapped,
            self.mascot_caught,
        ))

# ============================================================================
# ACTIONS
# ============================================================================

@dataclass
class Action:
    name: str
    precondition: callable  # GameState -> bool
    effect: callable        # GameState -> GameState
    advances_mascot: bool = False  # Most actions don't move mascot

def _copy_state(s: GameState, **overrides) -> GameState:
    """Helper to copy state with overrides."""
    return GameState(
        location=overrides.get('location', s.location),
        mascot_location=overrides.get('mascot_location', s.mascot_location),
        apron_revealed=overrides.get('apron_revealed', s.apron_revealed),
        has_apron=overrides.get('has_apron', s.has_apron),
        cabinet_opened=overrides.get('cabinet_opened', s.cabinet_opened),
        has_bowl=overrides.get('has_bowl', s.has_bowl),
        mascot_trapped=overrides.get('mascot_trapped', s.mascot_trapped),
        mascot_caught=overrides.get('mascot_caught', s.mascot_caught),
    )

def _move_mascot(s: GameState) -> MascotLocation:
    """Advance mascot to next position in cycle."""
    if s.mascot_trapped:
        return s.mascot_location  # Trapped mascot doesn't move
    current_idx = MASCOT_CYCLE.index(s.mascot_location) if s.mascot_location in MASCOT_CYCLE else 0
    next_idx = (current_idx + 1) % len(MASCOT_CYCLE)
    return MASCOT_CYCLE[next_idx]

def _mascot_in_room(s: GameState) -> bool:
    """Check if mascot is in player's current room."""
    if s.mascot_location in ["TABLE1", "TABLE2", "TABLE3"]:
        return s.location == "DINING"
    return s.location == s.mascot_location

def make_move_action(target: Location) -> Action:
    """Create a movement action."""
    valid_from = {
        "DINING": ["COUNTER"],
        "COUNTER": ["DINING", "KITCHEN"],
        "KITCHEN": ["COUNTER"],
    }

    def precondition(s: GameState) -> bool:
        return s.location in valid_from[target] and not s.mascot_caught

    def effect(s: GameState) -> GameState:
        return _copy_state(s, location=target)

    return Action(f"GO_{target}", precondition, effect)

def look_counter_action() -> Action:
    """LOOK at counter reveals apron hanging by kitchen door."""
    def precondition(s: GameState) -> bool:
        return s.location == "COUNTER" and not s.apron_revealed and not s.mascot_caught

    def effect(s: GameState) -> GameState:
        return _copy_state(s, apron_revealed=True)

    return Action("LOOK_COUNTER", precondition, effect)

def take_apron_action() -> Action:
    """Take apron from counter (must be revealed first)."""
    def precondition(s: GameState) -> bool:
        return (s.location == "COUNTER" and
                s.apron_revealed and
                not s.has_apron and
                not s.mascot_caught)

    def effect(s: GameState) -> GameState:
        return _copy_state(s, has_apron=True)

    return Action("TAKE_APRON", precondition, effect)

def open_cabinet_action() -> Action:
    """Open cabinet in kitchen to reveal bowl."""
    def precondition(s: GameState) -> bool:
        return s.location == "KITCHEN" and not s.cabinet_opened and not s.mascot_caught

    def effect(s: GameState) -> GameState:
        return _copy_state(s, cabinet_opened=True)

    return Action("OPEN_CABINET", precondition, effect)

def take_bowl_action() -> Action:
    """Take bowl from cabinet (must be opened first)."""
    def precondition(s: GameState) -> bool:
        return (s.location == "KITCHEN" and
                s.cabinet_opened and
                not s.has_bowl and
                not s.mascot_caught)

    def effect(s: GameState) -> GameState:
        return _copy_state(s, has_bowl=True)

    return Action("TAKE_BOWL", precondition, effect)

def use_bowl_action() -> Action:
    """Use bowl to trap mascot (must be in same room)."""
    def precondition(s: GameState) -> bool:
        return (s.has_bowl and
                not s.mascot_trapped and
                not s.mascot_caught and
                _mascot_in_room(s))

    def effect(s: GameState) -> GameState:
        return _copy_state(s, mascot_trapped=True)

    return Action("USE_BOWL", precondition, effect)

def use_apron_action() -> Action:
    """Use apron to catch trapped mascot. WIN CONDITION."""
    def precondition(s: GameState) -> bool:
        return (s.has_apron and
                s.mascot_trapped and
                not s.mascot_caught and
                _mascot_in_room(s))

    def effect(s: GameState) -> GameState:
        return _copy_state(s, mascot_caught=True)

    return Action("USE_APRON", precondition, effect)

def use_apron_fail_action() -> Action:
    """Use apron without trapping first. Fails, mascot moves."""
    def precondition(s: GameState) -> bool:
        return (s.has_apron and
                not s.mascot_trapped and
                not s.mascot_caught and
                _mascot_in_room(s))

    def effect(s: GameState) -> GameState:
        return _copy_state(s, mascot_location=_move_mascot(s))

    return Action("USE_APRON_FAIL", precondition, effect, advances_mascot=True)

def catch_bare_hands_action() -> Action:
    """Attempt catch without items. Always fails, mascot moves."""
    def precondition(s: GameState) -> bool:
        return (not s.has_apron and
                not s.has_bowl and
                not s.mascot_caught and
                _mascot_in_room(s))

    def effect(s: GameState) -> GameState:
        return _copy_state(s, mascot_location=_move_mascot(s))

    return Action("CATCH_BARE", precondition, effect, advances_mascot=True)

def wait_action() -> Action:
    """Do nothing. For testing state space."""
    def precondition(s: GameState) -> bool:
        return not s.mascot_caught

    def effect(s: GameState) -> GameState:
        return s  # No change

    return Action("WAIT", precondition, effect)

# ============================================================================
# GAME DEFINITION
# ============================================================================

ALL_ACTIONS = [
    make_move_action("DINING"),
    make_move_action("COUNTER"),
    make_move_action("KITCHEN"),
    look_counter_action(),
    take_apron_action(),
    open_cabinet_action(),
    take_bowl_action(),
    use_bowl_action(),
    use_apron_action(),
    use_apron_fail_action(),
    catch_bare_hands_action(),
    wait_action(),
]

INITIAL_STATE = GameState(
    location="DINING",
    mascot_location="TABLE2",
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
    trapped_states = sum(1 for s in all_states if s.mascot_trapped and not is_win(s))
    ready_to_trap = sum(1 for s in all_states if s.has_bowl and s.has_apron and not s.mascot_trapped and not is_win(s))
    exploring = sum(1 for s in all_states if not s.has_bowl or not s.has_apron)
    print(f"    Win states: {win_states}")
    print(f"    Mascot trapped (not won): {trapped_states}")
    print(f"    Ready to trap (bowl+apron, not trapped): {ready_to_trap}")
    print(f"    Still exploring (missing items): {exploring}")
    print()

    print("=" * 60)
    print("VALIDATION COMPLETE: NO DEAD ENDS")
    print("=" * 60)

    return True

# ============================================================================
# OPTIMAL PATH VERIFICATION
# ============================================================================

def verify_optimal_path():
    """
    Verify the intended optimal path works.

    Optimal sequence (8 commands):
    1. GO COUNTER
    2. LOOK (reveals apron)
    3. TAKE APRON
    4. GO KITCHEN
    5. OPEN CABINET
    6. TAKE BOWL
    7. GO to mascot's room
    8. USE BOWL (traps)
    9. USE APRON (win)
    """
    print()
    print("=" * 60)
    print("Optimal Path Verification")
    print("=" * 60)
    print()

    optimal_actions = [
        "GO_COUNTER",
        "LOOK_COUNTER",
        "TAKE_APRON",
        "GO_KITCHEN",
        "OPEN_CABINET",
        "TAKE_BOWL",
        "GO_COUNTER",   # Mascot might be at counter
        "GO_DINING",    # Or go to dining where mascot starts
        "USE_BOWL",
        "USE_APRON",
    ]

    state = INITIAL_STATE
    print(f"  Start: {state}")
    print()

    for action_name in optimal_actions:
        action = next((a for a in ALL_ACTIONS if a.name == action_name), None)
        if action and action.precondition(state):
            state = action.effect(state)
            status = "WIN!" if is_win(state) else ""
            print(f"  {action_name:20} -> trapped={state.mascot_trapped} caught={state.mascot_caught} {status}")
            if is_win(state):
                break
        else:
            print(f"  {action_name:20} -> (skipped, precondition false)")

    print()
    if is_win(state):
        print("  Result: WIN achieved on optimal path!")
        return True
    else:
        print("  Result: FAILED - optimal path doesn't win!")
        return False

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    success = validate_no_dead_ends()
    success = verify_optimal_path() and success

    if success:
        print()
        print("ALL VALIDATIONS PASSED")
        exit(0)
    else:
        print()
        print("VALIDATION FAILED")
        exit(1)
