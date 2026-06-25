import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const story = JSON.parse(fs.readFileSync(path.join(root, 'project', 'story.json'), 'utf8'));
const animationSystem = JSON.parse(fs.readFileSync(path.join(root, 'project', 'animation-presets.json'), 'utf8'));
const assetCalibration = JSON.parse(fs.readFileSync(path.join(root, 'project', 'asset-calibration.json'), 'utf8'));
const output = path.join(root, 'ae', 'Build_Midnight_Rules.jsx');

const jsx = `#target aftereffects
#targetengine "midnightRulesBuilder"

(function () {
  var STORY = ${JSON.stringify(story)};
  var ANIMATION = ${JSON.stringify(animationSystem)};
  var CALIBRATION = ${JSON.stringify(assetCalibration)};
  var FPS = 12;
  var WIDTH = 720;
  var HEIGHT = 1280;
  var ROOT = File($.fileName).parent.parent;

  function color(hex) {
    var value = hex.replace('#', '');
    return [
      parseInt(value.substr(0, 2), 16) / 255,
      parseInt(value.substr(2, 2), 16) / 255,
      parseInt(value.substr(4, 2), 16) / 255
    ];
  }

  function importAsset(relPath, folder) {
    var file = new File(ROOT.fsName + '/' + relPath);
    if (!file.exists) throw new Error('Missing asset: ' + file.fsName);
    var item = app.project.importFile(new ImportOptions(file));
    item.parentFolder = folder;
    return item;
  }

  function rect(comp, name, size, fillHex, position, roundness) {
    var layer = comp.layers.addShape();
    layer.name = name;
    var group = layer.property('ADBE Root Vectors Group').addProperty('ADBE Vector Group');
    group.name = name + '_SHAPE';
    var vectors = group.property('ADBE Vectors Group');
    var shape = vectors.addProperty('ADBE Vector Shape - Rect');
    shape.property('ADBE Vector Rect Size').setValue(size);
    shape.property('ADBE Vector Rect Roundness').setValue(roundness || 0);
    var fill = vectors.addProperty('ADBE Vector Graphic - Fill');
    fill.property('ADBE Vector Fill Color').setValue(color(fillHex));
    var stroke = vectors.addProperty('ADBE Vector Graphic - Stroke');
    stroke.property('ADBE Vector Stroke Color').setValue(color('#111615'));
    stroke.property('ADBE Vector Stroke Width').setValue(5);
    layer.property('ADBE Transform Group').property('ADBE Position').setValue(position);
    return layer;
  }

  function ellipse(comp, name, size, fillHex, position) {
    var layer = comp.layers.addShape();
    layer.name = name;
    var group = layer.property('ADBE Root Vectors Group').addProperty('ADBE Vector Group');
    group.name = name + '_SHAPE';
    var vectors = group.property('ADBE Vectors Group');
    var shape = vectors.addProperty('ADBE Vector Shape - Ellipse');
    shape.property('ADBE Vector Ellipse Size').setValue(size);
    var fill = vectors.addProperty('ADBE Vector Graphic - Fill');
    fill.property('ADBE Vector Fill Color').setValue(color(fillHex));
    var stroke = vectors.addProperty('ADBE Vector Graphic - Stroke');
    stroke.property('ADBE Vector Stroke Color').setValue(color('#111615'));
    stroke.property('ADBE Vector Stroke Width').setValue(5);
    layer.property('ADBE Transform Group').property('ADBE Position').setValue(position);
    return layer;
  }

  function addText(comp, name, text, position, fontSize, fillHex) {
    var layer = comp.layers.addText(text);
    layer.name = name;
    var doc = layer.property('ADBE Text Properties').property('ADBE Text Document').value;
    doc.fontSize = fontSize;
    doc.fillColor = color(fillHex);
    doc.font = 'MicrosoftYaHei';
    doc.applyFill = true;
    layer.property('ADBE Text Properties').property('ADBE Text Document').setValue(doc);
    layer.property('ADBE Transform Group').property('ADBE Position').setValue(position);
    return layer;
  }

  function addBoxText(comp, name, text, position, boxSize, fontSize, fillHex) {
    var layer = comp.layers.addBoxText(boxSize, text);
    layer.name = name;
    var doc = layer.property('ADBE Text Properties').property('ADBE Text Document').value;
    doc.fontSize = fontSize;
    doc.fillColor = color(fillHex);
    doc.font = 'MicrosoftYaHei';
    doc.applyFill = true;
    layer.property('ADBE Text Properties').property('ADBE Text Document').setValue(doc);
    layer.property('ADBE Transform Group').property('ADBE Position').setValue(position);
    return layer;
  }

  function key(prop, times, values) {
    for (var i = 0; i < times.length; i++) prop.setValueAtTime(times[i], values[i]);
  }

  function expressionFile(expression) {
    var files = {
      neutral: '表情-平静.png',
      serious: '表情-怀疑.png',
      worried: '表情-恐惧.png',
      shocked: '表情-惊讶.png',
      afraid: '表情-恐惧.png',
      blank: '表情-悲伤.png',
      smile: '表情-邪笑.png'
    };
    return files[expression] || files.neutral;
  }

  function applyMotion(layer, scene, basePosition) {
    var motionName = ANIMATION.actionMotion[scene.action] || 'still';
    var motion = ANIMATION.motions[motionName] || ANIMATION.motions.still;
    var seconds = Math.max(1, motion.durationFrames) / FPS;
    var start = [basePosition[0] + motion.fromX, basePosition[1] + motion.fromY];
    var end = [basePosition[0] + motion.toX, basePosition[1] + motion.toY];
    var transform = layer.property('ADBE Transform Group');
    transform.property('ADBE Position').setValue(end);
    transform.property('ADBE Opacity').setValue(motion.toOpacity * 100);
    if (motionName !== 'still') {
      key(transform.property('ADBE Position'), [0, seconds], [start, end]);
      key(transform.property('ADBE Opacity'), [0, seconds], [motion.fromOpacity * 100, motion.toOpacity * 100]);
    }
  }

  function buildGuard(comp, scene) {
    var legsL = rect(comp, 'CHAR_LinMo_Leg_L', [62, 195], '#111615', [310, 875], 28);
    var legsR = rect(comp, 'CHAR_LinMo_Leg_R', [62, 195], '#111615', [395, 875], 28);
    var armL = rect(comp, 'CHAR_LinMo_Arm_L', [58, 190], '#203b37', [280, 690], 28);
    var armR = rect(comp, 'CHAR_LinMo_Arm_R', [58, 190], '#203b37', [425, 690], 28);
    var torso = rect(comp, 'CHAR_LinMo_Torso', [170, 225], '#355b55', [352, 710], 18);
    var head = ellipse(comp, 'CHAR_LinMo_Head', [122, 132], '#d6a982', [352, 525]);
    rect(comp, 'CHAR_LinMo_Hat', [156, 54], '#203b37', [352, 468], 18);

    var eyeL = ellipse(comp, 'FACE_' + scene.expression + '_Eye_L', [12, 8], '#111615', [330, 520]);
    var eyeR = ellipse(comp, 'FACE_' + scene.expression + '_Eye_R', [12, 8], '#111615', [374, 520]);
    var mouthSize = scene.expression === 'shocked' ? [18, 22] : [30, 7];
    ellipse(comp, 'FACE_' + scene.expression + '_Mouth', mouthSize, '#111615', [352, 558]);
    head.moveBefore(eyeL);

    var rotL = armL.property('ADBE Transform Group').property('ADBE Rotate Z');
    var rotR = armR.property('ADBE Transform Group').property('ADBE Rotate Z');
    if (scene.action === 'point') key(rotR, [0, 1.2, 12], [8, -78, -78]);
    if (scene.action === 'read') {
      key(rotL, [0, 1], [-8, 48]);
      key(rotR, [0, 1], [8, -48]);
      rect(comp, 'PROP_Rule_Paper', [138, 96], '#e7e1d2', [352, 735], 2);
    }
    if (scene.action === 'walk' || scene.action === 'run') {
      var speed = scene.action === 'run' ? 0.22 : 0.36;
      for (var t = 0; t <= scene.duration; t += speed) {
        var phase = Math.round(t / speed) % 2 === 0 ? 1 : -1;
        rotL.setValueAtTime(t, phase * 24);
        rotR.setValueAtTime(t, -phase * 24);
        legsL.property('ADBE Transform Group').property('ADBE Rotate Z').setValueAtTime(t, -phase * 14);
        legsR.property('ADBE Transform Group').property('ADBE Rotate Z').setValueAtTime(t, phase * 14);
      }
    }
    if (scene.action === 'enter') {
      var parts = [legsL, legsR, armL, armR, torso, head, eyeL, eyeR];
      for (var p = 0; p < parts.length; p++) {
        var position = parts[p].property('ADBE Transform Group').property('ADBE Position');
        var finalPos = position.value;
        key(position, [0, 2.8], [[finalPos[0] - 350, finalPos[1]], finalPos]);
      }
    }
    return torso;
  }

  function buildAssetGuard(comp, scene, assetsFolder) {
    var poseBeats = ANIMATION.poseBeats[scene.action] || ANIMATION.poseBeats.idle;
    var pose = poseBeats[0];
    var stage = CALIBRATION.stage;
    var meta = CALIBRATION.poses[pose];
    if (!meta) throw new Error('Missing calibration for pose: ' + pose);
    var rel = 'public/免费素材库/处理后/人物/橙衣男/橙衣男-' + pose + '.png';
    var actorItem = importAsset(rel, assetsFolder);
    var actor = comp.layers.add(actorItem);
    actor.name = 'CHAR_LinMo_FREE_POSE_' + pose;
    var actorScale = stage.targetHeight / actorItem.height * 100;
    var scale = stage.targetHeight / meta.height;
    var imageWidth = meta.width * scale;
    var imageLeft = stage.left + (stage.wrapperWidth - imageWidth) / 2;
    var imageTop = stage.top + stage.wrapperHeight - stage.targetHeight;
    var actorPosition = [imageLeft + imageWidth / 2, imageTop + stage.targetHeight / 2];
    actor.property('ADBE Transform Group').property('ADBE Scale').setValue([actorScale, actorScale]);
    applyMotion(actor, scene, actorPosition);

    var faceRel = 'public/免费素材库/处理后/表情/' + expressionFile(scene.expression);
    var faceItem = importAsset(faceRel, assetsFolder);
    var face = comp.layers.add(faceItem);
    face.name = 'FACE_' + scene.expression + '_CALIBRATED';
    var faceSize = meta.face.size * scale;
    var faceLeft = stage.left + (stage.wrapperWidth - imageWidth) / 2 + meta.face.centerX * scale - faceSize / 2;
    var faceTop = imageTop + meta.face.centerY * scale - faceSize / 2;
    var faceScale = faceSize / faceItem.height * 100;
    face.property('ADBE Transform Group').property('ADBE Scale').setValue([faceScale, faceScale]);
    applyMotion(face, scene, [faceLeft + faceSize / 2, faceTop + faceSize / 2]);
    face.moveBefore(actor);
    return actor;
  }

  function addCaptions(comp, scene) {
    for (var i = 0; i < scene.beats.length; i++) {
      var plate = rect(comp, 'CAPTION_BG_' + (i + 1), [650, 170], '#111615', [360, 1130], 4);
      plate.property('ADBE Transform Group').property('ADBE Opacity').setValue(88);
      plate.inPoint = i * 5;
      plate.outPoint = (i + 1) * 5;
      var text = addBoxText(comp, 'CAPTION_' + (i + 1), scene.beats[i], [65, 1085], [590, 140], 34, '#f1eee5');
      text.inPoint = i * 5;
      text.outPoint = (i + 1) * 5;
    }
  }

  function buildScene(scene, assetsFolder, scenesFolder) {
    var comp = app.project.items.addComp(scene.id + '_' + scene.title, WIDTH, HEIGHT, 1, scene.duration, FPS);
    comp.parentFolder = scenesFolder;
    var rel = scene.id === 'S19' || scene.id === 'S20'
      ? 'public/免费素材库/背景/旧学校.png'
      : scene.location === 'corridor'
        ? 'public/免费素材库/背景/旧工厂.png'
        : 'public/免费素材库/背景/旧电影院.png';
    var bgItem = importAsset(rel, assetsFolder);
    var bg = comp.layers.add(bgItem);
    bg.name = 'BG_' + scene.location;
    var scale = Math.max(WIDTH / bgItem.width, HEIGHT / bgItem.height) * 100;
    bg.property('ADBE Transform Group').property('ADBE Scale').setValue([scale, scale]);
    key(bg.property('ADBE Transform Group').property('ADBE Scale'), [0, scene.duration], [[scale, scale], [scale * 1.07, scale * 1.07]]);
    var grade = comp.layers.addSolid(color('#07110f'), 'GRADE_DarkOverlay', WIDTH, HEIGHT, 1, scene.duration);
    grade.opacity.setValue(22);
    buildAssetGuard(comp, scene, assetsFolder);
    if (scene.fx !== 'none') {
      var fx = comp.layers.addSolid(color(scene.fx === 'final' || scene.fx === 'red' ? '#8e0010' : '#101f1d'), 'FX_' + scene.fx, WIDTH, HEIGHT, 1, scene.duration);
      fx.blendingMode = BlendingMode.ADD;
      key(fx.opacity, [0, 0.5, 1, scene.duration], [0, 18, 4, 8]);
    }
    addText(comp, 'SHOT_LABEL', scene.id + ' / ' + scene.title, [38, 72], 24, '#d7e1d8');
    addCaptions(comp, scene);
    return comp;
  }

  app.beginUndoGroup('Build Midnight Rules');
  try {
    app.newProject();
    var assetsFolder = app.project.items.addFolder('01_免费素材库');
    var scenesFolder = app.project.items.addFolder('02_镜头合成_可编辑');
    var masterFolder = app.project.items.addFolder('03_主时间线');
    var total = 0;
    for (var i = 0; i < STORY.scenes.length; i++) total += STORY.scenes[i].duration;
    var master = app.project.items.addComp('MASTER_午夜值班守则_5min', WIDTH, HEIGHT, 1, total, FPS);
    master.parentFolder = masterFolder;
    var cursor = 0;
    for (var s = 0; s < STORY.scenes.length; s++) {
      var sceneComp = buildScene(STORY.scenes[s], assetsFolder, scenesFolder);
      var sceneLayer = master.layers.add(sceneComp);
      sceneLayer.name = STORY.scenes[s].id + '_EDIT_IN_PRECOMP';
      sceneLayer.startTime = cursor;
      sceneLayer.inPoint = cursor;
      sceneLayer.outPoint = cursor + STORY.scenes[s].duration;
      cursor += STORY.scenes[s].duration;
    }
    var outputDir = new Folder(ROOT.fsName + '/output');
    if (!outputDir.exists) outputDir.create();
    var aep = new File(outputDir.fsName + '/午夜值班守则-可编辑.aep');
    app.project.save(aep);
    alert('完成：已创建20个可编辑镜头并保存到\\n' + aep.fsName);
  } catch (err) {
    alert('创建失败：' + err.toString());
    throw err;
  } finally {
    app.endUndoGroup();
  }
})();
`;

fs.writeFileSync(output, jsx, 'utf8');
console.log(`Generated ${output}`);
