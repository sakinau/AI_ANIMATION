import React from 'react';
import {Composition} from 'remotion';
import story from '../project/story.json';
import {
  AN_AE_FPS,
  AN_AE_TOTAL_FRAMES,
  AnAeMagicTest,
} from './AnAeMagicTest';
import {
  MAGIC_FPS,
  MAGIC_TOTAL_FRAMES,
  MagicDeliveryClimax,
} from './MagicDelivery';
import {
  STATE_MACHINE_FPS,
  STATE_MACHINE_TOTAL_FRAMES,
  StateMachineWukongTest,
} from './StateMachineWukongTest';
import {
  INTERACTION_TEST_FPS,
  INTERACTION_TEST_TOTAL_FRAMES,
  SceneInteractionTest,
} from './SceneInteractionTest';
import {
  CINEMATIC_TEST_FPS,
  CINEMATIC_TEST_TOTAL_FRAMES,
  CinematicInteractionTest,
} from './CinematicInteractionTest';
import {MidnightRules} from './Story';

export const FPS = 12;
export const TOTAL_FRAMES = story.scenes.reduce(
  (sum, scene) => sum + scene.duration * FPS,
  0,
);

export const Root: React.FC = () => (
  <>
    <Composition
      id="MidnightRules"
      component={MidnightRules}
      durationInFrames={TOTAL_FRAMES}
      fps={FPS}
      width={720}
      height={1280}
    />
    <Composition
      id="MagicDeliveryClimax"
      component={MagicDeliveryClimax}
      durationInFrames={MAGIC_TOTAL_FRAMES}
      fps={MAGIC_FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="AnAeMagicTest"
      component={AnAeMagicTest}
      durationInFrames={AN_AE_TOTAL_FRAMES}
      fps={AN_AE_FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="StateMachineWukongTest"
      component={StateMachineWukongTest}
      durationInFrames={STATE_MACHINE_TOTAL_FRAMES}
      fps={STATE_MACHINE_FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="SceneInteractionTest"
      component={SceneInteractionTest}
      durationInFrames={INTERACTION_TEST_TOTAL_FRAMES}
      fps={INTERACTION_TEST_FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="CinematicInteractionTest"
      component={CinematicInteractionTest}
      durationInFrames={CINEMATIC_TEST_TOTAL_FRAMES}
      fps={CINEMATIC_TEST_FPS}
      width={1920}
      height={1080}
    />
  </>
);
