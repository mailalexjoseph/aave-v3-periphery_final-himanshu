// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.10;

import {RewardsController} from '../../contracts/rewards/RewardsController.sol';
import {RewardsDataTypes} from '../../contracts/rewards/libraries/RewardsDataTypes.sol';
import {IERC20Detailed} from '@aave/core-v3/contracts/dependencies/openzeppelin/contracts/IERC20Detailed.sol';


contract RewardsControllerHarness is RewardsController {
  constructor(address emissionManager) RewardsController(emissionManager) {}

  // returns an asset's reward index
  function getAssetRewardIndex(address asset, address reward) external view returns (uint256) {
    return _assets[asset].rewards[reward].index;
  }
    function configureAssetsHelper(RewardsDataTypes.RewardsConfigInput[] memory rewardsInput) external returns(address) {
    require(rewardsInput.length == 1);
    require(IERC20Detailed(
        rewardsInput[0].asset
      ).decimals() == 0);
    _configureAssets(rewardsInput);
    return rewardsInput[0].asset;
  }


  function getUserAccured(address asset,address reward,address user) external view returns(uint256){
    return _assets[asset].rewards[reward].usersData[user].accrued;
  }

  function getlastUpdateTimestamp(address asset,address reward) external view returns(uint256){
    return _assets[asset].rewards[reward].lastUpdateTimestamp;
  }


  function getEmission(address asset, address reward) external view returns (uint256) {
    return _assets[asset].rewards[reward].emissionPerSecond;
  }

  function getLastUpdatedTimestamp(address asset, address reward) external view returns (uint256) {
    return _assets[asset].rewards[reward].lastUpdateTimestamp;
  }

  function getPendingRewards(
    address user,
    address reward,
    address asset,
    uint256 userBalance,
    uint256 totalSupply
  ) external view returns (uint256) {
    RewardsDataTypes.UserAssetBalance memory userAssetBalance;
    userAssetBalance.asset = asset;
    userAssetBalance.userBalance = userBalance;
    userAssetBalance.totalSupply = totalSupply;
    return _getPendingRewards(user, reward, userAssetBalance);
  }

  function isRewardEnable(address reward) external view returns (bool) {
    return _isRewardEnabled[reward];
  }

  function getFirstReward(address asset) external view returns (address) {
    return _assets[asset].availableRewards[0];
  }
  function getAssetRewardByIndex(address asset,uint128 i) external view returns (address) {
    return _assets[asset].availableRewards[i];
  }


  function getAvailableRewardsCount(address asset) external view returns (uint128) {
    return _assets[asset].availableRewardsCount;
  }

  function getAsset(uint256 i) external view returns (address) {
    return _assetsList[i];
  }

  function getReward(uint256 i) external view returns (address) {
    return _rewardsList[i];
  }

  function getRewardList() external view returns (address[] memory) {
    return _rewardsList;
  }

  function getAssetList() external view returns (address[] memory) {
    return _assetsList;
  }


}
