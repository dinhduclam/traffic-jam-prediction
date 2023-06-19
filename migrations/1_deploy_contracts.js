const TrafficJamPrediction = artifacts.require("TrafficJamPrediction");

module.exports = function(deployer) {
  deployer.deploy(TrafficJamPrediction);
};