const episodesService = {
  getAllEpisodes: async () => {
    const response = await fetch('http://51.21.128.134:4000/episodes/', {
      method: 'GET',
    });
    return response.json();
  },
  toogleBookmark: async ({ episodeId, bookmark }) => {
    const response = await fetch(`http://51.21.128.134:4000/episodes/${episodeId}`, {
      method: 'PUT',
      headers: {
        accept: 'application/json',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6,zh-CN;q=0.5,zh;q=0.4',
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        id: episodeId,
        is_bookmark: bookmark,
      }),
    });
    return response.json();
  },
};

export default episodesService;
