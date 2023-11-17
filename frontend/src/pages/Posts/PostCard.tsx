import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import FormatDate from 'components/FormatDate';
import MaxTextCard from 'components/MaxTextCard';
import { Box } from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from 'app/store.tsx';

const PostCard = ({ postId }: { postId?: number }) => {
  const post = useSelector((state: RootState) =>
    state.posts.data.find((postValue) => postValue.id === postId),
  );
  const { date, time } = FormatDate(post?.date);

  if (!postId) {
    return <div>Post IP doesn't exist</div>;
  }
  if (!post) {
    return <div>Post doesn't exist</div>;
  }

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
              <MaxTextCard text={post?.content} />
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

export default PostCard;
