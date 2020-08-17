#!/usr/bin/env python3

from xstate.machine import Machine
import time


# text style example, parallels states
# have an intalic and a bold sub-states

styleMachine = Machine(
    {
        "id": "styleMachine",
        "type": "parallel",
        "initial": "italic.on, bold.off",
        "states": {
            "italic": {
                "initial": "on",
                "states": {
                    "on": {"on": {"ITALIC": "off"}},
                    "off": {"on": {"ITALIC": "on"}}
                }
            },
            "bold": {
                "initial": "on",
                "states": {
                    "on": {"on": {"BOLD": "off"}},
                    "off": {"on": {"BOLD": "on"}}
                }
            }
        },
    }
)


if __name__ == "__main__":
    state = styleMachine.initial_state
    # print(state)