// Insert a secret into nedb upon user action

import { app } from 'electron';
import { Datastore } from 'nedb';

let db: Datastore = new Datastore({ filename: `${ app.getPath('userData') }/secrets`, autoload: true })

// TODO: insert secret into db upon user action
