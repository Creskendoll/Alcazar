const { contextBridge, ipcRenderer } = require('electron')
const react = require('react')
const reactDom = require('react-dom')

// const vault = require('./vault/vault')

contextBridge.exposeInMainWorld(
    'react',
    {
        React: react,
        ReactDOM: reactDom
    }
)
