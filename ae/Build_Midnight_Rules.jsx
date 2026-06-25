#target aftereffects
#targetengine "midnightRulesBuilder"

(function () {
  var STORY = {"title":"午夜值班守则","subtitle":"规则怪谈动画样片","scenes":[{"id":"S01","duration":15,"location":"lobby","title":"新工作","expression":"neutral","action":"enter","fx":"none","beats":["凌晨十一点五十分，林默第一次来到长宁工人电影院值夜班。","交班的老保安一句话也没说，只递来一张折得发白的纸。","纸的最上方写着：值班期间，请严格遵守以下规则。"]},{"id":"S02","duration":15,"location":"lobby","title":"规则一","expression":"serious","action":"read","fx":"rule","beats":["规则一：零点以后，售票大厅只允许出现一名保安。","如果监控中出现第二名保安，不要抬头确认。","立刻关闭三号屏幕，并在桌下数到三十。"]},{"id":"S03","duration":15,"location":"lobby","title":"规则二","expression":"serious","action":"point","fx":"rule","beats":["规则二：电梯显示负一层时，不要按开门键。","这座老影院没有地下室。","无论里面的人怎样呼救，都要回答：维修人员已经下班。"]},{"id":"S04","duration":15,"location":"corridor","title":"规则三","expression":"worried","action":"look","fx":"rule","beats":["规则三：一点十五分，放映厅后的员工通道会多出一扇门。","不要数门，也不要看门牌。","听到有人叫你的名字，就把手电筒照向自己的脚。"]},{"id":"S05","duration":15,"location":"lobby","title":"零点整","expression":"neutral","action":"idle","fx":"clock","beats":["墙上的秒针越过十二，整栋楼突然安静下来。","电话线没有接通，桌上的旧电话却响了一声。","林默想起纸背面还有一行小字：电话只会响一次。"]},{"id":"S06","duration":15,"location":"lobby","title":"第二名保安","expression":"shocked","action":"turn","fx":"glitch","beats":["三号监控里，一个穿同样制服的人走进大堂。","那个人停在林默身后，慢慢抬起了头。","屏幕中的脸，和林默一模一样。"]},{"id":"S07","duration":15,"location":"lobby","title":"数到三十","expression":"afraid","action":"hide","fx":"shadow","beats":["林默关掉三号屏幕，钻到桌下开始数数。","数到十七时，一双黑色皮鞋停在桌外。","一个和他相同的声音轻声问：你数错了吗？"]},{"id":"S08","duration":15,"location":"lobby","title":"不要回答","expression":"afraid","action":"freeze","fx":"pulse","beats":["林默咬住舌尖，没有回答。","他继续数到三十，皮鞋终于转身离开。","重新抬头时，三号屏幕上只剩一把空椅子。"]},{"id":"S09","duration":15,"location":"lobby","title":"负一层","expression":"worried","action":"look","fx":"elevator","beats":["零点四十分，电梯数字从七直接跳到了负一。","门缝里传出女人的哭声：求你开门，我的孩子还在里面。","开门键亮了起来，像是在等待他的手指。"]},{"id":"S10","duration":15,"location":"lobby","title":"标准回答","expression":"serious","action":"point","fx":"red","beats":["林默后退一步：维修人员已经下班。","哭声立刻停止。电梯门内传来指甲刮擦金属的声音。","显示屏重新变成一层，但门上多了五道湿漉漉的手印。"]},{"id":"S11","duration":15,"location":"lobby","title":"观众求助","expression":"neutral","action":"turn","fx":"none","beats":["一点十分，一名女观众跑来，说四号厅里有人一直敲门。","她递给林默一把钥匙，请他陪自己去员工通道。","钥匙牌写着四号厅，纸上的第四条规则却被墨水涂黑了。"]},{"id":"S12","duration":15,"location":"corridor","title":"员工通道","expression":"worried","action":"walk","fx":"flicker","beats":["林默来到放映厅后的员工通道，女人却已经不见了。","两侧房门整齐排列，尽头的红灯一明一灭。","他忽然发现，每一扇门上都写着四号厅。"]},{"id":"S13","duration":15,"location":"corridor","title":"不要数门","expression":"afraid","action":"freeze","fx":"doors","beats":["左边六扇，右边六扇，尽头似乎还有一扇。","林默意识到自己已经开始数门。","走廊两侧同时响起十三下门锁转动的声音。"]},{"id":"S14","duration":15,"location":"corridor","title":"有人叫他","expression":"shocked","action":"look","fx":"shadow","beats":["走廊尽头传来老保安的声音：林默，快过来。","他立刻把手电照向自己的脚。","光圈里却出现了两个人的影子。"]},{"id":"S15","duration":15,"location":"corridor","title":"影子先动","expression":"afraid","action":"run","fx":"chase","beats":["第二道影子抬起手，指向林默身后的房门。","门内传出自己的声音：快进来，外面的不是你。","林默关掉手电，凭记忆朝楼梯口狂奔。"]},{"id":"S16","duration":15,"location":"corridor","title":"被涂黑的规则","expression":"serious","action":"read","fx":"rule","beats":["楼梯间的墙上贴着另一份守则。","第四条没有被涂黑：不要帮助寻找四号厅的女观众。","四号厅已经封闭七年。她会把保安带给门后的东西。"]},{"id":"S17","duration":15,"location":"corridor","title":"纸上的新字","expression":"shocked","action":"read","fx":"write","beats":["林默手里的守则慢慢渗出一行红字。","规则五：如果你已经看见两个影子，请确认哪一个会呼吸。","不会呼吸的那个，才是你。"]},{"id":"S18","duration":15,"location":"corridor","title":"呼吸","expression":"afraid","action":"freeze","fx":"breath","beats":["林默屏住呼吸，胸口却仍在起伏。","身后的脚步也停了下来。另一个林默贴在他耳边呼吸。","他终于明白，守则并不是写给活人的。"]},{"id":"S19","duration":15,"location":"lobby","title":"清晨交班","expression":"blank","action":"enter","fx":"glitch","beats":["早上六点，新来的保安推开大堂玻璃门。","值夜班的林默坐在桌后，微笑着递出一张折得发白的纸。","他一句话也没有说。"]},{"id":"S20","duration":15,"location":"lobby","title":"规则零","expression":"smile","action":"point","fx":"final","beats":["新保安翻到纸的背面，那里多出了一条从未见过的规则。","规则零：如果交班人叫林默，请不要接过他递来的纸。","因为真正的林默，还在员工通道里数门。"]}]};
  var ANIMATION = {"motions":{"still":{"durationFrames":1,"fromX":0,"toX":0,"fromY":0,"toY":0,"fromOpacity":1,"toOpacity":1},"enter":{"durationFrames":18,"fromX":-55,"toX":0,"fromY":0,"toY":0,"fromOpacity":0,"toOpacity":1},"walkIn":{"durationFrames":30,"fromX":72,"toX":0,"fromY":0,"toY":0,"fromOpacity":1,"toOpacity":1},"runPast":{"durationFrames":24,"fromX":190,"toX":-310,"fromY":0,"toY":0,"fromOpacity":1,"toOpacity":0.25},"hide":{"durationFrames":12,"fromX":0,"toX":0,"fromY":0,"toY":82,"fromOpacity":1,"toOpacity":1}},"actionMotion":{"enter":"enter","walk":"walkIn","run":"runPast","hide":"hide"},"poseBeats":{"idle":["抱臂","指向","抱臂"],"read":["抱臂","指向","抱臂"],"point":["指向","抱臂","指向"],"look":["抱臂","指向","抱臂"],"turn":["指向","抱臂","指向"],"freeze":["抱臂","抱臂","指向"],"hide":["抱臂","抱臂","指向"],"walk":["行走","抱臂","指向"],"run":["行走","行走","抱臂"],"enter":["行走","抱臂","指向"]},"expressionBeats":{"neutral":["neutral","serious","worried"],"serious":["serious","worried","serious"],"worried":["worried","shocked","afraid"],"shocked":["shocked","afraid","serious"],"afraid":["afraid","shocked","afraid"],"blank":["blank","neutral","blank"],"smile":["neutral","smile","shocked"]}};
  var CALIBRATION = {"character":"橙衣男","stage":{"wrapperWidth":300,"wrapperHeight":640,"targetHeight":620,"left":190,"top":500},"poses":{"指向":{"width":337,"height":779,"face":{"centerX":192,"centerY":169,"size":90}},"抱臂":{"width":258,"height":779,"face":{"centerX":134,"centerY":169,"size":88}},"行走":{"width":204,"height":761,"face":{"centerX":112,"centerY":168,"size":86}},"坐姿":{"width":370,"height":720,"face":{"centerX":252,"centerY":154,"size":86}}}};
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
    alert('完成：已创建20个可编辑镜头并保存到\n' + aep.fsName);
  } catch (err) {
    alert('创建失败：' + err.toString());
    throw err;
  } finally {
    app.endUndoGroup();
  }
})();
