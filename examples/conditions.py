#!/usr/bin/env python3

from xstate.machine import Machine
import time


# text style example, parallels states
# have an intalic and a bold sub-states

machine = Machine(
    {
        "id": "machine",
        "initial": "on",
        "states": {
            "on" : {
                "on": {
                    "TOGGLE": {
                        "target": "off",
                        "cond": "isOk"
                    }
                }
            },
            "off": {
                "on": {"TOGGLE": "on"}
            }
        },
    },
    guards = {
        "isOk": lambda: True
    }
)


if __name__ == "__main__":
    state = machine.initial_state
    print(state)
    
    state = machine.transition(state, "TOGGLE")
    print(state)
    
    state = machine.transition(state, "TOGGLE")
    print(state)
