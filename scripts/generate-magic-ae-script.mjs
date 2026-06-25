import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const sequence = JSON.parse(
  fs.readFileSync(
    path.join(root, 'projects', 'magic-delivery', 'shots', 'climax_60s.json'),
    'utf8',
  ),
);
const output = path.join(root, 'ae', 'Build_Magic_Delivery.jsx');

const jsx = `#target aftereffects
#targetengine "magicDeliveryBuilder"

(function () {
  var SEQUENCE = ${JSON.stringify(sequence)};
  var FPS = SEQUENCE.fps || 12;
  var WIDTH = SEQUENCE.format && SEQUENCE.format.width ? SEQUENCE.format.width : 1920;
  var HEIGHT = SEQUENCE.format && SEQUENCE.format.height ? SEQUENCE.format.height : 1080;
  var CX = WIDTH / 2;
  var CY = HEIGHT / 2;
  var ROOT = File($.fileName).parent.parent;

  function color(hex) {
    var value = hex.replace('#', '');
    return [
      parseInt(value.substr(0, 2), 16) / 255,
      parseInt(value.substr(2, 2), 16) / 255,
      parseInt(value.substr(4, 2), 16) / 255
    ];
  }

  function key(prop, times, values) {
    for (var i = 0; i < times.length; i++) prop.setValueAtTime(times[i], values[i]);
  }

  function rect(comp, name, size, fillHex, position, opacity) {
    var layer = comp.layers.addShape();
    layer.name = name;
    var group = layer.property('ADBE Root Vectors Group').addProperty('ADBE Vector Group');
    var vectors = group.property('ADBE Vectors Group');
    vectors.addProperty('ADBE Vector Shape - Rect').property('ADBE Vector Rect Size').setValue(size);
    vectors.addProperty('ADBE Vector Graphic - Fill').property('ADBE Vector Fill Color').setValue(color(fillHex));
    var stroke = vectors.addProperty('ADBE Vector Graphic - Stroke');
    stroke.property('ADBE Vector Stroke Color').setValue(color('#111015'));
    stroke.property('ADBE Vector Stroke Width').setValue(5);
    layer.property('ADBE Transform Group').property('ADBE Position').setValue(position);
    if (opacity !== undefined) layer.property('ADBE Transform Group').property('ADBE Opacity').setValue(opacity);
    return layer;
  }

  function ellipse(comp, name, size, fillHex, position) {
    var layer = comp.layers.addShape();
    layer.name = name;
    var group = layer.property('ADBE Root Vectors Group').addProperty('ADBE Vector Group');
    var vectors = group.property('ADBE Vectors Group');
    vectors.addProperty('ADBE Vector Shape - Ellipse').property('ADBE Vector Ellipse Size').setValue(size);
    vectors.addProperty('ADBE Vector Graphic - Fill').property('ADBE Vector Fill Color').setValue(color(fillHex));
    layer.property('ADBE Transform Group').property('ADBE Position').setValue(position);
    return layer;
  }

  function textLayer(comp, name, text, position, size, fillHex, boxSize) {
    var layer = boxSize ? comp.layers.addBoxText(boxSize, text) : comp.layers.addText(text);
    layer.name = name;
    var doc = layer.property('ADBE Text Properties').property('ADBE Text Document').value;
    doc.fontSize = size;
    doc.fillColor = color(fillHex);
    doc.font = 'MicrosoftYaHei';
    doc.applyFill = true;
    layer.property('ADBE Text Properties').property('ADBE Text Document').setValue(doc);
    layer.property('ADBE Transform Group').property('ADBE Position').setValue(position);
    return layer;
  }

  function addCameraCtrl(comp, shot) {
    var ctrl = comp.layers.addNull();
    ctrl.name = 'CAMERA_CTRL_' + shot.camera.preset + '_' + shot.camera.framing;
    ctrl.property('ADBE Transform Group').property('ADBE Position').setValue([CX, CY]);
    var scale = ctrl.property('ADBE Transform Group').property('ADBE Scale');
    var pos = ctrl.property('ADBE Transform Group').property('ADBE Position');
    var intensity = Math.min(Math.max(shot.camera.motion_intensity || 0.2, 0), 0.75);
    if (shot.camera.preset === 'push_in' || shot.camera.preset === 'insert_closeup') {
      key(scale, [0, shot.duration], [[100, 100], [100 + intensity * 18, 100 + intensity * 18]]);
    } else if (shot.camera.preset === 'pull_back') {
      key(scale, [0, shot.duration], [[100 + intensity * 16, 100 + intensity * 16], [100, 100]]);
    } else if (shot.camera.preset === 'truck_left') {
      key(pos, [0, shot.duration], [[CX + intensity * 120, CY], [CX - intensity * 80, CY]]);
    } else if (shot.camera.preset === 'truck_right' || shot.camera.preset === 'establishing_pan') {
      key(pos, [0, shot.duration], [[CX - intensity * 120, CY], [CX + intensity * 80, CY]]);
    }
    return ctrl;
  }

  function addCharacter(comp, id, x, y, fill, label) {
    var root = comp.layers.addNull();
    root.name = 'CHAR_' + id + '_CTRL';
    root.property('ADBE Transform Group').property('ADBE Position').setValue([x, y]);
    rect(comp, 'CHAR_' + id + '_body', [120, 170], fill, [x, y + 45], 100).parent = root;
    ellipse(comp, 'CHAR_' + id + '_head', [96, 104], '#ffd8c6', [x, y - 75]).parent = root;
    textLayer(comp, 'CHAR_' + id + '_label', label, [x - 70, y - 84], 22, '#111015', [140, 34]).parent = root;
    return root;
  }

  function addCharacters(comp, shot) {
    if (shot.characters.join(',').indexOf('hero') >= 0) {
      addCharacter(comp, 'hero', WIDTH * 0.28, HEIGHT * 0.66, '#dfe8ff', 'hero');
      rect(comp, 'PROP_hero_sword', [18, 220], '#e7f4ff', [WIDTH * 0.28 + 82, HEIGHT * 0.54], 100);
    }
    if (shot.characters.join(',').indexOf('delivery_guy') >= 0) {
      addCharacter(comp, 'delivery_guy', WIDTH * 0.48, HEIGHT * 0.66, '#ff8a2a', 'delivery');
      rect(comp, 'PROP_delivery_bag', [110, 72], '#ffd15a', [WIDTH * 0.48 - 70, HEIGHT * 0.80], 100);
    }
    if (shot.characters.join(',').indexOf('demon_king') >= 0) {
      addCharacter(comp, 'demon_king', WIDTH * 0.68, HEIGHT * 0.57, '#b24a64', 'demon');
      rect(comp, 'CHAR_demon_king_cape', [220, 260], '#3d164f', [WIDTH * 0.68, HEIGHT * 0.68], 88);
    }
    if (shot.characters.join(',').indexOf('judge') >= 0) {
      rect(comp, 'CHAR_judge_popup', [560, 250], '#ebf8ff', [CX, HEIGHT * 0.24], 94);
      textLayer(comp, 'CHAR_judge_label', 'sky judge / auto service', [CX - 210, HEIGHT * 0.20], 32, '#12202c', [420, 84]);
    }
  }

  function addUI(comp, shot) {
    rect(comp, 'UI_' + shot.ui, [380, 126], '#fff1d6', [WIDTH * 0.78, HEIGHT * 0.20], 94);
    textLayer(comp, 'UI_TEXT_' + shot.ui, shot.ui, [WIDTH * 0.78 - 145, HEIGHT * 0.17], 30, '#d12335', [300, 84]);
  }

  function addVfx(comp, shot) {
    if (shot.vfx === 'none') return;
    var name = 'VFX_' + shot.vfx + '__reason_' + shot.vfx_reason;
    if (shot.vfx === 'camera_flash' || shot.vfx === 'impact_spark') {
      var fx = comp.layers.addSolid(color('#ffffff'), name, WIDTH, HEIGHT, 1, shot.duration);
      fx.blendingMode = BlendingMode.ADD;
      key(fx.opacity, [0, 0.12, 0.35, shot.duration], [0, 42, 0, 0]);
      return;
    }
    rect(comp, name, [260, 120], '#ffd36a', [WIDTH * 0.70, HEIGHT * 0.38], 35);
  }

  function addCaption(comp, shot) {
    rect(comp, 'SUB_BG', [WIDTH * 0.82, 130], '#08090c', [CX, HEIGHT - 86], 90);
    textLayer(comp, 'SUB_DIALOGUE', shot.speaker + ': ' + shot.dialogue, [WIDTH * 0.10, HEIGHT - 128], 34, '#fff7e8', [WIDTH * 0.80, 104]);
  }

  function buildShot(shot, scenesFolder) {
    var comp = app.project.items.addComp(shot.shot_id + '_' + shot.action, WIDTH, HEIGHT, 1, shot.duration, FPS);
    comp.parentFolder = scenesFolder;
    addCameraCtrl(comp, shot);
    comp.layers.addSolid(color('#170b14'), 'BG_BASE_' + shot.location, WIDTH, HEIGHT, 1, shot.duration);
    rect(comp, 'BG_midground_' + shot.location, [WIDTH * 0.75, 230], '#211220', [CX, HEIGHT * 0.58], 100);
    rect(comp, 'BG_floor', [WIDTH * 1.2, 260], '#141015', [CX, HEIGHT * 0.92], 100);
    addCharacters(comp, shot);
    addUI(comp, shot);
    addVfx(comp, shot);
    addCaption(comp, shot);
    textLayer(comp, 'SHOT_META', shot.shot_id + ' / ' + shot.camera.preset + ' / ' + shot.camera.framing, [40, 40], 22, '#fff1d6', [780, 36]);
    return comp;
  }

  app.beginUndoGroup('Build Magic Delivery Climax');
  try {
    app.newProject();
    var editFolder = app.project.items.addFolder('01_EDIT');
    var scenesFolder = app.project.items.addFolder('02_SHOTS');
    var total = 0;
    for (var i = 0; i < SEQUENCE.shots.length; i++) total += SEQUENCE.shots[i].duration;
    var master = app.project.items.addComp('MASTER_magic_delivery_climax_60s', WIDTH, HEIGHT, 1, total, FPS);
    master.parentFolder = editFolder;
    var cursor = 0;
    for (var s = 0; s < SEQUENCE.shots.length; s++) {
      var shotComp = buildShot(SEQUENCE.shots[s], scenesFolder);
      var layer = master.layers.add(shotComp);
      layer.name = SEQUENCE.shots[s].shot_id + '_EDIT_PRECOMP';
      layer.startTime = cursor;
      layer.inPoint = cursor;
      layer.outPoint = cursor + SEQUENCE.shots[s].duration;
      cursor += SEQUENCE.shots[s].duration;
    }
    var outputDir = new Folder(ROOT.fsName + '/output');
    if (!outputDir.exists) outputDir.create();
    var aep = new File(outputDir.fsName + '/magic-delivery-climax-editable.aep');
    app.project.save(aep);
    alert('Done: editable AE project created.\\n' + aep.fsName);
  } catch (err) {
    alert('Build failed: ' + err.toString());
    throw err;
  } finally {
    app.endUndoGroup();
  }
})();
`;

fs.writeFileSync(output, jsx, 'utf8');
console.log(`Generated ${output}`);
