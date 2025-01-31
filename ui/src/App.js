import { keyBy } from 'lodash-es';
import { useEffect, useState } from 'react';
import EndOfDayImg from "assets/eod.png";
import MorningImg from "assets/morning.png";
import WeeklyImg from "assets/weekly.png";
import EpisodeCard from './components/EpisodeCard';
import { BookmarkFilledIcon, CloseIcon, PlayIcon } from "icons";
import episodesService from './services/episodesService';

const config = {
  morning: {
    title: "Morning Brief",
    color: "#6f2dbd",
    img: MorningImg,
  },
  endOfDay: {
    title: "End of Day Recap",
    color: "#D01051",
    img: EndOfDayImg,
  },
  weekly: {
    title: "Weekly Wrap-Up",
    color: "#380B94",
    img: WeeklyImg,
  },
};

export function App() {
  const [episodesList, setEpisodesList] = useState({});

  const toogleBookmark = async (id, bookmark) => {
    try {
      const updatedEpisode = await episodesService.toogleBookmark({ episodeId: id, bookmark });
      setEpisodesList((prev) => ({ ...prev, [id]: updatedEpisode }));
    } catch (error) {
      console.log('Failed to update episode bookmark', error);
    }
  };

  useEffect(() => {
    const fetchAllEpisodes = async () => {
      try {
        const episodesList = await episodesService.getAllEpisodes();
        console.log(episodesList.body);
        setEpisodesList(keyBy(episodesList, 'id'));
      } catch (error) {
        console.log(error);
      }
    };
    fetchAllEpisodes();
  }, []);

  const episodes = Object.values(episodesList);

  return (
    <>
      <title>Today's Brief</title>

      <div className="flex-1 bg-[#0A0A0A] overflow-y-auto">
        <div className="flex h-9 flex-col items-start justify-start px-5 pt-2">
          <div className="flex items-center justify-start gap-1">
            <div className="text-[22px] font-bold leading-7 text-white">
              Today's Brief
            </div>
          </div>
        </div>

        <div className="no-scrollbar flex flex-row gap-4 overflow-auto px-5 pb-[30px] pt-[10px]">
          {Object.entries(config).map(([k, v]) => (
            <Poster key={k} color={v.color} img={v.img} />
          ))}
        </div>

        <div className="inline-flex h-[74px] flex-col items-start justify-start px-5 py-3">
          <div className="flex flex-col items-start justify-start gap-px pb-px">
            <div className="inline-flex items-center justify-start gap-1">
              <div className="font-['Inter'] text-[22px] font-bold leading-7 text-white">
                Catch Up on Past Briefs
              </div>
            </div>
            <div className="font-['Inter'] text-[15px] font-normal leading-tight text-[#757575]">
              {episodes.length} Episodes
            </div>
          </div>
        </div>
        <div className="no-scrollbar flex h-14 flex-row items-center justify-start gap-2 overflow-auto px-5 py-3">
          <Filter
            active
            icon={
              <BookmarkFilledIcon color="currentColor" width={16} height={16} />
            }
            label="Bookmarks"
          />

          <div className="h-7 border border-white/20" />

          <Filter active label={config.morning.title} />
          <Filter label={config.endOfDay.title} />
          <Filter label={config.weekly.title} />
        </div>
        <div>
          {episodes.map((episode) => 
            <EpisodeCard key={episode.id} episode={episode} toggleBookmark={toogleBookmark} />
          )}
        </div>
      </div>
    </>
  );
}

function Filter({ active, icon, label }) {
  return (
    <div
      className={cx(
        "flex shrink-0 items-center justify-center gap-2 rounded-[100px] border border-white/20 px-3 py-2",
        active ? "bg-white text-[#0A0A0A]" : "bg-[#3a3a3c] text-white",
      )}
    >
      {icon}
      <div className="text-[13px] font-semibold leading-none">{label}</div>
      {active && <CloseIcon color="#0A0A0A" width={16} height={16} />}
    </div>
  );
}

function Poster({ color, img }) {
  return (
    <div
      style={{ "--color": color }}
      className="flex h-[356px] flex-col items-start justify-start rounded-[14px] bg-[var(--color)]"
    >
      <div className="flex h-[356px] w-[267px] flex-col items-start justify-start overflow-hidden bg-black/10 shadow-[0px_6px_12px_0px_rgba(0,0,0,0.10)]">
        <div className="flex h-[210px] flex-col items-center justify-center self-stretch pb-[18px] pt-7">
          <img
            className="relative h-[164px] w-[164px] rounded-[5px] shadow-[0px_0px_40px_0px_rgba(0,0,0,0.10)]"
            src={img}
          />
        </div>
        <div className="flex shrink grow basis-0 flex-col items-start justify-between self-stretch px-4 pb-4">
          <div className="flex h-[89px] flex-col items-start justify-start gap-1 self-stretch">
            <div className="flex items-start justify-start gap-[3.50px]">
              <div className="text-[11px] font-semibold uppercase leading-[13px] tracking-tight text-white/50">
                Resume
              </div>
              <div className="text-[11px] uppercase leading-[13px] tracking-tight text-[#c2c2c2]">
                ·
              </div>
              <div className="text-[11px] font-semibold uppercase leading-[13px] tracking-tight text-white/50">
                Today
              </div>
            </div>
            <div className="flex h-[72px] flex-col items-start justify-start gap-1 self-stretch">
              <div className="self-stretch text-[15px] font-semibold leading-[18px] text-white opacity-90">
                Start Your Day: Morning Insights - 31 Jan 2025
              </div>
              <div className="line-clamp-2 self-stretch text-[13px] font-normal leading-none text-white/60">
                Discover the fascinating world of feline sleep patterns and
                learn why your cat may be onto something with its 16-hour sleep
                schedule.
              </div>
            </div>
          </div>
          <div className="flex items-center justify-between self-stretch">
            <div className="flex flex-col items-center justify-center overflow-hidden rounded-[100px] bg-white py-1.5 pl-[9px] pr-[11px] opacity-95">
              <div className="flex items-center justify-start gap-[7px]">
                <div className="flex flex-col items-start justify-start">
                  <div className="text-center text-[13px] leading-none text-[var(--color)]">
                    <PlayIcon color={color} width={12} height={16} />
                  </div>
                </div>
                <div className="flex items-center justify-start gap-[5px]">
                  <div className="relative h-[5px] w-[25px] overflow-hidden rounded-[100px]">
                    <div className="absolute left-0 top-0 h-[5px] w-[25px] bg-[var(--color)] opacity-30" />
                    <div className="absolute left-0 top-0 h-[5px] w-[15px] bg-[var(--color)]" />
                  </div>
                  <div className="flex h-4 flex-col items-start justify-end pb-[0.50px]">
                    <div className="flex items-start justify-end">
                      <div className="text-[13px] font-semibold leading-none text-[var(--color)]">
                        11
                      </div>
                      <div className="text-[13px] font-semibold leading-none text-[var(--color)]">
                        m
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="flex items-center justify-start gap-3.5">
              <div className="relative h-6 w-6 overflow-hidden" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function cx(...args) {
  return args.filter(Boolean).join(" ");
}
