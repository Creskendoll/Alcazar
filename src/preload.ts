const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld(
    'vault',
    {
        insertSecret: (secret: string) => ipcRenderer.send('insert-secret', secret)
    }
)
