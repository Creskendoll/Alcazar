// Executed in the browser context

const React = require('react');
const ReactDOM = require('react-dom');

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
                <button id="addSecretBtn" onClick={() => vault.insertSecret(this.state.newSecret)}>Add Secret +</button>
            </div>
        );
    }
}

// Render components
ReactDOM.render(
    <Vault />,
    document.getElementById('root')
)
