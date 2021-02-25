// Executed in the renderer context

import React, { Component } from 'react';
import ReactDOM from 'react-dom';

// Componenets
class Vault extends Component {
    constructor(props) {
        super(props);

        this.state = {
            secrets: [],
            newSecret: ''
        };
    };

    componentDidMount() {
        // Set secrets from db
        vault.retrieveAllSecrets()
            .then((allSecrets) => {
                this.setState({
                    secrets: allSecrets
                });
            });
    }

    updateNewSecret(e) {
        // Keep track of newSecret as the user types
        this.setState({
            newSecret: e.target.value
        });
    };

    insertSecret(secret) {
        // Insert secret into vault and update state
        vault.insertSecret(secret).then(insertedSecret => {
            this.setState({
                secrets: [
                    ...this.state.secrets,
                    insertedSecret
                ]
            });
        });
    };

    render() {
        return (
            <div className="vault">
                <div className="secrets">
                    {this.state.secrets.map(secret => 
                        <p key={secret._id}>{secret.secret}</p>
                    )}
                </div>
                <div className="insertSecret">
                    <input type="text" placeholder="secret" value={this.state.newSecret} onChange={e => this.updateNewSecret(e)}></input>
                    <button id="addSecretBtn" onClick={() => this.insertSecret(this.state.newSecret)}>Add Secret +</button>
                </div>
            </div>
        );
    };
};

// Render components
ReactDOM.render(
    <Vault />,
    document.getElementById('root')
);
