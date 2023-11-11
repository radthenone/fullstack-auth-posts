/// <reference types="vite/client" />
type ImportMetaEnv = {
  readonly API_BACKEND_URL: string;
  readonly TEST_URL: string;
  readonly NODE_ENV: string;
  readonly HOST: string;
  readonly PORT: string;
  // more env variables...
};

type ImportMeta = {
  readonly env: ImportMetaEnv;
};
