# pragma version ^0.4.1
"""
@license MIT
@title snek_token
@author Web3wanderer
@notice this is ERC-20 token
"""
# ------------------------------------------------------------------
#                             IMPORTS
# ------------------------------------------------------------------
from ethereum.ercs import IERC20

implements: IERC20

from snekmate.auth import ownable as own

from snekmate.tokens import erc20

initializes: own

initializes: erc20[ownable := own]
exports: erc20.__interface__

# ------------------------------------------------------------------
#                         STATE VARIABLES
# ------------------------------------------------------------------
NAME: constant(String[25]) = "snek_token"
SYMBOL: constant(String[5]) = "SNEK"
DECIMAL: constant(uint8) = 18
EIP712_VERSION: constant(String[20]) = "1"

# ------------------------------------------------------------------
#                            FUNCTIONS
# ------------------------------------------------------------------
@deploy
def __init__(initial_supply: uint256):
    own.__init__()
    erc20.__init__(NAME, SYMBOL, DECIMAL, NAME, EIP712_VERSION)
    erc20._mint(msg.sender, initial_supply)

# This is a bug! Remove it (but our stateful tests should catch it!)
@external
def super_mint():
    # We forget to update the total supply!
    # self.totalSupply += amount
    amount: uint256 = as_wei_value(100, "ether")
    erc20.balanceOf[msg.sender] = erc20.balanceOf[msg.sender] + amount
    log IERC20.Transfer(empty(address), msg.sender, amount)