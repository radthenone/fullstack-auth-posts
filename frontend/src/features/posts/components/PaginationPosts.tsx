import { ChangeEvent, useState, useEffect } from 'react';
import Pagination from '@mui/material/Pagination';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import PostCard from 'pages/Posts/PostCard.tsx';

type PaginationProps = {
  data: any[];
  start: number;
  end: number;
  count?: number;
  extra?: any[];
};

const PaginationPosts = ({ data, start, end, count, extra: tags }: PaginationProps) => {
  const [currentPage, setCurrentPage] = useState(start);
  const [dataPerPage] = useState(end);
  const lastIndex = currentPage * dataPerPage;
  const firstIndex = lastIndex - dataPerPage;
  const slicedData = data.slice(firstIndex, lastIndex);

  const handleChange = (_: ChangeEvent<unknown>, page: number) => {
    setCurrentPage(page);
  };

  useEffect(() => {
    setCurrentPage(1);
  }, [tags]);

  return (
    <>
      <Stack spacing={2}>
        <Box mx={{ minHeight: '100vh' }}>
          {slicedData.map((data) => (
            <PostCard key={data.id} postId={data.id} />
          ))}
        </Box>
        <Pagination
          count={count ?? 10}
          page={currentPage}
          onChange={handleChange}
          sx={{
            display: 'flex',
            justifyContent: 'center',
            marginBottom: '0px',
            marginTop: '20px',
          }}
        />
      </Stack>
    </>
  );
};

export default PaginationPosts;
