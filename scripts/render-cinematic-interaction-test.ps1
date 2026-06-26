$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$runtimeRoot = 'F:\Animation_AI'
$nodeBin = Join-Path $runtimeRoot 'tools\node'
$remotion = Join-Path $runtimeRoot 'node_modules\.bin\remotion.cmd'
$chrome = Join-Path $runtimeRoot 'node_modules\.remotion\chrome-headless-shell\win64\chrome-headless-shell-win64\chrome-headless-shell.exe'

$env:Path = "$nodeBin;$env:Path"
Set-Location $projectRoot
python scripts\expand_cinematic_beats.py projects\scene-interaction-test\shots\breakfast_activity_events.json --output projects\scene-interaction-test\shots\breakfast_activity_cinematic_generated.json
python scripts\validate_cinematic_shots.py projects\scene-interaction-test\shots\breakfast_activity_cinematic_generated.json
Set-Location (Join-Path $projectRoot 'preview')
& $remotion render index.ts CinematicInteractionTest '..\output\scene-interaction-breakfast-activity-cinematic-test.mp4' --codec=h264 --crf=24 --concurrency=4 --public-dir='..\public' --browser-executable=$chrome
