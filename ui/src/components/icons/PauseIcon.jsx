import React from 'react';

export const PauseIcon = ({ color = '#FFFFFF', height = 24, width = 24 }) => {
  return (
    <svg xmlns='http://www.w3.org/2000/svg' width={width} height={height} viewBox='0 0 58 57' fill='none'>
      <path
        d='M17.0469 48.8359C15.875 48.8359 14.9922 48.5391 14.3984 47.9453C13.8047 47.3516 13.5156 46.4688 13.5312 45.2969V12.8594C13.5312 11.7031 13.8281 10.8281 14.4219 10.2344C15.0156 9.64063 15.8906 9.34375 17.0469 9.34375H22.6719C23.8281 9.35938 24.7031 9.65625 25.2969 10.2344C25.8906 10.8125 26.1875 11.6875 26.1875 12.8594V45.2969C26.1875 46.4688 25.8906 47.3516 25.2969 47.9453C24.7031 48.5391 23.8281 48.8359 22.6719 48.8359H17.0469ZM35.3281 48.8359C34.1406 48.8359 33.25 48.5391 32.6562 47.9453C32.0781 47.3516 31.7891 46.4688 31.7891 45.2969V12.8594C31.7891 11.7031 32.0859 10.8281 32.6797 10.2344C33.2734 9.64063 34.1562 9.34375 35.3281 9.34375H40.9297C42.1016 9.34375 42.9766 9.64063 43.5547 10.2344C44.1484 10.8125 44.4453 11.6875 44.4453 12.8594V45.2969C44.4453 46.4688 44.1484 47.3516 43.5547 47.9453C42.9766 48.5391 42.1016 48.8359 40.9297 48.8359H35.3281Z'
        fill={color}
      />
    </svg>
  );
};
