// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable public recentWinner;
    address payable[] public players;
    uint256 public usdEntryFee;
    uint256 _randomness;
    AggregatorV3Interface internal ethUsdPriceFeed;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE public lottery_state;

    uint256 public _fee;
    bytes32 public _keyhash;

    event RequestedRandomness(bytes32 requestId);


    constructor(
        address priceFeedAddress,
        address vrfCoordinator,
        address link,
        uint256 fee,
        bytes32 keyhash
    ) public VRFConsumerBase(vrfCoordinator, link) {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        _fee = fee;
        _keyhash = keyhash;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN, "Lottery isn't open yet");
        require(msg.value >= getEntranceFee(), "Not enough ETH");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10;
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "A new Lottery can't be started"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(_keyhash, _fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "Lottery in wrong state"
        );
        require(randomness > 0, "Bad Random Number");
        uint256 indexOfWinner = randomness % players.length;
        recentWinner = players[indexOfWinner];

        recentWinner.transfer(address(this).balance);

        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;

        _randomness = randomness;
    }
}
