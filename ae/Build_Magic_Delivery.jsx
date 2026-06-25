#target aftereffects
#targetengine "magicDeliveryBuilder"

(function () {
  var SEQUENCE = {"project_id":"magic-delivery","sequence_id":"climax_60s_test","title":"魔王城签收拯救世界","runtime_seconds":60,"fps":12,"aspect":"16:9","format":{"width":1920,"height":1080},"shots":[{"shot_id":"C01","duration":5,"location":"demon_rooftop","beat":"世界末日倒计时，外卖员冲进魔王城天台","characters":["delivery_guy","demon_king","hero"],"action":"scooter_enter","expression":"determined_sweat","speaker":"旁白","dialogue":"世界末日，只差一个差评。","ui":"countdown","vfx":"dust_pop","vfx_reason":"外卖车急刹停住，尘土强调入场。","transition":"impact_cut","camera":{"preset":"establishing_pan","framing":"wide","motion_intensity":0.35,"focus":"delivery_guy"},"assets":{"required":["bg_demon_rooftop","delivery_guy","demon_king","hero","scooter","countdown_ui"],"optional":["foreground_rail","dust_fx"],"fallback":"使用宽景背景和车身剪影，不使用随机闪烁。"}},{"shot_id":"C02","duration":5,"location":"demon_rooftop","beat":"外卖员漂移停下，点名尾号 666","characters":["delivery_guy","demon_king"],"action":"hand_food_bag","expression":"neutral_to_smirk","speaker":"阿伟","dialogue":"尾号666的深渊麻辣烫，谁是寂寞魔王不吃香菜？","ui":"order_card","vfx":"none","vfx_reason":"","transition":"subtitle_slam","camera":{"preset":"push_in","framing":"medium","motion_intensity":0.25,"focus":"delivery_bag"},"assets":{"required":["delivery_guy","demon_king","delivery_bag","order_card_ui"],"optional":["foreground_table"],"fallback":"重点放大外卖袋和订单卡，减少背景依赖。"}},{"shot_id":"C03","duration":5,"location":"throne_front","beat":"魔王和勇者发现大战源于订单备注","characters":["demon_king","hero","delivery_guy"],"action":"shocked_recoil","expression":"shocked","speaker":"勇者","dialogue":"你备注写的是：毁灭世界，谢谢。","ui":"note_zoom","vfx":"none","vfx_reason":"","transition":"cut","camera":{"preset":"insert_closeup","framing":"insert","motion_intensity":0.2,"focus":"order_note"},"assets":{"required":["order_note_ui","hero","demon_king"],"optional":["receipt_prop"],"fallback":"用大号订单备注 UI 作为主画面。"}},{"shot_id":"C04","duration":5,"location":"sky_rift","beat":"天界审判者像客服弹窗一样出现","characters":["judge","delivery_guy"],"action":"system_popup","expression":"comic_panic","speaker":"天界审判者","dialogue":"检测到关键词：毁灭世界。已为您自动开启灭世服务。","ui":"customer_service","vfx":"red_alert","vfx_reason":"系统误判触发警报，红色提示只在弹窗入场时出现。","transition":"glitch_realm_shift","camera":{"preset":"over_shoulder","framing":"medium","motion_intensity":0.3,"focus":"judge_popup"},"assets":{"required":["judge_popup_ui","delivery_guy","sky_rift_bg"],"optional":["warning_icon"],"fallback":"用客服弹窗和红色边框表达天界审判。"}},{"shot_id":"C05","duration":5,"location":"battlefield","beat":"外卖员开启骑手战术面板","characters":["delivery_guy"],"action":"phone_tap","expression":"determined_sweat","speaker":"阿伟","dialogue":"别慌，我处理过比这更复杂的，小区18栋没有18栋。","ui":"tactical_map","vfx":"ui_burst","vfx_reason":"手机界面展开路线面板，特效限制在 UI 内。","transition":"whip_pan","camera":{"preset":"insert_closeup","framing":"insert","motion_intensity":0.35,"focus":"phone_ui"},"assets":{"required":["phone_prop","tactical_map_ui","delivery_guy_hand"],"optional":["map_icons"],"fallback":"用全屏 UI 插入镜头替代复杂战场。"}},{"shot_id":"C06","duration":5,"location":"demon_hall","beat":"外卖员补齐平台流程，骷髅兵举反光板","characters":["delivery_guy","skeleton"],"action":"proof_photo","expression":"serious","speaker":"阿伟","dialogue":"先拍照留证，免得平台说我没送到地狱。","ui":"photo_stamp","vfx":"camera_flash","vfx_reason":"拍照留证瞬间出现 2-4 帧闪光。","transition":"smoke_wipe_fast","camera":{"preset":"reaction_cut","framing":"medium","motion_intensity":0.2,"focus":"delivery_guy"},"assets":{"required":["delivery_guy","photo_stamp_ui","food_bag"],"optional":["skeleton","reflector_prop"],"fallback":"没有骷髅兵时用反光板道具和盖章 UI。"}},{"shot_id":"C07","duration":6,"location":"judgement_beam","beat":"外卖员对天空打人工客服","characters":["delivery_guy","judge"],"action":"voice_appeal","expression":"comic_panic","speaker":"阿伟","dialogue":"喂，人工客服！自动灭世不能点错就发货啊！","ui":"call_waiting","vfx":"loading_loop","vfx_reason":"人工客服等待动画，绑定在通话 UI 内。","transition":"cut","camera":{"preset":"pull_back","framing":"wide","motion_intensity":0.25,"focus":"judgement_beam"},"assets":{"required":["delivery_guy","call_waiting_ui","sky_beam_bg"],"optional":["judge_silhouette"],"fallback":"用通话 UI 和天空光柱表达客服等待。"}},{"shot_id":"C08","duration":5,"location":"demon_rooftop","beat":"保温箱挡圣剑，小票压魔法","characters":["delivery_guy","demon_king","hero"],"action":"block_with_bag","expression":"heroic_resolve","speaker":"阿伟","dialogue":"打可以，先签收。我超时一秒扣两块。","ui":"receipt_sign","vfx":"impact_spark","vfx_reason":"圣剑撞到保温箱的单点冲击。","transition":"match_cut_prop","camera":{"preset":"truck_right","framing":"medium","motion_intensity":0.4,"focus":"delivery_bag"},"assets":{"required":["delivery_guy","hero","delivery_bag","receipt_ui"],"optional":["impact_spark_fx"],"fallback":"用保温箱放大镜头和短促火花，不做全屏闪。"}},{"shot_id":"C09","duration":5,"location":"world_map","beat":"订单地址改成取消灭世，魔法阵重算路线","characters":["delivery_guy"],"action":"route_recalc","expression":"determined_sweat","speaker":"导航","dialogue":"已为您避开拥堵、天罚与世界毁灭。","ui":"route_map","vfx":"golden_path","vfx_reason":"路线重新规划时绘制金色路径。","transition":"impact_cut","camera":{"preset":"insert_closeup","framing":"insert","motion_intensity":0.3,"focus":"route_map"},"assets":{"required":["route_map_ui","phone_prop"],"optional":["world_map_bg"],"fallback":"地图 UI 全屏化，缺少世界地图时使用抽象路线。"}},{"shot_id":"C10","duration":5,"location":"sky_rift","beat":"撤回灭世服务需要手续费","characters":["judge","delivery_guy"],"action":"confirm_button","expression":"angry_panic","speaker":"天界审判者","dialogue":"撤回需收取手续费。","ui":"confirm_cancel","vfx":"crack_close","vfx_reason":"取消灭世裂缝闭合，表现危机解除。","transition":"cut","camera":{"preset":"push_in","framing":"closeup","motion_intensity":0.3,"focus":"confirm_button"},"assets":{"required":["confirm_cancel_ui","judge_popup_ui"],"optional":["sky_crack_fx"],"fallback":"以确认按钮近景作为主画面。"}},{"shot_id":"C11","duration":5,"location":"demon_rooftop","beat":"魔王吃到麻辣烫并给五星好评","characters":["demon_king","hero","delivery_guy"],"action":"eat_and_review","expression":"soft_realization","speaker":"魔王","dialogue":"五星好评已给。能再点一份吗？","ui":"five_star","vfx":"warm_steam","vfx_reason":"食物热气和五星评价绑定，表现危机转喜剧。","transition":"subtitle_slam","camera":{"preset":"pull_back","framing":"wide","motion_intensity":0.2,"focus":"group"},"assets":{"required":["demon_king","delivery_guy","food_box","five_star_ui"],"optional":["hero"],"fallback":"用食物盒和五星 UI 做笑点中心。"}},{"shot_id":"C12","duration":4,"location":"phone_closeup","beat":"新订单来自创世神","characters":["delivery_guy"],"action":"phone_closeup","expression":"blank","speaker":"阿伟","dialogue":"……我现在辞职还来得及吗？","ui":"new_order","vfx":"cosmic_ping","vfx_reason":"新订单提示音触发短促光点。","transition":"cut_to_black","camera":{"preset":"insert_closeup","framing":"insert","motion_intensity":0.15,"focus":"phone_ui"},"assets":{"required":["phone_prop","new_order_ui"],"optional":["cosmic_ping_fx"],"fallback":"用手机订单界面完成结尾钩子。"}}]};
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
    alert('Done: editable AE project created.\n' + aep.fsName);
  } catch (err) {
    alert('Build failed: ' + err.toString());
    throw err;
  } finally {
    app.endUndoGroup();
  }
})();
