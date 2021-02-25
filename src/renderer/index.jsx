import React from 'react';
import ReactDOM from 'react-dom';

function Vault() {
    const [secrets, setSecrets] = React.useState([]);
    const [newSecret, setNewSecret] = React.useState("");

    // componentDidMount
    React.useEffect(() => {
        vault.retrieveAllSecrets()
            .then((allSecrets) =>
                setSecrets(allSecrets)
            );
    }, []);

    function updateNewSecret(e) {
        // Keep track of newSecret as the user types
        setNewSecret(e.target.value);
    };

    function insertSecret(secret) {
        // Insert secret into vault and update state
        vault.insertSecret(secret).then(insertedSecret => {
            setSecrets([
                ...secrets,
                insertedSecret
            ]);
        });
    };

    return (
        <div className="vault">
            <div className="secrets">
                {secrets.map(secret =>
                    <p key={secret._id}>{secret.secret}</p>
                )}
            </div>
            <div className="insertSecret">
                <input type="text" placeholder="secret" value={newSecret} onChange={e => updateNewSecret(e)}></input>
                <button id="addSecretBtn" onClick={() => insertSecret(newSecret)}>Add Secret +</button>
            </div>
        </div>
    )
}


// Executed in the renderer context
// Render components
ReactDOM.render(
    <Vault />,
    document.getElementById('root')
);
