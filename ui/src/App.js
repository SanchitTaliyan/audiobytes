import EndOfDayImg from "assets/eod.png";
import MidImg from "assets/mid.png";
import MorningImg from "assets/morning.png";
import WeeklyImg from "assets/weekly.png";
import { compareDesc, format, isToday, isYesterday } from "date-fns";
import { BookmarkFilledIcon, CloseIcon, PlayIcon } from "icons";
import { keyBy } from "lodash-es";
import { useEffect, useState } from "react";
import EpisodeCard from "./components/EpisodeCard";
import { PauseIcon } from "./components/icons";
import { EPISODE_TYPE } from "./constants/enums";
import episodesService from "./services/episodesService";
import { useAudioPlayer, useEpisodePlayer } from "./player";

const config = {
  [EPISODE_TYPE.MORNING]: {
    title: "Morning Brief",
    color: "#6f2dbd",
    img: MorningImg,
  },
  [EPISODE_TYPE.MIDDAY]: {
    title: "MIdday Report",
    color: "#FFB834",
    img: MidImg,
  },
  [EPISODE_TYPE.EOD]: {
    title: "End of Day Recap",
    color: "#D01051",
    img: EndOfDayImg,
  },
  [EPISODE_TYPE.WEEKLY]: {
    title: "Weekly Wrap-Up",
    color: "#380B94",
    img: WeeklyImg,
  },
};

const intialFilters = {
  bookmark: false,
  morning: false,
  eod: false,
  weekly: false,
};

/**
 * @typedef {Object} Episode
 *
 * server properties
 * @property {string} id
 * @property {string} title
 * @property {string} description
 * @property {number} duration
 * @property {Date} published_at
 * @property {string} audio_link
 * @property {boolean} is_bookmark
 * @property {boolean} is_deleted
 *
 * local properties
 * @property {boolean} today
 */

/** @type {Episode[]} */
const initialEpisodesList = [];

export function App() {
  const [episodesList, setEpisodesList] = useState(initialEpisodesList);
  const [filters, setFilters] = useState(intialFilters);

  const toogleBookmark = async (episode) => {
    try {
      const updatedEpisode = await episodesService.toogleBookmark({
        episodeId: episode.id,
        bookmark: !episode.is_bookmark,
      });

      const nextEpisodesList = [...episodesList];
      const i = nextEpisodesList.indexOf(episode);
      nextEpisodesList[i] = updatedEpisode;

      setEpisodesList(nextEpisodesList);
    } catch (error) {
      console.log("Failed to update episode bookmark", error);
    }
  };

  const handleFilterClick = (filter, value) => {
    setFilters((prev) => ({ ...prev, [filter]: value }));
  };

  useEffect(() => {
    const fetchAllEpisodes = async () => {
      try {
        const episodesList = await episodesService.getAllEpisodes();
        episodesList.sort((a, b) =>
          compareDesc(a.published_at, b.published_at),
        );
        episodesList.forEach((ep) => {
          ep.today = isToday(ep.published_at);
        });
        setEpisodesList(episodesList);
      } catch (error) {
        console.log(error);
      }
    };
    fetchAllEpisodes();
  }, []);

  const episodes = episodesList.filter((episode) => {
    const { bookmark, morning, eod, weekly } = filters;
    if (bookmark && !episode.is_bookmark) return false;

    const filtersArray = [
      morning && EPISODE_TYPE.MORNING,
      eod && EPISODE_TYPE.EOD,
      weekly && EPISODE_TYPE.WEEKLY,
    ].filter((val) => !!val);

    if (!filtersArray.length) return true;

    return filtersArray.includes(episode.time_of_day);
  });

  // ignore filters for today's episodes
  const todayEpisodes = episodesList.filter((ep) => ep.today);

  return (
    <>
      <title>Today's Brief</title>

      <div className="flex flex-1 flex-col overflow-y-auto">
        <div className="flex h-9 flex-col items-start justify-start px-5 pt-2">
          <div className="flex items-center justify-start gap-1">
            <div className="text-[22px] font-bold leading-7 text-white">
              Today's Brief
            </div>
          </div>
        </div>

        <div className="no-scrollbar flex flex-shrink-0 flex-row gap-4 overflow-auto px-5 pb-[30px] pt-[10px]">
          {todayEpisodes.map((ep) => (
            <Poster key={ep.id} episode={ep} />
          ))}
        </div>

        <div className="sticky top-0 z-10 flex h-[74px] flex-col items-start justify-start bg-[#0A0A0A] px-5 py-3">
          <div className="flex flex-col items-start justify-start gap-px pb-px">
            <div className="flex items-center justify-start gap-1">
              <div className="font-['Inter'] text-[22px] font-bold leading-7 text-white">
                Catch Up on Past Briefs
              </div>
            </div>
            <div className="font-['Inter'] text-[15px] font-normal leading-tight text-[#757575]">
              {episodes.length} Episodes
            </div>
          </div>
        </div>

        <div className="no-scrollbar flex h-14 flex-shrink-0 flex-row items-center justify-start gap-2 overflow-x-auto px-5">
          <Filter
            active={filters.bookmark}
            value="bookmark"
            icon={
              <BookmarkFilledIcon color="currentColor" width={16} height={16} />
            }
            label="Bookmarks"
            onFilterClick={handleFilterClick}
          />

          <div className="h-7 border border-white/20" />

          <Filter
            active={filters.morning}
            value="morning"
            label={config.MORNING.title}
            onFilterClick={handleFilterClick}
          />
          <Filter
            active={filters.eod}
            value="eod"
            label={config.ENDOFDAY.title}
            onFilterClick={handleFilterClick}
          />
          <Filter
            active={filters.weekly}
            value="weekly"
            label={config.WEEKLY.title}
            onFilterClick={handleFilterClick}
          />
        </div>

        {episodes.map((episode) => (
          <EpisodeCard
            key={episode.id}
            episode={episode}
            toggleBookmark={() => toogleBookmark(episode)}
          />
        ))}
      </div>
    </>
  );
}

function Filter({ active, icon, label, value, onFilterClick }) {
  return (
    <div
      className={cx(
        "flex shrink-0 cursor-pointer items-center justify-center gap-2 rounded-[100px] border border-white/20 px-3 py-2",
        active ? "bg-white text-[#0A0A0A]" : "bg-[#3a3a3c] text-white",
      )}
      onClick={() => onFilterClick(value, !active)}
    >
      {icon}
      <div className="text-[13px] font-semibold leading-none">{label}</div>
      {active && <CloseIcon color="#0A0A0A" width={16} height={16} />}
    </div>
  );
}

function Poster({ episode }) {
  const { color, img } = config[episode.time_of_day];

  const { isSelected, isPlaying } = useEpisodePlayer(episode);

  return (
    <div
      style={{ "--color": color }}
      className={
        "flex h-[356px] flex-col items-start justify-start rounded-[14px] bg-[var(--color)]"
      }
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
                {isPlaying ? "Pause" : isSelected ? "Resume" : "Start"}
              </div>
              <div className="text-[11px] uppercase leading-[13px] tracking-tight text-white/50">
                ·
              </div>
              <div className="text-[11px] font-semibold uppercase leading-[13px] tracking-tight text-white/50">
                Today
              </div>
            </div>
            <div className="flex h-[72px] flex-col items-start justify-start gap-1 self-stretch">
              <div className="self-stretch text-[15px] font-semibold leading-[18px] text-white opacity-90">
                {episode.title} | {format(episode.published_at, "dd MMM yyyy")}
              </div>
              <div className="line-clamp-2 self-stretch text-[13px] font-normal leading-none text-white/60">
                Discover the fascinating world of feline sleep patterns and
                learn why your cat may be onto something with its 16-hour sleep
                schedule.
              </div>
            </div>
          </div>
          <div className="flex items-center justify-between self-stretch">
            <EpisodePlayer color={color} episode={episode} />
            <div className="flex items-center justify-start gap-3.5">
              <div className="relative h-6 w-6 overflow-hidden" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function EpisodePlayer({ episode }) {
  const seekTrackWidth = 25;

  const { color } = config[episode.time_of_day];

  const { pausePlayer, startPlayer } = useAudioPlayer();
  const { isSelected, isPlaying, progress, durationLabel } =
    useEpisodePlayer(episode);

  const seekBarWidth = progress * seekTrackWidth;

  return (
    <div
      style={{ "--color": color }}
      className="flex flex-col items-center justify-center overflow-hidden rounded-[100px] bg-white py-1.5 pl-[9px] pr-[11px] opacity-95"
      onClick={() => {
        if (isPlaying) pausePlayer();
        else startPlayer(episode);
      }}
    >
      <div className="flex items-center justify-start gap-[7px]">
        <div className="flex flex-col items-start justify-start">
          <div className="text-center text-[13px] leading-none text-[var(--color)]">
            {isPlaying ? (
              <PauseIcon color={color} width={12} height={16} />
            ) : (
              <PlayIcon color={color} width={12} height={16} />
            )}
          </div>
        </div>

        <div className="flex items-center justify-start gap-[5px]">
          {isSelected && (
            <div
              style={{ width: seekTrackWidth }}
              className="relative h-[5px] overflow-hidden rounded-[100px]"
            >
              <div
                style={{ width: seekTrackWidth }}
                className="absolute left-0 top-0 h-[5px] bg-[var(--color)] opacity-30"
              />
              <div
                style={{ width: seekBarWidth }}
                className="absolute left-0 top-0 h-[5px] w-[15px] bg-[var(--color)]"
              />
            </div>
          )}

          <div className="flex h-4 flex-col items-start justify-end pb-[0.50px]">
            <div className="flex items-start justify-end">
              <div className="text-[13px] font-semibold leading-none text-[var(--color)]">
                {durationLabel}
              </div>
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
