from typing import Tuple
from boa.contracts.abi.abi_contract import ABIContract
from moccasin.config import get_active_network
import boa

STARTING_ETH_BALANCE = int(1000e18)
STARTING_WETH_BALANCE = int(1e18)
STARTING_USDC_BALANCE = int(100e6) #USDC has 6 decimials 
def _add_eth_balance():
    boa.env.set_balance(boa.env.eoa, STARTING_ETH_BALANCE)
    
def _add_token_balance(usdc,weth):
    print(f"WETH STARTING {weth.balanceOf(boa.env.eoa)}")
    weth.deposit(value = STARTING_WETH_BALANCE)
    print(f"WETH ENDING {weth.balanceOf(boa.env.eoa)}")
    
    
    #Our conncected Network address
    our_address = boa.env.eoa
    
    
    #Mint  USdc
    #We will need to prank ourselves as owners inorder to mint 
    with boa.env.prank(usdc.owner()):
        usdc.updateMasterMinter(our_address)
    print(f"USDC ENDING {usdc.balanceOf(boa.env.eoa)}")
    usdc.configureMinter(our_address, STARTING_USDC_BALANCE )
    usdc.mint(our_address, STARTING_USDC_BALANCE)
    print(f"USDC ENDING {usdc.balanceOf(boa.env.eoa)}")
     
 
def setup_script() -> Tuple[ABIContract, ABIContract, ABIContract, ABIContract ]:
    print("Claiming faucets : ===============>")
    
    #Get active Network
    active_network = get_active_network()
    
    usdc = active_network.manifest_named("usdc")
    weth = active_network.manifest_named("weth")
    if active_network.is_local_or_forked_network():
        _add_eth_balance()
        _add_token_balance(usdc,weth)
    
    
    
def moccasin_main():
    setup_script()
    