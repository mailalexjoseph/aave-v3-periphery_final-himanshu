import "methods/Methods_base.spec";

using TransferStrategyHarness as TransferStrategyHarness;

///////////////// Properties ///////////////////////



methods {
    // summarize the internal 
    function computeNewIndexChange( uint256 totalSupply, uint256 block_timestamp, 
                                    uint256 lastUpdateTimestamp, uint256 distributionEnd, 
                                    uint256 emissionPerSecond, uint256 assetUnit ) internal  returns(uint256) => 
            symbolicIndexChange(totalSupply, block_timestamp, lastUpdateTimestamp, distributionEnd, emissionPerSecond);
    
    function computeNewIndexChange( uint256 totalSupply, uint256 block_timestamp, 
                                    uint256 lastUpdateTimestamp, uint256 distributionEnd, 
                                    uint256 emissionPerSecond, uint256 assetUnit ) external  returns(uint256) envfree;
            
}


//deterministic value
ghost symbolicIndexChange(uint256 /*totalSupply*/, 
                uint256 /*block_timestamp*/, 
                uint256 /*lastUpdateTimestamp*/, 
                uint256 /*distributionEnd*/,
                uint256 /*emissionPerSecond*/ ) returns uint256
    {
    axiom  
        // monotonicity on time 
        ( forall uint256 ts. forall uint256 t1. forall uint256 t2. forall uint256 last. forall uint256 dis. forall uint256 ePerSec. 
                t1 < t2 => symbolicIndexChange(ts,t1,last,dis,ePerSec) <= symbolicIndexChange(ts,t2,last,dis,ePerSec) );
        // zero for zero totalSupply
     axiom   ( forall uint256 t. forall uint256 last. forall uint256 dis. forall uint256 ePerSec. 
                symbolicIndexChange(0,t,last,dis,ePerSec) == 0); 

} 

function simplify_start(env e, address asset, address _reward) {
    require getAssetDecimals(e,asset) == 6; 
    require getlastUpdateTimestamp(e,asset,_reward) == e.block.timestamp;
}
rule monotonicityOverTime_simpleStart(address user) {
    
    env e1; 
    env e2;
    address[] assets;
    require (e1.block.timestamp < e2.block.timestamp);
    require ( assets.length  <= 1);
    simplify_start(e1, assets[0], reward);
    
    assert getUserRewards(e1, assets, user, reward) <=  getUserRewards(e2, assets, user, reward);

}


////////////////////          UNIT TESTS OF claimRewards functions   /////////////////////////////////////

//https://prover.certora.com/output/93750/6aeb518ddad5466d87e5aed6491e234e/?anonymousKey=73a246c6a26c3c09a9043dc26847939407c87a02
rule claimRewards_unit(){
    uint256 amount;address[] assets;address to;env e;address user=e.msg.sender;
    // require(user!=currentContract && user!=AToken && user!=reward);
    // require(assets.length==1 && assets[0]==AToken && getAvailableRewardsCount(e,AToken)==1 && getFirstReward(e,AToken)==reward && to!=TransferStrategyHarness);
    // require( assets[0]==AToken && assets[0]!=assets[1] && to!=TransferStrategyHarness);
    require( assets[0]==AToken && assets[0]!=assets[1] && getAvailableRewardsCount(e,assets[0])>=1 && getAvailableRewardsCount(e,assets[1])>=1 && getAssetRewardByIndex(e,assets[0],0)==reward && getAssetRewardByIndex(e,assets[1],0)==reward);
   
    uint256 before=getUserRewards(e,assets,user,reward);
    uint256 _rewardBalance=reward.balanceOf(e,to);

   uint256 transferred= claimRewards(e,assets,amount,to,reward);

    uint256 after=getUserRewards(e,assets,user,reward);
    uint256 rewardBalance_=reward.balanceOf(e,to);

   assert transferred<=amount;
   assert before >= amount => transferred==amount;
   assert  after==assert_uint256(before-transferred),"claimRewards unit test failed";
   assert to!=TransferStrategyHarness=> rewardBalance_==assert_uint256(_rewardBalance+transferred),"Reward balance of receiver must increament correctly";
}
//https://prover.certora.com/output/93750/6aeb518ddad5466d87e5aed6491e234e/?anonymousKey=73a246c6a26c3c09a9043dc26847939407c87a02
rule claimRewardsOnBehalf_unit(){
    uint256 amount;address[] assets;address to;env e;address user=e.msg.sender;
    // require(user!=currentContract && user!=AToken && user!=reward);
   // require(assets.length==1 && assets[0]==AToken && getAvailableRewardsCount(e,AToken)==1 && getFirstReward(e,AToken)==reward && to!=TransferStrategyHarness);

      //  require( assets[0]==AToken && assets[0]!=assets[1] && to!=TransferStrategyHarness);
         require( assets[0]==AToken && assets[0]!=assets[1] && getAvailableRewardsCount(e,assets[0])>=1 && getAvailableRewardsCount(e,assets[1])>=1 && getAssetRewardByIndex(e,assets[0],0)==reward && getAssetRewardByIndex(e,assets[1],0)==reward);

    uint256 before=getUserRewards(e,assets,user,reward);
    uint256 _rewardBalance=reward.balanceOf(e,to);

   uint256 transferred= claimRewardsOnBehalf(e,assets,amount,user,to,reward);

    uint256 after=getUserRewards(e,assets,user,reward);
    uint256 rewardBalance_=reward.balanceOf(e,to);

   assert transferred<=amount;
   assert before >= amount => transferred==amount;
   assert  after==assert_uint256(before-transferred),"claimRewards unit test failed";
    assert to!=TransferStrategyHarness=> rewardBalance_==assert_uint256(_rewardBalance+transferred),"Reward balance of receiver must increament correctly";
}
//https://prover.certora.com/output/93750/6aeb518ddad5466d87e5aed6491e234e/?anonymousKey=73a246c6a26c3c09a9043dc26847939407c87a02
rule claimRewardsToSelf_unit(){
    uint256 amount;address[] assets;env e;address user=e.msg.sender;
    // require(user!=currentContract && user!=AToken && user!=reward);
//     require(assets.length==1 && assets[0]==AToken && getAvailableRewardsCount(e,AToken)==1 && getFirstReward(e,AToken)==reward && e.msg.sender!=TransferStrategyHarness);
    // require( assets[0]==AToken && assets[0]!=assets[1] && e.msg.sender!=TransferStrategyHarness);
       require( assets[0]==AToken && assets[0]!=assets[1] && getAvailableRewardsCount(e,assets[0])>=1 && getAvailableRewardsCount(e,assets[1])>=1 && getAssetRewardByIndex(e,assets[0],0)==reward && getAssetRewardByIndex(e,assets[1],0)==reward);
   
    uint256 before=getUserRewards(e,assets,user,reward);
    uint256 _rewardBalance=reward.balanceOf(e,e.msg.sender);

   uint256 transferred= claimRewardsToSelf(e,assets,amount,reward);

    uint256 after=getUserRewards(e,assets,user,reward);
    uint256 rewardBalance_=reward.balanceOf(e,e.msg.sender);

     assert transferred<=amount;
   assert before >= amount => transferred==amount;
   assert  after==assert_uint256(before-transferred),"claimRewards unit test failed";
   assert e.msg.sender!=TransferStrategyHarness => rewardBalance_==assert_uint256(_rewardBalance+transferred),"Reward balance of receiver must increament correctly";
}

// Passed:- Reward lastUpdateTimestamp monotonically increase
// https://prover.certora.com/output/93750/37298007f21c4216906f263c610f9e1e?anonymousKey=f16b0c9c799a45921837477201b032a817be6b26
    rule lastupdatedtimestamp_keeps_growing(address asset,  method f) filtered { f -> !f.isView && f.selector!=sig:configureAssetsHelper(RewardsDataTypes.RewardsConfigInput[]).selector} {
        env e; calldataarg args;
        uint256 _last = getLastUpdatedTimestamp(e,asset, reward);
        require(e.block.timestamp >= _last);
        f(e, args);

        uint256 last_ = getLastUpdatedTimestamp(e,asset, reward);
        
        assert last_ >= _last;
    }
//Passed:- Only emission manager can set or change distributionEnd and emission
// https://prover.certora.com/output/93750/37298007f21c4216906f263c610f9e1e?anonymousKey=f16b0c9c799a45921837477201b032a817be6b26
rule emission_and_distributionEnd(method f)filtered{f->!f.isView && f.selector!=sig:configureAssetsHelper(RewardsDataTypes.RewardsConfigInput[]).selector}{
    env e;calldataarg args;
    uint _emission=getEmission(e,AToken,reward);
    uint _distribution=getDistributionEnd(e,AToken,reward);
    f(e,args);

    uint distribution_=getDistributionEnd(e,AToken,reward);
    uint emission_=getEmission(e,AToken,reward);

    assert _distribution!=distribution_ || _emission!=emission_  => e.msg.sender==getEmissionManager(e);
}


definition excludeOnlyEmission(method f) returns bool=
  f.selector!=sig:configureAssets(RewardsDataTypes.RewardsConfigInput[]).selector && 
  f.selector!=sig:configureAssetsHelper(RewardsDataTypes.RewardsConfigInput[]).selector && 
  f.selector!= sig:setTransferStrategy(address,address).selector &&
  f.selector!=sig:setRewardOracle(address,address).selector &&
  f.selector!=sig:setClaimer(address,address).selector &&
  f.selector!=sig:setEmissionPerSecond(address,address[],uint88[]).selector &&
  f.selector!=sig:setDistributionEnd(address,address,uint32).selector;

definition excludeHandleAction(method f) returns bool=
f.selector!=sig:handleAction(address,uint256,uint256).selector;

definition excludeConfigureAsset(method f) returns bool=
  f.selector!=sig:configureAssets(RewardsDataTypes.RewardsConfigInput[]).selector && 
  f.selector!=sig:configureAssetsHelper(RewardsDataTypes.RewardsConfigInput[]).selector;

//pending rewards can only remain same or be zero 
//Note:- if asset calls handleAction function with wrong totalSupply and userBalance it can wrongly update rewardData and any user accured rewards. 
// https://prover.certora.com/output/93750/0522927ccbb74468971ce1c6cc823623/?anonymousKey=924803aaf29c276b3be027eba17cee97171e1000
rule getPendingRewardRestriction(method f) filtered{f-> !f.isView && excludeOnlyEmission(f) && excludeHandleAction(f) && excludeConfigureAsset(f)}{
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

//passed:- only emission manager can set claimer
// https://prover.certora.com/output/93750/6aa043093ea04923978b3d37ea0c6dcb/?anonymousKey=b05181920b67c9f869c504ddddeed63dbe1167a4
rule setClaimer(method f) filtered{f->!f.isView} {
  env e;calldataarg args;address user;

  require(getClaimer(e,user)==0);

  f(e,args);

  assert getClaimer(e,user)!=0 => e.msg.sender==getEmissionManager(e);
}

//passed:- assetList must contain unique assets.
//https://prover.certora.com/output/93750/17bcd7bc1b8445f7961d37eab92a615e/?anonymousKey=26980e0a6c3b91ad2275dc1e812548761b08e43e
rule prop16_assetList(method f) filtered{f->!f.isView && f.selector!= sig:configureAssetsHelper(RewardsDataTypes.RewardsConfigInput[]).selector}{
  env e;calldataarg args;
  uint256 randomIndex;
  address[] _asset=getAssetList(e);
  require(_asset.length==1 && _asset[0]==AToken && getAssetDecimals(e,AToken)!=0 && AToken.decimals(e)!=0);

  f(e,args);

  address[] asset_=getAssetList(e);

  // require(randomIndex >0 && randomIndex <asset_.length);

  assert asset_.length>1 => e.msg.sender==getEmissionManager(e) ;
  assert randomIndex >0 && randomIndex <asset_.length => asset_[randomIndex]!=AToken;
}

//passed:- rewardsList array must contain unique rewards.
// https://prover.certora.com/output/93750/99e5099a7329426881c09d71563fbc5f/?anonymousKey=218e296e3479b38a6f6ca1c8f6a4718d269b2f62
rule prop16(method f) filtered{f->!f.isView && f.selector!= sig:configureAssetsHelper(RewardsDataTypes.RewardsConfigInput[]).selector}{
  env e;calldataarg args;
  uint256 randomIndex;
  address[] _reward=getRewardsList(e);
  require(_reward.length==1 && _reward[0]==reward && isRewardEnable(e,reward)==true);

  f(e,args);

  address[] reward_=getRewardsList(e);

  assert reward_.length>1 => e.msg.sender==getEmissionManager(e);
  assert randomIndex >0 && randomIndex <reward_.length => reward_[randomIndex]!=reward;
}


// emission,distributionEnd,totalSupply of a rewardData can only be changed by emissionManager
// https://prover.certora.com/output/93750/64486ffd3e9344e1ba058170a98bd874/?anonymousKey=8de6cb59b8933d2ad7494c88c5bbc15898af9e65
rule onlyEmissionManager(method f) filtered{f->!f.isView && f.selector!=sig:configureAssetsHelper(RewardsDataTypes.RewardsConfigInput[]).selector}{
  env e;calldataarg args;
  uint256 _emission;uint256 _disEnd;
  uint256 emission_;uint256 disEnd_;
 _,_emission,_,_disEnd= getRewardsData(AToken,reward);
 address _transferStrat=getTransferStrategy(e,reward);
 address _oracle=getRewardOracle(e,reward);

  f(e,args);

 address oracle_=getRewardOracle(e,reward);
 address transferStrat_=getTransferStrategy(e,reward);
  _,emission_,_,disEnd_= getRewardsData(AToken,reward);

  assert (_transferStrat!= transferStrat_ || _oracle!= oracle_|| emission_!=_emission || disEnd_!=_disEnd )=> e.msg.sender==getEmissionManager(e);
}

//after any operation index of rewardConfig can either be same or equal to futureIndex which is predetermined before operation
// https://prover.certora.com/output/93750/64486ffd3e9344e1ba058170a98bd874/?anonymousKey=8de6cb59b8933d2ad7494c88c5bbc15898af9e65
rule indexCorrectness(method f) filtered{f->!f.isView && excludeOnlyEmission(f) && excludeHandleAction(f)}{
  calldataarg args;env e;
  uint256 _current;uint256 _future;
  _current,_future=getAssetIndex(e,AToken,reward);
  f(e,args);
  uint256 current_;uint256 future_;
  current_,future_=getAssetIndex(e,AToken,reward);
  assert (_current==current_ && _future==future_) || (current_==_future && future_==_future);
}

  // Passed: Reward index monotonically increase
  // https://prover.certora.com/output/93750/64486ffd3e9344e1ba058170a98bd874/?anonymousKey=8de6cb59b8933d2ad7494c88c5bbc15898af9e65
rule user_index_keeps_growing(address user, method f,env e, calldataarg args) filtered { f -> !f.isView && excludeHandleAction(f)} {
   uint256 _index = getUserAssetIndex(user,AToken, reward);
   uint256 rewardIndex;
   rewardIndex,_=getAssetIndex(e,AToken,reward);
  require(_index <= rewardIndex);

   f(e, args);

   uint256 index_ = getUserAssetIndex(user,AToken, reward);
   
   assert index_ >= _index;
}

//passed
// https://prover.certora.com/output/93750/99e5099a7329426881c09d71563fbc5f/?anonymousKey=218e296e3479b38a6f6ca1c8f6a4718d269b2f62
rule prop16_availaleRewards_of_asset_must_be_unique{
 method f;calldataarg args; env e;uint128 x;uint128 y;uint256 lastUpdatedTime;
  _,_,lastUpdatedTime,_= getRewardsData(AToken,reward);
  require(getAvailableRewardsCount(e,AToken)==1 && getAssetRewardByIndex(e,AToken,0)==reward && lastUpdatedTime!=0 && e.block.timestamp!=0);
  f(e,args);
  assert getAvailableRewardsCount(e,AToken)>=2 =>  getAssetRewardByIndex(e,AToken,1)!=reward;
}



// rule prop17(method f,env e,calldataarg args)filtered{f->!f.isView && excludeOnlyEmission(f) && excludeHandleAction(f) && excludeConfigureAsset(f)}{
  
//   // address[] assets;address user;
//   // require(assets.length==1 &&assets[0]==AToken); 
//   address user;

//   require(getAvailableRewardsCount(e,AToken)>=1 && getAssetRewardByIndex(e,AToken,0)==reward && getAssetDecimals(e,AToken)==6);
//   mathint before_acc=getUserAccured(e,AToken,reward,user);
//   mathint before_pending=getPendingRewards(e,user,reward,AToken,AToken.balanceOf(e,user),AToken.scaledTotalSupply(e));

//   mathint _userIndex=getUserAssetIndex(e,user,AToken,reward);
//   mathint _currentAssetIndex;mathint _futureAssetIndex;
//   _currentAssetIndex,_futureAssetIndex= getAssetIndex(e,AToken,reward);
  
//   f(e,args);

//   mathint after_acc=getUserAccured(e,AToken,reward,user);
//   mathint after_pending=getPendingRewards(e,user,reward,AToken,AToken.balanceOf(e,user),AToken.scaledTotalSupply(e));

//   mathint userIndex_=getUserAssetIndex(e,user,AToken,reward);
//   mathint currentAssetIndex_;mathint futureAssetIndex_;
//   currentAssetIndex_,futureAssetIndex_= getAssetIndex(e,AToken,reward);

//   assert before_acc!=after_acc => after_pending==0;
//   assert before_pending!=after_pending => after_pending==0;
//   assert before_acc!=after_acc || before_pending!=after_pending => userIndex_== _futureAssetIndex && currentAssetIndex_==_futureAssetIndex && _futureAssetIndex==futureAssetIndex_;
// }
// rule prop17_break(method f,env e,calldataarg args)filtered{f->!f.isView && excludeOnlyEmission(f) && excludeHandleAction(f) && excludeConfigureAsset(f)}{
  
//   // address[] assets;address user;
//   // require(assets.length==1 &&assets[0]==AToken); 
//   address user;

//     require(getAvailableRewardsCount(e,AToken)>=1 && getAssetRewardByIndex(e,AToken,0)==reward && getAssetDecimals(e,AToken)==6);

//   mathint before_acc=getUserAccured(e,AToken,reward,user);
//   mathint before_pending=getPendingRewards(e,user,reward,AToken,AToken.balanceOf(e,user),AToken.scaledTotalSupply(e));

//   mathint _userIndex=getUserAssetIndex(e,user,AToken,reward);
//   mathint _currentAssetIndex;mathint _futureAssetIndex;
//   _currentAssetIndex,_futureAssetIndex= getAssetIndex(e,AToken,reward);
  
//   f(e,args);

//   mathint after_acc=getUserAccured(e,AToken,reward,user);
//   mathint after_pending=getPendingRewards(e,user,reward,AToken,AToken.balanceOf(e,user),AToken.scaledTotalSupply(e));

//   mathint userIndex_=getUserAssetIndex(e,user,AToken,reward);
//   mathint currentAssetIndex_;mathint futureAssetIndex_;
//   currentAssetIndex_,futureAssetIndex_= getAssetIndex(e,AToken,reward);

//   assert before_acc!=after_acc => after_pending==0;
//   // assert before_pending!=after_pending => after_pending==0;
//   // assert before_acc!=after_acc || before_pending!=after_pending => userIndex_== _futureAssetIndex && currentAssetIndex_==_futureAssetIndex && _futureAssetIndex==futureAssetIndex_;
// }

// passed:- in claimRewards passing assets array with unique and one AToken result same as assets array with 2 same AToken
// https://prover.certora.com/output/93750/e5aaac226a1d4781b5939642254dc458/?anonymousKey=0b8e36a72860469278f725eb20f9fdc1bbff4ea8
rule prop19{
  env e;
  address[] assets;
  address[] assetsUnique;
  uint256 amount;
  address to;
  require(assets.length==2 && assets[0]==assets[1] && assets[1]==AToken);
  require(assetsUnique.length==1 && assetsUnique[0]==AToken);

  storage initial=lastStorage;
  claimRewards(e,assets,amount,to,reward);
  storage storage_after_no_unique=lastStorage;

  claimRewards(e,assetsUnique,amount,to,reward) at initial;
  storage storage_after_unique=lastStorage;

  assert storage_after_no_unique==storage_after_unique;
}

// https://prover.certora.com/output/93750/72f2c8024d3044e7908ba8a567396e9d?anonymousKey=ecdd769e4203a3cde656348b85cb82a85acc0aa3 
rule prop19_claimAll{
  env e;
  address[] assets;
  address[] assetsUnique;
  uint256 amount;
  address to;
  require(assets.length==2 && assets[0]==assets[1] && assets[1]==AToken);
  require(assetsUnique.length==1 && assetsUnique[0]==AToken);

  // uint256 lastUpdatedTime;
  // _,_,lastUpdatedTime,_= getRewardsData(AToken,reward);

  // require(getAvailableRewardsCount(e,AToken)==1 && getAssetRewardByIndex(e,AToken,0)==reward && lastUpdatedTime!=0 && e.block.timestamp!=0);
  // require(g lastUpdatedTime!=0 && e.block.timestamp!=0);

  storage initial=lastStorage;
  claimAllRewards(e,assets,to);
  storage storage_after_no_unique=lastStorage;

  claimAllRewards(e,assetsUnique,to) at initial;
  storage storage_after_unique=lastStorage;

  assert storage_after_no_unique==storage_after_unique;
}

// if any reward is part of rewardList , it must have transferStrategy and rewardOracle.
// https://prover.certora.com/output/93750/ebc8db1231e14e0291a36f9cb0cee298?anonymousKey=a2334fec12124c39887c91c1f6e7924a310d2506
invariant prop20(env e)
  isRewardEnable(e,reward) => getTransferStrategy(e,reward)!=0
  filtered{f->f.selector!= sig:configureAssetsHelper(RewardsDataTypes.RewardsConfigInput[]).selector}


//passed:- claimRewards() is same as claimRewardsToSelf() if to == e.msg.sender in former.
// https://prover.certora.com/output/93750/240e8c0a862d421aaca81f09dedda238/?anonymousKey=af0f52c6667933f5003d4c57e76d5591c1dd0468
rule prop21(){
  address[] assets;
  uint256 amount;
  address to;
  env e;
  storage initial=lastStorage;
  claimRewards(e,assets,amount,to,reward);
  storage first=lastStorage;
  claimRewardsToSelf(e,assets,amount,reward) at initial;
  storage second=lastStorage;
  require assets.length == 2; 

  assert to==e.msg.sender => first==second;
}



//passed :- if userA has more pending reward balance than userB then either asset balance of userA must be greater or userA index must be lesser.
// https://prover.certora.com/output/93750/5301c95278764cdea51314f3cacd33b1/?anonymousKey=2cf16f713371438654ff4154dab973f58caf95f3
rule prop22(method f)filtered{f->!f.isView}{
  env e;
  calldataarg args;
  address userA;address userB;
  address[] assetList=getAssetList(e);
  address[] rewardList=getRewardsList(e);
  require(getlastUpdateTimestamp(e,AToken,reward) <= e.block.timestamp);
  require(rewardList.length<=1);
  require(getAssetDecimals(e,AToken)==6);
  require(AToken.scaledTotalSupply(e)!=0);

  require( 
    getPendingRewards(e,userA,reward,AToken,AToken.balanceOf(e,userA),AToken.scaledTotalSupply(e)) > getPendingRewards(e,userB,reward,AToken,AToken.balanceOf(e,userB),AToken.scaledTotalSupply(e)) && 
    (AToken.balanceOf(e,userA) > AToken.balanceOf(e,userB) || getUserAssetIndex(userA,AToken,reward) < getUserAssetIndex(userB,AToken,reward))
   );

    f(e,args);

    assert getPendingRewards(e,userA,reward,AToken,AToken.balanceOf(e,userA),AToken.scaledTotalSupply(e)) >
    getPendingRewards(e,userB,reward,AToken,AToken.balanceOf(e,userB),AToken.scaledTotalSupply(e)) =>
    (
      (AToken.balanceOf(e,userA) > AToken.balanceOf(e,userB) || getUserAssetIndex(userA,AToken,reward) < getUserAssetIndex(userB,AToken,reward))
    );
}

//passed:- rewardBalance of user cannot increase by any operation.
// https://prover.certora.com/output/93750/b6e056d3032844299188fc5881bf5f6d/?anonymousKey=872f50f771e38b7af065e77185336d80192195d1
rule prop24(method f,calldataarg args,env e)filtered{f->!f.isView && excludeHandleAction(f) && excludeOnlyEmission(f) && f.selector!= sig:configureAssetsHelper(RewardsDataTypes.RewardsConfigInput[]).selector}{
  address user;
  address[] assets;
  require(assets.length==1 && assets[0]==AToken);

  uint256 before=getUserRewards(e,assets,user,reward);

  f(e,args);

  uint256 after=getUserRewards(e,assets,user,reward);

  assert after <= before;
}

//passed:- if userA does any operation , this should not change userB netRewardBalance(unless userA if authorized or userB itself).
// https://prover.certora.com/output/93750/142266d9ba2e4c7c8b9abc91871773ce/?anonymousKey=48add144a7e5ab4a0b428ff2fe25e9888b516a40

rule prop25(method f,calldataarg args,env e)filtered{f->!f.isView && excludeHandleAction(f) && excludeOnlyEmission(f) && f.selector!= sig:configureAssetsHelper(RewardsDataTypes.RewardsConfigInput[]).selector}{
  address user;
  require(e.msg.sender!=user && getClaimer(user)!=e.msg.sender);
  address[] assets;
  require(assets.length==1 && assets[0]==AToken );

  uint256 beforeNet= getUserRewards(e,assets,user,reward);
  uint256 before_acc=getUserAccured(e,AToken,reward,user);
  f(e,args);
  uint256 afterNet= getUserRewards(e,assets,user,reward);
  uint256 after_acc=getUserAccured(e,AToken,reward,user); 

  assert before_acc==after_acc; 
  assert beforeNet==afterNet;
}


//passed:- if there occur any change in user accured rewards then his pending rewards must be 0. 
// https://prover.certora.com/output/93750/e5393f366db7467f8324002a8e50b74d/?anonymousKey=7135177ca4c5ec79d19b8d9663094144bc330eae
// @Note:- excluding configure asset coz  emission manager can add a new asset-reward pair with different asst but same reward as in this rule which can change user accured balance.
rule prop26(method f,calldataarg args,env e)filtered{f->!f.isView && excludeConfigureAsset(f)}{
  address user;
  address[] assets=getAssetList(e);
  require(assets.length==1 && assets[0]==AToken && getAssetDecimals(e,AToken)==6);
  require(getAvailableRewardsCount(e,AToken)>=1 && getAssetRewardByIndex(e,AToken,0)==reward);

  uint256 before=getUserAccruedRewards(e,user,reward);
  f(e,args);
  uint256 after=getUserAccruedRewards(e,user,reward);

  assert before!=after => getUserRewards(e,assets,user,reward)==after; //pending reward is 0.
}

//passed:- future index does not change by any operation.(only change with time). https://prover.certora.com/output/93750/133861b59beb4b6783708d95fa0a43cf/?anonymousKey=3adc8c104120998fedb926b881b23b55aab99833
rule prop28(method f,env e,env e2,calldataarg args)filtered{f->!f.isView && excludeOnlyEmission(f) && excludeConfigureAsset(f) && excludeHandleAction(f)}{
  uint256 _neew;uint256 neew_;uint256 neew_future_;

  require(getLastUpdatedTimestamp(e,AToken,reward)<=e.block.timestamp);
 _,_neew = getAssetIndex(e,AToken,reward);
 f(e,args);
 _,neew_ = getAssetIndex(e,AToken,reward);
 _,neew_future_ = getAssetIndex(e2,AToken,reward);

 assert _neew==neew_;
 assert e2.block.timestamp > e.block.timestamp=>neew_future_ >= neew_;
}

