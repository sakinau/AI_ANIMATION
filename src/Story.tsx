import React from 'react';
import {
  AbsoluteFill,
  Easing,
  Img,
  Sequence,
  interpolate,
  random,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import animationSystem from '../project/animation-presets.json';
import assetCalibration from '../project/asset-calibration.json';
import story from '../project/story.json';
import {FPS} from './Root';

type Scene = (typeof story.scenes)[number];
type Expression = Scene['expression'];

const colors = {
  ink: '#111615',
  paper: '#e7e1d2',
  uniform: '#355b55',
  uniformDark: '#203b37',
  skin: '#d6a982',
  red: '#b31f2a',
  light: '#d7e1d8',
};

const ease = (frame: number, input: number[], output: number[]) =>
  interpolate(frame, input, output, {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

const expressionFiles: Record<Expression, string> = {
  neutral: '表情-平静.png',
  serious: '表情-怀疑.png',
  worried: '表情-恐惧.png',
  shocked: '表情-惊讶.png',
  afraid: '表情-恐惧.png',
  blank: '表情-悲伤.png',
  smile: '表情-邪笑.png',
};

type PoseName = keyof typeof assetCalibration.poses;

const poseBeatMap = animationSystem.poseBeats as Record<string, PoseName[]>;
const expressionBeatMap = animationSystem.expressionBeats as Record<string, Expression[]>;
const actionMotionMap = animationSystem.actionMotion as Record<string, string>;
const motionMap = animationSystem.motions as Record<
  string,
  {
    durationFrames: number;
    fromX: number;
    toX: number;
    fromY: number;
    toY: number;
    fromOpacity: number;
    toOpacity: number;
  }
>;

const CalibratedPose: React.FC<{
  pose: PoseName;
  expression: Expression;
  opacity: number;
}> = ({pose, expression, opacity}) => {
  const stage = assetCalibration.stage;
  const meta = assetCalibration.poses[pose];
  const scale = stage.targetHeight / meta.height;
  const imageWidth = meta.width * scale;
  const imageLeft = (stage.wrapperWidth - imageWidth) / 2;
  const imageTop = stage.wrapperHeight - stage.targetHeight;
  const faceSize = meta.face.size * scale;
  const faceLeft = imageLeft + meta.face.centerX * scale - faceSize / 2;
  const faceTop = imageTop + meta.face.centerY * scale - faceSize / 2;
  return (
    <div style={{position: 'absolute', inset: 0, opacity}}>
      <Img
        src={staticFile(`免费素材库/处理后/人物/橙衣男/橙衣男-${pose}.png`)}
        style={{
          position: 'absolute',
          left: imageLeft,
          top: imageTop,
          width: imageWidth,
          height: stage.targetHeight,
        }}
      />
      <Img
        src={staticFile(`免费素材库/处理后/表情/${expressionFiles[expression]}`)}
        style={{
          position: 'absolute',
          left: faceLeft,
          top: faceTop,
          width: faceSize,
          height: faceSize,
          objectFit: 'contain',
        }}
      />
    </div>
  );
};

const Guard: React.FC<{scene: Scene; localFrame: number; ghost?: boolean}> = ({
  scene,
  localFrame,
  ghost = false,
}) => {
  const beatFrames = 5 * FPS;
  const expressionStepFrames = Math.round(2.5 * FPS);
  const beatIndex = Math.min(2, Math.floor(localFrame / beatFrames));
  const beatLocalFrame = localFrame % beatFrames;
  const poses = poseBeatMap[scene.action] ?? poseBeatMap.idle;
  const expressions = expressionBeatMap[scene.expression] ?? expressionBeatMap.neutral;
  const expressionSequence = [
    expressions[0],
    expressions[1],
    expressions[1],
    expressions[2],
    expressions[2],
    expressions[0],
  ];
  const expressionStep = Math.min(
    expressionSequence.length - 1,
    Math.floor(localFrame / expressionStepFrames),
  );
  const pose = poses[beatIndex];
  const expression = expressionSequence[expressionStep];
  const previousPose = beatIndex === 0 ? pose : poses[beatIndex - 1];
  const previousExpression =
    expressionStep === 0 ? expression : expressionSequence[expressionStep - 1];
  const poseMix = beatIndex === 0 ? 1 : ease(beatLocalFrame, [0, 4], [0, 1]);
  const motionName = actionMotionMap[scene.action] ?? 'still';
  const motion = motionMap[motionName];
  const motionProgress = interpolate(
    localFrame,
    [0, Math.max(1, motion.durationFrames)],
    [0, 1],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.bezier(0.22, 1, 0.36, 1),
    },
  );
  const moveX = interpolate(motionProgress, [0, 1], [motion.fromX, motion.toX]);
  const moveY = interpolate(motionProgress, [0, 1], [motion.fromY, motion.toY]);
  const motionOpacity = interpolate(
    motionProgress,
    [0, 1],
    [motion.fromOpacity, motion.toOpacity],
  );
  const read = scene.action === 'read';
  const opacity = (ghost ? 0.52 : 1) * motionOpacity;
  const stage = assetCalibration.stage;
  return (
    <div
      style={{
        position: 'absolute',
        left: ghost ? 388 : stage.left,
        top: stage.top,
        width: stage.wrapperWidth,
        height: stage.wrapperHeight,
        opacity,
        filter: ghost ? 'brightness(0) drop-shadow(0 0 18px #7c111b)' : 'drop-shadow(0 18px 14px rgba(0,0,0,.45))',
        transform: `translate(${moveX}px, ${moveY}px) scale(${ghost ? 0.96 : 1})`,
      }}
    >
      {ghost ? (
        <Img
          src={staticFile('免费素材库/处理后/人物/黑西装-站姿.png')}
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            objectPosition: 'center bottom',
          }}
        />
      ) : (
        <>
          {beatIndex > 0 ? (
            <CalibratedPose pose={previousPose} expression={previousExpression} opacity={1 - poseMix} />
          ) : null}
          <CalibratedPose pose={pose} expression={expression} opacity={poseMix} />
        </>
      )}
      {read ? (
        <div style={{position: 'absolute', left: 88, top: 300, width: 124, height: 90, background: colors.paper, border: `4px solid ${colors.ink}`, transform: 'rotate(-4deg)', boxShadow: '0 6px 10px rgba(0,0,0,.25)'}} />
      ) : null}
    </div>
  );
};

const EffectSprite: React.FC<{scene: Scene; localFrame: number}> = ({scene, localFrame}) => {
  const effect =
    scene.fx === 'chase'
      ? '一溜烟'
      : ['shadow', 'breath'].includes(scene.fx)
        ? '烟阵圈'
        : ['pulse', 'glitch'].includes(scene.fx)
          ? '大灰尘'
          : ['red', 'final', 'write'].includes(scene.fx)
            ? '撞击星'
            : null;
  if (!effect) return null;
  const count = effect === '撞击星' ? 6 : 24;
  const index = Math.floor(localFrame / 2) % count;
  return (
    <Img
      src={staticFile(`免费素材库/处理后/特效帧/${effect}/frame-${String(index).padStart(3, '0')}.png`)}
      style={{
        position: 'absolute',
        right: effect === '一溜烟' ? 30 : 90,
        bottom: effect === '一溜烟' ? 240 : 360,
        width: effect === '一溜烟' ? 500 : 430,
        opacity: 0.82,
        mixBlendMode: 'screen',
      }}
    />
  );
};

const Effects: React.FC<{scene: Scene; localFrame: number}> = ({scene, localFrame}) => {
  const pulse = (Math.sin(localFrame * 0.5) + 1) / 2;
  const red = ['red', 'final', 'chase', 'write'].includes(scene.fx);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {red ? <AbsoluteFill style={{background: `rgba(150,0,12,${0.08 + pulse * 0.13})`, mixBlendMode: 'screen'}} /> : null}
      {scene.fx === 'glitch' ? (
        <AbsoluteFill style={{transform: `translateX(${(random(localFrame) - 0.5) * 18}px)`, boxShadow: `inset ${pulse * 18}px 0 rgba(210,20,30,.24), inset -${pulse * 14}px 0 rgba(20,180,170,.17)`}} />
      ) : null}
      {scene.fx === 'flicker' ? <AbsoluteFill style={{background: `rgba(0,0,0,${localFrame % 19 < 3 ? 0.48 : 0.08})`}} /> : null}
      {scene.fx === 'clock' ? (
        <div style={{position: 'absolute', right: 52, top: 150, color: '#f2eadd', fontSize: 72, fontFamily: 'monospace', textShadow: '0 0 16px #b31f2a'}}>00:00</div>
      ) : null}
      {scene.fx === 'elevator' ? (
        <div style={{position: 'absolute', left: 286, top: 240, padding: '8px 18px', background: '#17090a', color: '#ff2439', font: 'bold 58px monospace', border: '4px solid #3d3432'}}>-1</div>
      ) : null}
      {scene.fx === 'rule' || scene.fx === 'write' ? (
        <div style={{position: 'absolute', right: 44, top: 230, width: 250, padding: 22, background: 'rgba(231,225,210,.92)', color: '#251e1a', border: '4px solid #2b2521', transform: `rotate(${Math.sin(localFrame / 20) * 1.5}deg)`, fontSize: 27, lineHeight: 1.35}}>
          值班守则<br /><span style={{color: colors.red}}>{scene.title}</span>
        </div>
      ) : null}
      {scene.fx === 'shadow' || scene.fx === 'chase' || scene.fx === 'breath' ? <Guard scene={scene} localFrame={localFrame + 8} ghost /> : null}
      <EffectSprite scene={scene} localFrame={localFrame} />
      {['pulse', 'breath'].includes(scene.fx) ? <AbsoluteFill style={{boxShadow: `inset 0 0 ${80 + pulse * 120}px rgba(120,0,10,.65)`}} /> : null}
      <AbsoluteFill style={{background: 'linear-gradient(to bottom, rgba(0,0,0,.12), transparent 25%, transparent 70%, rgba(0,0,0,.52))'}} />
    </AbsoluteFill>
  );
};

const Caption: React.FC<{scene: Scene; localFrame: number}> = ({scene, localFrame}) => {
  const index = Math.min(2, Math.floor(localFrame / (5 * FPS)));
  const within = localFrame % (5 * FPS);
  const opacity = ease(within, [0, 5, 5 * FPS - 8, 5 * FPS], [0, 1, 1, 0]);
  return (
    <div style={{position: 'absolute', left: 38, right: 38, bottom: 66, minHeight: 166, padding: '28px 32px', background: 'rgba(8,12,12,.9)', borderLeft: `7px solid ${colors.red}`, color: '#f1eee5', fontFamily: 'Microsoft YaHei, sans-serif', fontSize: 38, lineHeight: 1.48, opacity, boxShadow: '0 8px 30px rgba(0,0,0,.45)'}}>
      {scene.beats[index]}
    </div>
  );
};

const SceneView: React.FC<{scene: Scene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const isCorridor = scene.location === 'corridor';
  const backgroundFile =
    scene.id === 'S19' || scene.id === 'S20'
      ? '免费素材库/背景/旧学校.png'
      : isCorridor
        ? '免费素材库/背景/旧工厂.png'
        : '免费素材库/背景/旧电影院.png';
  const zoom = ease(frame, [0, scene.duration * FPS], [1.025, 1.055]);
  const shake = ['chase', 'glitch', 'final'].includes(scene.fx) ? (random(frame) - 0.5) * 12 : 0;
  return (
    <AbsoluteFill style={{background: '#080b0b', overflow: 'hidden', transform: `translate(${shake}px, ${-shake * 0.4}px)`}}>
      <Img
        src={staticFile(backgroundFile)}
        style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`, filter: scene.id === 'S19' ? 'brightness(.72) sepia(.2)' : 'brightness(.34) saturate(.6) hue-rotate(8deg)'}}
      />
      <AbsoluteFill style={{background: 'rgba(4,12,11,.17)'}} />
      <div style={{position: 'absolute', left: 34, top: 42, color: colors.light, fontFamily: 'Microsoft YaHei, sans-serif', fontSize: 24, borderTop: `4px solid ${colors.red}`, paddingTop: 9, textShadow: '0 2px 7px #000'}}>
        {scene.id} / {scene.title}
      </div>
      <Guard scene={scene} localFrame={frame} />
      <Effects scene={scene} localFrame={frame} />
      <Caption scene={scene} localFrame={frame} />
    </AbsoluteFill>
  );
};

export const MidnightRules: React.FC = () => {
  let cursor = 0;
  return (
    <AbsoluteFill style={{background: colors.ink}}>
      {story.scenes.map((scene) => {
        const from = cursor;
        const duration = scene.duration * FPS;
        cursor += duration;
        return (
          <Sequence key={scene.id} from={from} durationInFrames={duration}>
            <SceneView scene={scene} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
