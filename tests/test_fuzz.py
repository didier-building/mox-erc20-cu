from hypothesis.stateful import (  # Imports classes and decorators from hypothesis for stateful testing
    RuleBasedStateMachine,  # Base class for state machine testing
    initialize,  # Decorator for initialization methods
    invariant,  # Decorator for invariant methods that should always hold true
    rule,  # Decorator for rules that define possible state transitions
)
from eth.constants import ZERO_ADDRESS, UINT_256_MAX #import Ethereum constants
from boa.util.abi import Address # Imports the Address class to handle Ethereum addresses
import boa
from script.deploy import deploy #import deploy function from local script
from boa.test.strategies import strategy
from hypothesis import strategies as stra
from hypothesis import assume, settings

MINTERS_COUNT = 10

class StateFullFuzzer(RuleBasedStateMachine):# Defines a test class that inherits from RuleBasedStateMachine
    def __init__(self): #constructor method
        super().__init__() #calls parent class constructor

    
    @initialize() #marks this method to run once at the begining of each test cases 
    def setup(self): #set up  method to initialize the test environment
        self.contract = deploy() #deploys the contract using imported deploy function
        self.minters =[Address("0x" + ZERO_ADDRESS.hex())] #create initioa minter with zero address
        while Address("0x" + ZERO_ADDRESS.hex()) in self.minters: #ensures that the zero address is not in the list of minters
            self.minters = [boa.env.generate_address() for _ in range (MINTERS_COUNT)] #generates a list of random addresses for minters

    @rule( #decorator to mark this method as the rule state machine
            amount=strategy("uint256"), #gerates a random uint256 value for the amount
            minters_seed = stra.integers(min_value = 0, max_value = MINTERS_COUNT - 1) # generate random indices for minters list
       )

    def mint(self, amount, minters_seed):
        assume(self.contract.totalSupply() + amount <= UINT_256_MAX) #assumes that the total supply does not exceed the maximum value for uint256
        minter = self.minters[minters_seed]
        self.contract.mint(minter, amount) #calls the mint function of the contract with the selected minter and amount
        
    @rule(
        minter_seed = stra.integers(min_value = 0, max_value = MINTERS_COUNT - 1), #generate random indices for minters list

    )
    def super_mint(self, minter_seed):
        minter = self.minters[minter_seed]
        with boa.env.prank(minter): #prank the minter address
            self.contract.super_mint() 

    @invariant()
    def account_balance_should_never_exceeds_total_supply(self):
        supply = self.contract.totalSupply() #get the total supply of the contract
        for minter in self.minters:
            balance = self.contract.balanceOf(minter)
            assert balance <= supply, f"Balance of {minter} exceeds total supply"
            assert balance >= 0, f"Balance of {minter} is negative"

token_state_fuzzer = StateFullFuzzer.TestCase
token_state_fuzzer.settings = settings(
    max_examples=1000,  # Set the maximum number of examples to 1000
    stateful_step_count=60  # Set the number of stateful steps to 60
)