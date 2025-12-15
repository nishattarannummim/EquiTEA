// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EquiTEAWage {
    address public admin;
    mapping(string => address) public workerWallets;
    mapping(string => uint) public wageRates;

    event WagePaid(string workerID, address worker, uint wage);

    constructor() {
        admin = msg.sender;
    }

    function registerWorker(string memory workerID, address walletAddress) public {
        require(msg.sender == admin, "Only admin can register workers");
        workerWallets[workerID] = walletAddress;
    }

    function setWageRate(string memory workerID, uint ratePerKg) public {
        require(msg.sender == admin, "Only admin can set wage");
        wageRates[workerID] = ratePerKg;
    }

    function processWage(string memory workerID, uint weightInKg) public payable {
        uint amount = weightInKg * wageRates[workerID];
        payable(workerWallets[workerID]).transfer(amount);
        emit WagePaid(workerID, workerWallets[workerID], amount);
    }
}