type LoginRequestType = {
  email: string;
  password: string;
};

type LoginResponseType = {
  accessToken: string;
  refreshToken: string;
};

type RegisterMailRequestType = {
  email: string;
  password: string;
  birthday: string;
  avatar: string;
};

type RegisterRequestType = {
  email: string;
  password: string;
  birthday: string;
  avatar: string;
};

export type { LoginRequestType, LoginResponseType, RegisterRequestType, RegisterMailRequestType };
