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
import sequence from '../projects/scene-interaction-test/shots/breakfast_activity_test.json';

type Shot = (typeof sequence.shots)[number];

export const INTERACTION_TEST_FPS = 12;
export const INTERACTION_TEST_TOTAL_FRAMES = sequence.shots.reduce(
  (sum, shot) => sum + shot.duration * INTERACTION_TEST_FPS,
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

const asset = (path: string) => staticFile(`scene-interaction-test/${path}`);
const pack = (path: string) => staticFile(`scene-interaction-test/scene-packs/${path}`);

const backgrounds: Record<string, string> = {
  'scene_customer_room_01:wide': pack('scene_customer_room_01/backgrounds/wide.png'),
  'scene_customer_room_01:close_table': pack('scene_customer_room_01/backgrounds/close_table.png'),
  'scene_customer_room_01:close_tv': pack('scene_customer_room_01/backgrounds/close_tv.png'),
  'scene_fantasy_market_01:wide': pack('scene_fantasy_market_01/backgrounds/wide.png'),
  'scene_overlay_vfx_01:speed_stage': pack('scene_overlay_vfx_01/backgrounds/speed_stage.png'),
};

const sceneProps = {
  coffeeTable: pack('scene_customer_room_01/layers/coffee_table_front.png'),
  sofa: pack('scene_customer_room_01/layers/sofa_front.png'),
  tvWarning: pack('scene_customer_room_01/props/tv_popup_warning.png'),
  phoneTable: pack('scene_customer_room_01/props/phone_table.png'),
  notice: pack('scene_fantasy_market_01/props/notice_close.png'),
  speedLines: pack('scene_overlay_vfx_01/props/speed_lines_horizontal.png'),
  whiteFlash: pack('scene_overlay_vfx_01/props/wipe_white_flash.png'),
  orderPopup: pack('scene_overlay_vfx_01/props/order_popup_normal.png'),
  bubbleLeft: pack('scene_overlay_vfx_01/props/dialogue_bubble_left.png'),
  bubbleRight: pack('scene_overlay_vfx_01/props/dialogue_bubble_right.png'),
  exclaim: pack('scene_overlay_vfx_01/props/reaction_exclaim.png'),
  question: pack('scene_overlay_vfx_01/props/reaction_question.png'),
};

const localAssets = {
  xiaoming: asset('assets/xiaoming.png'),
  friend: asset('assets/friend.png'),
  fridgeClosed: asset('assets/fridge_closed.png'),
  fridgeOpen: asset('assets/fridge_open.png'),
  breakfast: asset('assets/breakfast_table.png'),
  breakfastClose: asset('assets/breakfast_close.png'),
  phoneCall: asset('assets/phone_call_friend.png'),
  activityBanner: asset('assets/activity_banner.png'),
};

const Caption: React.FC<{shot: Shot; frame: number}> = ({shot, frame}) => {
  const {fps} = useVideoConfig();
  const duration = shot.duration * fps;
  const opacity = ease(frame, [0, 6, duration - 8, duration], [0, 1, 1, 0]);
  return (
    <div
      style={{
        position: 'absolute',
        left: 58,
        right: 58,
        bottom: 40,
        minHeight: 118,
        padding: '20px 26px',
        background: 'rgba(20, 18, 16, 0.88)',
        borderLeft: '8px solid #ffb23f',
        color: '#fff7e8',
        fontFamily: 'Microsoft YaHei, sans-serif',
        fontSize: 32,
        lineHeight: 1.35,
        opacity,
        boxShadow: '0 12px 30px rgba(0,0,0,.35)',
      }}
    >
      <div style={{fontWeight: 900, color: '#ffd979', marginBottom: 6}}>
        {shot.shot_id} | {shot.beat}
      </div>
      <div>{shot.dialogue}</div>
    </div>
  );
};

const TestNote: React.FC<{shot: Shot}> = ({shot}) => (
  <div
    style={{
      position: 'absolute',
      top: 22,
      left: 34,
      maxWidth: 760,
      padding: '12px 16px',
      borderRadius: 10,
      background: 'rgba(255, 245, 210, .92)',
      border: '4px solid #221a14',
      color: '#221a14',
      fontFamily: 'Microsoft YaHei, sans-serif',
      fontSize: 22,
      fontWeight: 800,
    }}
  >
    测试点：{shot.test_focus}
  </div>
);

const Character: React.FC<{
  src: string;
  x: number;
  y: number;
  scale?: number;
  flip?: boolean;
  bob?: number;
}> = ({src, x, y, scale = 1, flip = false, bob = 0}) => (
  <Img
    src={src}
    style={{
      position: 'absolute',
      left: x,
      top: y + bob,
      width: 260 * scale,
      height: 520 * scale,
      objectFit: 'contain',
      transform: `scaleX(${flip ? -1 : 1})`,
      filter: 'drop-shadow(0 14px 12px rgba(0,0,0,.35))',
    }}
  />
);

const FridgeBeat: React.FC<{frame: number}> = ({frame}) => {
  const open = frame > 20;
  const foodX = ease(frame, [25, 56], [1040, 710]);
  const foodY = ease(frame, [25, 56], [330, 690]);
  return (
    <>
      <Img
        src={open ? localAssets.fridgeOpen : localAssets.fridgeClosed}
        style={{position: 'absolute', left: 1220, top: 230, width: 360}}
      />
      <Img
        src={localAssets.breakfast}
        style={{
          position: 'absolute',
          left: foodX,
          top: foodY,
          width: 230,
          opacity: ease(frame, [22, 30], [0, 1]),
          filter: 'drop-shadow(0 10px 10px rgba(0,0,0,.3))',
        }}
      />
    </>
  );
};

const PhoneCall: React.FC<{frame: number}> = ({frame}) => (
  <Img
    src={localAssets.phoneCall}
    style={{
      position: 'absolute',
      right: 180,
      top: 170,
      width: 360,
      transform: `scale(${ease(frame, [0, 10], [0.82, 1])}) rotate(${Math.sin(frame / 4) * 1.2}deg)`,
      filter: 'drop-shadow(0 16px 18px rgba(0,0,0,.32))',
    }}
  />
);

const MarketExtras: React.FC<{frame: number}> = ({frame}) => {
  const bannerScale = ease(frame, [8, 20], [0.7, 1]);
  return (
    <>
      <Img src={localAssets.activityBanner} style={{position: 'absolute', left: 530, top: 120, width: 620, transform: `scale(${bannerScale})`}} />
      <Img src={sceneProps.notice} style={{position: 'absolute', left: 1160, top: 190, width: 310, opacity: 0.94}} />
      <Img src={sceneProps.exclaim} style={{position: 'absolute', left: 825, top: 68, width: 190, transform: `scale(${ease(frame % 18, [0, 8, 18], [0.8, 1.08, 0.8])})`}} />
    </>
  );
};

const getCamera = (shot: Shot, frame: number) => {
  const duration = shot.duration * INTERACTION_TEST_FPS;
  const t = ease(frame, [0, duration], [0, 1], Easing.inOut(Easing.ease));
  switch (shot.camera) {
    case 'morning_push':
      return {x: 0, y: -20 * t, scale: 1 + 0.08 * t};
    case 'pan_to_fridge':
      return {x: -95 * t, y: 0, scale: 1.04};
    case 'table_insert':
      return {x: 0, y: -10 * t, scale: 1.03};
    case 'sofa_tv':
      return {x: 0, y: 0, scale: 1.04 + 0.03 * Math.sin(t * Math.PI)};
    case 'tv_close':
      return {x: 0, y: 0, scale: 1.02};
    case 'phone_push':
      return {x: 36 * t, y: -6 * t, scale: 1 + 0.07 * t};
    case 'dialogue_split':
      return {x: 0, y: 0, scale: 1.02};
    case 'event_establish':
      return {x: -70 + 140 * t, y: 0, scale: 1.04};
    default:
      return {x: 0, y: 0, scale: 1};
  }
};

const Scene: React.FC<{shot: Shot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const bgKey = `${shot.scene_pack}:${shot.background}`;
  const camera = getCamera(shot, frame);
  const bob = Math.sin(frame / 8) * 4;

  return (
    <AbsoluteFill style={{background: '#111', overflow: 'hidden'}}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          transform: `translate(${camera.x}px, ${camera.y}px) scale(${camera.scale})`,
        }}
      >
        <Img src={backgrounds[bgKey]} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover'}} />

        {shot.action === 'time_skip' ? (
          <>
            <Img src={sceneProps.speedLines} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0.88}} />
            <Img src={sceneProps.whiteFlash} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: ease(frame, [0, 8, 40, 60], [0, 0.3, 0.88, 0])}} />
          </>
        ) : null}

        {shot.scene_pack === 'scene_customer_room_01' && shot.background !== 'close_table' && shot.background !== 'close_tv' ? (
          <>
            <Character src={localAssets.xiaoming} x={shot.action === 'wake_up' ? ease(frame, [0, 35], [820, 720]) : shot.action.includes('phone') || shot.action === 'call_friend' ? 620 : 540} y={shot.action === 'wake_up' ? ease(frame, [0, 35], [560, 480]) : 480} scale={0.82} bob={bob} />
            {shot.action === 'phone_dialogue' ? <Character src={localAssets.friend} x={1060} y={485} scale={0.78} flip bob={-bob} /> : null}
            {shot.action === 'open_fridge_take_food' ? <FridgeBeat frame={frame} /> : null}
            {shot.action === 'eat_watch_tv' ? <Img src={localAssets.breakfast} style={{position: 'absolute', left: 800, top: 730, width: 300}} /> : null}
            {shot.action === 'eat_watch_tv' ? <Img src={sceneProps.tvWarning} style={{position: 'absolute', left: 745, top: 255, width: 420, transform: `scale(${ease(frame, [20, 34], [0.8, 1])})`}} /> : null}
            {shot.action === 'call_friend' ? <PhoneCall frame={frame} /> : null}
            {shot.action === 'phone_dialogue' ? (
              <>
                <Img src={sceneProps.bubbleLeft} style={{position: 'absolute', left: 330, top: 145, width: 470}} />
                <Img src={sceneProps.bubbleRight} style={{position: 'absolute', right: 300, top: 145, width: 470}} />
                <Img src={sceneProps.question} style={{position: 'absolute', right: 500, top: 315, width: 160}} />
              </>
            ) : null}
            <Img src={sceneProps.sofa} style={{position: 'absolute', inset: 0, width: '100%', height: '100%'}} />
            <Img src={sceneProps.coffeeTable} style={{position: 'absolute', inset: 0, width: '100%', height: '100%'}} />
          </>
        ) : null}

        {shot.background === 'close_table' ? (
          <>
            <Img src={localAssets.breakfastClose} style={{position: 'absolute', left: 570, top: 245, width: 760, transform: `scale(${ease(frame, [0, 12], [0.86, 1])})`}} />
            <Img src={sceneProps.exclaim} style={{position: 'absolute', left: 1170, top: 180, width: 170}} />
          </>
        ) : null}

        {shot.background === 'close_tv' ? (
          <>
            <Img src={localAssets.activityBanner} style={{position: 'absolute', left: 520, top: 210, width: 870, transform: `scale(${ease(frame, [0, 14], [0.78, 1])})`}} />
            <Img src={sceneProps.orderPopup} style={{position: 'absolute', right: 170, top: 540, width: 430}} />
          </>
        ) : null}

        {shot.scene_pack === 'scene_fantasy_market_01' ? (
          <>
            <MarketExtras frame={frame} />
            <Character src={localAssets.xiaoming} x={575} y={490} scale={0.75} bob={bob} />
            <Character src={localAssets.friend} x={1010} y={490} scale={0.75} flip bob={-bob} />
            <Img src={sceneProps.bubbleLeft} style={{position: 'absolute', left: 355, top: 170, width: 440}} />
          </>
        ) : null}
      </div>

      <TestNote shot={shot} />
      <Caption shot={shot} frame={frame} />
    </AbsoluteFill>
  );
};

export const SceneInteractionTest: React.FC = () => {
  let cursor = 0;
  return (
    <AbsoluteFill style={{background: '#101014'}}>
      {sequence.shots.map((shot) => {
        const from = cursor;
        const durationInFrames = shot.duration * INTERACTION_TEST_FPS;
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
