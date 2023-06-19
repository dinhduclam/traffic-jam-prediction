// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract TrafficJamPrediction {

    enum RoadType{
        Expressway,
        NationalHighway,
        StateHighway,
        MajorDistrictRoad,
        OtherDistrictRoad,
        RuralRoad
    }

    enum RoadCondition{
        Smooth,
        Moderate,
        Poor,
        ExtremelyBad
    }

    enum RoadEvent{
        Construction,
        Accident,
        Barricades,
        TollBooth,
        DemonstrationsOrProtests,
        Marathon,
        Others
    }

    struct Location {
        int256 latitude;
        int256 longitude;
    }

    struct Incident {
        Location location;
        RoadType roadType;
        RoadCondition roadCondition;
        RoadEvent roadEvent;
        uint timeslot;
    }

    mapping(address => bool) public accounts;
    mapping(uint => Incident) public incidents;
    mapping(uint => bool) public uniqueIncidents;
    mapping(uint => address) public firstUser;

    uint public incidentCount;
    uint public tokenReward;

    event IncidentShared(uint indexed incidentId, address indexed user, uint timestamp);

    constructor() {
        incidentCount = 0;
        tokenReward = 10; // Adjust the token reward as needed
    }

    function createAccount() external {
        require(!accounts[msg.sender], "Account already exists");
        accounts[msg.sender] = true;
    }

    function shareIncident(
        int256 _latitude,
        int256 _longitude,
        RoadType _roadType,
        RoadCondition _roadCondition,
        RoadEvent _event
    ) external {
        require(accounts[msg.sender], "Account does not exist");

        uint currentTimestamp = block.timestamp;
        uint incidentId = incidentCount++;

        incidents[incidentId] = Incident({
            location: Location({
                latitude: _latitude,
                longitude: _longitude
            }),
            roadType: _roadType,
            roadCondition: _roadCondition,
            roadEvent: _event,
            timeslot: 1 //TODO: calculate timeslot from timestamp
        });

        //TODO: Check unique incident
        if (!uniqueIncidents[incidentId]) {
            uniqueIncidents[incidentId] = true;
            firstUser[incidentId] = msg.sender;
            emit IncidentShared(incidentId, msg.sender, currentTimestamp);
        }
    }

    function getTrafficJamProbability()
        external
        pure
        returns (uint probability)
    {
        probability = calculateProbability();
        return probability;
    }

    function calculateProbability()
        internal
        pure
        returns (uint probability)
    {
        probability = 40;
        return probability;
    }
}