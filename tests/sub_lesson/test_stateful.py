from hypothesis.stateful import rule, RuleBasedStateMachine
from contracts.sub_lesson import stateful_fuzz_solvable
from boa.test.strategies import strategy
from hypothesis import settings


class StatefulFuzzer(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.contract = stateful_fuzz_solvable.deploy()
        print("Deployed contract succesfullly!...")
    # 'Rules' -> Actions, and can have properties, invariants
    # "invariants" -> Properties that always hold true
    @rule(new_number=strategy("uint256"))
    def change_number(self, new_number):
        self.contract.change_number(new_number)
        print(f"Changed number to {new_number}")

    @rule(input_number=strategy("uint256"))
    def input_number_always_returns__itself(self, input_number):
        assert self.contract.always_returns_input_number(input_number) == input_number, f"Failed for {input_number}"

TestStatefulFuzzing = StatefulFuzzer.TestCase

TestStatefulFuzzing.settings = settings(max_examples=10000, stateful_step_count=90)