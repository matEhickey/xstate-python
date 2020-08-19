from typing import Dict, List
from xstate.state_node import StateNode
from xstate.state import State
from xstate.algorithm import enter_states, get_state_value, main_event_loop
from xstate.event import Event
from xstate.assign import Assigner


class Machine:
    root: StateNode
    _id_map: Dict[str, StateNode]
    actions: [lambda: None]

    def __init__(self, config, actions={}, guards= {}):
        self.id = config["id"]
        self.initial_context = config["context"] if("context" in config.keys()) else {}
        self._id_map = {}
        self.root = StateNode(
            config, machine=self, key=config.get("id", "(machine)"), parent=None
        )
        self.states = self.root.states
        self.actions = actions
        
        self.guards = guards

    def transition(self, state: State, event: str):
        (configuration, _actions) = main_event_loop(self, state, Event(event))

        value = get_state_value(self.root, configuration=configuration)
        actions, warnings = self._get_actions(_actions)
        for w in warnings: print(w)
        
        context = self.executeTransitionActions(value, state.context)
        return State(configuration=configuration, context=context, actions=actions)

    def _get_actions(self, actions) -> [lambda: None]:
        result = []
        errors = []
        for action in actions:
            if action.type in self.actions:
                result.append(self.actions[action.type])
            else:
                errors.append("No '{}' action".format(action.type)) 
        return result, errors
    
    def executeTransitionActions(self, state, context):
        _state = None
        _context = dict(context) if context else {}
        
        if(type(state) == dict):
            _state = self
            for s in [*state.keys()][0].split("."):
                _state = _state.states[s]
        else:
            _state = self.states[state]
        
        transitionActions = _state.transitions[0].actions
        for action in transitionActions:
            for key in Assigner.actions[action.type]:
                value = Assigner.actions[action.type][key](context)
                _context[key] = value
        
        return _context
        
    def state_from(self, state_value) -> State:
        configuration = self._get_configuration(state_value=state_value)

        return State(configuration=configuration, context=None)

    def _register(self, state_node: StateNode):
        state_node.machine = self
        self._id_map[state_node.id] = state_node

    def _get_by_id(self, id: str) -> StateNode:
        return self._id_map.get(id, None)

    def _get_configuration(self, state_value, parent=None) -> List[StateNode]:
        if parent is None:
            parent = self.root

        if isinstance(state_value, str):
            state_node = parent.states.get(state_value, None)

            if state_node is None:
                raise ValueError(f"State node {state_value} is missing")

            return [state_node]

        configuration = []

        for key in state_value.keys():
            state_node = parent.states.get(key)
            configuration.append(state_node)

            configuration += self._get_configuration(
                state_value.get(key), parent=state_node
            )

        return configuration

    @property
    def initial_state(self) -> State:
        (configuration, _actions, internal_queue) = enter_states(
            [self.root.initial],
            configuration=set(),
            states_to_invoke=set(),
            history_value={},
            actions=[],
            internal_queue=[],
        )
        
        state = self.root.initial.target[0].id.split(".")[-1]
        context = self.executeTransitionActions(state, self.initial_context)
        actions, warnings = self._get_actions(_actions)
        for w in warnings: print(w)
        
        return State(configuration=configuration, context=context, actions=actions)
