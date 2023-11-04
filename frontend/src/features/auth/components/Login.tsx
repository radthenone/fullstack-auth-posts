import {ChangeEvent, useState} from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setCredentials } from './authSlice';

import { useLoginMutation } from '../../app/services/auth';
import type { LoginRequest } from '../../app/services/auth';

function PasswordInput({
  name,
  onChange,
}: {
  name: string;
  onChange: (event: ChangeEvent<HTMLInputElement>) => void;
}) {
  const [show, setShow] = useState(false);
  const handleClick = () => setShow(!show);

  return (
  );
}

export const Login = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [formState, setFormState] = useState<LoginRequest>({
    username: '',
    password: '',
  });

  const [login, { isLoading }] = useLoginMutation();

  const handleChange = ({ target: { name, value } }: React.ChangeEvent<HTMLInputElement>) =>
    setFormState((prev) => ({ ...prev, [name]: value }));

  return (

  );
};

export default Login;
