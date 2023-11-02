import { configureStore, combineReducers } from '@reduxjs/toolkit';
import thunk from 'redux-thunk';
import logger from 'redux-logger';

const rootReducer = combineReducers({});

const createMiddleware = () => {
  if (process.env.NODE_ENV === 'development') {
    return [thunk, logger];
  } else {
    return [];
  }
};

const middleware = createMiddleware();

const store = configureStore({
  reducer: rootReducer,
  middleware: middleware,
  devTools: true,
});

export default store;
