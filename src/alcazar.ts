import { app, BrowserWindow } from "electron";
import Main from "./main";
import "./vault/vault";

// Start the Alcazar app
Main.main(app, BrowserWindow);
