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
import sequence from '../projects/magic-delivery/shots/climax_60s.json';

type Shot = (typeof sequence.shots)[number];

export const MAGIC_FPS = 12;
export const MAGIC_TOTAL_FRAMES = sequence.shots.reduce(
  (sum, shot) => sum + shot.duration * MAGIC_FPS,
  0,
);

const clampEase = (
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

const colors = {
  ink: '#101015',
  red: '#d12335',
  gold: '#ffd36a',
  orange: '#ff8a2a',
  cyan: '#7ee6ff',
  paper: '#fff1d6',
  purple: '#51316d',
  green: '#40e38b',
};

const fxFrameCounts: Record<string, number> = {
  dust: 24,
  hit_star: 6,
  smoke_ring: 24,
  speed_smoke: 24,
  sweat: 24,
};

const getCameraTransform = (shot: Shot, frame: number, durationFrames: number) => {
  const preset = shot.camera?.preset ?? 'static_hold';
  const t = clampEase(frame, [0, durationFrames], [0, 1], Easing.inOut(Easing.ease));
  const intensity = Math.min(Math.max(shot.camera?.motion_intensity ?? 0.2, 0), 0.75);
  const px = 120 * intensity;
  const scaleStep = 0.16 * intensity;
  switch (preset) {
    case 'establishing_pan':
      return {x: -px + px * 2 * t, y: 0, scale: 1.04};
    case 'push_in':
      return {x: 0, y: -18 * intensity * t, scale: 1 + scaleStep * t};
    case 'pull_back':
      return {x: 0, y: 10 * intensity * t, scale: 1 + scaleStep * (1 - t)};
    case 'truck_left':
      return {x: px * (1 - t), y: 0, scale: 1.05};
    case 'truck_right':
      return {x: -px * (1 - t), y: 0, scale: 1.05};
    case 'over_shoulder':
      return {x: -24 * intensity + 16 * intensity * t, y: 0, scale: 1.06};
    case 'insert_closeup':
      return {x: 0, y: -10 * intensity * t, scale: 1.08 + scaleStep * 0.55 * t};
    case 'reaction_cut':
      return {x: 0, y: 0, scale: 1.05};
    default:
      return {x: 0, y: 0, scale: 1};
  }
};

const bgByLocation: Record<string, string[]> = {
  demon_rooftop: ['#20101e', '#6d1721', '#12080c'],
  throne_front: ['#150a14', '#432046', '#0f090d'],
  sky_rift: ['#060916', '#18265e', '#07070c'],
  battlefield: ['#181417', '#4b251c', '#0c0a0a'],
  demon_hall: ['#1a0b0e', '#3a1d25', '#0b0708'],
  judgement_beam: ['#07131c', '#1b5064', '#08090e'],
  world_map: ['#121923', '#234a45', '#080b0d'],
  phone_closeup: ['#05070a', '#14223a', '#05070a'],
};

const Caption: React.FC<{shot: Shot; localFrame: number}> = ({shot, localFrame}) => {
  const opacity = clampEase(localFrame, [0, 5, shot.duration * MAGIC_FPS - 8, shot.duration * MAGIC_FPS], [0, 1, 1, 0]);
  return (
    <div
      style={{
        position: 'absolute',
        left: 34,
        right: 34,
        bottom: 54,
        minHeight: 150,
        padding: '24px 28px',
        background: 'rgba(7,8,12,.9)',
        borderLeft: `7px solid ${colors.orange}`,
        boxShadow: '0 10px 30px rgba(0,0,0,.45)',
        color: '#fff7e8',
        fontFamily: 'Microsoft YaHei, sans-serif',
        fontSize: 34,
        lineHeight: 1.42,
        opacity,
      }}
    >
      <span style={{color: colors.gold, fontWeight: 800}}>{shot.speaker}：</span>
      {shot.dialogue}
    </div>
  );
};

const Face: React.FC<{expression: string; scale?: number}> = ({expression, scale = 1}) => {
  const panic = ['comic_panic', 'angry_panic', 'shocked'].includes(expression);
  const blank = expression === 'blank';
  const smile = expression === 'neutral_to_smirk' || expression === 'soft_realization';
  return (
    <div style={{position: 'absolute', inset: 0, transform: `scale(${scale})`}}>
      <div style={{position: 'absolute', left: 33, top: 40, width: panic ? 18 : 28, height: panic ? 22 : 10, border: '4px solid #151515', borderRadius: 20, background: blank ? '#151515' : '#fff'}} />
      <div style={{position: 'absolute', right: 33, top: 40, width: panic ? 18 : 28, height: panic ? 22 : 10, border: '4px solid #151515', borderRadius: 20, background: blank ? '#151515' : '#fff'}} />
      <div style={{position: 'absolute', left: 62, top: panic ? 84 : 92, width: panic ? 42 : 54, height: panic ? 34 : 16, borderBottom: panic ? '0' : '5px solid #151515', border: panic ? '5px solid #151515' : undefined, borderRadius: panic ? 22 : '0 0 40px 40px', transform: smile ? 'rotate(4deg)' : 'none'}} />
      {panic ? <div style={{position: 'absolute', right: -16, top: 6, color: colors.cyan, fontSize: 42, fontWeight: 900}}>汗</div> : null}
    </div>
  );
};

const DeliveryGuy: React.FC<{shot: Shot; localFrame: number}> = ({shot, localFrame}) => {
  const enter = shot.action === 'scooter_enter';
  const shield = shot.action === 'block_with_bag';
  const phone = ['phone_tap', 'voice_appeal', 'confirm_button', 'phone_closeup'].includes(shot.action);
  const x = enter ? clampEase(localFrame, [0, 18], [-260, 0]) : 0;
  const recoil = shield ? Math.sin(localFrame * 0.8) * 7 : 0;
  const y = shot.action === 'shocked_recoil' ? clampEase(localFrame, [0, 8], [0, 20]) : 0;
  return (
    <div
      style={{
        position: 'absolute',
        left: 265 + x + recoil,
        top: 555 + y,
        width: 190,
        height: 478,
        filter: 'drop-shadow(0 18px 16px rgba(0,0,0,.55))',
      }}
    >
      {enter ? (
        <div style={{position: 'absolute', left: -82, top: 344, width: 285, height: 54, borderRadius: 34, background: '#1a1d23', border: `7px solid ${colors.orange}`}}>
          <div style={{position: 'absolute', left: 26, top: 34, width: 54, height: 54, borderRadius: 60, background: '#070708', border: '7px solid #d5d5d5'}} />
          <div style={{position: 'absolute', right: 24, top: 34, width: 54, height: 54, borderRadius: 60, background: '#070708', border: '7px solid #d5d5d5'}} />
        </div>
      ) : null}
      <Img
        src={staticFile('magic-delivery/characters/delivery_guy.png')}
        style={{position: 'absolute', left: 0, top: 0, width: 190, height: 478, objectFit: 'contain'}}
      />
      <div style={{position: 'absolute', left: 50, top: 74, width: 92, height: 92}}>
        <Face expression={shot.expression} scale={0.64} />
      </div>
      {phone ? <div style={{position: 'absolute', right: -18, top: 170, width: 52, height: 82, borderRadius: 14, background: '#12161d', border: '5px solid #151515', transform: 'rotate(-12deg)'}} /> : null}
      {shield ? <div style={{position: 'absolute', left: -56, top: 210, width: 144, height: 98, borderRadius: 18, background: '#f0a43a', border: '5px solid #151515', transform: 'rotate(-9deg)'}} /> : null}
      <div style={{position: 'absolute', left: -10, top: 258, width: 88, height: 66, background: '#ffd15a', border: '5px solid #151515', borderRadius: 12, transform: 'rotate(5deg)'}}>
        <div style={{fontSize: 19, fontWeight: 900, textAlign: 'center', paddingTop: 15}}>外卖</div>
      </div>
    </div>
  );
};

const DemonKing: React.FC<{shot: Shot; localFrame: number}> = ({shot, localFrame}) => {
  const shocked = ['shocked_recoil', 'eat_and_review'].includes(shot.action);
  const y = shocked ? clampEase(localFrame, [0, 7], [0, -22]) : Math.sin(localFrame / 12) * 5;
  return (
    <div style={{position: 'absolute', left: 410, top: 360 + y, width: 280, height: 398, filter: 'drop-shadow(0 18px 20px rgba(0,0,0,.65))'}}>
      <Img
        src={staticFile('magic-delivery/characters/demon_king.png')}
        style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain'}}
      />
      <div style={{position: 'absolute', left: 67, top: 96, width: 92, height: 86}}>
        <Face expression={shocked ? 'shocked' : 'villain_smirk'} scale={0.58} />
      </div>
      <div style={{position: 'absolute', left: 85, top: 222, width: 82, height: 88, borderRadius: 20, background: '#ffbc49', border: '5px solid #120914', display: shot.action === 'eat_and_review' ? 'block' : 'none'}}>
        <div style={{fontSize: 20, padding: 12, fontWeight: 900}}>麻辣烫</div>
      </div>
    </div>
  );
};

const Hero: React.FC<{localFrame: number}> = ({localFrame}) => (
  <div style={{position: 'absolute', left: 36, top: 540 + Math.sin(localFrame / 9) * 4, width: 244, height: 344, opacity: 0.95, filter: 'drop-shadow(0 16px 14px rgba(0,0,0,.42))'}}>
    <Img
      src={staticFile('magic-delivery/characters/hero.png')}
      style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain'}}
    />
    <div style={{position: 'absolute', left: 78, top: 43, width: 78, height: 72}}>
      <Face expression="shocked" scale={0.48} />
    </div>
  </div>
);

const Judge: React.FC<{localFrame: number}> = ({localFrame}) => (
  <div style={{position: 'absolute', left: 104, top: 118 + Math.sin(localFrame / 15) * 5, width: 510, height: 265, borderRadius: 28, background: 'rgba(235,248,255,.92)', border: `7px solid ${colors.cyan}`, boxShadow: `0 0 ${28 + localFrame % 20}px ${colors.cyan}`}}>
    <div style={{position: 'absolute', left: 32, top: 28, width: 100, height: 100, borderRadius: 60, background: '#fff', border: '5px solid #1e3345'}}>
      <div style={{fontSize: 52, textAlign: 'center', paddingTop: 16}}>客</div>
    </div>
    <div style={{position: 'absolute', left: 150, top: 36, right: 22, color: '#12202c', fontSize: 34, fontWeight: 900, lineHeight: 1.25}}>天界审判者<br /><span style={{fontSize: 25, color: colors.red}}>自动灭世客服</span></div>
  </div>
);

const Background: React.FC<{shot: Shot; localFrame: number}> = ({shot}) => {
  const palette = bgByLocation[shot.location] ?? bgByLocation.demon_rooftop;
  const bgFile = shot.location === 'phone_closeup' || shot.location === 'world_map'
    ? 'magic-delivery/backgrounds/cinema.jpg'
    : shot.location === 'demon_hall' || shot.location === 'throne_front'
      ? 'magic-delivery/backgrounds/earth_house.jpg'
      : 'magic-delivery/backgrounds/factory.jpg';
  return (
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 22%, ${palette[1]}, ${palette[0]} 45%, ${palette[2]})`, overflow: 'hidden'}}>
      <Img
        src={staticFile(bgFile)}
        style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(.38) saturate(.75) hue-rotate(-12deg)'}}
      />
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% 35%, rgba(255,96,45,.2), ${palette[2]}cc 72%)`}} />
      <div style={{position: 'absolute', left: 286, top: 120, width: 148, height: 360, background: 'rgba(255,226,119,.08)', clipPath: 'polygon(40% 0, 60% 0, 100% 100%, 0 100%)'}} />
      {Array.from({length: 9}).map((_, i) => (
        <div key={i} style={{position: 'absolute', left: 50 + i * 78, top: 190 + (i % 2) * 42, width: 3, height: 140, background: 'rgba(255,255,255,.18)', transform: `rotate(${i % 2 ? -18 : 18}deg)`}} />
      ))}
      <div style={{position: 'absolute', top: 42, left: 34, color: '#fff2d8', fontSize: 24, fontFamily: 'Microsoft YaHei', borderTop: `4px solid ${colors.orange}`, paddingTop: 8}}>{shot.shot_id} / {shot.beat}</div>
    </AbsoluteFill>
  );
};

const UIOverlay: React.FC<{shot: Shot; localFrame: number}> = ({shot, localFrame}) => {
  const pop = clampEase(localFrame, [0, 8], [0.85, 1], Easing.out(Easing.back(1.8)));
  if (shot.ui === 'new_order') {
    return (
      <div style={{position: 'absolute', left: 70, right: 70, top: 280, transform: `scale(${pop})`, padding: 30, borderRadius: 24, background: '#fff', color: '#101015', border: `8px solid ${colors.green}`, fontFamily: 'Microsoft YaHei'}}>
        <div style={{fontSize: 32, fontWeight: 900}}>新订单</div>
        <div style={{fontSize: 44, fontWeight: 900, marginTop: 22}}>创世神</div>
        <div style={{fontSize: 30, marginTop: 16}}>备注：重启宇宙，微辣</div>
      </div>
    );
  }
  const textByUi: Record<string, string> = {
    countdown: `灭世倒计时 00:${String(Math.max(0, 60 - Math.floor(localFrame / MAGIC_FPS))).padStart(2, '0')}`,
    order_card: '订单备注：少香菜，别毁灭世界',
    note_zoom: '毁灭世界，谢谢',
    customer_service: '自动服务已开启',
    tactical_map: '骑手战术面板',
    photo_stamp: '已拍照留证',
    call_waiting: '正在转接人工客服...',
    receipt_sign: '请在此处签收',
    route_map: '路线重算中',
    confirm_cancel: '是否撤回灭世服务？',
    five_star: '★★★★★ 五星好评',
  };
  return (
    <div style={{position: 'absolute', right: 38, top: 170, width: 315, minHeight: 112, transform: `scale(${pop})`, padding: 22, background: 'rgba(255,244,219,.94)', color: '#241510', border: '5px solid #2b1712', boxShadow: '0 12px 22px rgba(0,0,0,.35)', fontFamily: 'Microsoft YaHei'}}>
      <div style={{fontSize: 24, color: colors.red, fontWeight: 900}}>系统提示</div>
      <div style={{fontSize: 30, lineHeight: 1.25, fontWeight: 900, marginTop: 8}}>{textByUi[shot.ui] ?? shot.ui}</div>
    </div>
  );
};

const VfxOverlay: React.FC<{shot: Shot; localFrame: number}> = ({shot, localFrame}) => {
  const pulse = (Math.sin(localFrame * 0.55) + 1) / 2;
  const flash = ['camera_flash', 'impact_spark'].includes(shot.vfx) && localFrame < 4;
  const fx =
    shot.vfx === 'dust_pop'
      ? 'dust'
      : shot.vfx === 'camera_flash' || shot.vfx === 'impact_spark'
        ? 'hit_star'
        : shot.vfx === 'loading_loop'
          ? 'smoke_ring'
          : shot.expression === 'comic_panic' || shot.expression === 'angry_panic'
              ? 'sweat'
              : null;
  const frameIndex = fx ? Math.floor(localFrame / 2) % fxFrameCounts[fx] : 0;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {shot.vfx === 'red_alert' ? <AbsoluteFill style={{background: `rgba(205,20,42,${0.08 + (localFrame < 12 ? pulse * 0.12 : 0)})`, mixBlendMode: 'screen'}} /> : null}
      {shot.vfx === 'golden_path' || shot.vfx === 'warm_steam' ? <AbsoluteFill style={{boxShadow: `inset 0 0 ${80 + pulse * 110}px rgba(255,203,84,.62)`}} /> : null}
      {flash ? <AbsoluteFill style={{background: 'rgba(255,255,255,.68)'}} /> : null}
      {fx ? (
        <Img
          src={staticFile(`magic-delivery/fx/${fx}/frame-${String(frameIndex).padStart(3, '0')}.png`)}
          style={{
            position: 'absolute',
            right: fx === 'sweat' ? 180 : 70,
            bottom: fx === 'speed_smoke' ? 280 : 385,
            width: fx === 'speed_smoke' ? 460 : 360,
            opacity: fx === 'sweat' ? 0.72 : 0.82,
            mixBlendMode: 'screen',
          }}
        />
      ) : null}
      {shot.vfx === 'loading_loop' ? <div style={{position: 'absolute', left: 300, top: 410, width: 120, height: 120, borderRadius: 100, border: `12px solid rgba(255,255,255,.2)`, borderTopColor: colors.cyan, transform: `rotate(${localFrame * 22}deg)`}} /> : null}
      {shot.vfx === 'crack_close' ? <div style={{position: 'absolute', left: 90, top: 98, right: 90, height: 8, background: colors.cyan, boxShadow: `0 0 ${20 + pulse * 35}px ${colors.cyan}`, transform: `scaleX(${1 - clampEase(localFrame, [0, 45], [0, .9])})`}} /> : null}
      <AbsoluteFill style={{background: 'linear-gradient(to bottom, rgba(0,0,0,.12), transparent 32%, transparent 70%, rgba(0,0,0,.52))'}} />
    </AbsoluteFill>
  );
};

const Scene: React.FC<{shot: Shot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const durationFrames = shot.duration * fps;
  const camera = getCameraTransform(shot, frame, durationFrames);
  const showJudge = shot.characters.includes('judge');
  const showHero = shot.characters.includes('hero');
  const showDemon = shot.characters.includes('demon_king');
  return (
    <AbsoluteFill style={{background: colors.ink, overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, transform: `translate(${camera.x}px, ${camera.y}px) scale(${camera.scale})`}}>
        <Background shot={shot} localFrame={frame} />
        {showDemon ? <DemonKing shot={shot} localFrame={frame} /> : null}
        {showHero ? <Hero localFrame={frame} /> : null}
        {showJudge ? <Judge localFrame={frame} /> : null}
        <DeliveryGuy shot={shot} localFrame={frame} />
      </div>
      <VfxOverlay shot={shot} localFrame={frame} />
      <UIOverlay shot={shot} localFrame={frame} />
      <Caption shot={shot} localFrame={frame} />
    </AbsoluteFill>
  );
};

export const MagicDeliveryClimax: React.FC = () => {
  let cursor = 0;
  return (
    <AbsoluteFill style={{background: colors.ink}}>
      {sequence.shots.map((shot) => {
        const from = cursor;
        const durationInFrames = shot.duration * MAGIC_FPS;
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
