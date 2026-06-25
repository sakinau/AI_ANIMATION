# 我给魔王送外卖，结果拯救了世界

这是正式动画制作流的第一个项目目录。

## 文件结构

- `docs/00_Project_Bible.md`：项目总设定。
- `docs/01_Story_Outline.md`：五幕故事大纲。
- `docs/02_Scene_List.md`：10 个分场。
- `shots/climax_60s.yaml`：1 分钟高潮测试片镜头表，给人审阅。
- `shots/climax_60s.json`：同一镜头表的运行时数据，给 Remotion/AE 脚本读取。
- `workflow/asset_pipeline.yaml`：素材目录、授权记录和 Chrome 检索规则。
- `workflow/edit_presets.yaml`：动作、表情、转场和 QA 预设。
- `assets/00_license_records/asset_manifest.csv`：素材授权/来源登记表。
- `renders/`：测试帧和预览输出。

## 当前测试片

Composition：`MagicDeliveryClimax`

```powershell
npm run validate:magic
npm run build:ae:magic
npm run render:magic
```

当前测试片使用程序化占位角色和 UI，目标是验证生产闭环，不代表最终美术质量。下一步素材 agent 可以按 `workflow/asset_pipeline.yaml` 用 Chrome 找素材或用 AI 生成主角、魔王、魔王城背景、外卖道具，再替换占位图层。

## AE

运行 `npm run build:ae:magic` 会生成：

```text
ae/Build_Magic_Delivery.jsx
```

在 After Effects 中运行该脚本，会创建每镜头预合成和 `MASTER_magic_delivery_climax_60s` 主时间线。
