// Executed in the renderer context

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
                <button id="addSecretBtn" onClick={() => insertSecret(this.state.newSecret)}>Add Secret +</button>
            </div>
        );
    }
}

// Render components & load page
vault.retrieveAllSecrets().then(allSecrets => console.log(allSecrets));

ReactDOM.render(
    <Vault />,
    document.getElementById('root')
)

// Functions
function insertSecret(secret) {
    // Insert secret into vault and render newly inserted secret
    vault.insertSecret(secret).then(insertedSecret => console.log(insertedSecret));
}
