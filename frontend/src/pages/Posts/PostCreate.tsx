import { useAddPost } from 'app/posts/hooks';
import { ChangeEvent, FormEvent, useState } from 'react';
import { PostType, TagType, PostTypeWithoutId } from 'types';
import { TextField, Select, Input, Box, Chip, Container, Grid, Typography } from '@mui/material';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import { useGetTagsQuery } from 'app/tags/hooks';
import { DateTimeField } from '@mui/x-date-pickers/DateTimeField';
import dayjs from 'dayjs';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';

const todayDate = new Date();
const defaultValue: dayjs.Dayjs = dayjs();

export const PostCreate = () => {
  const { isCreated, setPost, error, isError } = useAddPost();
  const [title, setTitle] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [content, setContent] = useState('');
  const [author, setAuthor] = useState('');
  const [dateData, setDate] = useState<Date>(todayDate);
  const [link, setLink] = useState('');
  const [tagData, setTagData] = useState<TagType[]>([]);
  const tagsQuery = useGetTagsQuery();

  const post: PostTypeWithoutId = {
    title,
    image: image?.name ?? '',
    content,
    author,
    date: dateData.toString(),
    link,
    tags: tagData,
  };

  const addPost = (post: PostType) => {
    setPost(post);
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    addPost(post as PostType);
  };

  const handleDateChange = (newDate: Date | null) => {
    const dateAsDayjs = dayjs(newDate);
    setDate(dateAsDayjs.toDate());
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      setImage(files[0]);
    }
  };

  const handleChange = (
    event: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>,
  ) => {
    const { name, value } = event.target;
    switch (name) {
      case 'title':
        setTitle(value);
        break;
      case 'content':
        setContent(value);
        break;
      case 'author':
        setAuthor(value);
        break;
      case 'link':
        setLink(value);
        break;
      default:
        break;
    }
  };

  return (
    <Container sx={{ m: 1, display: 'flex', alignItems: 'center', flexDirection: 'column' }}>
      <Box sx={{ width: '100%', border: '1px solid black', p: 3 }}>
        <Typography variant="h4" gutterBottom>
          PostCreate
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Post title"
                id="title"
                name="title"
                placeholder="Enter post title"
                onChange={handleChange}
                required
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Input
                fullWidth
                id="image"
                name="image"
                type="file"
                onChange={handleFileChange}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Post content"
                id="content"
                name="content"
                placeholder="Enter post content"
                onChange={handleChange}
                multiline
                rows={4}
                required
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Post author"
                id="author"
                name="author"
                placeholder="Enter post author"
                onChange={handleChange}
                required
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DateTimeField
                  label="Post date"
                  name="date"
                  onChange={handleDateChange}
                  required
                  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                  // @ts-ignore
                  defaultValue={defaultValue}
                />
              </LocalizationProvider>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Post link"
                id="link"
                name="link"
                placeholder="Enter post link"
                onChange={handleChange}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <Select
                fullWidth
                required
                multiple
                label="Post tags"
                id="tag"
                name="tag"
                value={tagData.map((tag) => tag.name)}
                onChange={(event) => {
                  const selectedTags = tagsQuery.data.filter((tag) =>
                    (event.target.value as string[]).includes(tag.name),
                  );
                  setTagData(selectedTags);
                }}
                renderValue={(selected: string[]) => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap' }}>
                    {selected.map((value) => (
                      <Chip
                        key={value}
                        label={value}
                        sx={{
                          m: 0.5,
                          backgroundColor: '#1976D2',
                          color: 'white',
                          borderRadius: '4px',
                          borderStyle: 'initial',
                          borderWidth: '0',
                          boxShadow:
                            'rgba(0, 0, 0, 0.2) 0 3px 1px -2px, rgba(0, 0, 0, 0.14) 0 2px 2px 0, rgba(0, 0, 0, 0.12) 0 1px 5px 0',
                          boxSizing: 'content-box',
                        }}
                      />
                    ))}
                  </Box>
                )}
              >
                {tagsQuery.data.map((tagValue: TagType) => (
                  <MenuItem key={tagValue.id} value={tagValue.name}>
                    {tagValue.name}
                  </MenuItem>
                ))}
              </Select>
            </Grid>
          </Grid>
          <Button type="submit" variant="contained" sx={{ mt: 2 }}>
            Add Post
          </Button>
        </form>
        <Box sx={{ mt: 2 }}>
          {isCreated && !isError ? (
            <Typography variant="body1">Post created</Typography>
          ) : (
            <Typography variant="body1">{error}</Typography>
          )}
        </Box>
      </Box>
    </Container>
  );
};
