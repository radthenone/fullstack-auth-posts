import { Button, FormLabel, TextField } from '@mui/material';
import { useAddTagMutation } from 'app/tags/hooks';
import { FormEvent, useState } from 'react';

export const CreateTagForm = () => {
  const [name, setName] = useState<string>('');
  const { addTag, isError, isCreated, error } = useAddTagMutation();
  const tag: { name: string } = { name };

  const handleAddTag = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    addTag(tag);
    setName('');
  };

  return (
    <>
      <form onSubmit={handleAddTag}>
        <FormLabel htmlFor="name">Post name</FormLabel>
        {isError && name === '' ? <p>Enter post name</p> : <p>{name}</p>}
        {isError && <p>{error}</p>}
        <TextField
          id="name"
          name="name"
          type="password"
          placeholder="Enter tag name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Button type="submit">Add Post</Button>
      </form>
      {isCreated && <h1>Created</h1>}
    </>
  );
};
