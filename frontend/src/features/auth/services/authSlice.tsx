import { createSlice } from '@reduxjs/toolkit';
import type { UserType } from 'types/users/userTypes.tsx';
import type { RootState } from 'app/store.tsx';

type AuthState = {
  user: UserType | null;
  token: string | null;
};

const authState: AuthState = {
  user: null,
  token: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState: authState,
  reducers: {
    login: (state, action) => {
      const { user, accessToken } = action.payload;
      localStorage.setItem('user', JSON.stringify(user));
      state.user = user;
      localStorage.setItem('token', JSON.stringify(accessToken));
      state.token = accessToken;
    },
    logout: (state) => {
      localStorage.removeItem('user');
      state.user = null;
      localStorage.removeItem('token');
      state.token = null;
    },
  },
});

export const { login, logout } = authSlice.actions;

export const auth = authSlice;

export const selectCurrentUser = (state: RootState) => state.auth.user;
export const selectCurrentToken = (state: RootState) => state.auth.token;
