$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$runtimeRoot = 'F:\Animation_AI'
$nodeBin = Join-Path $runtimeRoot 'tools\node'
$remotion = Join-Path $runtimeRoot 'node_modules\.bin\remotion.cmd'
$chrome = Join-Path $runtimeRoot 'node_modules\.remotion\chrome-headless-shell\win64\chrome-headless-shell-win64\chrome-headless-shell.exe'

$env:Path = "$nodeBin;$env:Path"
Set-Location (Join-Path $projectRoot 'preview')
& $remotion render index.ts StateMachineWukongTest '..\output\state-machine-kana-rina-60s-test.mp4' --codec=h264 --crf=24 --concurrency=4 --public-dir='..\public' --browser-executable=$chrome
