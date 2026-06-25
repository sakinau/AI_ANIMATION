import React from 'react';
import {
  AbsoluteFill,
  Easing,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import sequence from '../projects/magic-delivery/shots/an_ae_60s_test.json';

type Shot = (typeof sequence.shots)[number];

export const AN_AE_FPS = sequence.fps;
export const AN_AE_TOTAL_FRAMES = sequence.shots.reduce(
  (sum, shot) => sum + shot.duration * AN_AE_FPS,
  0,
);

const ease = (
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

const bodyByPose: Record<string, string> = {
  idle: '免费素材库/处理后/人物/橙衣男/橙衣男-抱臂.png',
  walk: '免费素材库/处理后/人物/橙衣男/橙衣男-行走.png',
  point: '免费素材库/处理后/人物/橙衣男/橙衣男-指向.png',
  sit: '免费素材库/处理后/人物/橙衣男/橙衣男-坐姿.png',
};

const faceByExpression: Record<string, string> = {
  neutral: '免费素材库/处理后/表情_标准化/表情-平静.png',
  doubtful: '免费素材库/处理后/表情_标准化/表情-怀疑.png',
  shocked: '免费素材库/处理后/表情_标准化/表情-惊讶.png',
  angry: '免费素材库/处理后/表情_标准化/表情-愤怒.png',
  furious: '免费素材库/处理后/表情_标准化/表情-暴怒.png',
  smirk: '免费素材库/处理后/表情_标准化/表情-邪笑.png',
  happy: '免费素材库/处理后/表情_标准化/表情-狂喜.png',
};

const faceAnchors: Record<string, {left: number; top: number; width: number; height: number}> = {
  idle: {left: 121, top: 116, width: 142, height: 104},
  walk: {left: 123, top: 132, width: 142, height: 104},
  point: {left: 126, top: 116, width: 142, height: 104},
  sit: {left: 124, top: 108, width: 142, height: 104},
};

const backgroundByName: Record<string, string> = {
  旧工厂: '免费素材库/背景/旧工厂.png',
  旧学校: '免费素材库/背景/旧学校.png',
  旧电影院: '免费素材库/背景/旧电影院.png',
};

const fxByName: Record<string, {folder: string; frames: number}> = {
  一溜烟: {folder: '免费素材库/处理后/特效帧/一溜烟', frames: 24},
  大灰尘: {folder: '免费素材库/处理后/特效帧/大灰尘', frames: 24},
  撞击星: {folder: '免费素材库/处理后/特效帧/撞击星', frames: 6},
  汗水: {folder: '免费素材库/处理后/特效帧/汗水', frames: 24},
  烟阵圈: {folder: '免费素材库/处理后/特效帧/烟阵圈', frames: 24},
};

const cameraTransform = (shot: Shot, frame: number, total: number) => {
  const t = ease(frame, [0, total], [0, 1], Easing.inOut(Easing.ease));
  const beat = frame < total * 0.52 ? 0 : ease(frame, [total * 0.52, total * 0.62], [0, 1], Easing.out(Easing.ease));
  const intensity = Math.min(Math.max(shot.camera.motion_intensity, 0), 0.75);
  const px = 170 * intensity;
  const scaleStep = 0.18 * intensity;
  switch (shot.camera.preset) {
    case 'establishing_pan':
      return {x: -px + px * 2 * t - beat * 45, y: -beat * 12, scale: 1.02 + beat * 0.06};
    case 'push_in':
      return {x: -beat * 52, y: -20 * intensity * t, scale: 1 + scaleStep * t + beat * 0.07};
    case 'pull_back':
      return {x: beat * 38, y: 10 * intensity * t, scale: 1 + scaleStep * (1 - t)};
    case 'truck_right':
      return {x: -px + px * 1.4 * t, y: -beat * 10, scale: 1.04 + beat * 0.05};
    case 'over_shoulder':
      return {x: -35 * intensity + 20 * intensity * t + beat * 70, y: 0, scale: 1.05 + beat * 0.06};
    case 'insert_closeup':
      return {x: beat * 52, y: -8 * intensity * t, scale: 1.12 + scaleStep * t + beat * 0.1};
    case 'reaction_cut':
      return {x: beat * 36, y: 0, scale: 1.16 + beat * 0.08};
    default:
      return {x: 0, y: 0, scale: 1};
  }
};

const Subtitle: React.FC<{shot: Shot; frame: number}> = ({shot, frame}) => {
  const opacity = ease(frame, [0, 6, shot.duration * AN_AE_FPS - 8, shot.duration * AN_AE_FPS], [0, 1, 1, 0]);
  return (
    <div
      style={{
        position: 'absolute',
        left: 170,
        right: 170,
        bottom: 72,
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
  );
};

const Mouth: React.FC<{talking: boolean; frame: number}> = ({talking, frame}) => {
  const phase = talking ? Math.floor(frame / 3) % 4 : 0;
  const height = [6, 22, 14, 8][phase];
  const width = [36, 30, 42, 32][phase];
  return (
    <div
      style={{
        position: 'absolute',
        left: 48,
        top: 68,
        width,
        height,
        border: '4px solid #151515',
        borderTop: phase === 0 ? '0' : '4px solid #151515',
        borderRadius: phase === 0 ? '0 0 28px 28px' : 24,
        background: phase === 0 ? 'transparent' : '#fff',
      }}
    />
  );
};

const DeliveryCharacter: React.FC<{shot: Shot; frame: number}> = ({shot, frame}) => {
  const enterX = shot.action === 'enter_walk' ? ease(frame, [0, 24], [-520, 0]) : 0;
  const actionBeat = shot.duration * AN_AE_FPS * 0.42;
  const activePose =
    shot.action === 'explain_point' && frame < actionBeat
      ? 'idle'
      : shot.action === 'panic_talk' && Math.floor(frame / 18) % 2 === 0
        ? 'point'
        : shot.body_pose;
  const activeExpression =
    shot.mouth === 'talk' && Math.floor(frame / 22) % 3 === 1
      ? shot.expression === 'furious'
        ? 'shocked'
        : 'angry'
      : shot.expression;
  const walkBob = activePose === 'walk' ? Math.sin(frame * 0.9) * 5 : Math.sin(frame * 0.18) * 2;
  const pose = bodyByPose[activePose] ?? bodyByPose.idle;
  const face = faceByExpression[activeExpression] ?? faceByExpression.neutral;
  const anchor = faceAnchors[activePose] ?? faceAnchors.idle;
  const gesturePop = ease(frame, [0, 10, 18], [0, 1, 0.92], Easing.out(Easing.back(1.8)));
  return (
    <div
      style={{
        position: 'absolute',
        left: 560 + enterX,
        top: 228 + walkBob,
        width: 360,
        height: 780,
        filter: 'drop-shadow(0 22px 22px rgba(0,0,0,.38))',
      }}
    >
      <Img src={staticFile(pose)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain'}} />
      <div style={{position: 'absolute', left: anchor.left, top: anchor.top, width: anchor.width, height: anchor.height}}>
        <Img src={staticFile(face)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain'}} />
        <Mouth talking={shot.mouth === 'talk'} frame={frame} />
      </div>
      <div style={{position: 'absolute', left: 120, bottom: 108, padding: '8px 14px', background: '#ffd15a', border: '4px solid #151515', borderRadius: 10, fontSize: 24, fontWeight: 900}}>外卖</div>
      {shot.action === 'panic_talk' || shot.action === 'explain_point' ? (
        <div style={{position: 'absolute', right: -28, top: 94, transform: `scale(${gesturePop}) rotate(-8deg)`, padding: '10px 16px', borderRadius: 14, background: '#fff1d6', border: '4px solid #151515', fontSize: 26, fontWeight: 900}}>重点！</div>
      ) : null}
    </div>
  );
};

const DemonProxy: React.FC<{shot: Shot; frame: number}> = ({shot, frame}) => {
  const show = ['A03', 'A06', 'A07'].includes(shot.shot_id);
  if (!show) return null;
  const happy = shot.expression === 'happy';
  const y = Math.sin(frame * 0.2) * 5;
  const armPop = ease(frame, [0, 12, 24], [0, 1, 0.86], Easing.out(Easing.back(1.5)));
  return (
    <div style={{position: 'absolute', right: 410, top: 282 + y, width: 330, height: 520, filter: 'drop-shadow(0 24px 22px rgba(0,0,0,.45))'}}>
      <Img src={staticFile('magic-delivery/characters/demon_king.png')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain'}} />
      <div style={{position: 'absolute', left: -18, top: 210, transform: `scale(${armPop}) rotate(6deg)`, padding: '10px 14px', background: '#fff1d6', border: '4px solid #151515', borderRadius: 14, fontSize: 24, fontWeight: 900}}>
        {happy ? '好评！' : '差评！'}
      </div>
    </div>
  );
};

const Vfx: React.FC<{shot: Shot; frame: number}> = ({shot, frame}) => {
  const meta = fxByName[shot.vfx];
  if (!meta) return null;
  const index = Math.floor(frame / 2) % meta.frames;
  const wide = shot.vfx === '一溜烟' || shot.vfx === '大灰尘';
  return (
    <Img
      src={staticFile(`${meta.folder}/frame-${String(index).padStart(3, '0')}.png`)}
      style={{
        position: 'absolute',
        left: wide ? 280 : 1110,
        bottom: wide ? 135 : 372,
        width: wide ? 520 : 280,
        opacity: shot.vfx === '汗水' ? 0.75 : 0.86,
        mixBlendMode: 'screen',
      }}
    />
  );
};

const AeOverlay: React.FC<{shot: Shot; frame: number}> = ({shot, frame}) => {
  const pop = ease(frame, [0, 8], [0.9, 1], Easing.out(Easing.back(1.4)));
  return (
    <>
      <div
        style={{
          position: 'absolute',
          right: 90,
          top: 86,
          width: 430,
          minHeight: 126,
          padding: '22px 26px',
          background: 'rgba(255,244,219,.94)',
          border: '5px solid #241510',
          color: '#241510',
          fontFamily: 'Microsoft YaHei, sans-serif',
          boxShadow: '0 14px 26px rgba(0,0,0,.28)',
          transform: `scale(${pop})`,
        }}
      >
        <div style={{fontSize: 24, color: '#d12335', fontWeight: 900}}>系统提示</div>
        <div style={{fontSize: 34, lineHeight: 1.25, marginTop: 8, fontWeight: 900}}>{shot.ui}</div>
      </div>
      <Vfx shot={shot} frame={frame} />
      <Subtitle shot={shot} frame={frame} />
    </>
  );
};

const Scene: React.FC<{shot: Shot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const total = shot.duration * fps;
  const camera = cameraTransform(shot, frame, total);
  const bg = backgroundByName[shot.background] ?? backgroundByName.旧工厂;
  return (
    <AbsoluteFill style={{background: '#101015', overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, transform: `translate(${camera.x}px, ${camera.y}px) scale(${camera.scale})`}}>
        <Img src={staticFile(bg)} style={{position: 'absolute', inset: -40, width: 'calc(100% + 80px)', height: 'calc(100% + 80px)', objectFit: 'cover', filter: 'brightness(.72) saturate(.86)'}} />
        <AbsoluteFill style={{background: 'linear-gradient(to bottom, rgba(0,0,0,.08), rgba(0,0,0,.12) 58%, rgba(0,0,0,.45))'}} />
        <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 162, background: 'rgba(15,16,19,.34)'}} />
        <DemonProxy shot={shot} frame={frame} />
        <DeliveryCharacter shot={shot} frame={frame} />
      </div>
      <AeOverlay shot={shot} frame={frame} />
    </AbsoluteFill>
  );
};

export const AnAeMagicTest: React.FC = () => {
  let cursor = 0;
  return (
    <AbsoluteFill style={{background: '#101015'}}>
      {sequence.shots.map((shot) => {
        const from = cursor;
        const durationInFrames = shot.duration * AN_AE_FPS;
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
