import "methods/Methods_base.spec";

using TransferStrategyMultiRewardHarness as TransferStrategyHarness;
using DummyERC20_rewardTokenB as rewardB;
///////////////// Properties ///////////////////////

// https://prover.certora.com/output/93750/9f696d5e25fe41248ef9d5b3d08af51a?anonymousKey=392139d04ff5d2eed3a6665b920a2237bf330529
rule handleAction(){
    env e;address user=e.msg.sender;
    uint256 before=getPendingRewards(e,user,reward,AToken,AToken.scaledBalanceOf(e,user),AToken.scaledTotalSupply(e));

    handleAction(e,user,AToken.scaledTotalSupply(e),AToken.scaledBalanceOf(e,user));
    uint256 after=getPendingRewards(e,user,reward,AToken,AToken.scaledBalanceOf(e,user),AToken.scaledTotalSupply(e));

    assert before!=after => user==AToken;
}

//passed:-if distribution time has passed,index stops growing.
// https://prover.certora.com/output/93750/9f696d5e25fe41248ef9d5b3d08af51a?anonymousKey=392139d04ff5d2eed3a6665b920a2237bf330529
rule indexCannotExceed(){
    env e;method f;calldataarg args;
    require(getLastUpdatedTimestamp(e,AToken,reward) >= getDistributionEnd(e,AToken,reward));

    uint256 _index;
    _index,_=getAssetIndex(e,AToken,reward);

    f(e,args);

    uint256 index_;
    index_,_=getAssetIndex(e,AToken,reward);

    assert _index==index_;
}

// Passed: Reward index monotonically increase
// https://prover.certora.com/output/93750/30b0ef501aac4fb8a5af737a7fb4a696/?anonymousKey=6aa1e754e68755bc4a71ed55efd9c176ae3810c7
rule user_index_keeps_growing(address user, method f) filtered { f -> !f.isView } {
    uint256 _index = getUserAssetIndex(user,AToken, reward);
    require(_index <= getAssetRewardIndex(AToken,reward));
    env e; calldataarg args;
    f(e, args);
    uint256 index_ = getUserAssetIndex(user,AToken, reward);
    
    assert index_ >= _index;
}
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

/***
  @Note:- in all claimAll(except claimAllRewards) functions unit test if 'require(to!=TransferStrategyHarness)' constraint is removed it timesout.Although it would have given better coverage if the mentioned constraint was removed and assertions were :-
  assert reward_Balance_==0 && rewardB_Balance_==0;
  assert to!=TransferStrategyHarness => to_reward_Token_balance_==_to_reward_Token_balance + _reward_Balance;
  assert to!=TransferStrategyHarness => to_rewardB_Token_balance_ == _to_rewardB_Token_balance + _rewardB_Balance;

  report link(timeouts):
   claimAllRewardsToSelf:- https://prover.certora.com/output/93750/41fb2d052a3048dc84ac2c78be09f4e4/?anonymousKey=f72b6379bd2f6de20e9d87d345bc01a4f146d6a3
   claimAllRewardsOnBehalf:- https://prover.certora.com/output/93750/5cf9bc44dad94022a5aa0c6a685084ac/?anonymousKey=304674e0443fb3209a2b5997bc98bc78cbb234f2

**/

// 
//passed:-  unit test of claimAllRewards.
// https://prover.certora.com/output/93750/096ba306872b420698cf89371503a832/?anonymousKey=b5223b52a6183ab2d330c7091a759eac359c49ae
rule claimAllRewards(){
  env e;address to;
  // require(to!=TransferStrategyHarness);
  address[] rewards=getRewardsList(e);
  require(rewards.length==2 && rewards[0]==reward && rewards[1]==rewardB && reward!=rewardB);
  address[] assets;
  require(assets.length==1 && assets[0]==AToken);
  simplify_start(e,AToken,reward);
  require(getAvailableRewardsCount(e,AToken)==2 && getAssetRewardByIndex(e,AToken,0)==reward && getAssetRewardByIndex(e,AToken,1)==rewardB);

  uint256 _reward_Balance=getUserRewards(e,assets,e.msg.sender,reward);
  uint256 _rewardB_Balance=getUserRewards(e,assets,e.msg.sender,rewardB);

  uint256 _to_reward_Token_balance= reward.balanceOf(e,to);
  uint256 _to_rewardB_Token_balance= rewardB.balanceOf(e,to);

  claimAllRewards(e,assets,to);

  uint256 reward_Balance_=getUserRewards(e,assets,e.msg.sender,reward);
  uint256 rewardB_Balance_=getUserRewards(e,assets,e.msg.sender,rewardB);

  mathint to_reward_Token_balance_= reward.balanceOf(e,to);
  mathint to_rewardB_Token_balance_= rewardB.balanceOf(e,to);


  assert reward_Balance_==0 && rewardB_Balance_==0;
  assert to!=TransferStrategyHarness => to_reward_Token_balance_==_to_reward_Token_balance + _reward_Balance;
  assert to!=TransferStrategyHarness => to_rewardB_Token_balance_ == _to_rewardB_Token_balance + _rewardB_Balance;
}

//passed:- unit test of claimAllRewardsOnBehalf
// https://prover.certora.com/output/93750/97ab2c5c67a54efb9dde94bb93686dd1/?anonymousKey=a01960eb5ede2479066dac3434c8acb92addfc1f
rule claimAllRewardsOnBehalf(){
  env e;address to;address user;
  require(to!=TransferStrategyHarness);
  address[] rewards=getRewardsList(e);
  require(rewards.length==2 && rewards[0]==reward && rewards[1]==rewardB && reward!=rewardB);
  address[] assets;
  require(assets.length==1 && assets[0]==AToken);
  simplify_start(e,AToken,reward);
  require(getAvailableRewardsCount(e,AToken)==2 && getAssetRewardByIndex(e,AToken,0)==reward && getAssetRewardByIndex(e,AToken,1)==rewardB);

  uint256 _reward_Balance=getUserRewards(e,assets,user,reward);
  uint256 _rewardB_Balance=getUserRewards(e,assets,user,rewardB);

  uint256 _to_reward_Token_balance= reward.balanceOf(e,to);
  uint256 _to_rewardB_Token_balance= rewardB.balanceOf(e,to);

  claimAllRewardsOnBehalf(e,assets,user,to);

  uint256 reward_Balance_=getUserRewards(e,assets,user,reward);
  uint256 rewardB_Balance_=getUserRewards(e,assets,user,rewardB);

  mathint to_reward_Token_balance_= reward.balanceOf(e,to);
  mathint to_rewardB_Token_balance_= rewardB.balanceOf(e,to);


  assert reward_Balance_==0 && rewardB_Balance_==0;
  assert to_reward_Token_balance_==_to_reward_Token_balance + _reward_Balance;
  assert to_rewardB_Token_balance_ == _to_rewardB_Token_balance + _rewardB_Balance;
}
// passed:- unit test of claimAllRewardsToSelf()
//https://prover.certora.com/output/93750/6c44c7372c0748f787d81b908e1ae95c/?anonymousKey=f9c0f3d1456a0a966cd58460f59de62af75b3fe1
rule claimAllRewardsToSelf(){
  env e;address to=e.msg.sender;
  require(to!=TransferStrategyHarness);
  address[] rewards=getRewardsList(e);
  require(rewards.length==2 && rewards[0]==reward && rewards[1]==rewardB && reward!=rewardB);
  address[] assets;
  require(assets.length==1 && assets[0]==AToken);
  simplify_start(e,AToken,reward);
  require(getAvailableRewardsCount(e,AToken)==2 && getAssetRewardByIndex(e,AToken,0)==reward && getAssetRewardByIndex(e,AToken,1)==rewardB);

  uint256 _reward_Balance=getUserRewards(e,assets,e.msg.sender,reward);
  uint256 _rewardB_Balance=getUserRewards(e,assets,e.msg.sender,rewardB);

  uint256 _to_reward_Token_balance= reward.balanceOf(e,to);
  uint256 _to_rewardB_Token_balance= rewardB.balanceOf(e,to);

  claimAllRewardsToSelf(e,assets);

  uint256 reward_Balance_=getUserRewards(e,assets,e.msg.sender,reward);
  uint256 rewardB_Balance_=getUserRewards(e,assets,e.msg.sender,rewardB);

  mathint to_reward_Token_balance_= reward.balanceOf(e,to);
  mathint to_rewardB_Token_balance_= rewardB.balanceOf(e,to);


  assert reward_Balance_==0 && rewardB_Balance_==0;
  assert to_reward_Token_balance_==_to_reward_Token_balance + _reward_Balance;
  assert to_rewardB_Token_balance_ == _to_rewardB_Token_balance + _rewardB_Balance;
}
// passed:- zero address must have zero reward balance
// https://prover.certora.com/output/93750/7da5d6735b674578b45fe2e7fa67bda6/?anonymousKey=8fe28a6c389db08afd182dea66f7c38edf28876f
rule bug2_zero_address(){
    env e;address user=e.msg.sender;method f;calldataarg args;
    require(reward.balanceOf(e,0)==0 && user!=0 );
    f(e,args);
    assert reward.balanceOf(e,0)==0;

}
