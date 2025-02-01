import { getDefaultStore, atom, useAtom } from "jotai";
import { useMemo } from "react";

const store = getDefaultStore();
/**
 * @typedef {Object} Player
 * @property {Episode} episode
 * @property {number} duration
 * @property {number} currentTime
 * @property {boolean} paused
 */
/** @type {Player|undefined} */
let initialPlayer;

const playerAtom = atom(initialPlayer);

const audioCtx = new Audio();

audioCtx.ontimeupdate = () => {
  const player = store.get(playerAtom);
  if (!player) return;
  const currentTime = Math.round(audioCtx.currentTime);
  store.set(playerAtom, { ...player, currentTime });
};

audioCtx.onpause = () => {
  const player = store.get(playerAtom);
  if (!player) return;
  store.set(playerAtom, { ...player, paused: true });
};

audioCtx.onplay = () => {
  const player = store.get(playerAtom);
  if (!player) return;
  store.set(playerAtom, { ...player, paused: false });
};

audioCtx.ondurationchange = () => {
  const player = store.get(playerAtom);
  if (!player) return;
  const duration = Math.floor(audioCtx.duration);
  store.set(playerAtom, { ...player, duration });
};

audioCtx.onended = () => {
  const player = store.get(playerAtom);
  if (!player) return;
  store.set(playerAtom, undefined);
};

export function useAudioPlayer() {
  const [player, setPlayer] = useAtom(playerAtom);

  const startPlayer = (episode) => {
    if (!player || player.episode !== episode) {
      setPlayer({ episode, currentTime: 0 });
      audioCtx.src = episode.audio_link;
    }
    audioCtx.play();
  };

  const pausePlayer = () => {
    audioCtx.pause();
  };

  const seekAudio = (seconds) => {
    audioCtx.currentTime = Math.max(0, Math.min(seconds, audioCtx.duration));
  };

  return { player, startPlayer, pausePlayer, seekAudio };
}

export function useEpisodePlayer(episode) {
  const episdeDuration = episode.duration;

  const { player } = useAudioPlayer();

  const { duration, ...foo } = useMemo(() => {
    if (!player)
      return {
        isSelected: false,
        isPlaying: false,
        duration: episdeDuration,
        progress: 0,
      };

    const isSelected = player.episode === episode;
    const isPlaying = isSelected && !player.paused;

    const duration = isSelected ? player.duration || 0 : episdeDuration;

    const progress = player.currentTime / duration;
    const currentTime = player.currentTime;
    const remainingTime = episdeDuration - currentTime;

    return {
      isSelected,
      isPlaying,
      duration,
      progress,
      currentTime,
      remainingTime,
    };
  }, [player]);

  const durationLabel =
    duration < 60 ? `${duration} s` : `${Math.floor(duration / 60)} m`;

  return {
    ...foo,
    durationLabel,
  };
}
