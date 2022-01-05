# Fleebmarket frontend

This project contains a react app used in complement with django to provide the fleebmarket frontend

## Setup

To build this project, you will need `nodejs`, and a package manager, either `yarn` or `npm`.
Once this is done, you can install dependencies with `yarn install`

## Develop

Run `REACT_APP_CUSTOM_PORT=8000 yarn start`: this will start the application, connecting to a chosen backend on the specified port on localhost.

## Build

Run `yarn build`. In order to make fleebmarket use the built files, the content of `build/static` must be accessible as static files to the django backend, e.g. in `fleebmarket_django/static/search_app`. 

You can either copy them manually, or make a symlink from `build/static` to `fleebmarket_django/static/search_app`.

# Default readme: basic information

In the project directory, you can run:

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `yarn test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

