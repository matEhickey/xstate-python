from xstate.machine import Machine
from xstate.state import State
from xstate.assign import assign


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


def test_context():
    state = machine.initial_state
    assert state.context["int"] is 1

    state = machine.transition(state, "TOGGLE")
    assert state.context["int"] is 0

    state = machine.transition(state, "TOGGLE")
    assert state.context["int"] is 1
    
def test_functionnal_context():
    first_state = machine.initial_state
    assert first_state.value is "on"
    assert first_state.context["int"] is 1
    
    state = machine.transition(first_state, "TOGGLE")
    assert state.value is "off"
    assert state.context["int"] is 0
        
    state = machine.transition(first_state, "TOGGLE")
    assert state.value is "off"
    assert state.context["int"] is 0
    