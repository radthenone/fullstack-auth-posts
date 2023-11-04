import { configureStore, combineReducers } from '@reduxjs/toolkit';
import thunk from 'redux-thunk';
import logger from 'redux-logger';

import { api } from 'app/services/api.tsx';
import auth from 'features/auth/authSlice';

const rootReducer = combineReducers({
  [api.reducerPath]: api.reducer,
  auth,
});

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

export type RootState = ReturnType<typeof store.getState>;
