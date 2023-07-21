TrafficJamPrediction = new function TrafficJamPrediction(){
    this.contractAdress = '0x43933D410651385B67AFEbc3097882a254254b79'
    this.provider = 'ws://localhost:7545'
    this.maxGas = 1000000
    this.contract = null

    this.initContract = async function(){
        const trafficJamPrediction = await fetch('./contracts/TrafficJamPrediction.json')
            .then(function (response) {
                return response.json();
            });

        const web3 = new Web3(this.provider);
        this.contract = new web3.eth.Contract(trafficJamPrediction.abi, this.contractAdress);
        console.log(this.contract)
    }

    this.getAccount = async function(){
        if (window.ethereum) {
            try {
              const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
              return accounts[0];
            } catch (error) {
                throw new Error(`Get account address from MetaMask fail! ${error.message}`)
            }
        }
    }

    this.shareIncident = async function(latitude, longitude, roadId, roadType, roadCondition, event, timestamp){
        if (typeof this.contract == 'undefined'){
            const response = {
                success: false,
                message: `Share incident fail! Contract is not defined`
            };
            console.log(response);
            return response;
        }

        sender = await this.getAccount();
        var response = await this.contract.methods
                    .shareIncident(latitude, longitude, roadId, roadType, roadCondition, event, timestamp)
                    .send({from: sender, gas: this.maxGas})
                    .then(data => {
                        console.log(data)
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

    this.createAccount = async function(){
        if (typeof this.contract == 'undefined'){
            const response = {
                success: false,
                message: `Create account fail! Contract is not defined`
            };
            return response;
        }

        sender = await this.getAccount();
        var response = await this.contract.methods
                .createAccount()
                .send({from: sender, gas: this.maxGas})
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