// Executed in the browser context

import React from 'react';
import ReactDOM from 'react-dom';

// Components

class Vault extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            newSecret: ''
        };
    }

    updateNewSecret(e) {
        this.setState({
            newSecret: e.target.value
        });
    }

    render() {
        return (
            <div className="vault">
                <input type="text" placeholder="secret" value={this.state.newSecret} onChange={e => this.updateNewSecret(e)}></input>
                <button id="addSecretBtn" onClick={() => insertSecret(this.state.newSecret)}>Add Secret +</button>
            </div>
        );
    }
}

// Render components

ReactDOM.render(
    <Vault />,
    document.getElementById('root')
);

// Functions

function insertSecret(secret) {
    alert(secret);
}
