// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import {MintableIncentivizedERC20} from "@aave/core-v3/contracts/protocol/tokenization/base/MintableIncentivizedERC20.sol";
import {IPool} from '@aave/core-v3/contracts/interfaces/IPool.sol';

contract DummyERC20_AToken is MintableIncentivizedERC20 {
    
      constructor(
    IPool pool,
    string memory name,
    string memory symbol,
    uint8 decimals
  ) MintableIncentivizedERC20(pool, name, symbol, decimals) {
    // Intentionally left blank
  }

    function scaledTotalSupply() public view returns (uint256) {assembly { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00270000, 1037618708519) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00270001, 0) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00270002, 0) }
        return super.totalSupply();
    }

    function scaledBalanceOf(address account) public view returns (uint256) {assembly { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00280000, 1037618708520) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00280001, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00280003, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00286000, account) }
        return super.balanceOf(account);
    }

    function getScaledUserBalanceAndSupply(address account) public view returns (uint256, uint256){assembly { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00260000, 1037618708518) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00260001, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00260003, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00266000, account) }
        return (scaledBalanceOf(account), scaledTotalSupply());
    }

    function mint(address account, uint128 amount) external {
        _mint(account, amount);
    }

    function burn(address account, uint128 amount) external {
        _burn(account, amount);
    }
}