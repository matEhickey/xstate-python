#!/usr/bin/env python3

from xstate.machine import Machine
from xstate.assign import assign
import time


machine = Machine(
    {
        "id": "machine",
        "initial": "on",
        "context": {
            "int": 0
        },
        "states": {
            "on" : {
                "on": {
                    "TOGGLE": {
                        "target": "off",
                        "actions": [{"type": "increaseInt"}]
                    }
                }
            },
            "off": {
                "on": {
                    "TOGGLE": {
                        "target": "on",
                        "actions": [{"type": "decreaseInt"}]
                    }
                }
            }
        },
    },
    actions = {
        "increaseInt": assign("increaseInt", {
            "int": lambda context: context["int"] + 1
        }),
        "decreaseInt": assign("decreaseInt", {
            "int": lambda context: context["int"] - 1
        })
    }
)


if __name__ == "__main__":
    state = machine.initial_state
    
    for i in range(10):
        for action in state.actions: action()
        print(state)
    
        state = machine.transition(state, "TOGGLE")
        time.sleep(1)
