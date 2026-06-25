import React from 'react';
import {
  AbsoluteFill,
  Easing,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import sequence from '../projects/magic-delivery/shots/state_machine_wukong_test.json';

type Shot = (typeof sequence.shots)[number];
type TrackItem = {
  time: number;
  state: string;
  x: number;
  y: number;
  scale: number;
};

type CharacterKind = 'wukong' | 'monk' | 'demon';

export const STATE_MACHINE_FPS = sequence.fps;
export const STATE_MACHINE_TOTAL_FRAMES = sequence.shots.reduce(
  (sum, shot) => sum + shot.duration * STATE_MACHINE_FPS,
  0,
);

const WIDTH = sequence.format.width;
const HEIGHT = sequence.format.height;
const FREE_LIBRARY = '免费素材库';

const bgByName: Record<string, string> = {
  stage: `${FREE_LIBRARY}/背景/旧学校.png`,
  factory: `${FREE_LIBRARY}/背景/旧工厂.png`,
  cinema: `${FREE_LIBRARY}/背景/旧电影院.png`,
};

const characterAssets: Record<CharacterKind, Partial<Record<string, string>> & {default: string}> = {
  wukong: {
    default: `${FREE_LIBRARY}/处理后/人物/橙衣男/橙衣男-抱臂.png`,
    walk: `${FREE_LIBRARY}/处理后/人物/橙衣男/橙衣男-行走.png`,
    point: `${FREE_LIBRARY}/处理后/人物/橙衣男/橙衣男-指向.png`,
    attack: `${FREE_LIBRARY}/处理后/人物/橙衣男/橙衣男-指向.png`,
  },
  monk: {
    default: `${FREE_LIBRARY}/处理后/人物/黑西装-站姿.png`,
  },
  demon: {
    default: `${FREE_LIBRARY}/处理后/人物/潮男-站姿.png`,
  },
};

const fxByName: Record<string, {folder: string; frames: number; wide?: boolean}> = {
  speed_smoke: {folder: `${FREE_LIBRARY}/处理后/特效帧/一溜烟`, frames: 24, wide: true},
  dust: {folder: `${FREE_LIBRARY}/处理后/特效帧/大灰尘`, frames: 24, wide: true},
  hit_star: {folder: `${FREE_LIBRARY}/处理后/特效帧/撞击星`, frames: 6},
  sweat: {folder: `${FREE_LIBRARY}/处理后/特效帧/汗水`, frames: 24},
  smoke_ring: {folder: `${FREE_LIBRARY}/处理后/特效帧/烟阵圈`, frames: 24},
};

const stateStyle: Record<
  string,
  {
    label: string;
    tint: string;
    lean: number;
    mouth?: boolean;
    burst?: string;
    shake?: number;
    squash?: number;
  }
> = {
  idle: {label: '待机', tint: '#ffe4a3', lean: 0},
  talk: {label: '说话', tint: '#fff2c8', lean: -1, mouth: true},
  walk: {label: '行走', tint: '#d9f2ff', lean: -4},
  point: {label: '指认', tint: '#ffd15a', lean: -8, burst: '看这里'},
  shock: {label: '震惊', tint: '#fff', lean: 7, burst: '？！', shake: 8, squash: 1.06},
  recoil: {label: '后退', tint: '#e5ddff', lean: 10, burst: '退！', shake: 4},
  attack: {label: '出击', tint: '#ff816b', lean: -14, burst: '打！', shake: 6, squash: 1.10},
  think: {label: '怀疑', tint: '#c9f0d2', lean: 2, burst: '不对'},
  disguise: {label: '伪装', tint: '#e7eef7', lean: 0},
  reveal: {label: '现形', tint: '#f25f5c', lean: -2, burst: '露馅'},
};

const timed = (
  frame: number,
  input: number[],
  output: number[],
  easing = Easing.bezier(0.22, 1, 0.36, 1),
) =>
  interpolate(frame, input, output, {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing,
  });

const pickTrack = (track: TrackItem[], time: number) => {
  let current = track[0];
  let next = track[track.length - 1];
  for (let i = 0; i < track.length; i++) {
    if (track[i].time <= time) {
      current = track[i];
      next = track[i + 1] ?? track[i];
    }
  }
  const span = Math.max(0.001, next.time - current.time);
  const t = Math.min(1, Math.max(0, (time - current.time) / span));
  const smooth = t * t * (3 - 2 * t);
  return {
    state: current.state,
    x: current.x + (next.x - current.x) * smooth,
    y: current.y + (next.y - current.y) * smooth,
    scale: current.scale + (next.scale - current.scale) * smooth,
  };
};

const cameraAt = (shot: Shot, time: number) => {
  const keys = shot.camera.keyframes;
  let current = keys[0];
  let next = keys[keys.length - 1];
  for (let i = 0; i < keys.length; i++) {
    if (keys[i].time <= time) {
      current = keys[i];
      next = keys[i + 1] ?? keys[i];
    }
  }
  const span = Math.max(0.001, next.time - current.time);
  const t = Math.min(1, Math.max(0, (time - current.time) / span));
  const smooth = t * t * (3 - 2 * t);
  return {
    x: current.x + (next.x - current.x) * smooth,
    y: current.y + (next.y - current.y) * smooth,
    scale: current.scale + (next.scale - current.scale) * smooth,
  };
};

const Character: React.FC<{kind: CharacterKind; track?: TrackItem[]; frame: number}> = ({
  kind,
  track,
  frame,
}) => {
  if (!track?.length) return null;
  const active = pickTrack(track, frame / STATE_MACHINE_FPS);
  const spec = stateStyle[active.state] ?? stateStyle.idle;
  const walkBob = active.state === 'walk' ? Math.sin(frame * 0.72) * 10 : Math.sin(frame * 0.14) * 2;
  const shakeX = spec.shake ? Math.sin(frame * 2.8) * spec.shake : 0;
  const pop = spec.squash ? timed(frame % 16, [0, 5, 16], [1, spec.squash, 1]) : 1;
  const flip = kind === 'monk' ? -1 : 1;
  const asset = characterAssets[kind][active.state] ?? characterAssets[kind].default;
  const width = kind === 'demon' ? 300 : 330;
  const height = kind === 'wukong' ? 680 : 610;
  const characterName = kind === 'wukong' ? '香奈' : kind === 'monk' ? '里奈' : '主持人';

  return (
    <div
      style={{
        position: 'absolute',
        left: active.x * WIDTH - width / 2 + shakeX,
        top: active.y * HEIGHT - height + walkBob,
        width,
        height,
        transform: `scale(${active.scale * pop}) rotate(${spec.lean}deg)`,
        transformOrigin: '50% 94%',
        filter: 'drop-shadow(0 24px 20px rgba(0,0,0,.42))',
      }}
    >
      <Img
        src={staticFile(asset)}
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          transform: `scaleX(${flip})`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: 62,
          bottom: 76,
          padding: '8px 14px',
          background: spec.tint,
          border: '4px solid #151515',
          borderRadius: 10,
          fontFamily: 'Microsoft YaHei, sans-serif',
          fontSize: 24,
          fontWeight: 900,
        }}
      >
        {`${characterName}·${spec.label}`}
      </div>
      {spec.burst ? (
        <div
          style={{
            position: 'absolute',
            right: -24,
            top: -16,
            padding: '10px 16px',
            background: '#fff1d6',
            border: '4px solid #151515',
            borderRadius: 16,
            fontFamily: 'Microsoft YaHei, sans-serif',
            fontSize: 32,
            fontWeight: 900,
            transform: 'rotate(-8deg)',
          }}
        >
          {spec.burst}
        </div>
      ) : null}
    </div>
  );
};

const Vfx: React.FC<{shot: Shot; frame: number}> = ({shot, frame}) => {
  const meta = fxByName[shot.vfx];
  if (!meta) return null;
  const index = Math.floor(frame / 2) % meta.frames;
  return (
    <Img
      src={staticFile(`${meta.folder}/frame-${String(index).padStart(3, '0')}.png`)}
      style={{
        position: 'absolute',
        left: meta.wide ? 300 : 1040,
        bottom: meta.wide ? 125 : 370,
        width: meta.wide ? 600 : 320,
        opacity: shot.vfx === 'sweat' ? 0.72 : 0.88,
        mixBlendMode: 'screen',
      }}
    />
  );
};

const UIAndSubtitle: React.FC<{shot: Shot; frame: number}> = ({shot, frame}) => {
  const pop = timed(frame, [0, 8], [0.92, 1], Easing.out(Easing.back(1.35)));
  const opacity = timed(frame, [0, 6, shot.duration * STATE_MACHINE_FPS - 8, shot.duration * STATE_MACHINE_FPS], [0, 1, 1, 0]);
  return (
    <>
      <div
        style={{
          position: 'absolute',
          right: 86,
          top: 76,
          width: 470,
          minHeight: 128,
          padding: '22px 26px',
          background: 'rgba(255,244,219,.94)',
          border: '5px solid #241510',
          color: '#241510',
          fontFamily: 'Microsoft YaHei, sans-serif',
          boxShadow: '0 14px 26px rgba(0,0,0,.28)',
          transform: `scale(${pop})`,
        }}
      >
        <div style={{fontSize: 24, color: '#d12335', fontWeight: 900}}>状态提示</div>
        <div style={{fontSize: 34, lineHeight: 1.25, marginTop: 8, fontWeight: 900}}>{shot.ui}</div>
      </div>
      <div
        style={{
          position: 'absolute',
          left: 170,
          right: 170,
          bottom: 70,
          minHeight: 118,
          padding: '24px 32px',
          background: 'rgba(8,9,12,.88)',
          color: '#fff7e8',
          fontFamily: 'Microsoft YaHei, sans-serif',
          fontSize: 40,
          lineHeight: 1.35,
          borderLeft: '8px solid #ff8a2a',
          boxShadow: '0 18px 32px rgba(0,0,0,.38)',
          opacity,
        }}
      >
        <span style={{color: '#ffd36a', fontWeight: 900}}>{shot.speaker}: </span>
        {shot.dialogue}
      </div>
      <Vfx shot={shot} frame={frame} />
    </>
  );
};

const Scene: React.FC<{shot: Shot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const time = frame / STATE_MACHINE_FPS;
  const camera = cameraAt(shot, time);
  const bg = bgByName[shot.background] ?? bgByName.stage;
  const tracks = shot.state_timeline as Record<string, TrackItem[] | undefined>;

  return (
    <AbsoluteFill style={{background: '#101015', overflow: 'hidden'}}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          transform: `translate(${camera.x}px, ${camera.y}px) scale(${camera.scale})`,
          transformOrigin: '50% 50%',
        }}
      >
        <Img
          src={staticFile(bg)}
          style={{
            position: 'absolute',
            inset: -70,
            width: 'calc(100% + 140px)',
            height: 'calc(100% + 140px)',
            objectFit: 'cover',
            filter: 'brightness(.70) saturate(.88)',
          }}
        />
        <AbsoluteFill style={{background: 'linear-gradient(to bottom, rgba(0,0,0,.08), rgba(0,0,0,.12) 58%, rgba(0,0,0,.48))'}} />
        <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 145, background: 'rgba(12,13,16,.32)'}} />
        <Character kind="demon" track={tracks.demon} frame={frame} />
        <Character kind="monk" track={tracks.monk} frame={frame} />
        <Character kind="wukong" track={tracks.wukong} frame={frame} />
      </div>
      <UIAndSubtitle shot={shot} frame={frame} />
    </AbsoluteFill>
  );
};

export const StateMachineWukongTest: React.FC = () => {
  let cursor = 0;
  return (
    <AbsoluteFill style={{background: '#101015'}}>
      {sequence.shots.map((shot) => {
        const from = cursor;
        const durationInFrames = shot.duration * STATE_MACHINE_FPS;
        cursor += durationInFrames;
        return (
          <Sequence key={shot.shot_id} from={from} durationInFrames={durationInFrames}>
            <Scene shot={shot} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
