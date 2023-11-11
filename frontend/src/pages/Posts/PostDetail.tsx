import { useGetPostQuery } from 'app/services/old';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import FormatDate from 'components/FormatDate';
import { Box } from '@mui/material';

const PostDetail = ({ postId }: { postId?: number }) => {
  const { data: post, isLoading, isError, error } = useGetPostQuery(Number(postId));

  if (!postId) {
    return <div>Brak postId w adresie URL</div>;
  }

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error: {(error as Error).message}</div>;
  }

  const { date, time } = FormatDate(post?.date);

  return (
    <>
      <Box sx={{ p: '5px', m: '5px' }}>
        <Card>
          <CardMedia sx={{ height: 240 }} image={post?.image} title={post?.title} />
          <CardContent>
            <Typography gutterBottom variant="h5" component="div">
              {post?.title}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {post?.content}
            </Typography>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ display: 'flex', justifyContent: 'flex-end' }}
            >
              {date} {time}
            </Typography>
          </CardContent>
          <CardActions sx={{ justifyContent: 'space-between' }}>
            <Button size="small" href={post?.link}>
              Learn More
            </Button>
          </CardActions>
        </Card>
      </Box>
    </>
  );
};

export default PostDetail;
