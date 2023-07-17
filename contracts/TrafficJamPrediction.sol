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
        string roadId;
        RoadType roadType;
        RoadCondition roadCondition;
        RoadEvent roadEvent;
        uint day;
        uint timeslot;
        address firstUser;
        uint confirmNumber;
    }

    mapping(address => bool) public accounts;
    mapping(string => Incident) public incidents;
    mapping(string => bool) public incidentExist;
    mapping(string => mapping(address => bool)) public incidentConfirm;

    uint public incidentCount;
    uint public tokenReward;

    event IncidentShared(string indexed incidentHash, Incident incident);
    event IncidentConfirm(string indexed incidentHash, address user);

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
        string memory _roadId,
        RoadType _roadType,
        RoadCondition _roadCondition,
        RoadEvent _event,
        uint256 _timestamp
    ) external {
        require(accounts[msg.sender], "Account does not exist");

        uint256 currentTimestamp = _timestamp == 0 ? block.timestamp : _timestamp;
        uint _timeslot = calculateTimeslot(currentTimestamp);
        uint _day = calculateDay(currentTimestamp);
        string memory incidentHash = _roadId;
        incidentHash = string.concat(incidentHash, "_");
        incidentHash = string.concat(incidentHash, uintToString(_timeslot));
        incidentHash = string.concat(incidentHash, "_");
        incidentHash = string.concat(incidentHash, uintToString(_day));

        require(incidentConfirm[incidentHash][msg.sender] == false, "You already share this incident");
        //TODO: Check unique incident
        if (!incidentExist[incidentHash]) {
            incidents[incidentHash] = Incident({
                location: Location({
                    latitude: _latitude,
                    longitude: _longitude
                }),
                roadId: _roadId,
                roadType: _roadType,
                roadCondition: _roadCondition,
                roadEvent: _event,
                day: _day,
                timeslot: _timeslot,
                firstUser: msg.sender,
                confirmNumber: 0
            });
            incidentExist[incidentHash] = true;
            incidentConfirm[incidentHash][msg.sender] = true;
            emit IncidentShared(incidentHash, incidents[incidentHash]);
        }
        else{
            incidents[incidentHash].confirmNumber++;
            incidentConfirm[incidentHash][msg.sender] = true;
            emit IncidentConfirm(incidentHash, msg.sender);
        }
    }

    function getIncident(string memory hash)
        external 
        view
        returns (Incident memory incident)
    {
        incident = incidents[hash];
        return incident;
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

    uint256 constant TIMESLOT_DURATION = 30 minutes;

    function calculateTimeslot(uint256 _timestamp) public pure returns (uint) {
        uint256 secondsInDay = 24 hours;
        uint256 secondsSinceMidnight = _timestamp % secondsInDay;
        uint256 timeslot = secondsSinceMidnight / TIMESLOT_DURATION;
        return timeslot;
    }

    function calculateDay(uint256 _timestamp) public pure returns (uint) {
        uint256 secondsInDay = 24 hours;
        return _timestamp / secondsInDay;
    }

    function uintToString(uint v) public pure returns (string memory str) {
        uint maxlength = 100;
        bytes memory reversed = new bytes(maxlength);
        uint i = 0;
        while (v != 0) {
            uint remainder = v % 10;
            v = v / 10;
            if (remainder == 0){
                reversed[i++] = '0';
            }
            else if (remainder == 1){
                reversed[i++] = '1';
            }
            else if (remainder == 2){
                reversed[i++] = '2';
            }
            else if (remainder == 3){
                reversed[i++] = '3';
            }
            else if (remainder == 4){
                reversed[i++] = '4';
            }
            else if (remainder == 5){
                reversed[i++] = '5';
            }
            else if (remainder == 6){
                reversed[i++] = '6';
            }
            else if (remainder == 7){
                reversed[i++] = '7';
            }
            else if (remainder == 8){
                reversed[i++] = '8';
            }
            else if (remainder == 9){
                reversed[i++] = '9';
            }
        }
        bytes memory s = new bytes(i);
        for (uint j = 0; j < i; j++) {
            s[j] = reversed[i - 1 - j];
        }
        str = string(s);
    }
}