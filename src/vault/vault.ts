// Insert & retrieve secrets from the secret vault

import { ipcMain, app } from 'electron';

const Datastore = require('nedb-promises');
let vaultDB = new Datastore({ filename: `${ app.getPath('userData') }/secrets`, autoload: true });

ipcMain.handle('retrieve-all-secrets', async (e) => {
    return await vaultDB.find({}).exec();
});

ipcMain.handle('insert-secret', async (e, secret: string) => {
    return await vaultDB.insert({ secret: secret });
});
