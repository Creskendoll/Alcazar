// Start the Alcazar app

import { app, BrowserWindow } from 'electron';
import { execSync } from 'child_process';
import Main from './main';

// Compile SASS
execSync(`sass ./style.scss ./dist/style.css`);

// Compile TypeScript
execSync(`tsc`);

Main.main(app, BrowserWindow);