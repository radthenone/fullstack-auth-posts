import { SyntheticEvent } from 'react';
import { Tabs, Tab, Box } from '@mui/material';
import { TagType } from '@/types';

type TabsProps = {
  tags: TagType[] | undefined;
  value: number;
  handleChange: (event: SyntheticEvent, newValue: number) => void;
};

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

const TabsScroll = ({ tags, value, handleChange }: TabsProps) => {
  return (
    <Box sx={{ width: '100%' }}>
      <Box
        sx={{
          borderBottom: 1,
          borderColor: 'divider',
          '@media (maxWidth: 1200px)': {
            display: 'flex',
          },
        }}
      >
        <Tabs
          value={value}
          onChange={handleChange}
          aria-label="basic tabs example"
          sx={{
            m: 1,
            '@media (maxWidth: 1200px)': {
              display: 'flex',
            },
          }}
          scrollButtons="auto"
          variant="scrollable"
        >
          {tags?.map((tag, index) => <Tab key={tag.id} label={tag.name} {...a11yProps(index)} />)}
        </Tabs>
      </Box>
    </Box>
  );
};

export default TabsScroll;
