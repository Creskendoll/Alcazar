// Start the Alcazar app

import { execSync } from 'child_process';

// TODO: Can we do this compilation using `npm pack`?
// TODO: Compile TypeScript with Babel

// Move preload script to ./dist
execSync(`cp ./src/preload.js ./dist/preload.js`);

// Compile TypeScript
execSync(`tsc`);

// Compile JSX
execSync(`browserify ./src/renderer/script.jsx -t babelify --outfile ./dist/bundle.js`);

// Compile SASS
execSync(`sass ./src/scss/style.scss ./dist/css/style.css`);

import { app, BrowserWindow } from 'electron';

import Main from './main';
import './vault/vault'

Main.main(app, BrowserWindow);