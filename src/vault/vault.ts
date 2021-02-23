// Insert a secret into nedb upon user action

import { ipcMain } from 'electron';

ipcMain.on('insert-secret', (e, secret) => {
    console.log(secret);
});
