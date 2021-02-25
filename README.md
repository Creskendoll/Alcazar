# Alcazar

A necessarily password-less MFA-based desktop secret vault.

## Development

### Run the project

In order to build and run the project run:

-   `npm start`

This will bundle the resources into a `/dist` directory and launch the Electron app.

### Issues

2021.02.25

-   Can't bundle sub-folders in the renderer folder.
-   Need to add hot reload.
-   React can be written with Typescript.
-   The `exposeInMainWorld` stuff in `preload.ts` feels janky.
