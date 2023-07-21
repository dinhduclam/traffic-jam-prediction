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
    uint256 public tokenReward;
    uint256 public minimunTokenGetProbability;


    event IncidentShared(string indexed incidentHash, Incident incident);
    event IncidentConfirm(string indexed incidentHash, address user);

    constructor () {
        incidentCount = 0;
        tokenReward = 1 ether;
        minimunTokenGetProbability = 2 ether;
    }

    function donate() external payable  {
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
    ) external payable{
        require(accounts[msg.sender], "Account does not exist");

        uint256 timestamp = _timestamp == 0 ? block.timestamp : _timestamp;

        uint _timeslot = calculateTimeslot(timestamp);
        uint _day = calculateDay(timestamp);
        
        string memory hash = incidentHash(_roadId, _day, _timeslot);

        require(incidentConfirm[hash][msg.sender] == false, "You already share this incident");
        //TODO: Check unique incident
        if (!incidentExist[hash]) {
            incidents[hash] = Incident({
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
            incidentExist[hash] = true;
            incidentConfirm[hash][msg.sender] = true;
            emit IncidentShared(hash, incidents[hash]);
        }
        else{
            incidents[hash].confirmNumber++;
            incidentConfirm[hash][msg.sender] = true;
            if (incidents[hash].confirmNumber == 3){
                address payable firstUser = payable(incidents[hash].firstUser);
                firstUser.transfer(tokenReward);
            }
            emit IncidentConfirm(hash, msg.sender);
        }
    }

    function getIncident(string memory hash)
        public  
        view
        returns (Incident memory incident)
    {
        require(accounts[msg.sender], "Account does not exist");
        incident = incidents[hash];
        return incident;
    }

    function getTrafficJamIncident(
        string memory _roadId,
        uint256 _timestamp
        )
        external
        payable
        returns (Incident memory incident)
    {
        require(accounts[msg.sender], "Account does not exist");
        require(msg.value >= minimunTokenGetProbability, "Insufficient Ether sent");

        uint256 timestamp = _timestamp == 0 ? block.timestamp : _timestamp;
        uint _timeslot = calculateTimeslot(timestamp);
        uint _day = calculateDay(timestamp);

        string memory hash = incidentHash(_roadId, _day, _timeslot);
        return getIncident(hash);
    }

    function incidentHash(
        string memory _roadId,
        uint _day,
        uint _timeslot
    ) internal pure returns (string memory hash)
    {
        hash = _roadId;
        hash = string.concat(hash, "_");
        hash = string.concat(hash, uintToString(_timeslot));
        hash = string.concat(hash, "_");
        hash = string.concat(hash, uintToString(_day));
    }

    uint256 constant TIMESLOT_DURATION = 30 minutes;

    function calculateTimeslot(uint256 _timestamp) internal pure returns (uint) {
        uint256 secondsInDay = 24 hours;
        uint256 secondsSinceMidnight = _timestamp % secondsInDay;
        uint256 timeslot = secondsSinceMidnight / TIMESLOT_DURATION;
        return timeslot;
    }

    function calculateDay(uint256 _timestamp) internal pure returns (uint) {
        uint256 secondsInDay = 24 hours;
        return _timestamp / secondsInDay;
    }

    function uintToString(uint v) internal pure returns (string memory str) {
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