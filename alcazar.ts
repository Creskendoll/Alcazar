// Start the Alcazar app

import { execSync } from 'child_process';

// Compile TypeScript
execSync(`tsc`);

// Compile SASS
execSync(`sass ./scss/style.scss ./dist/css/style.css`);

import { app, BrowserWindow } from 'electron';
import Main from './main';

Main.main(app, BrowserWindow);