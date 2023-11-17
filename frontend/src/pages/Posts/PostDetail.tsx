import { useGetPostQuery } from 'app/posts/hooks';
import FormatDate from 'components/FormatDate.tsx';
import { Card, CardMedia, CardContent, Box } from '@mui/material';
import Button from '@mui/material/Button';

const PostDetail = () => {
  const post = useGetPostQuery();
  const { date, time } = FormatDate(post?.date);

  return (
    <>
      <Box
        sx={{
          p: '5px',
          m: '5px',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Card sx={{ padding: '10px' }}>
          <CardMedia
            sx={{
              height: 500,
              width: 500,
              margin: 'auto',
            }}
            image={post?.image}
            title={post?.title}
          />
          <CardContent
            sx={{
              justifyContent: 'center',
              alignItems: 'center',
              display: 'flex',
              flexDirection: 'column',
              padding: '10px',
            }}
          >
            <h1>{post?.title}</h1>
          </CardContent>
          <CardContent
            sx={{
              padding: '10px',
              justifyContent: 'space-between',
              alignItems: 'flex-end',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <p>
              {date} {time}
            </p>
          </CardContent>
          <CardContent sx={{ padding: '10px' }}>
            <p>{post?.content}</p>
          </CardContent>
          <Box
            sx={{
              justifyContent: 'flex-end',
              display: 'flex',
            }}
          >
            <Button
              sx={{
                padding: '10px',
              }}
              variant="outlined"
              href="/"
            >
              Go back
            </Button>
          </Box>
        </Card>
      </Box>
    </>
  );
};

export default PostDetail;
