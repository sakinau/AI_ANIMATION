$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$runtimeRoot = 'F:\Animation_AI'
$nodeBin = Join-Path $runtimeRoot 'tools\node'
$remotion = Join-Path $runtimeRoot 'node_modules\.bin\remotion.cmd'
$chrome = Join-Path $runtimeRoot 'node_modules\.remotion\chrome-headless-shell\win64\chrome-headless-shell-win64\chrome-headless-shell.exe'

$env:Path = "$nodeBin;$env:Path"
Set-Location (Join-Path $projectRoot 'preview')
& $remotion studio index.ts --port=3000 --public-dir='..\public' --browser-executable=$chrome
