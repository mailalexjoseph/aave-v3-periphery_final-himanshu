import "methods/Methods_base.spec";

///////////////// Properties ///////////////////////

// Emission manager can configure asset-reward pair in which asset have 0 decimals but now set its emissionPerSecond using 'setEmissionPerSecond' func. So there is inconsistancy as configure asset does not check for 0 decimals but setEmissionPerSecond does.
rule prop18(){
  env e;
  calldataarg args;
  address asset;
  address[] rewards;
  uint88[] newEmissionsPerSecond;
  bool zero_decimal_succes;
  require(rewards.length==newEmissionsPerSecond.length && rewards.length >0);

  asset= configureAssetsHelper(e,args);

  setEmissionPerSecond@withrevert(e,asset,rewards,newEmissionsPerSecond);

  assert lastReverted==false;
}
// Emission manager can push same asset with 0 decimals multiple times in _assetList.
// https://prover.certora.com/output/93750/585784e3af004af2883134c5fb79a418?anonymousKey=62b800fe0ab1976d7e2f0eab233b6f05b9dcad62
rule prop16_assetList_without_constraint(method f) filtered{f->!f.isView && f.selector!= sig:configureAssetsHelper(RewardsDataTypes.RewardsConfigInput[]).selector}{
  env e;calldataarg args;
  uint256 randomIndex;
  address[] _asset=getAssetList(e);
  require(_asset.length==1 && _asset[0]==AToken);

  f(e,args);

  address[] asset_=getAssetList(e);

  // require(randomIndex >0 && randomIndex <asset_.length);

  assert asset_.length>1 => e.msg.sender==getEmissionManager(e) ;
  assert randomIndex >0 && randomIndex <asset_.length => asset_[randomIndex]!=AToken;
}

//pending rewards can only remain same or be zero 
//Note:- if asset calls handleAction function with wrong totalSupply and userBalance it can wrongly update rewardData and any user accured rewards. 
rule getPendingRewardRestriction(method f) filtered{f-> !f.isView && excludeOnlyEmission(f) && excludeConfigureAsset(f)}{
  env e;
  address user;
  calldataarg args;
  address[] assets=getAssetList(e);
  require(assets.length==1);
  
  mathint _getPending = getUserRewards(e,assets,user,reward) - getUserAccruedRewards(e,user,reward);

  f(e,args);

  mathint getPending_ = getUserRewards(e,assets,user,reward) - getUserAccruedRewards(e,user,reward);

  // assert getPending_ >= _getPending || getPending_==0;
  assert getPending_ == _getPending || getPending_==0;
}