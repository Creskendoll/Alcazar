import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld(
    'vault',
    {
        retrieveAllSecrets: () => ipcRenderer.invoke('retrieve-all-secrets'),
        insertSecret: (secret: string) => ipcRenderer.invoke('insert-secret', secret)
    }
)
