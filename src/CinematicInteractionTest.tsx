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
import sequence from '../projects/scene-interaction-test/shots/breakfast_activity_cinematic_generated.json';

type Shot = (typeof sequence.shots)[number];

export const CINEMATIC_TEST_FPS = 12;
export const CINEMATIC_TEST_TOTAL_FRAMES = sequence.shots.reduce(
  (sum, shot) => sum + shot.duration * CINEMATIC_TEST_FPS,
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

const root = (path: string) => staticFile(`scene-interaction-test/${path}`);
const pack = (path: string) => root(`scene-packs/${path}`);

const backgrounds: Record<string, string> = {
  'scene_customer_room_01:wide': pack('scene_customer_room_01/backgrounds/wide.png'),
  'scene_customer_room_01:close_table': pack('scene_customer_room_01/backgrounds/close_table.png'),
  'scene_customer_room_01:close_tv': pack('scene_customer_room_01/backgrounds/close_tv.png'),
  'scene_fantasy_market_01:wide': pack('scene_fantasy_market_01/backgrounds/wide.png'),
  'scene_overlay_vfx_01:speed_stage': pack('scene_overlay_vfx_01/backgrounds/speed_stage.png'),
};

const assets = {
  xiaoming: root('assets/xiaoming.png'),
  friend: root('assets/friend.png'),
  fridgeClosed: root('assets/fridge_closed.png'),
  fridgeOpen: root('assets/fridge_open.png'),
  breakfast: root('assets/breakfast_table.png'),
  breakfastClose: root('assets/breakfast_close.png'),
  phoneCall: root('assets/phone_call_friend.png'),
  activityBanner: root('assets/activity_banner.png'),
  sofa: pack('scene_customer_room_01/layers/sofa_front.png'),
  coffeeTable: pack('scene_customer_room_01/layers/coffee_table_front.png'),
  tvWarning: pack('scene_customer_room_01/props/tv_popup_warning.png'),
  phoneTable: pack('scene_customer_room_01/props/phone_table.png'),
  notice: pack('scene_fantasy_market_01/props/notice_close.png'),
  bubbleLeft: pack('scene_overlay_vfx_01/props/dialogue_bubble_left.png'),
  bubbleRight: pack('scene_overlay_vfx_01/props/dialogue_bubble_right.png'),
  exclaim: pack('scene_overlay_vfx_01/props/reaction_exclaim.png'),
  question: pack('scene_overlay_vfx_01/props/reaction_question.png'),
  speedLines: pack('scene_overlay_vfx_01/props/speed_lines_horizontal.png'),
};

const Caption: React.FC<{shot: Shot; frame: number}> = ({shot, frame}) => {
  const {fps} = useVideoConfig();
  const duration = shot.duration * fps;
  const opacity = ease(frame, [0, 5, duration - 5, duration], [0, 1, 1, 0]);
  return (
    <div
      style={{
        position: 'absolute',
        left: 72,
        right: 72,
        bottom: 34,
        minHeight: 88,
        padding: '18px 24px',
        background: 'rgba(18, 16, 14, 0.86)',
        color: '#fff6e2',
        fontFamily: 'Microsoft YaHei, sans-serif',
        fontSize: 34,
        lineHeight: 1.32,
        opacity,
        boxShadow: '0 12px 28px rgba(0,0,0,.34)',
      }}
    >
      {shot.dialogue}
    </div>
  );
};

const Character: React.FC<{
  src: string;
  x: number;
  y: number;
  scale?: number;
  flip?: boolean;
  lean?: number;
}> = ({src, x, y, scale = 1, flip = false, lean = 0}) => (
  <Img
    src={src}
    style={{
      position: 'absolute',
      left: x,
      top: y,
      width: 260 * scale,
      height: 520 * scale,
      objectFit: 'contain',
      transform: `scaleX(${flip ? -1 : 1}) rotate(${lean}deg)`,
      transformOrigin: '50% 90%',
      filter: 'drop-shadow(0 16px 12px rgba(0,0,0,.35))',
    }}
  />
);

const HandProxy: React.FC<{x: number; y: number; scale?: number; rotate?: number}> = ({
  x,
  y,
  scale = 1,
  rotate = 0,
}) => (
  <div
    style={{
      position: 'absolute',
      left: x,
      top: y,
      width: 210 * scale,
      height: 86 * scale,
      borderRadius: 52,
      background: '#ffd9ae',
      border: `${8 * scale}px solid #231914`,
      transform: `rotate(${rotate}deg)`,
      boxShadow: '0 12px 16px rgba(0,0,0,.28)',
    }}
  >
    <div
      style={{
        position: 'absolute',
        right: -28 * scale,
        top: 14 * scale,
        width: 62 * scale,
        height: 48 * scale,
        borderRadius: 30,
        background: '#ffd9ae',
        border: `${7 * scale}px solid #231914`,
      }}
    />
  </div>
);

const FridgeInterior: React.FC<{frame: number}> = ({frame}) => (
  <AbsoluteFill
    style={{
      background: '#dff5ff',
      border: '34px solid #25313d',
      boxSizing: 'border-box',
    }}
  >
    <div style={{position: 'absolute', left: 120, right: 120, top: 230, height: 10, background: '#6e8795'}} />
    <div style={{position: 'absolute', left: 120, right: 120, top: 530, height: 10, background: '#6e8795'}} />
    <Img
      src={assets.breakfast}
      style={{
        position: 'absolute',
        left: 585,
        top: 285,
        width: 520,
        transform: `scale(${ease(frame, [0, 20], [0.88, 1])})`,
      }}
    />
    <div
      style={{
        position: 'absolute',
        left: 1150,
        top: 285,
        width: 190,
        height: 310,
        background: '#bfe7ff',
        border: '12px solid #1e252b',
      }}
    />
    <HandProxy x={ease(frame, [12, 34], [1600, 950])} y={360} scale={1.15} rotate={-8} />
  </AbsoluteFill>
);

const SceneFrame: React.FC<{shot: Shot; children: React.ReactNode; bg?: string}> = ({
  shot,
  children,
  bg,
}) => {
  const frame = useCurrentFrame();
  const duration = shot.duration * CINEMATIC_TEST_FPS;
  const move = shot.camera.move;
  const t = ease(frame, [0, duration], [0, 1], Easing.inOut(Easing.ease));
  const transform =
    move === 'push_in'
      ? `scale(${1 + 0.08 * t})`
      : move === 'pull_back'
        ? `scale(${1.08 - 0.08 * t})`
        : move === 'pan'
          ? `translateX(${-70 + 140 * t}px) scale(1.05)`
          : move === 'truck'
            ? `translateX(${45 * Math.sin(t * Math.PI)}px) scale(1.04)`
            : 'scale(1)';
  return (
    <AbsoluteFill style={{background: '#111', overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, transform}}>
        {bg ? (
          <Img
            src={bg}
            style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover'}}
          />
        ) : null}
        {children}
      </div>
      <Caption shot={shot} frame={frame} />
    </AbsoluteFill>
  );
};

const RoomLayers: React.FC<{withTable?: boolean}> = ({withTable = true}) => (
  <>
    <Img src={assets.sofa} style={{position: 'absolute', inset: 0, width: '100%', height: '100%'}} />
    {withTable ? (
      <Img src={assets.coffeeTable} style={{position: 'absolute', inset: 0, width: '100%', height: '100%'}} />
    ) : null}
  </>
);

const ScreenPanel: React.FC<{children: React.ReactNode}> = ({children}) => (
  <div
    style={{
      position: 'absolute',
      left: 430,
      top: 165,
      width: 1060,
      height: 600,
      background: '#20262f',
      border: '18px solid #10151c',
      borderRadius: 16,
      boxShadow: '0 20px 38px rgba(0,0,0,.35)',
      color: '#fff5d4',
      fontFamily: 'Microsoft YaHei, sans-serif',
      overflow: 'hidden',
    }}
  >
    {children}
  </div>
);

const EventExtras: React.FC = () => (
  <>
    <Img src={assets.activityBanner} style={{position: 'absolute', left: 560, top: 95, width: 620}} />
    <Img src={assets.notice} style={{position: 'absolute', left: 1210, top: 190, width: 315}} />
  </>
);

const renderShot = (shot: Shot, frame: number) => {
  const bgKey = `${shot.scene_pack}:${shot.background}`;
  const bg = backgrounds[bgKey];
  const lean = Math.sin(frame / 8) * 1.5;

  switch (shot.action) {
    case 'wake_establish':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Character src={assets.xiaoming} x={790} y={ease(frame, [0, 30], [565, 510])} scale={0.78} lean={lean} />
          <RoomLayers />
        </SceneFrame>
      );

    case 'tv_idle_insert':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <ScreenPanel>
            <div style={{fontSize: 54, fontWeight: 900, padding: '90px 90px 20px'}}>今日活动预告</div>
            <div style={{fontSize: 42, padding: '20px 90px'}}>下午三点</div>
            <div style={{fontSize: 42, padding: '10px 90px'}}>城市广场限时试吃大会</div>
            <div style={{position: 'absolute', right: 80, bottom: 70, fontSize: 82}}>!</div>
          </ScreenPanel>
        </SceneFrame>
      );

    case 'wake_reaction':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Character src={assets.xiaoming} x={740} y={355} scale={1.12} lean={lean} />
          <Img src={assets.exclaim} style={{position: 'absolute', left: 985, top: 230, width: 170}} />
        </SceneFrame>
      );

    case 'approach_fridge':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Img src={assets.fridgeClosed} style={{position: 'absolute', left: 1220, top: 230, width: 360}} />
          <Character src={assets.xiaoming} x={ease(frame, [0, 42], [420, 830])} y={470} scale={0.82} lean={lean} />
          <RoomLayers />
        </SceneFrame>
      );

    case 'fridge_handle_contact':
      return (
        <SceneFrame shot={shot}>
          <AbsoluteFill style={{background: '#dbeef7'}} />
          <div style={{position: 'absolute', left: 600, top: 80, width: 520, height: 820, border: '20px solid #1b2229', background: '#edfaff'}} />
          <div style={{position: 'absolute', left: 1030, top: 415, width: 48, height: 210, borderRadius: 18, background: '#4f5c67'}} />
          <HandProxy x={ease(frame, [0, 26], [210, 805])} y={450} scale={1.25} rotate={4} />
        </SceneFrame>
      );

    case 'fridge_inside_pov':
      return (
        <SceneFrame shot={shot}>
          <FridgeInterior frame={frame} />
        </SceneFrame>
      );

    case 'food_to_hand_close':
      return (
        <SceneFrame shot={shot}>
          <AbsoluteFill style={{background: '#dff5ff'}} />
          <Img
            src={assets.breakfast}
            style={{
              position: 'absolute',
              left: ease(frame, [0, 24], [615, 850]),
              top: ease(frame, [0, 24], [330, 410]),
              width: 480,
              filter: 'drop-shadow(0 18px 18px rgba(0,0,0,.3))',
            }}
          />
          <HandProxy x={760} y={520} scale={1.35} rotate={-10} />
        </SceneFrame>
      );

    case 'food_reaction_close':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Character src={assets.xiaoming} x={710} y={360} scale={1.1} lean={lean} />
          <Img src={assets.breakfast} style={{position: 'absolute', left: 1010, top: 615, width: 320}} />
        </SceneFrame>
      );

    case 'place_breakfast_overhead':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <HandProxy x={ease(frame, [0, 24], [1250, 900])} y={260} scale={0.85} rotate={-20} />
          <Img src={assets.breakfastClose} style={{position: 'absolute', left: 560, top: 230, width: 780}} />
        </SceneFrame>
      );

    case 'place_breakfast_result':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Img
            src={assets.breakfastClose}
            style={{
              position: 'absolute',
              left: 520,
              top: 210,
              width: 850,
              transform: `scale(${ease(frame, [0, 12], [0.92, 1])})`,
              filter: 'drop-shadow(0 16px 18px rgba(0,0,0,.22))',
            }}
          />
        </SceneFrame>
      );

    case 'eat_medium':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Character src={assets.xiaoming} x={620} y={500} scale={0.82} lean={lean} />
          <Img src={assets.breakfast} style={{position: 'absolute', left: 805, top: 730, width: 300}} />
          <Img src={assets.tvWarning} style={{position: 'absolute', left: 745, top: 255, width: 420, opacity: ease(frame, [18, 28], [0, 1])}} />
          <RoomLayers />
        </SceneFrame>
      );

    case 'activity_tv_insert':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <ScreenPanel>
            <Img src={assets.activityBanner} style={{position: 'absolute', left: 120, top: 70, width: 820}} />
            <div style={{position: 'absolute', left: 150, top: 365, fontSize: 48, fontWeight: 900}}>暗号：早餐自由</div>
            <div style={{position: 'absolute', left: 150, top: 455, fontSize: 36}}>凭暗号领取双倍早餐券</div>
          </ScreenPanel>
        </SceneFrame>
      );

    case 'activity_reaction':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Character src={assets.xiaoming} x={720} y={350} scale={1.12} lean={lean} />
          <Img src={assets.exclaim} style={{position: 'absolute', left: 970, top: 215, width: 190}} />
        </SceneFrame>
      );

    case 'phone_pickup_insert':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Img src={assets.phoneTable} style={{position: 'absolute', left: 820, top: 400, width: 250}} />
          <HandProxy x={ease(frame, [0, 24], [1240, 925])} y={455} scale={0.9} rotate={-15} />
        </SceneFrame>
      );

    case 'phone_screen_insert':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Img src={assets.phoneCall} style={{position: 'absolute', left: 690, top: 150, width: 540}} />
        </SceneFrame>
      );

    case 'caller_close':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Character src={assets.xiaoming} x={695} y={350} scale={1.12} lean={lean} />
          <Img src={assets.phoneCall} style={{position: 'absolute', left: 1080, top: 330, width: 220}} />
        </SceneFrame>
      );

    case 'receiver_close':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Character src={assets.friend} x={720} y={355} scale={1.1} flip lean={-lean} />
          <Img src={assets.bubbleRight} style={{position: 'absolute', left: 990, top: 235, width: 420}} />
        </SceneFrame>
      );

    case 'phone_split_dialogue':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Img src={assets.speedLines} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0.42}} />
          <Character src={assets.xiaoming} x={430} y={420} scale={0.85} lean={lean} />
          <Character src={assets.friend} x={1230} y={420} scale={0.85} flip lean={-lean} />
          <Img src={assets.bubbleLeft} style={{position: 'absolute', left: 250, top: 170, width: 470}} />
          <Img src={assets.bubbleRight} style={{position: 'absolute', right: 250, top: 170, width: 470}} />
        </SceneFrame>
      );

    case 'event_wide':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <EventExtras />
          <Character src={assets.xiaoming} x={ease(frame, [0, 35], [380, 570])} y={500} scale={0.72} />
        </SceneFrame>
      );

    case 'over_shoulder_meet':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <EventExtras />
          <Character src={assets.xiaoming} x={350} y={455} scale={1.0} />
          <Character src={assets.friend} x={1080} y={500} scale={0.76} flip />
        </SceneFrame>
      );

    case 'event_notice_insert':
      return (
        <SceneFrame shot={shot}>
          <AbsoluteFill style={{background: '#f5e7ac'}} />
          <div
            style={{
              position: 'absolute',
              left: 360,
              top: 125,
              width: 1200,
              height: 640,
              border: '16px solid #1f1b18',
              borderRadius: 28,
              background: '#fff1c5',
              fontFamily: 'Microsoft YaHei, sans-serif',
              color: '#2a2118',
              boxShadow: '0 22px 38px rgba(0,0,0,.25)',
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                height: 112,
                background: '#e84c42',
                color: '#fff8e8',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 60,
                fontWeight: 900,
              }}
            >
              下午三点 活动现场见
            </div>
            <div style={{fontSize: 54, fontWeight: 900, padding: '72px 90px 28px'}}>
              凭暗号领取双倍早餐券
            </div>
            <div style={{fontSize: 43, padding: '0 90px 24px'}}>
              暗号：早餐自由
            </div>
            <div style={{fontSize: 36, padding: '0 90px', lineHeight: 1.45}}>
              排队请保持理智，早餐不负责拯救世界。
            </div>
          </div>
        </SceneFrame>
      );

    case 'event_two_shot':
      return (
        <SceneFrame shot={shot} bg={bg}>
          <EventExtras />
          <Character src={assets.xiaoming} x={580} y={500} scale={0.76} />
          <Character src={assets.friend} x={1010} y={500} scale={0.76} flip />
          <Img src={assets.question} style={{position: 'absolute', left: 910, top: 335, width: 145}} />
        </SceneFrame>
      );

    default:
      return (
        <SceneFrame shot={shot} bg={bg}>
          <Character src={assets.xiaoming} x={730} y={470} scale={0.85} />
          <RoomLayers />
        </SceneFrame>
      );
  }
};

const ShotScene: React.FC<{shot: Shot}> = ({shot}) => {
  const frame = useCurrentFrame();
  return renderShot(shot, frame);
};

export const CinematicInteractionTest: React.FC = () => {
  let cursor = 0;
  return (
    <AbsoluteFill style={{background: '#101014'}}>
      {sequence.shots.map((shot) => {
        const from = cursor;
        const durationInFrames = shot.duration * CINEMATIC_TEST_FPS;
        cursor += durationInFrames;
        return (
          <Sequence key={shot.shot_id} from={from} durationInFrames={durationInFrames}>
            <ShotScene shot={shot} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
