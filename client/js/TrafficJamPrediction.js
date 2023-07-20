

class TrafficJamPrediction {
    contractAdress = '0x7325C124fa8Fa9e057D65984fd16FB07Eb738B22'
    provider = 'ws://localhost:7545'
    maxGas = 1000000
    contract = null

    constructor(){

    }

    initContract = async function(){
        const trafficJamPrediction = await fetch('./contracts/TrafficJamPrediction.json')
            .then(function (response) {
                return response.json();
            });

        const web3 = new Web3(provider);
        contract = new web3.eth.Contract(trafficJamPrediction.abi, contractAdress);
    }

    getAccount = async function(){
        if (window.ethereum) {
            try {
              const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
              return accounts[0];
            } catch (error) {
                throw new Error(`Get account address from MetaMask fail! ${error.message}`)
            }
        }
    }

    shareIncident = async function(latitude, longitude, roadType, roadCondition, event){
        if (typeof contract == 'undefined'){
            const response = {
                success: false,
                message: `Share incident fail! Contract is not defined`
            };
            console.log(response);
            return response;
        }

        sender = await this.getAccount();
        var response = await contract.methods
                    .shareIncident(latitude, longitude, roadType, roadCondition, event)
                    .send({from: sender, gas: maxGas})
                    .then(_ => {
                        const response = {
                            success: true,
                            message: 'Share incident successfully!'
                        };

                        return response;
                    })
                    .catch(err => {
                        const response = {
                            success: false,
                            message: `Share incident fail! ${err.message}`
                        };

                        return response;
                    });

        return response;
    }

    createAccount = async function(){
        if (typeof contract == 'undefined'){
            const response = {
                success: false,
                message: `Create account fail! Contract is not defined`
            };
            return response;
        }

        sender = await this.getAccount();
        var response = await contract.methods
                .createAccount()
                .send({from: sender, gas: maxGas})
                .then(_ => {
                    const response = {
                        success: true,
                        message: `Create account successfully!`
                    };

                    return response;
                })
                .catch(err => {
                    const response = {
                        success: false,
                        message: `Create account fail! ${err.message}`
                    };

                    return response;
                });

        return response;
    }
}

window.addEventListener('load', () => {
    TrafficJamPrediction.initContract();
})