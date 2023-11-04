import { createSlice } from '@reduxjs/toolkit';
import type { UserType } from 'types/userTypes';
import type { RootState } from 'app/store';

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
      state.user = user;
      state.token = accessToken;
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
    },
  },
});

export const { login, logout } = authSlice.actions;

export default authSlice.reducer;

export const selectCurrentUser = (state: RootState) => state.auth.user;
export const selectCurrentToken = (state: RootState) => state.auth.token;
